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
        return "fan turned on"
    elif state == "off":
        write_verbose("fan turned off")
        return "fan turned off"
    else:
        return "invalid command"


def heater(state):
    if state == "on":
        write_verbose("heater turned on")
        return "heater turned on"
    elif state == "off":
        write_verbose("heater turned off")
        return "heater turned off"
    else:
        return "invalid command"


def air_conditioning(state):
    if state == "on":
        write_verbose("ac turned on")
        return "ac turned on"
    elif state == "off":
        write_verbose("ac turned off")
        return "ac turned off"
    else:
        return "invalid command"


def init_gpio():
    write_verbose('Setting up GPIO...')
    gpio.setwarnings(False)
    gpio.setmode(BOARD_MODE)

    gpio.setup(FAN_PIN, gpio.OUT)
    gpio.setup(HEATER_PIN, gpio.OUT)
    gpio.setup(AC_PIN, gpio.OUT)

    subprocess.Popen("echo " + str(FAN_PIN) + " > /sys/class/gpio/export", shell=True)
    subprocess.Popen("echo " + str(HEATER_PIN) + " > /sys/class/gpio/export", shell=True)
    subprocess.Popen("echo " + str(AC_PIN) + " > /sys/class/gpio/export", shell=True)

    write_verbose('GPIO setup completed.')


def write_verbose(s, new_line=False):
    if VERBOSE:
        print(s)
        if new_line is True:
            print('')


def getHVACState():
    heatStatus = int(subprocess.Popen("cat /sys/class/gpio/gpio" + str(HEATER_PIN) + " /value", shell=True,
                                      stdout=subprocess.PIPE).stdout.read().strip())
    coolStatus = int(subprocess.Popen("cat /sys/class/gpio/gpio" + str(AC_PIN) + " /value", shell=True,
                                      stdout=subprocess.PIPE).stdout.read().strip())
    fanStatus = int(subprocess.Popen("cat /sys/class/gpio/gpio" + str(FAN_PIN) + " /value", shell=True,
                                     stdout=subprocess.PIPE).stdout.read().strip())

    if heatStatus == 1 and fanStatus == 1:
        # heating
        return 1

    elif coolStatus == 1 and fanStatus == 1:
        # cooling
        return -1

    elif heatStatus == 0 and coolStatus == 0 and fanStatus == 0:
        # idle
        return 0

    else:
        # broken
        return 2
