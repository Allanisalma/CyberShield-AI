from pathlib import Path
from collections import Counter
import csv
BASE_DIR = Path(__file__).parent
LOG_FILE = BASE_DIR / "auth.log"
REPORT_FILE = BASE_DIR / "security_report.csv"
THRESHOLD = 5
def analyze_logs():
    if not LOG_FILE.exists():
        print("ERROR: auth.log was not found")
        return
    failed_attempts = Counter()
    total_events = 0
    successful_events = 0
    with LOG_FILE.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            total_events += 1
            ip = row["ip"]
            status = row["status"]
            if status == "SUCCESS":
                successful_events += 1
            elif status == "FAILED":
                failed_attempts[ip] += 1
    alerts = []
    for ip, count in failed_attempts.most_common():
        if count >= THRESHOLD:
            alerts.append({"ip": ip, "failed_attempts": count, "severity": "High"})
    with REPORT_FILE.open("w", encoding="utf-8", newline="") as file:
        fieldnames = ["ip", "failed_attempts", "severity"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(alerts)
    print("\n===== CyberShield AI =====")
    print(f"Total events: {total_events}")
    print(f"Successful logins: {successful_events}")
    print(f"Failed logins: {sum(failed_attempts.values())}")
    print(f"Alerts found: {len(alerts)}")
    for alert in alerts:
        print(f"[{alert['severity']}] " f"IP {alert['ip']} | " f"Failed_attempts: {alert['failed_attempts']}")
        print(f"\nReport saved to: {REPORT_FILE}")
if __name__ == "__main__":
    analyze_logs()