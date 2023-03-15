inverter_ip = "192.168.1.23"
# set inverter_port to 502 for ModbusTCP,
# If you have a WiNet-S dongle set to 8082 to use HTTP requests
inverter_port = 502
# Slave Defaults
# Sungrow: 0x01
# SMA: 3
slave = 0x01
model = "sungrow-sh5k"
timeout = 3
scan_interval = 10

# Optional:
dweepy_uuid = "random-uuid"

# optional
# prometheus = True
# prometheus_port = 8000

# Optional:
influxdb_ip = "192.168.1.128"
influxdb_port = 8086
influxdb_user = "user"
influxdb_password = "password"
influxdb_database = "inverter"
influxdb_ssl = True
influxdb_verify_ssl = False

# Optional
#mqtt_server = "192.168.1.128"
#mqtt_port = 1883
#mqtt_topic = "inverter/stats"
#mqtt_username = "user"
#mqtt_password = "password"

# Optional
#pvoutput_api = "api_key"
#pvoutput_sid = "system_id"
# 60 for regular accounts, 300 for donation accounts
#pvoutput_rate_limit = 60
# This sends the c1 option to PVOutput. See here for details https://pvoutput.org/help/api_specification.html#cumulative-energy
#pvoutput_cumulative = True
# This only sends the v2 and v4 (Power) values to PVOutput. See here for details https://pvoutput.org/help/api_specification.html#power-and-energy-calculation
#pvoutput_power_only = False


# Optional: save telemetry to a json file
#json_file = "telemetry.json"
# This option, when set to True, writes new lines to the end of the current file.  When set to False you get a single (latest) line per file
#append_log = False
