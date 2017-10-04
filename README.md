# Solariot

Leverage your IoT enabled Solar PV Inverter to stream your solar energy usage
data to a real time dashboard.

Solariot will connect directly to your Inverter using Modbus TCP. 

Currently, Solariot is able to talk to a Sungrow SH5K inverter. However,
the script is designed to allow any Modbus TCP enabled Inverter to be queried by
using your own Modbus register map file.

Once the Inverter has been queried, data is collected and stream to two optional
destinations: dweet.io and / or an InfluxDB. From there, you will need to create
your own dashboard, such as Freeboard and Grafana. 

Here's an example use case with [Freeboard](https://freeboard.io/) as a real 
time dashboard and data visualization tool for a Sungrow Inverter (and attached
battery) system:

![alt tag](docs/freeboard-dashboard-solar-example.png)

With Grafana:

![alt tag](docs/influxdb-grafana-example.png)

## Pre-requisites

The Inverter must be accessible on the network using TCP.

This script should work on most Inverters that talk Modbus TCP. You can 
customise your own modbus register file.

Install the required Python libraries for pymodbus, dweepy and influxdb:

```
pip install -r requirements.txt
```

## Installation

1. Download or clone this repository to your local workstation. Install the 
required libraries (see Pre-requisites section above).

2. Update the config.py with your values, such as the Inverter's IP address, 
port, inverter model (which corresponds to the modbus register file) and the
register addresses Solariot should scan from.

3. Run the solariot.py script.

## Integration with PVOutput.org and Grafana

If you are using Grafana as your dashboard, a neat little trick is to then
incorporate your Grafana panels with your PVOutput as system photos. From your
PV Ladder page, click on your photos to view the real time Grafana images: 

![alt tag](docs/animated-pvoutout-grafana-integration.gif)

1. Obtain your Grafana panel direct link, see their documentation: <http://docs.grafana.org/reference/sharing/#direct-link-rendered-image>.

2. In your PVOutput "Edit System" page, add your Grafana panel link in the 
"Image Link" field. Append "&png" to the link. Note, if the URL is longer than 
100 characters, use a URL shortener service instead (such as <https://goo.gl>).
Don't forget to append the "&png" string to your URL.

3. Now go to your system in the PV Ladder page and click on the photos.

:bulb: Tip: You can add any URL image, such as the latest weather radar image 
:wink:
