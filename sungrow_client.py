#!/usr/bin/env python

from pymodbus.client.sync import ModbusTcpClient
import dweepy
import config

client = ModbusTcpClient(config.inverter_ip, timeout=3, port=502)
client.connect()

slave = 0x01
inverter = {}

modmap = {"5008":  "internal_temp_10",
          "5011":  "pv1_voltage_10",
          "5012":  "pv1_current_10",
          "5013":  "pv2_voltage_10",
          "5014":  "pv1_current_10",
          "5017":  "total_pv_power",
          "5019":  "grid_voltage_10",
          "5022":  "inverter_current_10",
          "5031":  "consumption?",
          "5036":  "grid_frequency_10",
          "13003": "total_pv_energy",
          "13006": "total_export_energy_10",
          "13008": "load_power",
          "13010": "export_power",
          "13011": "grid_import_or_export",
          "13013": "total_charge_energy",
          "13015": "co2_emission_reduction",
          "13018": "total_use_energy",
          "13020": "battery_voltage_10",
          "13022": "battery_power",
          "13023": "battery_level_10",
          "13024": "battery_health_10",
          "13025": "battery_temp_10",
          "13027": "total_discharge_energy_10",
          "13029": "use_power",
          "13034": "pv_power"
         }

holding_register = {"5000": "year",
                     "5001": "month",
                     "5002": "day",
                     "5003": "hour",
                     "5004": "minute",
                     "5005": "second",
                    }

def load_registers(type,start,COUNT=100):
  try:
    if type == "read":
      rr = client.read_input_registers(start, count=COUNT, unit=slave)
    elif type == "holding":
      rr = client.read_holding_registers(start, count=COUNT, unit=slave)
    for num in range(0, COUNT):
      run = start + num + 1
      if type == "read" and modmap.get(str(run)):
        if '_10' in modmap.get(str(run)):
          inverter[modmap.get(str(run))[:-3]] = float(rr.registers[num])/10
        else:
          inverter[modmap.get(str(run))] = rr.registers[num]
      elif type == "holding" and holding_register.get(str(run)):
        inverter[holding_register.get(str(run))] = rr.registers[num]
  except Exception as err:
    print "[ERROR] %s" % err

while True:
  try:
    inverter = {}
    load_registers("read",5000,100) 
    load_registers("read",13000,100) 
    load_registers("holding",4999,100) 
    # Work out if the grid power is being imported or exported
    if inverter['grid_import_or_export'] == 65535:
      export_power = (65535 - inverter['export_power']) * -1
      inverter['export_power'] = export_power
    inverter['timestamp'] = "%s/%s/%s %s:%02d:%02d" % (inverter['day'],inverter['month'],inverter['year'],inverter['hour'],inverter['minute'],inverter['second'])
    result = dweepy.dweet_for(config.guid,inverter)
    print result
  except Exception as err:
    print "[ERROR] %s" % err
    client.close()
    client.connect()
