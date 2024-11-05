import time
from datetime import datetime
import random
from collections import defaultdict

log_sources = ["AServer1", "AServer2", "DBServer1", "NetworkRouter"]
event_types = ["Info", "Error", "Warn", "Debug"]


def generate_log(source):
    event_type = random.choice(event_types)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"{event_type} - Sample log message from {source}"
    return {
        "timestamp": timestamp,
        "source": source,
        "event_type": event_type,
        "message": message
    }

def capture_logs(num_logs):
    logs = []
    for _ in range(num_logs):
        source = random.choice(log_sources)
        log_entry = generate_log(source)
        logs.append(log_entry)
        time.sleep(0.1) 
    return logs

def correlate_events(logs):
    event_count = defaultdict(lambda: defaultdict(int))  
    correlated_events = []
    for log in logs:
        event_count[log["source"]][log["event_type"]] += 1
        if event_count[log["source"]]["ERROR"] >= 3:  
            correlated_events.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "correlation_rule": "ERROR Spike",
                "source": log["source"],
                "message": f"High number of ERROR events detected on {log['source']}"
            })

    return correlated_events


def display_logs(logs):
    print("\nCaptured Logs:")
    for log in logs:
        print(f"{log['timestamp']} | {log['source']} | {log['event_type']} | {log['message']}")

def display_correlated_events(correlated_events):
    if correlated_events:
        print("\nCorrelated Events:")
        for event in correlated_events:
            print(f"{event['timestamp']} | {event['correlation_rule']} | {event['source']} | {event['message']}")
    else:
        print("\nNo correlated events detected.")

def main():
    while True:
        print("\nLog Capturing and Event Correlation")
        print("1. Capture Logs")
        print("2. Correlate Events")
        print("3. Terminate")
        choice = input("Choose an option : ")

        if choice == '1':
            num_logs = int(input("Enter the number of logs to capture: "))
            logs = capture_logs(num_logs)
            display_logs(logs)

        elif choice == '2':
            num_logs = int(input("Enter the number of logs to capture and correlate: "))
            logs = capture_logs(num_logs)
            display_logs(logs)
            correlated_events = correlate_events(logs)
            display_correlated_events(correlated_events)

        elif choice == '3':
            print("Terminating the program.")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()