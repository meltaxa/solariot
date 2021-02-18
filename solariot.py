#!/usr/bin/env python

# Copyright (c) 2017 Dennis Mellican
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from SungrowModbusTcpClient import SungrowModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from influxdb import InfluxDBClient
from importlib import import_module
from threading import Thread

import paho.mqtt.client as mqtt
import datetime
import requests
import argparse
import logging
import dweepy
import json
import time
import sys


MIN_SIGNED   = -2147483648
MAX_UNSIGNED =  4294967295

requests.packages.urllib3.disable_warnings() 

# Load in the config module
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", default="config", help="Python module to load as our config")
parser.add_argument("-v", "--verbose", action="count", default=0, help="Level of verbosity 0=ERROR 1=INFO 2=DEBUG")
args = parser.parse_args()

if args.verbose == 0:
    log_level = logging.WARNING
elif args.verbose == 1:
    log_level = logging.INFO
else:
    log_level = logging.DEBUG

logging.basicConfig(level=log_level)

config = import_module(args.config)
logging.info(f"Loaded config {config.model}")

# SMA datatypes and their register lengths
# S = Signed Number, U = Unsigned Number, STR = String
sma_moddatatype = {
  "S16": 1,
  "U16": 1,
  "S32": 2,
  "U32": 2,
  "U64": 4,
  "STR16": 8,
  "STR32": 16,
}

# Load the modbus register map for the inverter
modmap_file = f"modbus-{config.model}"

try:
    modmap = import_module(modmap_file)
except ModuleNotFoundError:
    logging.error(f"Unable to locate {modmap_file}.py")
    sys.exit(1)

# This will try the Sungrow client otherwise will default to the standard library.
client_payload = {
    "host": config.inverter_ip,
    "timeout": config.timeout,
    "RetryOnEmpty": True,
    "retries": 3,
    "port": config.inverter_port,
}

if "sungrow-" in config.model:
    logging.info("Creating SungrowModbusTcpClient")
    client = SungrowModbusTcpClient.SungrowModbusTcpClient(**client_payload)
else:
    logging.info("Creating ModbusTcpClient")
    client = ModbusTcpClient(**client_payload)

logging.info("Connecting")
client.connect()
client.close()
logging.info("Connected")

# Configure MQTT
if hasattr(config, "mqtt_server"):
    mqtt_client = mqtt.Client(getattr(config, "mqtt_client_name", "pv_data"))

    if hasattr(config, "mqtt_username") and hasattr(config, "mqtt_password"):
        mqtt_client.username_pw_set(config.mqtt_username, config.mqtt_password)

    if config.mqtt_port == 8883:
        mqtt_client.tls_set()

    mqtt_client.connect(config.mqtt_server, port=config.mqtt_port)
    logging.info("Configured MQTT Client")
else:
    mqtt_client = None
    logging.info("No MQTT configuration detected")

# Configure InfluxDB
if hasattr(config, "influxdb_ip"):
    flux_client = InfluxDBClient(
        config.influxdb_ip,
        config.influxdb_port,
        config.influxdb_user,
        config.influxdb_password,
        config.influxdb_database,
        ssl=config.influxdb_ssl,
        verify_ssl=config.influxdb_verify_ssl,
    )

    logging.info("Configured InfluxDB Client")
else:
    flux_client = None
    logging.info("No InfluxDB configuration detected")

# Inverter Scanning
inverter = {}
bus = json.loads(modmap.scan)

def load_registers(register_type, start, count=100):
    try:
        if register_type == "read":
            rr = client.read_input_registers(
                int(start),
                count=count,
                unit=config.slave,
            )
        elif register_type == "holding":
            rr = client.read_holding_registers(
                int(start),
                count=count,
                unit=config.slave,
            )
        else:
            raise RuntimeError(f"Unsupported register type: {type}")
    except Exception as err:
        logging.warning("No data. Try increasing the timeout or scan interval.")

    if len(rr.registers) != count:
        logging.warning(f"Mismatched number of registers read {len(rr.registers)} != {count}")
        return

    for num in range(0, count):
        run = int(start) + num + 1

        if type == "read" and modmap.read_register.get(str(run)):
            if "_10" in modmap.read_register.get(str(run)):
                inverter[modmap.read_register.get(str(run))[:-3]] = float(rr.registers[num]) / 10
            else:
                inverter[modmap.read_register.get(str(run))] = rr.registers[num]
        elif type == "holding" and modmap.holding_register.get(str(run)):
            inverter[modmap.holding_register.get(str(run))] = rr.registers[num]

# Function for polling data from the target and triggering writing to log file if set
def load_sma_register(registers):
    # Request each register from datasets, omit first row which contains only column headers
    for thisrow in registers:
        name = thisrow[0]
        startPos = thisrow[1]
        type = thisrow[2]
        format = thisrow[3]
    
        # If the connection is somehow not possible (e.g. target not responding)
        # show a error message instead of excepting and stopping
        try:
            received = client.read_input_registers(
                address=startPos,
                count=sma_moddatatype[type],
                unit=config.slave
            )
        except Exception:
            thisdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.error(f"{thisdate}: Connection not possible, check settings or connection")
            return
    
        message = BinaryPayloadDecoder.fromRegisters(received.registers, endian=Endian.Big)

        # Provide the correct result depending on the defined datatype
        if type == "S32":
            interpreted = message.decode_32bit_int()
        elif type == "U32":
            interpreted = message.decode_32bit_uint()
        elif type == "U64":
            interpreted = message.decode_64bit_uint()
        elif type == "STR16":
            interpreted = message.decode_string(16)
        elif type == "STR32":
            interpreted = message.decode_string(32)
        elif type == "S16":
            interpreted = message.decode_16bit_int()
        elif type == "U16":
            interpreted = message.decode_16bit_uint()
        else:
            # If no data type is defined do raw interpretation of the delivered data
            interpreted = message.decode_16bit_uint()
    
        # Check for "None" data before doing anything else
        if ((interpreted == MIN_SIGNED) or (interpreted == MAX_UNSIGNED)):
            displaydata = None
        else:
            # Put the data with correct formatting into the data table
            if format == "FIX3":
                displaydata = float(interpreted) / 1000
            elif format == "FIX2":
                displaydata = float(interpreted) / 100
            elif format == "FIX1":
                displaydata = float(interpreted) / 10
            else:
                displaydata = interpreted
    
        logging.debug(f"************** {name} = {displaydata}")
        inverter[name] = displaydata
  
    # Add timestamp
    inverter["00000 - Timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def publish_influx(metrics):
    target = flux_client.write_points([metrics])
    logging.info("Published to InfluxDB")
    return target

def publish_dweepy(inverter):
    result = dweepy.dweet_for(config.dweepy_uuid, inverter)
    logging.info("Published to dweet.io")
    return result

def publish_mqtt(inverter):
    result = mqtt_client.publish(config.mqtt_topic, json.dumps(inverter).replace('"', '\"'))
    logging.info("Published to MQTT")
    return result

# Core monitoring loop
def scrape_inverter():
    """ Connect to the inverter and scrape the metrics """
    client.connect()

    inverter = {}

    if "sungrow-" in config.model:
        for i in bus["read"]:
            load_registers("read", i["start"], int(i["range"]))
        for i in bus["holding"]:
            load_registers("holding", i["start"], int(i["range"]))
  
        # Sungrow inverter specifics:
        # Work out if the grid power is being imported or exported
        if config.model == "sungrow-sh5k" and inverter["grid_import_or_export"] == 65535:
            export_power = (65535 - inverter["export_power"]) * -1
            inverter["export_power"] = export_power

            inverter["timestamp"] = "%s/%s/%s %s:%02d:%02d" % (
                inverter["day"],
                inverter["month"],
                inverter["year"],
                inverter["hour"],
                inverter["minute"],
                inverter["second"],
            )
    elif "sma-" in config.model:
        load_sma_register(modmap.sma_registers)
    else:
        raise RuntimeError(f"Unsupported inverter model detected: {config.model}")

    client.close()

    logging.info(inverter)
    return inverter


while True:
    try:
        # Scrape the inverter
        inverter = scrape_inverter()

        # Optionally publish the metrics if enabled
        if mqtt_client is not None:
            t = Thread(target=publish_mqtt, args=(inverter,))
            t.start()

        if hasattr(config, "dweepy_uuid"):
            t = Thread(target=publish_dweepy, args=(inverter,))
            t.start()

        if flux_client is not None:
            metrics = {
                "measurement": "Sungrow",
                "tags": {
                    "location": "Gabba",
                },
                "fields": inverter,
            }

            t = Thread(target=publish_influx, args=(metrics,))
            t.start()
    except Exception as err:
        # Enable for debugging, otherwise it can be noisy and display false positives
        logging.debug(str(err))
        client.close()

    # Sleep until the next scan
    time.sleep(config.scan_interval)
