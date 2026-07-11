"""
The SH10RS has 4 solar inputs, but is only single phase. It appears
that internally it's almost identical to the three-phase hybrid
inverters, as it responds with zero to queries against them.
There are more addresses that contain data, but I didn't investigate
what they actually were.

Use the modbus-sungrow-scanall.py map to dump all the potential
registers.

Cross-checked against Sungrow's "Communication Protocol of Residential
Hybrid Inverter" V1.1.4 on 2026-07-10 and corrected against live readings
where the doc and this specific unit disagreed (see per-register comments
below). Several registers the doc lists (e.g. daily_import_energy,
grid_frequency's old 5148 alternative) are confirmed non-functional on
this hardware despite being documented; several the doc marks "reserved"
(e.g. 5031, 5091) return real data and are kept as empirical findings.

Copyright: Rob Thomas <xrobau@gmail.com> May 2024

Licenced under the MIT licence and any additional licence that
the solariot project may be released under.
"""

read_register = {
  "5001":  "nominal_active_power_10",
  "5002":  "output_type",
  "5003":  "daily_power_yield_0.01",  # Wh (intentional: raw * 100 converts the doc's 0.1kWh unit to Wh)
  "5004":  "total_power_yield_u32_10",  # kWh. Was read as a single register (wraps every 6553.5kWh); now a proper U32 pair
  "5006":  "total_running_time",  # doc marks 5006-5007 reserved; kept as empirical (reads 0 currently)
  "5008":  "internal_temp_s16_10",  # doc: S16, was read unsigned
  "5009":  "apparent_power_1000",  # From Inverter to Grid/Home; doc marks 5009-5010 reserved, kept as empirical
  "5011":  "pv1_voltage_10",
  "5012":  "pv1_current_10",
  "5013":  "pv2_voltage_10",
  "5014":  "pv2_current_10",
  "5015":  "pv3_voltage_10",
  "5016":  "pv3_current_10",  # Note pv4 is 5115/5116
  "5017":  "total_pv_power_u32",  # W. doc: Total DC power. Was read as a single register; now a proper U32 pair
  "5019":  "grid_voltage_a_10",
  "5020":  "grid_voltage_b_10",  # V, returns zero (single phase)
  "5021":  "grid_voltage_c_10",  # V, returns zero (single phase)
  "5022":  "inverter_current_a_10",  # A. doc marks 5022-5030 reserved; kept as empirical. See also the officially documented 13031-13033
  "5023":  "inverter_current_b_10",  # A, returns zero
  "5024":  "inverter_current_c_10",  # A, returns zero
  "5031":  "total_active_power_alt",  # undocumented (doc has a gap here); see the officially documented 13034-13035 total_active_power
  "5033":  "reactive_power_s32",  # var. Was read as a single unsigned register; now a proper S32 pair
  "5035":  "power_factor_s16_1000",  # doc: S16, 0.001. Previously misaddressed at 5034 (that's actually reactive_power's high word) and read unsigned
  "5036":  "grid_frequency_10",  # Use grid_frequency_precise (5242) instead
  "5038":  "work_state",  # undocumented (doc has a gap here); kept as empirical
  "5091":  "meter_load_power",  # undocumented; reads 0 even during confirmed active grid draw - looks non-functional on this unit. See meter_active_power_a (5603, S32) for a documented, verified-working alternative
  "5115":  "pv4_voltage_10",
  "5116":  "pv4_current_10",
  "5146":  "negative_voltage_to_ground",  # 0.1V, undocumented; kept as empirical
  "5147":  "bus_voltage",  # 0.1V, undocumented; kept as empirical
  "5214":  "battery_power_wide_s32",  # W, signed. Charge/discharge direction; use in place of battery_power (13022, unsigned) for PVOutput's b1
  "5242":  "grid_frequency_precise_100",  # 0.01Hz -> Hz. Replaces the old 5148 entry, which reads 0 (non-functional) despite the grid being live; 5242 is the doc's official high-precision register and reads correctly (verified 49.99Hz)
  "13000":  "running_state",  # Was misaddressed at 13001 (that's actually power_flow_status). Verified live: 0x8200 = 'Dispatch Running' (Appendix 4.1)
  "13001":  "power_flow_status",  # Was mislabeled 'running_state'. Verified live: bitmask, e.g. 40 = bit3 (load active) + bit5 (importing from grid) (Appendix 4.2)
  "13002":  "daily_pv_energy_10",
  "13003":  "total_pv_energy_u32_10",  # Was a single register; now a proper U32 pair
  "13005":  "daily_export_energy_pv_10",  # Renamed from daily_export_energy: doc scope is PV export only, not total export. See daily_export_energy_total (13045) for all-source, currently unmapped - ask if you want it added
  "13006":  "total_export_energy_pv_u32_10",  # Renamed (PV-only scope, see 13005) and fixed to a proper U32 pair
  "13008":  "load_power_s32",  # W. Was a single register; now a proper S32 pair (no observed numeric difference yet - high word is still 0 on this young system)
  "13010":  "export_power_s32",  # W. Was a single register; now a proper S32 pair. Absorbs register 13011, so the old standalone 'grid_import_or_export' entry (unused by this model anyway - that logic is sh5k-specific in solariot.py) is gone
  "13012":  "daily_charge_energy_pv_10",  # Renamed from daily_charge_energy: doc scope is PV-sourced charging only. See daily_charge_energy_total (13040) for all-source, currently unmapped
  "13013":  "total_charge_energy_pv_u32_10",  # Renamed (PV-only scope, see 13012) and fixed to a proper U32 pair. The general/all-source lifetime figure is total_charge_energy (13041), used for the PVOutput 'Battery Lifetime Charge' mapping instead of this one
  "13017":  "daily_direct_pv_consumption_10",  # Renamed from daily_use_energy: doc name is 'Daily direct energy consumption' - PV energy consumed directly by loads only, NOT total daily consumption (there's no single register for that; see chat notes on the load_power-based PVOutput workaround)
  "13018":  "total_direct_pv_consumption_u32_10",  # Renamed (see 13017) and fixed to a proper U32 pair
  "13020":  "battery_voltage_10",
  "13021":  "battery_current_10",  # doc: U16 unsigned (no direction). See battery_current_precise (5631, S16) for a signed alternative if needed
  "13022":  "battery_power",  # doc: U16 unsigned (no direction) - confirmed NOT usable for signed charge/discharge values. Use battery_power_wide (5214, S32) instead
  "13023":  "battery_level_10",
  "13024":  "battery_health_10",
  "13025":  "battery_temp_s16_10",  # doc: S16, was read unsigned
  "13026":  "daily_discharge_energy_10",
  "13027":  "total_discharge_energy_u32_10",  # Was a single register; now a proper U32 pair
  "13029":  "self_consumption_today_10",  # 0.1%. Was missing the /10 scale entirely (raw value used directly)
  "13030":  "grid_state",  # doc marks 13030 reserved; kept as empirical
  "13031":  "grid_current_a_s16_10",  # Renamed from backup_current_a: doc says 13031-13033 is 'Phase A/B/C current' (grid-side), signed. Was read unsigned. Actual backup-circuit current is a different, currently unmapped register block (5720-5722)
  "13032":  "grid_current_b_s16_10",  # See 13031
  "13033":  "grid_current_c_s16_10",  # See 13031
  "13034":  "total_active_power_s32",  # W. The officially documented register (was a naming collision with the undocumented 5031, renamed to total_active_power_alt). Was a single register; now a proper S32 pair
  "13036":  "daily_import_energy_10",  # Was missing the /10 scale. NOTE: confirmed non-functional on this unit as of 2026-07-10 - reads 0 despite verified ~45kWh import that day (cross-checked against the Sungrow app and a third-party IoTaWatt meter). total_import_energy (13037) does update correctly, so the lifetime counter works even though this daily one doesn't
  "13037":  "total_import_energy_u32_10",  # Was a single register; now a proper U32 pair. Verified working (increases over time), unlike the daily_import_energy (13036) counter
  "13039":  "battery_capacity_10",  # 0.1kWh (or 1Ah for lead-acid). Was wrongly addressed at 13038, which is actually the high word of total_import_energy's U32 pair (13037-13038)
  "13041":  "total_charge_energy_u32_10",  # New: the general/all-source lifetime battery charge figure (doc: 'Total Charge Energy'), used for the PVOutput 'Battery Lifetime Charge' mapping. The old 13013 entry only counted PV-sourced charging - see total_charge_energy_pv
  "13043":  "drm_state"
}

holding_register = {
  "5000":  "year",
  "5001":  "month",
  "5002":  "day",
  "5003":  "hour",
  "5004":  "minute",
  "5005":  "second"
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
       "start": "12999",
       "range": "101"
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
  "Energy Consumption": "daily_direct_pv_consumption",
  "Power Consumption": "load_power",
  "Temperature": "internal_temp",
  "Voltage": "grid_voltage_a",
  "Battery Power": "battery_power_pvoutput",
  "Battery State of Charge": "battery_level",
  "Battery Lifetime Charge": "total_charge_energy",
  "Battery Lifetime Discharge": "total_discharge_energy"
}
