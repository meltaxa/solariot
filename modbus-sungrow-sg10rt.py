read_register = {
  "5003": "daily_power_yield_0.01", # Wh
  "5004": "total_power_yield_100",  # MWh
  "5006": "total_ongrid_running_time",  # hr
  "5008": "internal_temp_10",       # C
  "5009": "apparent_power_0.001",  	# kVa
  "5011": "pv1_voltage_10",         # V
  "5012": "pv1_current_10",         # A
  "5013": "pv2_voltage_10",         # V
  "5014": "pv2_current_10",         # A
  "5017": "total_pv_power",         # W
  "5019": "grid_voltage_a_10",      # V
  "5020": "grid_voltage_b_10",		  # V
  "5021": "grid_voltage_c_10",		  # V
  "5022": "inverter_current_a_10",  # A
  "5023": "inverter_current_b_10",  # A
  "5024": "inverter_current_c_10",  # A
  "5031": "total_active_power",     # W
  "5036": "grid_frequency_10",      # Hz
  "5071": "array_insulation_resistance_10",  	# k-ohm
  "5113": "daily_operation_time",  				# m
  "5128": "monthly_power_yield_0.01",			# Wh
  
  "5216": "export_power_overflow",  # W - House Grid Consumption (+ = importing, - = exporting) #new read register
  "5217": "export_power_indicator", # W - House Grid Consumption Overflow Indicator				#new read register
  "5218": "power_meter",            # W - House Overall Consumption								#new read register

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
            "start": "5100",
            "range": "125"
        }
  ],
  "holding": [
    {
      "start": "4999",
      "range": "10"
    }
  ]
}"""

# Match Modbus registers to pvoutput api fields
# Reference: https://pvoutput.org/help.html#api-addstatus
pvoutput = {
  "Energy Generation": "daily_power_yield",
  "Power Generation": "total_active_power",
  "Temperature": "internal_temp",
  "Voltage": "grid_voltage_a"
}
