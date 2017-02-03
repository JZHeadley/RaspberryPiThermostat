import sys

from RPi import GPIO
from flask import Config

from SimpleDaemon import Daemon

# config = ConfigParser.ConfigParser()
# config.read('config.py')

# FAN_PIN = config.get('Config', 'FAN_PIN')
# HEATER_PIN = config.get('Config', 'HEATER_PIN')
# AC_PIN = config.get('Config', 'AC_PIN')

config = Config('config')

FAN_PIN = config.get('FAN_PIN')
HEATER_PIN = config.get('HEATER_PIN')
AC_PIN = config.get('AC_PIN')


class ThermostatDaemon(Daemon):
    def run(self):
        return


if __name__ == "__main__":
    daemon = ThermostatDaemon('ThermostatDaemon.pid')

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(HEATER_PIN, GPIO.OUT)
            GPIO.setup(AC_PIN, GPIO.OUT)
            GPIO.setup(FAN_PIN, GPIO.OUT)
            GPIO.output(HEATER_PIN, False)
            GPIO.output(AC_PIN, False)
            GPIO.output(FAN_PIN, False)
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start | stop | restart" % sys.argv[0]
        sys.exit(2)
