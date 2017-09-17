# sungrow_client

Stream your Sungrow Inverter data to a real time dashboard.

![alt tag](docs/freeboard-dashboard-solar-example.png)

## Prequisites

The Sungrow Inverter must be accessible on the network using TCP.

This script should work on most Sungrow Inverters. See the section below on confirmed
models.

Metrics are streamed to [dweet.io](https://dweet.io/) a free IoT messaging service. No sign up is required.

Data is visualised using a free dashboard service from [Freeboard](https://freeboard.io/). 

Install the required Python libraries for pymodbus and dweepy:

```
pip install -r requirements.txt
```

## Installation

1. Log in to the PubNub site and generate your API keys.

2. Download or clone this repository to your local workstation.

3. Update the config.py file with your inverter's IP address and give your Inverter a unique name which will be used in dweet.io. Generate a random UUID at (https://www.uuidgenerator.net)[https://www.uuidgenerator.net/].

4. Run the sungrow_client script.

5. Log in to the Freeboard website and create a dashboard using your dweet.io as a data source.

## The Sungrow Modbus Map

This script works on the following confirmed Sungrow Inverter models:
* SH5K+ (connected to a GCL Battery)

The Sungrow SH5K+ modbus map was generated manually by scraping all registers. There are
still outstanding metrics to be identified. Help me complete the map.

Input registers:
```
5008:  internal_temp
5011:  pv1_voltage
5012:  pv1_current
5013:  pv2_voltage
5014:  pv1_current
5017:  total_pv_power
5019:  grid_voltage
5022:  inverter_current
5031:  consumption?
5036:  grid_frequency
13003: total_pv_energy
13006: total_export_energy
13008: load_power
13010: export_power
13013: total_charge_energy
13015: co2_emission_reduction
13018: total_use_energy
13020: battery_voltage
13022: battery_power
13023: battery_level
13024: battery_health
13025: battery_temp
13027: total_discharge_energy
13029: use_power
13034: pv_power
```

Holding registers:
```
5000: Year
5001: Month
5002: Day
5003: Hour (24hr)
5004: Minute
5005: Second
```

