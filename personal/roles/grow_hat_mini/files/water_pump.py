#!/usr/bin/python3
import yaml

from grow.pump import Pump


# Import settings
config = yaml.safe_load(open('/etc/default/grow'))

pump = Pump(1)
pump.dose(config['channel1']['pump_speed'], config['channel1']['pump_time'], blocking=False)