# PDER - PingDropEventRecorder

This script monitors your internet connection and logs any disruptions to a file. It also maintains real-time statistics about the connection's uptime and downtime.

## Features

- Logs internet drops and reconnections with timestamps.
- Tracks total downtime and average downtime per drop.
- Provides real-time statistics, including:
  - Total drops
  - Drops per hour
  - Total and average downtime
- Outputs stats to both the console and a log file.

## Usage

1. Run the script using Python:
   ```bash
   python PDER.py
   ```

2. The script will create the following log files in the same directory:
   - `internet_disruptions.log`: Logs when the internet drops and reconnects, including the duration of each drop.
   - `internet_stats.log`: Stores real-time statistics about the connection.

3. View real-time statistics in the terminal while the script is running.

## Files Generated

- **`internet_disruptions.log`**: Example output:
  ```
  Disconnected at 2025-01-05 13:50:00, Reconnected at 2025-01-05 13:50:10, Downtime: 0:00:10
  Disconnected at 2025-01-05 14:10:00, Reconnected at 2025-01-05 14:10:20, Downtime: 0:00:20
  ```

- **`internet_stats.log`**: Example output:
  ```
  Script Start Time: 2025-01-05 13:46:55
  Total Drops: 2
  Drops This Hour: 2
  Average Drops Per Hour: 2.00
  Total Downtime: 0:00:30
  Average Downtime Per Drop: 0:00:15
  ```

## License

This script is open-source and available under the [MIT License](LICENSE).
