inverter_ip = "192.168.1.23"
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
# Optional:
influxdb_ip = "192.168.1.128"
influxdb_port = 8086
influxdb_user = "user"
influxdb_password = "password"
influxdb_database = "inverter"
influxdb_ssl = True
influxdb_verify_ssl = False
# Optional
mqtt_server = "192.168.1.128"
mqtt_port = 1883
mqtt_topic = "inverter/stats"
