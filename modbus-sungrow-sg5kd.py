read_register = {
  "5003":  "daily_power_yield_10",
  "5004":  "total_power_yield",
  "5008":  "internal_temp_10",
  "5011":  "pv1_voltage_10",
  "5012":  "pv1_current_10",
  "5013":  "pv2_voltage_10",
  "5014":  "pv2_current_10",
  "5017":  "total_pv_power",
  "5019":  "grid_voltage_10",
  "5022":  "inverter_current_10",
  "5031":  "total_active_power",
  "5036":  "grid_frequency_10",
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
       "range": "40"
     }
  ],
  "holding": [
    {
      "start": "4999",
      "range": "100"
    }
  ]
}"""
