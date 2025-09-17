# Waybar Hardware Info Module

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight Python module for Waybar that displays real-time CPU and GPU temperatures in your Wayland status bar. Perfect for Arch Linux users running Hyprland who want to keep an eye on their system's thermal performance.

![Example showing CPU and GPU temperatures in Waybar](docs/screenshot.png)

*Note: Image above is for illustrative purposes. Actual appearance depends on your Waybar styling.*

## Features

- 🌡️ **Accurate Temperature Monitoring**: Displays both CPU and GPU temperatures in Celsius
- 🔧 **Multi-GPU Support**: Works with NVIDIA, AMD, and Intel graphics cards
- ⚡ **Lightweight**: Minimal system resource usage with configurable refresh intervals
- 🛡️ **Robust Error Handling**: Gracefully handles missing sensors or unavailable data
- 🎨 **Waybar Integration**: Native JSON output designed specifically for Waybar
- ⚙️ **Customizable**: Command-line options for adjusting refresh intervals

## Requirements

- Python 3.10 or higher
- Waybar on a Wayland compositor (Hyprland, Sway, etc.)
- Required Python packages:
  - `psutil` (for CPU temperature)
- System tools (at least one required for GPU temperature):
  - `nvidia-smi` (for NVIDIA GPUs)
  - `sensors` from lm-sensors package (for AMD/Intel GPUs)

## Installation

1. Clone this repository or download the `hwinfo.py` script:
   ```bash
   git clone https://github.com/yourusername/waybar-hardware-info.git
   cd waybar-hardware-info
   ```

2. Install required Python packages:
   ```bash
   pip install psutil
   ```

3. Install system dependencies for GPU monitoring:
   - For NVIDIA GPUs: Install the NVIDIA drivers which include `nvidia-smi`
   - For AMD/Intel GPUs: Install `lm-sensors` package:
     ```bash
     # Arch Linux
     sudo pacman -S lm-sensors
     
     # Ubuntu/Debian
     sudo apt install lm-sensors
     ```

4. Configure the module in your Waybar configuration (see Configuration section below)

## Usage

Run the script directly to see output:
```bash
python hwinfo.py
```

The script will output JSON data compatible with Waybar:
```json
{
  "text": "CPU: 45°C | GPU: 38°C",
  "tooltip": "Hardware Info\nCPU Temp: 45°C\nGPU: NVIDIA GeForce RTX 3070\nGPU Temp: 38°C\nUpdated: 14:30:22",
  "class": "hwinfo",
  "alt": "hwinfo"
}
```

## Configuration

Add the following to your Waybar configuration file (typically `~/.config/waybar/config`):

```json
"custom/hwinfo": {
  "exec": "python3 /path/to/hwinfo.py",
  "interval": 30,
  "return-type": "json"
}
```

Add the following to your Waybar CSS file (typically `~/.config/waybar/style.css`):

```css
#custom-hwinfo {
  color: #a3be8c;
  font-weight: bold;
  padding: 0 5px;
}

#custom-hwinfo:hover {
  background-color: #4c566a;
}
```

## Command-Line Options

- `--interval SECONDS`: Set the update interval in seconds (default: 30)

Example with custom interval:
```bash
python hwinfo.py --interval 60
```

## How It Works

The script uses multiple methods to gather hardware temperature data:

1. **CPU Temperature**:
   - Primary method: Uses `psutil.sensors_temperatures()` to read CPU temperature sensors
   - Fallback method: Reads from `/sys/class/thermal/thermal_zone*/temp` if psutil is unavailable

2. **GPU Temperature**:
   - NVIDIA: Executes `nvidia-smi` to get GPU temperature
   - AMD/Intel: Parses output from the `sensors` command
   - If no GPU is detected or tools are unavailable, displays "N/A"

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Waybar community for creating an excellent customizable status bar
- Inspired by the need for simple, effective hardware monitoring in tiling window manager environments