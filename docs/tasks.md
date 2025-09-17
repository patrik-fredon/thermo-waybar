# Implementation Tasks

## Phase 1: Project Setup and Core Structure

1.  **Task 1.1:** Create project directory structure.
    *   Create `hwinfo.py` script file.
    *   Ensure `docs/` directory exists (already present).
2.  **Task 1.2:** Set up Python environment.
    *   Define minimum Python version (3.10).
    *   List dependencies (`psutil`).
3.  **Task 1.3:** Implement basic CLI argument parsing.
    *   Add `--interval` flag with default value of 30 seconds.
    *   Add help documentation for the flag.
4.  **Task 1.4:** Create placeholder functions for core logic.
    *   `get_cpu_temperature()`: Placeholder returning "N/A".
    *   `get_gpu_info()`: Placeholder returning {"name": "N/A", "temperature": "N/A"}.
    *   `format_waybar_output(cpu_temp, gpu_info)`: Placeholder returning a basic JSON structure.
5.  **Task 1.5:** Implement main execution loop.
    *   Infinite loop that calls the core logic functions.
    *   Uses `time.sleep()` based on the interval.
    *   Prints the JSON output to stdout.
    *   Includes basic `try...except` block for error handling in the loop.

## Phase 2: Core Functionality Implementation

6.  **Task 2.1:** Implement `get_cpu_temperature()` using `psutil`.
    *   Use `psutil.sensors_temperatures()` to get CPU temps.
    *   Calculate average temperature across all CPU cores.
    *   Implement fallback to `/sys/class/thermal/` if `psutil` fails or returns no data.
7.  **Task 2.2:** Implement `get_gpu_info()` for detection and temperature fetching.
    *   **Subtask 2.2.1:** Detect GPU type (NVIDIA, AMD, Intel).
        *   Check for `nvidia-smi` command.
        *   Check `sensors` command output for AMD (`amdgpu`) or Intel (`i915`) indicators.
    *   **Subtask 2.2.2:** Fetch temperature based on detected GPU type.
        *   NVIDIA: Execute `nvidia-smi` command.
        *   AMD/Intel: Parse `sensors` command output.
    *   **Subtask 2.2.3:** Handle cases where no GPU is detected or temperature cannot be fetched.
8.  **Task 2.3:** Enhance `format_waybar_output()` with full functionality.
    *   Construct `text` field: "CPU: X°C | GPU: Y°C".
    *   Construct `tooltip` field with detailed information and timestamp.
    *   Set `class` and `alt` fields to "hwinfo".
    *   Return valid JSON string.
9.  **Task 2.4:** Improve error handling and logging.
    *   Add more specific `try...except` blocks within `get_cpu_temperature` and `get_gpu_info`.
    *   Log errors to stderr without crashing the script.
    *   Ensure "N/A" is returned gracefully on any failure.

## Phase 3: Testing and Integration

10. **Task 3.1:** Test script execution manually.
    *   Run `python hwinfo.py` and verify output format.
    *   Test `--interval` flag.
    *   Verify error handling by temporarily disabling sensors.
11. **Task 3.2:** Integrate with Waybar.
    *   Configure `~/.config/waybar/config` to use the script.
    *   Add CSS styles in `~/.config/waybar/style.css`.
    *   Restart Waybar and verify the module displays correctly.
12. **Task 3.3:** Perform end-to-end testing.
    *   Observe CPU and GPU temperature updates in Waybar.
    *   Test tooltip display on hover.
    *   Verify behavior with different interval settings.

## Phase 4: Optimization and Polish

13. **Task 4.1:** Optimize script for resource usage.
    *   Profile the script to ensure minimal CPU/memory impact.
    *   Optimize subprocess calls and file reads.
14. **Task 4.2:** Code review and cleanup.
    *   Ensure code is clean, well-commented, and follows Python best practices.
    *   Make sure functions are modular and easily extensible.
15. **Task 4.3:** Finalize documentation.
    *   Update README if necessary.
    *   Ensure `docs/PRD_implementation.md` is aligned with the final implementation.

## Future Enhancements (Post-MVP)

16. **Task 5.1:** Add fan speed monitoring.
17. **Task 5.2:** Add per-core CPU temperature display.
18. **Task 5.3:** Add color-coded temperature thresholds.
19. **Task 5.4:** Support AMD ROCm and Intel oneAPI GPU metrics.