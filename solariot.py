#!/usr/bin/env python

# Copyright (c) 2017 Dennis Mellican
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from pymodbus.client.sync import ModbusTcpClient
import config
import dweepy
import json
import time
from influxdb import InfluxDBClient
import requests
requests.packages.urllib3.disable_warnings() 

# Load the modbus register map for the inverter
modmap_file = "modbus-" + config.model
modmap = __import__(modmap_file)

client = ModbusTcpClient(config.inverter_ip, 
                         timeout=3, 
                         port=config.inverter_port)
client.connect()

try:
  flux_client = InfluxDBClient(config.influxdb_ip,
                               config.influxdb_port,
                               config.influxdb_user,
                               config.influxdb_password,
                               config.influxdb_database,
                               ssl=config.influxdb_ssl,
                               verify_ssl=config.influxdb_verify_ssl)
except:
  flux_client = None

inverter = {}
bus = json.loads(modmap.scan)

def load_registers(type,start,COUNT=100):
  try:
    if type == "read":
      rr = client.read_input_registers(int(start), 
                                       count=int(COUNT), 
                                       unit=config.slave)
    elif type == "holding":
      rr = client.read_holding_registers(int(start), 
                                         count=int(COUNT), 
                                         unit=config.slave)
    for num in range(0, int(COUNT)):
      run = int(start) + num + 1
      if type == "read" and modmap.read_register.get(str(run)):
        if '_10' in modmap.read_register.get(str(run)):
          inverter[modmap.read_register.get(str(run))[:-3]] = float(rr.registers[num])/10
        else:
          inverter[modmap.read_register.get(str(run))] = rr.registers[num]
      elif type == "holding" and modmap.holding_register.get(str(run)):
        inverter[modmap.holding_register.get(str(run))] = rr.registers[num]
  except Exception as err:
    print "[ERROR] %s" % err

while True:
  try:
    inverter = {}
    for i in bus['read']:
      load_registers("read",i['start'],i['range']) 
    for i in bus['holding']:
      load_registers("holding",i['start'],i['range']) 

    # Sungrow inverter specifics:
    # Work out if the grid power is being imported or exported
    if config.model == "sungrow-sh5k" and \
       inverter['grid_import_or_export'] == 65535:
        export_power = (65535 - inverter['export_power']) * -1
        inverter['export_power'] = export_power
    inverter['timestamp'] = "%s/%s/%s %s:%02d:%02d" % (
      inverter['day'],
      inverter['month'],
      inverter['year'],
      inverter['hour'],
      inverter['minute'],
      inverter['second'])
    print inverter
    try:
      result = dweepy.dweet_for(config.dweepy_uuid,inverter)
      print "[INFO] Sent to dweet.io"
    except:
      result = None
    if flux_client is not None:
      metrics = {}
      tags = {}
      fields = {}
      metrics['measurement'] = "Sungrow"
      tags['location'] = "Gabba"
      metrics['tags'] = tags
      metrics['fields'] = inverter
      flux_client.write_points([metrics])
      print "[INFO] Sent to InfluxDB"

  except Exception as err:
    print "[ERROR] %s" % err
    client.close()
    client.connect()
  time.sleep(8)
