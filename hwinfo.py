#!/usr/bin/env python3
"""
Waybar module for displaying CPU and GPU temperatures.

This script fetches hardware temperatures and outputs JSON compatible with Waybar.
"""

import argparse
import json
import time
import sys
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Display CPU and GPU temperatures in Waybar.")
    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Update interval in seconds (default: 30)"
    )
    return parser.parse_args()

def get_cpu_temperature():
    """
    Get CPU temperature using psutil (preferred) or fallback to /sys/class/thermal.
    
    Returns:
        float or str: Average CPU temperature in Celsius, or "N/A" if not available.
    """
    try:
        # Try using psutil first
        import psutil
        temps = psutil.sensors_temperatures()
        
        if not temps:
            logger.warning("psutil.sensors_temperatures() returned no data.")
        else:
            # Look for common CPU sensor names
            cpu_keys = ['coretemp', 'k10temp', 'acpi', 'x86_pkg_temp']
            for key in cpu_keys:
                if key in temps:
                    # Calculate average temperature across all entries for this sensor
                    total_temp = 0
                    count = 0
                    for entry in temps[key]:
                        if entry.current is not None:
                            total_temp += entry.current
                            count += 1
                    
                    if count > 0:
                        avg_temp = total_temp / count
                        logger.debug(f"CPU temperature (psutil, {key}): {avg_temp:.1f}°C")
                        return round(avg_temp, 1)
            
            # If no known keys found, try to find any sensor with 'cpu' in its name
            for name, entries in temps.items():
                if 'cpu' in name.lower() or 'core' in name.lower():
                    total_temp = 0
                    count = 0
                    for entry in entries:
                        if entry.current is not None:
                            total_temp += entry.current
                            count += 1
                    
                    if count > 0:
                        avg_temp = total_temp / count
                        logger.debug(f"CPU temperature (psutil, detected {name}): {avg_temp:.1f}°C")
                        return round(avg_temp, 1)
                        
    except ImportError:
        logger.warning("psutil not installed. Falling back to /sys/class/thermal.")
    except Exception as e:
        logger.error(f"Error getting CPU temperature with psutil: {e}")

    # Fallback to /sys/class/thermal
    try:
        import glob
        import os
        
        thermal_paths = glob.glob('/sys/class/thermal/thermal_zone*/temp')
        if not thermal_paths:
            logger.warning("No thermal zones found in /sys/class/thermal/")
            return "N/A"
            
        total_temp = 0
        count = 0
        
        for path in thermal_paths:
            # Check if this is a CPU sensor by looking at the type file
            type_path = os.path.join(os.path.dirname(path), 'type')
            try:
                with open(type_path, 'r') as f:
                    sensor_type = f.read().strip().lower()
                
                # Common CPU sensor types
                cpu_types = ['coretemp', 'k10temp', 'acpi', 'x86_pkg_temp']
                if any(cpu_type in sensor_type for cpu_type in cpu_types):
                    with open(path, 'r') as f:
                        temp_milli = int(f.read().strip())
                        temp_celsius = temp_milli / 1000.0
                        total_temp += temp_celsius
                        count += 1
                        logger.debug(f"CPU temperature (sysfs, {sensor_type}): {temp_celsius:.1f}°C")
            except (IOError, ValueError) as e:
                logger.warning(f"Could not read temperature from {path}: {e}")
                continue
                
        if count > 0:
            avg_temp = total_temp / count
            return round(avg_temp, 1)
        else:
            logger.warning("No CPU temperature found in /sys/class/thermal/ (no matching sensor types)")
            return "N/A"
            
    except Exception as e:
        logger.error(f"Error getting CPU temperature from /sys/class/thermal: {e}")
        
    return "N/A"

def get_gpu_info():
    """
    Detect GPU type and get temperature.
    
    Returns:
        dict: A dictionary containing 'name' and 'temperature' keys.
    """
    import shutil
    import subprocess
    
    # Check for NVIDIA GPU
    if shutil.which("nvidia-smi"):
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,temperature.gpu", "--format=csv,noheader,nounits"],
                capture_output=True,
                text=True,
                check=True,
                timeout=5  # Timeout after 5 seconds
            )
            
            # Parse the output (e.g., "GeForce RTX 3070, 55")
            lines = result.stdout.strip().split('\n')
            if lines:
                parts = lines[0].split(', ')
                if len(parts) == 2:
                    name = parts[0].strip()
                    temp = float(parts[1].strip())
                    logger.debug(f"GPU temperature (NVIDIA): {temp}°C")
                    return {"name": name, "temperature": round(temp, 1)}
                    
        except subprocess.CalledProcessError as e:
            logger.error(f"nvidia-smi command failed: {e}")
        except subprocess.TimeoutExpired:
            logger.error("nvidia-smi command timed out")
        except Exception as e:
            logger.error(f"Error getting NVIDIA GPU temperature: {e}")
            
        # If we get here, nvidia-smi failed
        return {"name": "NVIDIA", "temperature": "N/A"}
    
    # Check for AMD/Intel GPU using sensors
    if shutil.which("sensors"):
        try:
            result = subprocess.run(
                ["sensors"],
                capture_output=True,
                text=True,
                check=True,
                timeout=5  # Timeout after 5 seconds
            )
            
            # Parse sensors output
            # Look for lines with amdgpu, radeon, or i915 and temp readings
            lines = result.stdout.strip().split('\n')
            for i, line in enumerate(lines):
                if 'amdgpu' in line.lower() or 'radeon' in line.lower():
                    # Look for temp line after the adapter line
                    for j in range(i+1, min(i+5, len(lines))):  # Check next few lines
                        temp_line = lines[j]
                        if 'temp1:' in temp_line and '°C' in temp_line:
                            # Extract temperature (e.g., "temp1:       +55.0°C  (crit = +100.0°C, hyst = +90.0°C)")
                            temp_part = temp_line.split('+')[1].split('°C')[0]
                            temp = float(temp_part)
                            logger.debug(f"GPU temperature (AMD): {temp}°C")
                            return {"name": "AMD", "temperature": round(temp, 1)}
                            
                elif 'i915' in line.lower():
                    # Look for temp line after the adapter line
                    for j in range(i+1, min(i+5, len(lines))):  # Check next few lines
                        temp_line = lines[j]
                        if 'temp1:' in temp_line and '°C' in temp_line:
                            # Extract temperature
                            temp_part = temp_line.split('+')[1].split('°C')[0]
                            temp = float(temp_part)
                            logger.debug(f"GPU temperature (Intel): {temp}°C")
                            return {"name": "Intel", "temperature": round(temp, 1)}
                            
        except subprocess.CalledProcessError as e:
            logger.error(f"sensors command failed: {e}")
        except subprocess.TimeoutExpired:
            logger.error("sensors command timed out")
        except Exception as e:
            logger.error(f"Error parsing sensors output: {e}")
            
        # If we get here, sensors parsing failed
        return {"name": "AMD/Intel", "temperature": "N/A"}
    
    # No GPU detected or tools not available
    logger.info("No GPU detected or required tools (nvidia-smi, sensors) not found.")
    return {"name": "N/A", "temperature": "N/A"}

def format_waybar_output(cpu_temp, gpu_info):
    """
    Format the output as a JSON string compatible with Waybar.
    
    Args:
        cpu_temp (float or str): CPU temperature.
        gpu_info (dict): Dictionary with GPU name and temperature.
        
    Returns:
        str: JSON formatted string for Waybar.
    """
    import datetime
    
    # Format the main text display
    if isinstance(cpu_temp, (int, float)):
        cpu_text = f"{cpu_temp}°C"
    else:
        cpu_text = "N/A"
        
    if isinstance(gpu_info['temperature'], (int, float)):
        gpu_text = f"{gpu_info['temperature']}°C"
    else:
        gpu_text = "N/A"
        
    text = f"CPU: {cpu_text} | GPU: {gpu_text}"
    
    # Format the tooltip with more detailed information
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    tooltip = f"Hardware Info\n"
    tooltip += f"CPU Temp: {cpu_text}\n"
    tooltip += f"GPU: {gpu_info['name']}\n"
    tooltip += f"GPU Temp: {gpu_text}\n"
    tooltip += f"Updated: {timestamp}"
    
    output = {
        "text": text,
        "tooltip": tooltip,
        "class": "hwinfo",
        "alt": "hwinfo"
    }
    return json.dumps(output, indent=None)

def main():
    """Main execution loop."""
    args = parse_arguments()
    interval = args.interval
    
    logger.info(f"Starting Waybar hardware info module with interval {interval}s")
    
    try:
        while True:
            try:
                cpu_temp = get_cpu_temperature()
                gpu_info = get_gpu_info()
                output_json = format_waybar_output(cpu_temp, gpu_info)
                print(output_json, flush=True)
            except Exception as e:
                logger.error(f"Error in main loop iteration: {e}")
                # Print a minimal error JSON to prevent Waybar from crashing
                error_output = {
                    "text": "CPU: N/A | GPU: N/A",
                    "tooltip": f"Error: {e}",
                    "class": "hwinfo-error",
                    "alt": "hwinfo-error"
                }
                print(json.dumps(error_output, indent=None), flush=True)
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, exiting.")
        sys.exit(0)

if __name__ == "__main__":
    main()