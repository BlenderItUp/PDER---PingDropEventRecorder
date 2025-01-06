import time
import requests
from datetime import datetime, timedelta
import signal
import curses
import argparse  # Add argparse for command-line arguments

class InternetMonitor:
    def __init__(self, failure_threshold=3, min_downtime=timedelta(seconds=3), check_connectivity_timeout=1, log_update_interval=30):
        # Initialize monitoring parameters
        self.start_time = datetime.now()  # Start time of the monitoring session
        self.total_drops = 0  # Total number of connectivity drops
        self.total_downtime = timedelta(0)  # Cumulative downtime
        self.hourly_drops = {}  # Dictionary to track drops per hour
        self.last_down_time = None  # Timestamp of the last detected downtime
        self.is_down = False  # Flag to indicate if the internet is currently down
        self.failure_count = 0  # Counter for consecutive failed checks
        self.log_buffer = []  # Buffer for storing disruption logs before writing to file
        self.last_log_time = datetime.now()  # Timestamp of the last log update

        # Configurable parameters
        self.failure_threshold = failure_threshold  # Number of consecutive failures to consider a drop
        self.min_downtime = min_downtime  # Minimum downtime duration to log a disruption
        self.check_connectivity_timeout = check_connectivity_timeout  # Interval between connectivity checks
        self.log_update_interval = log_update_interval  # Interval for updating logs

        # Log file names with timestamps
        self.disruption_log = f"internet_disruptions_{self.start_time.strftime('%Y-%m-%d_%H-%M-%S')}.log"
        self.stats_log = f"internet_stats_{self.start_time.strftime('%Y-%m-%d_%H-%M-%S')}.log"

    def log_disruption(self, start_time=None, end_time=None):
        # Log a connectivity disruption with its start and end times
        if start_time and end_time:
            downtime = end_time - start_time
            self.log_buffer.append(f"Disconnected at {start_time.strftime('%Y-%m-%d %H:%M:%S')}, "
                                    f"Reconnected at {end_time.strftime('%Y-%m-%d %H:%M:%S')}, "
                                    f"Downtime: {downtime}\n")

    def write_log_buffer(self):
        # Write buffered logs to the disruption log file
        if self.log_buffer:
            with open(self.disruption_log, "a") as f:
                f.writelines(self.log_buffer)
            self.log_buffer = []

    def get_stats(self):
        # Calculate and return various monitoring statistics
        uptime = datetime.now() - self.start_time  # Total uptime since the script started
        current_time = datetime.now()
        average_downtime = self.total_downtime / self.total_drops if self.total_drops else timedelta(0)  # Average downtime per drop
        elapsed_hours = max(uptime.total_seconds() / 3600, 1 / 3600)  # Elapsed time in hours (minimum of 1 second)
        average_drops_per_hour = self.total_drops / elapsed_hours  # Average number of drops per hour

        stats = {
            "script_start_time": self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            "current_time": current_time.strftime('%Y-%m-%d %H:%M:%S'),
            "total_drops": self.total_drops,
            "drops_this_hour": self.hourly_drops.get(current_time.hour, 0),
            "average_drops_per_hour": average_drops_per_hour,
            "total_downtime": self.total_downtime,
            "average_downtime_per_drop": average_downtime,
        }
        return stats

    def log_stats(self):
        # Write current statistics to the stats log file
        stats = self.get_stats()
        with open(self.stats_log, "w") as f:
            f.write(f"Script Start Time: {stats['script_start_time']} | Current Time: {stats['current_time']}\n")
            f.write(f"Total Drops: {stats['total_drops']}\n")
            f.write(f"Drops This Hour: {stats['drops_this_hour']}\n")
            f.write(f"Average Drops Per Hour: {stats['average_drops_per_hour']:.2f}\n")
            f.write(f"Total Downtime: {stats['total_downtime']}\n")
            f.write(f"Average Downtime Per Drop: {stats['average_downtime_per_drop']}\n")

    def display_stats(self, stdscr):
        # Display real-time statistics on the terminal using curses
        stats = self.get_stats()
        stdscr.clear()
        stdscr.addstr(0, 0, f"Script Start Time: {stats['script_start_time']} | Current Time: {stats['current_time']}")
        stdscr.addstr(1, 0, f"Total Drops: {stats['total_drops']}")
        stdscr.addstr(2, 0, f"Drops This Hour: {stats['drops_this_hour']}")
        stdscr.addstr(3, 0, f"Average Drops Per Hour: {stats['average_drops_per_hour']:.2f}")
        stdscr.addstr(4, 0, f"Total Downtime: {stats['total_downtime']}")
        stdscr.addstr(5, 0, f"Average Downtime Per Drop: {stats['average_downtime_per_drop']}")
        stdscr.refresh()

    def check_connectivity(self):
        # Check internet connectivity by pinging multiple URLs
        test_urls = ["https://www.google.com", "https://www.cloudflare.com"]
        for url in test_urls:
            try:
                response = requests.head(url, timeout=1)  # Use HEAD request for faster response
                if response.status_code == 200:
                    return True
            except requests.RequestException:
                continue
        return False  # No URL responded successfully

    def should_update_log(self):
        # Determine if it's time to update the log based on the update interval
        now = datetime.now()
        if (now - self.last_log_time).seconds >= self.log_update_interval:
            self.last_log_time = now
            return True
        return False

    def handle_exit(self, signal, frame):
        # Handle script exit gracefully (e.g., on Ctrl+C)
        self.write_log_buffer()  # Ensure all buffered logs are written
        print("Exiting gracefully...")
        exit(0)

    def monitor(self, stdscr):
        # Main monitoring loop
        signal.signal(signal.SIGINT, self.handle_exit)  # Catch Ctrl+C to handle exit

        while True:
            if self.check_connectivity():
                if self.is_down:
                    reconnect_time = datetime.now()
                    downtime = reconnect_time - self.last_down_time
                    if downtime >= self.min_downtime:
                        self.total_downtime += downtime
                        self.log_disruption(start_time=self.last_down_time, end_time=reconnect_time)
                        self.total_drops += 1
                        current_hour = reconnect_time.hour
                        self.hourly_drops[current_hour] = self.hourly_drops.get(current_hour, 0) + 1
                    self.is_down = False
                    self.failure_count = 0
            else:
                if not self.is_down:
                    self.last_down_time = datetime.now()
                    self.is_down = True  # Mark as down immediately
                self.failure_count += 1

                # Check if the downtime has exceeded the minimum downtime
                if self.is_down and (datetime.now() - self.last_down_time) >= self.min_downtime:
                    downtime = datetime.now() - self.last_down_time
                    self.total_downtime += downtime
                    self.log_disruption(start_time=self.last_down_time, end_time=datetime.now())
                    self.total_drops += 1
                    current_hour = datetime.now().hour
                    self.hourly_drops[current_hour] = self.hourly_drops.get(current_hour, 0) + 1
                    self.is_down = False  # Reset the down flag to avoid duplicate logs
                    self.failure_count = 0


            if self.should_update_log():
                self.write_log_buffer()
                self.log_stats()

            self.display_stats(stdscr)
            time.sleep(self.check_connectivity_timeout)  # Pause between checks

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Monitor internet connectivity and log disruptions.")
    parser.add_argument("--failure-threshold", type=int, default=3, help="Number of consecutive failures to consider the internet down (default: 3)")
    parser.add_argument("--min-downtime", type=int, default=3, help="Minimum downtime in seconds to log a disruption (default: 3 seconds)")
    parser.add_argument("--check-interval", type=int, default=1, help="Time in seconds between connectivity checks (default: 1 second)")
    parser.add_argument("--log-interval", type=int, default=60, help="Interval in seconds for updating logs (default: 60 seconds)")
    parser.add_argument("--help-settings", action="store_true", help="List configurable settings and their descriptions.")

    args = parser.parse_args()

    if args.help_settings:
        print("Configurable Settings:")
        print("  --failure-threshold : Number of consecutive failures to consider the internet down.")
        print("  --min-downtime      : Minimum downtime (in seconds) to log a disruption.")
        print("  --check-interval    : Time (in seconds) between connectivity checks.")
        print("  --log-interval      : Interval (in seconds) for updating logs.")
        exit(0)

    # Run the monitor in a curses wrapper for terminal display
    curses.wrapper(lambda stdscr: InternetMonitor(
        failure_threshold=args.failure_threshold,
        min_downtime=timedelta(seconds=args.min_downtime),
        check_connectivity_timeout=args.check_interval,
        log_update_interval=args.log_interval
    ).monitor(stdscr))
