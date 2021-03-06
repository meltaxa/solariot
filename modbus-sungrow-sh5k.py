read_register = {
  "5001":  "5001",
  "5003":  "5003",
  "5004":  "5004",
  "5005":  "5005",
  "5006":  "5006",        
  "5007":  "5007",    
  "5008":  "internal_temp_10",
  "5009":  "5009",    
  "5011":  "pv1_voltage_10",
  "5012":  "pv1_current_10",
  "5013":  "pv2_voltage_10",
  "5014":  "pv2_current_10",
  "5015":  "5015",    
  "5016":  "5016",    
  "5017":  "total_pv_power",
  "5018":  "5018",    
  "5019":  "grid_voltage_10",
  "5020":  "5020",    
  "5021":  "5021",    
  "5022":  "inverter_current_10",
  "5023":  "5023",    
  "5031":  "5031",
  "5032":  "5032",
  "5036":  "grid_frequency_10",
  "5037":  "5037",
  "13001": "running_state",
  "13002": "daily_pv_energy_10",
  "13003": "total_pv_energy_10",
  "13004": "13004",
  "13005": "daily_export_energy_10",
  "13006": "total_export_energy_10",
  "13007": "13007",
  "13008": "load_power",
  "13009": "13009",
  "13010": "export_power",
  "13011": "grid_import_or_export",
  "13012": "daily_charge_energy_10",
  "13013": "total_charge_energy_10",
  "13014": "13014",
  "13015": "co2_emission_reduction",
  "13016": "13016",
  "13017": "daily_use_energy_10",
  "13018": "total_use_energy_10",
  "13019": "13019",
  "13020": "battery_voltage_10",
  "13021": "battery current_10",
  "13022": "battery_power",
  "13023": "battery_level_10",
  "13024": "battery_health_10",
  "13025": "battery_temp_10",
  "13026": "daily_discharge_energy_10",
  "13027": "total_discharge_energy_10",
  "13028": "13028",
  "13029": "use_power",
  "13030": "13030",
  "13031": "inverter_current_10",
  "13032": "13032",
  "13033": "13033",
  "13034": "pv_power",
  "13035": "13035",
  "13036": "13036",
  "13037": "13037",
  "13038": "13038"
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
       "start": "5000",
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
