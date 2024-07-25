import os
import time

from influxdb_client_3 import InfluxDBClient3, Point
from pyctiarbin import CyclerInterface
from dotenv import load_dotenv
load_dotenv()

token = os.environ.get("INFLUXDB_TOKEN")
org = "Eng"
host = "https://us-east-1-1.aws.cloud2.influxdata.com"

client = InfluxDBClient3(host=host, token=token, org=org)

CYCLER_INTERFACE_CONFIG = {
    "ip_address": "127.0.0.1",
    "port": 9031,
    "timeout_s": 3,
    "msg_buffer_size": 4096
}

cycler_interface = CyclerInterface(CYCLER_INTERFACE_CONFIG)
channel_status = cycler_interface.read_channel_status(channel=8)

database="arbin-cycler"

tag_names = ['status', 'schedule', 'testname', 'step_and_cycle_format']
field_names = ['test_time_s', 'step_time_s', 'voltage_v', 'current_a', 'power_w', 'charge_capacity_ah', 'discharge_capacity_ah', 'charge_energy_wh', 'discharge_energy_wh']

while True:
    for channel_num in range(1, 9):
        channel_status = cycler_interface.read_channel_status(channel=channel_num)
        if channel_status['status'] in ('Idle', 'Finished'):
            continue
        point = Point("channel_status").tag("channel_num_1based", channel_num)
        for tag_name in tag_names:
            point = point.tag(tag_name, channel_status[tag_name])
        for field_name in field_names:
            point = point.field(field_name, channel_status[field_name])
        client.write(database=database, record=point)
        print(point)
    time.sleep(5)