# PDER - PingDropEventRecorder

This script monitors your internet connection, logs disruptions, and provides real-time and historical statistics about the connection's uptime and downtime.

## Features

- Logs internet drops and reconnections with timestamps and downtime durations.
- Tracks total downtime, average downtime per drop, and hourly drop rates.
- Provides real-time statistics, including:
  - Total drops
  - Drops per hour
  - Total and average downtime
- Outputs stats to both the console and log files.
- Configurable parameters via command-line arguments.
- Help option to display configurable settings and their descriptions.

## Installation and Setup

Follow these steps to install and run the project:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/PDER.git
   cd PDER
   ```

2. **Set Up a Virtual Environment** (optional but recommended):
   - For **Linux/macOS**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - For **Windows (Command Prompt)**:
     ```cmd
     python -m venv venv
     .venv\Scripts\activate
     ```
   - For **Windows (PowerShell)**:
     ```powershell
     python -m venv venv
     .\.venv\Scripts\Activate.ps1
     ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Script**:
   ```bash
   python PDER.py [OPTIONS]
   ```

## Usage

### Command-Line Arguments

- `--failure-threshold`: Number of consecutive failures to consider the internet down (default: 3).
- `--min-downtime`: Minimum downtime in seconds to log a disruption (default: 3 seconds).
- `--check-interval`: Time in seconds between connectivity checks (default: 1 second).
- `--log-interval`: Interval in seconds for updating logs (default: 60 seconds).
- `--help-settings`: Displays all configurable settings and their descriptions.

**Example**:
```bash
python PDER.py --failure-threshold 5 --min-downtime 5 --check-interval 2 --log-interval 120
```

### Generated Files

- `internet_disruptions_<timestamp>.log`: Logs internet drops and reconnections with timestamps and downtime durations.
- `internet_stats_<timestamp>.log`: Stores real-time statistics about the connection.

### Help Option

To display the configurable settings and their descriptions, run:
```bash
python PDER.py --help-settings
```

### Real-Time Stats

View real-time statistics in the terminal while the script is running. The script uses the `curses` library for dynamic updates.

## Files Generated

- **`internet_disruptions_<timestamp>.log`**:
  Example output:
  ```
  Disconnected at 2025-01-05 13:50:00, Reconnected at 2025-01-05 13:50:10, Downtime: 0:00:10
  Disconnected at 2025-01-05 14:10:00, Reconnected at 2025-01-05 14:10:20, Downtime: 0:00:20
  ```

- **`internet_stats_<timestamp>.log`**:
  Example output:
  ```
  Script Start Time: 2025-01-05 13:46:55
  Total Drops: 2
  Drops This Hour: 2
  Average Drops Per Hour: 2.00
  Total Downtime: 0:00:30
  Average Downtime Per Drop: 0:00:15
  ```

## Configurable Settings

- `--failure-threshold`: Number of consecutive failures to consider the internet down.
- `--min-downtime`: Minimum downtime (in seconds) to log a disruption.
- `--check-interval`: Time (in seconds) between connectivity checks.
- `--log-interval`: Interval (in seconds) for updating logs.

## License

This script is open-source and available under the [MIT License](LICENSE).
