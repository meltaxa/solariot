"""
The SH10RS has 4 solar inputs, but is only single phase. It appears
that internally it's almost identical to the three-phase hybrid
inverters, as it responds with zero to queries against them.
There are more addresses that contain data, but I didn't investigate
what they actually were.

Use the modbus-sungrow-scanall.py map to dump all the potential
registers.

Copyright: Rob Thomas <xrobau@gmail.com> May 2024

Licenced under the MIT licence and any additional licence that
the solariot project may be released under.
"""

read_register = {
  "5001":  "nominal_active_power_10",
  "5002":  "output_type",
  "5003":  "daily_power_yield_0.01", # Wh
  "5004":  "total_power_yield_100",  # MWh, but use 5144 instead
  "5006":  "total_running_time",
  "5008":  "internal_temp_10",
  "5009":  "apparent_power_1000", # From Inverter to Grid/Home
  "5011":  "pv1_voltage_10",
  "5012":  "pv1_current_10",
  "5013":  "pv2_voltage_10",
  "5014":  "pv2_current_10",
  "5015":  "pv3_voltage_10",
  "5016":  "pv3_current_10", # Note pv4 is 5115/5116
  "5017":  "total_pv_power",
  "5019":  "grid_voltage_a_10",
  "5020":  "grid_voltage_b_10", # V, returns zero
  "5021":  "grid_voltage_c_10", # V, returns zero
  "5022":  "inverter_current_a_10",  # A
  "5023":  "inverter_current_b_10",  # A, returns zero
  "5024":  "inverter_current_c_10",  # A, returns zero
  "5031":  "total_active_power",
  "5033":  "reactive_power",
  "5034":  "power_factor",
  "5035":  "real_power_factor",
  "5036":  "grid_frequency_10", # Use 5148 instead
  "5038":  "work_state",
  "5091":  "meter_load_power",
  "5115":  "pv4_voltage_10",
  "5116":  "pv4_current_10",
  "5144":  "total_power_yield_10000", # 0.1kWh > MWh - Higher Accuracy (See: 5004)
  "5146":  "negative_voltage_to_ground", # 0.1V
  "5147":  "bus_voltage", # 0.1V
  "5148":  "grid_frequency_100", # 0.01Hz > Hz - Higher Accuracy (See: 5036)
  "13001": "running_state",
  "13002": "daily_pv_energy_10",
  "13003": "total_pv_energy_10",
  "13005": "daily_export_energy_10",
  "13006": "total_export_energy_10",
  "13008": "load_power",
  "13010": "export_power",
  "13011": "grid_import_or_export",
  "13012": "daily_charge_energy_10",
  "13013": "total_charge_energy_10",
  "13015": "co2_emission_reduction",
  "13017": "daily_use_energy_10",
  "13018": "total_use_energy_10",
  "13020": "battery_voltage_10",
  "13021": "battery_current_10",
  "13022": "battery_power",
  "13023": "battery_level_10",
  "13024": "battery_health_10",
  "13025": "battery_temp_10",
  "13026": "daily_discharge_energy_10",
  "13027": "total_discharge_energy_10",
  "13029": "self_consumption_power_today",
  "13030": "grid_state",
  "13031": "backup_current_a_10",
  "13032": "backup_current_b_10",
  "13033": "backup_current_c_10",
  "13034": "pv_power",
  "13035": "total_active_power",
  "13036": "daily_import_energy",
  "13037": "total_import_energy",
  "13038": "battery_capacity"
}

holding_register = {
  "5000": "year",
  "5001": "month",
  "5002": "day",
  "5003": "hour",
  "5004": "minute",
  "5005": "second"
}

scan = """{
  "read": [
     {
       "start": "4999",
       "range": "100"
     },
     {
       "start": "5099",
       "range": "100"
     },
     {
       "start": "5199",
       "range": "100"
     },
     {
       "start": "13000",
       "range": "100"
     }
  ],
  "holding": [
     {
       "start": "4999",
       "range": "100"
     }
  ]
}"""

# Match Modbus registers to pvoutput api fields
# Reference: https://pvoutput.org/help.html#api-addstatus
pvoutput = {
  "Energy Generation": "daily_pv_energy",
  "Power Generation": "total_pv_power",
  "Energy Consumption": "daily_use_energy",
  "Power Consumption": "load_power",
  "Temperature": "internal_temp",
  "Voltage": "grid_voltage"
}
