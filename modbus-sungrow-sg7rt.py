""" 
Model,	Type code, 	MPPT,	String/MPPT
SG7.0RT	0x243C		2		2;1
"""

read_register = {
#  "5000": "device_type_code",				# Inverter Model, See Appendix 6
  "5001": "nominal_active_power_10",		# 0.1kW > kW 		- Max kW Inverter can run at
#  "5002": "output_type",					# 0=2P, 1=3P4L, 2=3P3L
  "5003": "daily_power_yield_10",			# 0.1 kWh > kWh 	- Daily, Energy generated (PVOutput: Energy Generation)
#  "5004": "total_power_yield_1000",		# kWh > MWh - accuracy to 1 (use 5114)
  "5006": "total_ongrid_running_time",		# hr
  "5008": "internal_temp_10",				# 0.1C > C
  "5009": "apparent_power_1000",			# 0.1Va > KVa 		- From Inverter to Grid/Home
  "5011": "mppt1_voltage_10",				# 0.1V > V
  "5012": "mppt1_current_10",				# 0.1A > A
  "5013": "mppt2_voltage_10",				# 0.1V > V
  "5014": "mppt2_current_10",				# 0.1A > A
#  "5015": "mppt3_voltage_10",				# 0.1V > V
#  "5016": "mppt3_current_10",				# 0.1A > A
  "5017": "total_pv_power",					# W - From Panels to Inverter
  "5019": "phase_voltage_a_10",			# 0.1V > V
  "5020": "phase_voltage_b_10",			# 0.1V > V
  "5021": "phase_voltage_c_10",			# 0.1V > V
  "5022": "phase_current_a_10",			# 0.1A > A
  "5023": "phase_current_b_10",			# 0.1A > A
  "5024": "phase_current_c_10",			# 0.1A > A
#  "5025": - 5030: Reserved, All scan at xFF xFF
  "5031": "total_active_power",				# W					- Current, Inverter to Grid/Home (PVOutput: Power Generation)
  "5033": "total_reactive_power",			# W
  "5035": "power_factor",           		# >0 leading, <0 lagging
  "5036": "grid_frequency_10",      		# 0.1Hz > Hz (Use 5148)
#  "5037":  Reserved
  "5037": "unknown_aa",            			# TBD
#  "5038": "work_state1",					# See Appendix 1. 5039-5045 Fault Date+time
#  "5046": - 5048: Reserved, All scan at x00 x00
  "5049": "nominal_reactive_power",			# 0.1kV		
#  "5071": "array_insulation_resistance_10",# k-ohm
#  "5072": - 5076: Reserved, All scan at xFF xFF
#  "5077": "active_power_reg_setpoint_1000",# 1w > kW
#  "5079": "reactive_power_reg_setpoint", 	# 1Va
#  "5081": "work_state2",					# See Appendix 2.
  # Meter power 5083 - 5104
  "5083": "meter_power_overflow",					# 1w				- (65535 - meter_power) = Inverter to Grid
  "5084": "meter_power_indicator",					# 1w
#  "5085": "meter_phase_a",					# 1w
#  "5087": "meter_phase_b",					# 1w
#  "5089": "meter_phase_c",					# 1w
  "5091": "meter_load_power",				# 1w				- meter_load_power = Grid to House
#  "5093": "meter_daily_export",			# 0.1Kw
#  "5095": "meter_total_export",			# 0.1Kw
#  "5097": "meter_daily_import",			# 0.1Kw
#  "5099": "meter_total_import",			# 0.1Kw
#  "5101": "meter_daily_consumption",		# 0.1Kw
#  "5103": "meter_toal_consumption",		# 0.1Kw  
  "5113": "daily_operation_time",			# 1m
#  "5114": "present_country",				# See Appendix 4
#  "5115": "mppt4_voltage_10",				# 0.1V > V
#  "5116": "mppt4_current_10",				# 0.1A > A
#  "5117": "mppt5_voltage_10",				# 0.1V > V
#  "5118": "mppt5_current_10",				# 0.1A > A
#  "5119": "mppt6_voltage_10",				# 0.1V > V
#  "5120": "mppt6_current_10",				# 0.1A > A
#  "5121": "mppt7_voltage_10",				# 0.1V > V
#  "5122": "mppt7_current_10",				# 0.1A > A
#  "5123": "mppt8_voltage_10",				# 0.1V > V
#  "5124": "mppt8_current_10",				# 0.1A > A
#  "5125": - 5027: Reserved
  "5128": "monthly_power_yields_10",  		# 0.1kW
#  "5130": "mppt9_voltage_10",         		# 0.1V > V
#  "5131": "mppt9_current_10",         		# 0.1A > A
#  "5132": "mppt10_voltage_10",         	# 0.1V > V
#  "5133": "mppt10_current_10",         	# 0.1A > A
#  "5134": "mppt11_voltage_10",         	# 0.1V > V
#  "5135": "mppt11_current_10",         	# 0.1A > A
#  "5136": "mppt12_voltage_10",         	# 0.1V > V
#  "5137": "mppt12_current_10",         	# 0.1A > A
#  "5138": - 5143: Reserved
  "5144": "total_power_yield_10000",  		# 0.1kWh > MWh - Higher Accuracy (See: 5004)
  "5146": "negative_voltage_to_ground", 	# 0.1V
  "5147": "bus_voltage", 					# 0.1V
  "5148": "grid_frequency_100",      		# 0.01Hz > Hz - Higher Accuracy (See: 5036)
#  "5149": Reserved, All scan at xFF xFF
#  "5150": "pid_work_state",      			# 2: PID Recover Operation, 4: Anti-PID Operation, 8: PID Abnormity
#  "5151": "pid_alarm_code",      			# 432:PID resistance abnormal 433:PID function abnormal 434:PID overvoltage/overcur rent protection
#  "5152": - 7012: Reserved
  "5216": "export_power_overflow",			# W - House Grid Consumption (+ = importing, - = exporting) #new read register
  "5217": "export_power_indicator", 		# W - House Grid Consumption Overflow Indicator				#new read register
  "5218": "power_meter",            		# W - House Overall Consumption		
  "5220": "unknown_cb",            			# TBD
  "5221": "unknown_cc",            			# TBD
  "5222": "unknown_cd",            			# TBD
#  "5223": "x_daily_power_yield",			# Seems to be: 5003: daily_power_yield
#  "5224": "x_monthly_power_yields",		# Seems to be: 5128: monthly_power_yields
#  "5226": "x_total_power_yield",			# Seems to be: 5144: total_power_yield
#  "5228": "x_total_power_yield",			# Seems to be: 5144: total_power_yield
#  "5230": "x_total_ongrid_running_time",   # Seems to be: 5006: total_ongrid_running_time
#  "5232": "x_apparent_power",          	# Seems to be: 5009: apparent_power
  "5234": "unknown_cm",            			# TBD
  "5235": "unknown_cn",            			# TBD
#  "5236": "x_total_pv_power",            	# Seems to be: 5017: total_pv_power
#  "5238": "x_apparent_power",            	# Seems to be: 5009: apparent_power
#  "5240": "x_daily_operation_time",        # Seems to be: 5113: daily_operation_time
#  "5241": "x_power_factor",            	# Seems to be: 5035: power_factor
#  "5242": "x_grid_frequency",            	# Seems to be: 5148: grid_frequency
#  "5243": "x_negative_voltage_to_ground",	# Seems to be: 5146: negative_voltage_to_ground
#  "5244": "x_bus_voltage",            		# Seems to be: 5147: bus_voltage
#  "5245": "x_internal_temp",     			# Seems to be: 5008: internal_temp
#  "5246": "x_array_insulation_resistance",	# Seems to be: 5071: array_insulation_resistance
#  "5247": "x_phase_voltage_a",       		# Seems to be: 5019: phase_voltage_a
#  "5248": "x_phase_voltage_b",       		# Seems to be: 5020: phase_voltage_b
#  "5249": "x_phase_voltage_c",       		# Seems to be: 5021: phase_voltage_c
#  "5250": "x_phase_current_a",       		# Seems to be: 5022: phase_current_a
#  "5251": "x_phase_current_b",       		# Seems to be: 5023: phase_current_b
#  "5252": "x_phase_current_c",       		# Seems to be: 5024: phase_current_c
#  "7013": "string_1_current",     			# 0.01A
#  "7014": "string_2_current",        		# 0.01A
#  "7015": "string_3_current",        		# 0.01A
#  "7016": "string_4_current",         		# 0.01A
#  "7017": "string_5_current",         		# 0.01A
#  "7018": "string_6_current",         		# 0.01A
#  "7019": "string_7_current",         		# 0.01A
#  "7020": "string_8_current",        		# 0.01A
#  "7021": "string_9_current",       		# 0.01A
#  "7022": "string_10_current",        		# 0.01A
#  "7023": "string_11_current",        		# 0.01A
#  "7024": "string_12_current",        		# 0.01A
#  "7025": "string_13_current",        		# 0.01A
#  "7026": "string_14_current",        		# 0.01A
#  "7027": "string_15_current",        		# 0.01A
#  "7028": "string_16_current",         	# 0.01A
#  "7029": "string_17_current",         	# 0.01A
#  "7030": "string_18_current",        		# 0.01A
#  "7031": "string_19_current",        		# 0.01A
#  "7032": "string_20_current",        		# 0.01A
#  "7033": "string_21_current",        		# 0.01A
#  "7034": "string_22_current",        		# 0.01A
#  "7035": "string_23_current",         	# 0.01A
#  "7036": "string_24_current"         		# 0.01A
}

holding_register = {
  "5000": "year",
  "5001": "month",
  "5002": "day",
  "5003": "hour",
  "5004": "minute",
  "5005": "second",
  "5006": "start_stop", 					# 0xCF (Start) 0xCE (Stop)
#  "5007": "power_limitation_switch", 		# 0xAA: Enable; 0x55: Disable
#  "5008": "power_limitation_setting", 		# See Appendix 6
#  "5009": Reserved
#  "5010": "export_power_limitation", 		# 0xAA: Enable; 0x55: Disable
#  "5011": "export_power_limitation_value", # Export power limitation value
#  "5012": "current_transformer_output_cur",# 1-100
#  "5013": "current_transformer_range", 	# 1-10000
#  "5014": "current transformer", 			# 10- Internal 1- External
#  "5015": "export_power_limitation_perc", 	# 1-1000
#  "5016": "installed_pv_power", 			# 1-30000
#  "5019": "power_factor_setting", 			# 1-10000
#  "5020": "schedule_achieve_ol",			# 0xAA: Enable; 0x55: Disable
#  "5021": - 5033: Reserved
#  "5035": "night_svg_switch", 				# 0xAA: Enable; 0x55: Disable
#  "5036": "reactive_power_adjustment_mode", # 
#  "5037": "reactive_power_perc_setting", 	# -1000 to 1000
#  "5038": Reserved
#  "5039": "power_limitation_adjustment", 	# See Appendix 6
#  "5040": "reactive_power_adjustment", 		# See Appendix 6
#  "5040": "pid_recovery", 					# 0xAA: Enable; 0x55: Disable
#  "5042": "anti_pid", 						# 0xAA: Enable; 0x55: Disable
#  "5043": "full_day_pid_suppression", 		# 0xAA: Enable; 0x55: Disable
#  "5044": - 5047: Reserved
#  "5049": - 5154 - Q(U) Curve
#  "5155": - 5199: Reserved
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
        }
  ],
  "holding": [
    {
      "start": "4999",
      "range": "20"
    }
  ]
}"""

# Match Modbus registers to pvoutput api fields
# Reference: https://pvoutput.org/help.html#api-addstatus
pvoutput = {
  "Energy Generation": "daily_power_yield",
  "Power Generation": "total_active_power",
  "Power Consumption": "meter_load_power",
  "Temperature": "internal_temp",
  "Voltage": "phase_voltage_b"
}
