import subprocess

import RPi.GPIO as gpio

from app import app

FAN_PIN = app.config['FAN_PIN']
HEATER_PIN = app.config['HEATER_PIN']
AC_PIN = app.config['AC_PIN']
RELAY_ON = False
RELAY_OFF = (not RELAY_ON)

BOARD_MODE = gpio.BCM
VERBOSE = app.config['DEBUG']


def fan(state):
    if state == "on":
        write_verbose("fan turned on")
        gpio.output(FAN_PIN, gpio.LOW)
        gpio.output(HEATER_PIN, gpio.HIGH)
        gpio.output(AC_PIN, gpio.HIGH)
        return "fan turned on"
    else:
        return "invalid command"


def heater(state):
    if state == "on":
        write_verbose("heater turned on")
        gpio.output(FAN_PIN, gpio.LOW)
        gpio.output(HEATER_PIN, gpio.LOW)
        gpio.output(AC_PIN, gpio.HIGH)
        return "heater turned on"
    else:
        return "invalid command"


def air_conditioning(state):
    if state == "on":
        write_verbose("ac turned on")
        gpio.output(FAN_PIN, gpio.LOW)
        gpio.output(HEATER_PIN, gpio.LOW)
        gpio.output(AC_PIN, gpio.LOW)
        return "ac turned on"
    else:
        return "invalid command"


def system_off():
    write_verbose("System has been turned off")
    turn_off_system()
    return "System has been turned off"


def init_gpio():
    write_verbose('Setting up GPIO...')
    gpio.setwarnings(False)
    gpio.setmode(BOARD_MODE)

    gpio.setup(FAN_PIN, gpio.OUT)
    gpio.setup(HEATER_PIN, gpio.OUT)
    gpio.setup(AC_PIN, gpio.OUT)

    write_verbose('GPIO setup completed.')


def turn_off_system():
    gpio.output(FAN_PIN, gpio.HIGH)
    gpio.output(HEATER_PIN, gpio.HIGH)
    gpio.output(AC_PIN, gpio.HIGH)


def get_heater_status():
    return int(subprocess.Popen("cat /sys/class/gpio/gpio" + str(HEATER_PIN) + "/value", shell=True,
                                stdout=subprocess.PIPE).stdout.read().strip())


def get_ac_status():
    return int(subprocess.Popen("cat /sys/class/gpio/gpio" + str(AC_PIN) + "/value", shell=True,
                                stdout=subprocess.PIPE).stdout.read().strip())


def get_fan_status():
    return int(subprocess.Popen("cat /sys/class/gpio/gpio" + str(FAN_PIN) + "/value", shell=True,
                                stdout=subprocess.PIPE).stdout.read().strip())


def write_verbose(s, new_line=False):
    if VERBOSE:
        print(s)
        if new_line is True:
            print('')
