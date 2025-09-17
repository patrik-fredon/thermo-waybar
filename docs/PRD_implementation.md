# Product Requirements Document (PRD)

**Project:** Waybar Hardware Info Module (Arch Linux + Hyprland + Wayland)
**Author:** \FredonBytes
**Date:** \17/09/2025

---

## 1. Overview

This project is a **Python module** that integrates with **Waybar** on Arch Linux running **Hyprland** (Wayland compositor).
The module will display detailed system hardware information (CPU & GPU temperature) in Waybar in a **professional, fancy, and detailed** format.

The script will:

* Run in the background.
* Every 30 seconds, fetch CPU and GPU temperatures.
* Output JSON data compatible with Waybar’s **custom module** input format.
* Provide a clean, styled presentation in the Waybar bar.

---

## 2. Goals & Objectives

* Provide **reliable and accurate** hardware temperature monitoring.
* Display temperatures in **human-friendly format** (°C, with optional emojis/icons).
* Detect GPU only if present; otherwise, skip gracefully.
* Maintain **low system resource usage**.
* Be modular, so users can easily adjust refresh rate or add more hardware metrics in the future.

---

## 3. Non-Goals

* Full system monitoring (memory, disk, network).
* Advanced GPU utilization tracking (only temperature is in scope).
* GUI/graphical interface outside Waybar JSON output.

---

## 4. Functional Requirements

### 4.1 Data Collection

* **CPU Temperature:**

  * Use `psutil` (preferred) or `hwmon` via `/sys/class/thermal` as fallback.
  * Report the **average temperature** across all cores.

* **GPU Temperature:**

  * Detect GPU type:

    * NVIDIA: use `nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader,nounits`.
    * AMD: use `sensors` (`amdgpu-pci-*`) if available.
    * Intel iGPU: use `sensors` (`i915`) if available.
  * If no GPU is detected, return `"GPU: N/A"`.

### 4.2 JSON Output Format (Waybar compatible)

* Example output:

```json
{
  "text": "CPU: 42°C | GPU: 38°C",
  "tooltip": "Hardware Info\nCPU Temp: 42°C\nGPU Temp: 38°C",
  "class": "hwinfo",
  "alt": "hwinfo"
}
```

* **Fields explained:**

  * `text`: Compact one-line view for Waybar.
  * `tooltip`: Detailed multi-line info when hovering.
  * `class`: Used for CSS styling (e.g., `.hwinfo`).
  * `alt`: Alternate identifier for status bar usage.

### 4.3 Interval

* Run check **every 30 seconds**.
* Configurable via command-line flag `--interval <seconds>` (default 30).

### 4.4 Error Handling

* If temperature cannot be read, display `"N/A"`.
* Ensure the script does not crash Waybar if a sensor is missing.

---

## 5. Technical Requirements

* **Environment:**

  * Arch Linux (rolling).
  * Waybar + Hyprland (Wayland compositor).
  * Python ≥ 3.10.

* **Dependencies:**

  * `psutil`
  * `subprocess` (for GPU commands).
  * `json` (standard library).

* **Waybar Config Integration:**

  * Example `~/.config/waybar/config`:

```json
"custom/hwinfo": {
  "exec": "python3 ~/.config/waybar/scripts/hwinfo.py",
  "interval": 30,
  "return-type": "json"
}
```

* **Waybar CSS Styling (`~/.config/waybar/style.css`):**

```css
#custom-hwinfo {
  color: #a3be8c;
  font-weight: bold;
  padding: 0 5px;
}
```

---

## 6. User Experience (UX)

* **Normal State:**

  * Compact view: `CPU: 42°C | GPU: 38°C`
  * Tooltip when hovered:

    ```
    Hardware Info
    CPU Temp: 42°C
    GPU Temp: 38°C
    Updated: 12:45:30
    ```

* **GPU Missing:**

  * `CPU: 42°C | GPU: N/A`

* **Error State:**

  * `CPU: N/A | GPU: N/A`

---

## 7. Future Enhancements (Not in MVP)

* Add fan speed monitoring.
* Add per-core CPU temperature display.
* Add color-coded temperature thresholds (green/yellow/red).
* Support AMD ROCm and Intel oneAPI GPU metrics.

---

## 8. Acceptance Criteria

1. Module must successfully display CPU temperature.
2. Module must attempt GPU detection and display temperature if available.
3. JSON output must be Waybar compatible (`return-type=json`).
4. Interval must default to 30 seconds but be configurable.
5. Script must handle missing sensors gracefully.
6. Tooltip must show detailed information.

