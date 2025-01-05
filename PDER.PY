import time
import os
from datetime import datetime, timedelta

# Globals for statistics
start_time = datetime.now()
total_drops = 0
total_downtime = timedelta(0)
hourly_drops = {}
last_down_time = None
is_down = False

def log_disruption(log_file, start_time=None, end_time=None):
    """Logs the details of an internet disruption."""
    with open(log_file, "a") as f:
        if start_time and end_time:
            downtime = end_time - start_time
            f.write(f"Disconnected at {start_time.strftime('%Y-%m-%d %H:%M:%S')}, "
                    f"Reconnected at {end_time.strftime('%Y-%m-%d %H:%M:%S')}, "
                    f"Downtime: {downtime}\n")


def get_stats():
    """Calculates and returns the current statistics."""
    uptime = datetime.now() - start_time
    average_downtime = total_downtime / total_drops if total_drops else timedelta(0)
    elapsed_hours = max(uptime.total_seconds() / 3600, 1 / 3600)  # Ensure at least 1 second to avoid divide-by-zero
    average_drops_per_hour = total_drops / elapsed_hours

    stats = {
        "script_start_time": start_time.strftime('%Y-%m-%d %H:%M:%S'),
        "total_drops": total_drops,
        "drops_this_hour": hourly_drops.get(datetime.now().hour, 0),
        "average_drops_per_hour": average_drops_per_hour,
        "total_downtime": total_downtime,
        "average_downtime_per_drop": average_downtime,
    }
    return stats

def log_stats(stats_file):
    """Logs statistics to a file."""
    stats = get_stats()
    with open(stats_file, "w") as f:
        f.write(f"Script Start Time: {stats['script_start_time']}\n")
        f.write(f"Total Drops: {stats['total_drops']}\n")
        f.write(f"Drops This Hour: {stats['drops_this_hour']}\n")
        f.write(f"Average Drops Per Hour: {stats['average_drops_per_hour']:.2f}\n")
        f.write(f"Total Downtime: {stats['total_downtime']}\n")
        f.write(f"Average Downtime Per Drop: {stats['average_downtime_per_drop']}\n")

def display_stats():
    """Displays real-time stats in the console."""
    stats = get_stats()
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Script Start Time: {stats['script_start_time']}")
    print(f"Total Drops: {stats['total_drops']}")
    print(f"Drops This Hour: {stats['drops_this_hour']}")
    print(f"Average Drops Per Hour: {stats['average_drops_per_hour']:.2f}")
    print(f"Total Downtime: {stats['total_downtime']}")
    print(f"Average Downtime Per Drop: {stats['average_downtime_per_drop']}")

def check_connectivity():
    """Checks internet connectivity by pinging a reliable server."""
    return os.system("ping -n 1 8.8.8.8 >nul 2>&1") == 0

def main():
    global total_drops, total_downtime, last_down_time, is_down

    disruption_log = "internet_disruptions.log"
    stats_log = "internet_stats.log"
    
    while True:
        if check_connectivity():
            # Internet is up
            if is_down:
                # Record reconnection details
                reconnect_time = datetime.now()
                downtime = reconnect_time - last_down_time
                total_downtime += downtime
                log_disruption(disruption_log, start_time=last_down_time, end_time=reconnect_time)
                is_down = False
        else:
            # Internet is down
            if not is_down:
                # Record drop details
                last_down_time = datetime.now()
                total_drops += 1
                current_hour = last_down_time.hour
                hourly_drops[current_hour] = hourly_drops.get(current_hour, 0) + 1
                log_disruption(disruption_log)
                is_down = True

        # Update stats log and console
        log_stats(stats_log)
        display_stats()
        time.sleep(10)

if __name__ == "__main__":
    main()
