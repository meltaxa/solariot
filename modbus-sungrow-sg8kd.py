read_register = {
  "5001": "inverter_size_10",      # KW
  "5003": "daily_power_yield_0.01", # Wh
  "5004": "total_power_yield_100",  # MWh
  "5006": "inverter_power_on_hours",  #hrs
  "5008": "internal_temp_10",       # C
  "5011": "pv1_voltage_10",         # V
  "5012": "pv1_current_10",         # A
  "5013": "pv2_voltage_10",         # V
  "5014": "pv2_current_10",         # A
  "5017": "total_pv_power",         # W
  "5019": "grid_voltage_10",        # V
  "5022": "inverter_current_10",    # A
  "5031": "total_active_power",     # W
  "5036": "grid_frequency_10",      # Hz
  "5083": "export_power_overflow",  # W - House Grid Consumption (+ = importing, - = exporting)
  "5084": "export_power_indicator", # W - House Grid Consumption Overflow Indicator
  "5091": "house_loads", # W - House Used Power - All sources
  "5093": "daily_export_energy_0.01", # Wh
  "5095": "total_export_energy_10", # KWh
  "5097": "daily_import_energy_0.01", # Wh
  "5099": "total_import_energy_10", # KWh
  "5101": "daily_self_consumption_energy_0.01", # Wh
  "5103": "total_self_consumption_energy_10",   # KWh
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
            "range": "110"
        }
  ],
  "holding": [
    {
      "start": "4999",
      "range": "6"
    }
  ]
}"""

