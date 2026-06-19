import random
import time
from influxdb_client import InfluxDBClient, Point

client = InfluxDBClient(url="http://localhost:8086", token="marker-token", org="srh")
write_api = client.write_api()

total = 0
good = 0
defective = 0
print("Sending marker line telemetry. Press Ctrl+C to stop.")
while True:
    total += 1
    if random.random() < 0.12:
        defective += 1
        state = 3
        faulted = 1
    else:
        good += 1
        state = 1
        faulted = 0
    point = Point("marker_line").field("total_parts", total).field("good_parts", good).field("defective_parts", defective).field("state_code", state).field("faulted", faulted)
    write_api.write(bucket="marker_line", org="srh", record=point)
    print(f"total={total} good={good} defective={defective}")
    time.sleep(1)
