try:
    from influxdb_client import InfluxDBClient, Point, WritePrecision
except Exception:
    InfluxDBClient = None
    Point = None
    WritePrecision = None

class InfluxWriter:
    def __init__(self):
        self.enabled = False
        self.client = None
        if InfluxDBClient is None:
            return
        try:
            self.client = InfluxDBClient(url="http://localhost:8086", token="marker-token", org="srh")
            self.write_api = self.client.write_api()
            self.enabled = True
        except Exception:
            self.enabled = False

    def write_line_status(self, line):
        if not self.enabled:
            return
        try:
            point = (
                Point("marker_line")
                .field("total_parts", line.total_parts)
                .field("good_parts", line.good_parts)
                .field("defective_parts", line.defective_parts)
                .field("state_code", line.state_code())
                .field("faulted", 1 if line.faulted else 0)
            )
            self.write_api.write(bucket="marker_line", org="srh", record=point)
        except Exception:
            pass
