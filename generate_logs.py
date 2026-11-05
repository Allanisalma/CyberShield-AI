import random
from datetime import datetime, timedelta
from pathlib import Path
random.seed(42)  # For reproducibility
normal_ips = ["192.168.1.10","192.168.1.25","10.0.0.7","172.16.0.4",]
test_ip = "203.0.113.50"
events =[]
start_time = datetime(2026, 10, 21, 10, 0, 0)
for i in range(40):
    timestamp = start_time + timedelta(minutes=i * 2)
    ip = random.choice(normal_ips)
    status = random.choices(["SUCCESS", "FAILED"], weights=[8, 2], k=1)[0]
    events.append((timestamp, ip, status))
for i in range(7):
    timestamp = start_time + timedelta(minutes=100 + i)
    events.append((timestamp, test_ip, "FAILED"))
events.sort(key=lambda event: event[0])
output_file = Path(__file__).parent / "auth.log"
with output_file.open("w", encoding="utf-8") as file:
    file.write("timestamp,ip,status\n")
    for timestamp, ip, status in events:
        file.write(f"{timestamp.isoformat()},{ip},{status}\n")
print("CyberShield AI - Log Generator")
print(f"Total events created: {len(events)}")
print(f"Log file saved to: {output_file}")
print("Expected test case: 7 failed logins attempts from 203.0.113.50")
