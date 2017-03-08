import json
import sys
import time

from RPi import GPIO
from flask import Config

from GetTemperature import read_temp
from SimpleDaemon import Daemon
from thermostat_controls import air_conditioning, system_off

config = Config('config')

FAN_PIN = config.get('FAN_PIN')
HEATER_PIN = config.get('HEATER_PIN')
AC_PIN = config.get('AC_PIN')
check_time = 15


def get_target_temp():
    with open('settings.json', 'r') as f:
        data = json.load(f)
    return data['TARGET_TEMP']


def get_current_mode():
    with open('settings.json', 'r') as f:
        data = json.load(f)
    return data['TARGET_MODE']


def get_current_temp():
    return read_temp()


class ThermostatDaemon(Daemon):
    # TODO: need to account for a margin of error somewhere in here.
    def run(self):
        while True:
            current_mode = get_current_mode()
            if current_mode == 'cool':
                if get_current_temp() > get_target_temp():
                    # yet to reach target
                    air_conditioning("on")
                    pass
                elif get_current_temp() <= get_target_temp():
                    # we've at least achieved our target so we stop cooling here
                    system_off()
                    pass


            elif current_mode == 'heat':
                pass

            elif current_mode == 'off':
                # We don't care what temp it is, just turn the system off.
                system_off()
                pass
            else:
                return "I'm tired of you breaking things..."
            print get_target_temp()
            print get_current_temp()
            time.sleep(check_time)


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
        elif 'run' == sys.argv[1]:
            daemon.run()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start | stop | restart | run" % sys.argv[0]
        sys.exit(2)
