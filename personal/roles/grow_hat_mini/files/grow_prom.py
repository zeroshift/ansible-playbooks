#!/usr/bin/python3

import argparse
import logging
import time
import yaml
from grow.moisture import Moisture
from ltr559 import LTR559
from prometheus_client import start_http_server, Gauge, Counter


def _get_args():
    """Get arguments and options."""
    parser = argparse.ArgumentParser(description="grow_prom", prog="grow_prom.py")

    parser.add_argument(
        "-c",
        "--config",
        dest="config_path",
        action="store",
        default="/etc/default/grow",
        type=str,
        metavar="CONFIG PATH",
        help="Set path to the config file (Default: %(default)s",
    )
    parser.add_argument(
        "-i",
        "--interval",
        dest="interval",
        action="store",
        default=15,
        type=int,
        metavar="NUM_SECONDS",
        help="Interval to sleep between collections (Default: %(default)s",
    )
    parser.add_argument(
        "-p",
        "--port",
        dest="bind_port",
        action="store",
        default=8000,
        type=int,
        metavar="PORT",
        help="Port to bind to (Default: %(default)s",
    )
    parser.add_argument(
        "-l",
        "--log-level",
        dest="log",
        action="store",
        default="info",
        type=str,
        metavar="LOG LEVEL",
        help="Set the log level. (Default: %(default)s)",
    )
    parser.add_argument(
        "--log-file",
        dest="log_file",
        action="store",
        default=None,
        type=str,
        metavar="LOG_FILE",
        help="Set the log file.",
    )

    args = parser.parse_args()
    return args


def main():
    args = _get_args()
    # Setup Logging
    numeric_log_level = getattr(logging, args.log.upper(), None)
    if not isinstance(numeric_log_level, int):
        raise ValueError("Invalid log level: %s" % args.log)
    logging.basicConfig(
        level=numeric_log_level,
        format="[%(levelname)s] %(message)s",
        filename=args.log_file,
    )

    # Start
    logging.info("Starting up...")

    # Import settings
    config = yaml.safe_load(open(args.config_path))

    # Setup moisture sensors for reading
    sensors = []
    for sensor_num in [1, 2, 3]:
        sensor = Moisture(sensor_num)
        if ("channel{0}".format(sensor_num)) in config.keys():
            sensors.append(sensor)

    # Setup light sensor for reading
    light = LTR559()

    soil_moisture = Gauge("grow_soil_moisture", "Soil Moisture", ["channel", "plant"])
    soil_saturation = Gauge(
        "grow_soil_saturation", "Soil Saturation", ["channel", "plant"]
    )
    soil_dry_point = Gauge("grow_soil_dry_point", "Dry Point", ["channel", "plant"])
    soil_wet_point = Gauge("grow_soil_wet_point", "Dry Point", ["channel", "plant"])
    lux = Gauge("grow_light_lux", "Lux")

    # Start prometheus server
    start_http_server(args.bind_port)

    # Gather/export data
    while True:
        # Re-read settings if changed by monitor app
        config = yaml.safe_load(open(args.config_path))

        for i in range(0, 3):
            channel_num = i + 1
            channel_name = "channel{}".format(channel_num)
            if channel_name in config.keys():
                plant_name = config[channel_name]["name"]

                # Set wet/dry points
                logging.debug("Setting wet/dry points.")
                sensors[i].set_dry_point(config[channel_name]["dry_point"])
                sensors[i].set_wet_point(config[channel_name]["wet_point"])

                # Track soil moisture/saturation
                logging.debug("Tracking soil moisture/saturation.")
                soil_moisture.labels(channel_name, plant_name).set(sensors[i].moisture)
                soil_saturation.labels(channel_name, plant_name).set(sensors[i].saturation)

                # Track wet/dry points
                logging.debug("Tracking wet/dry points.")
                soil_dry_point.labels(channel_name, plant_name).set(
                    config[channel_name]["dry_point"]
                )
                soil_wet_point.labels(channel_name, plant_name).set(
                    config[channel_name]["wet_point"]
                )

        # Update/track light sensor lux
        logging.debug("Updating light sensor.")
        light.update_sensor()

        logging.debug("Tracking light lux.")
        lux.set(light.get_lux())

        logging.debug("Sleeping for {}".format(args.interval))
        time.sleep(args.interval)

    # End
    logging.info("Shutting down ...")


if __name__ == "__main__":
    main()
