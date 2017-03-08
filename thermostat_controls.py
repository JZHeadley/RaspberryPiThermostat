import RPi.GPIO as gpio

from app import app

FAN_PIN = app.config['FAN_PIN']
HEATER_PIN = app.config['HEATER_PIN']
AC_PIN = app.config['AC_PIN']
RELAY_ON = False
RELAY_OFF = (not RELAY_ON)

BOARD_MODE = gpio.BCM


def fan(state):
    """

    Args:
        state: state for the fan pin to be set to.

    Returns: a confirmation that the fan has changed

    """
    if state == "on":
        write_verbose("fan turned on")
        gpio.output(FAN_PIN, gpio.LOW)
        gpio.output(HEATER_PIN, gpio.HIGH)
        gpio.output(AC_PIN, gpio.HIGH)
        return "fan turned on"
    else:
        return "invalid command"


def heater(state):
    """

    Args:
        state: state for the heater pin to be set to.

    Returns: a confirmation that the heater has changed

    """
    if state == "on":
        write_verbose("heater turned on")
        gpio.output(FAN_PIN, gpio.LOW)
        gpio.output(HEATER_PIN, gpio.LOW)
        gpio.output(AC_PIN, gpio.HIGH)
        return "heater turned on"
    else:
        return "invalid command"


def air_conditioning(state):
    """

    Args:
        state: state for the a/c pin to be set to.

    Returns: a confirmation that the a/c has changed

    """
    if state == "on":
        write_verbose("ac turned on")
        gpio.output(FAN_PIN, gpio.LOW)
        gpio.output(HEATER_PIN, gpio.LOW)
        gpio.output(AC_PIN, gpio.LOW)
        return "ac turned on"
    else:
        return "invalid command"


def system_off():
    """

    Returns: a confirmation that the system has been turned off

    """
    write_verbose("System has been turned off")
    turn_off_system()
    return "System has been turned off"


def init_gpio():
    """
        Initializes the gpio pins for the RaspberryPi
    """
    write_verbose('Setting up GPIO...')
    gpio.setwarnings(True)
    gpio.setmode(BOARD_MODE)

    gpio.setup(FAN_PIN, gpio.OUT)
    gpio.setup(HEATER_PIN, gpio.OUT)
    gpio.setup(AC_PIN, gpio.OUT)

    write_verbose('GPIO setup completed.')


def turn_off_system():
    """
        Turns off all of the pins so the system will stop
    """
    gpio.output(FAN_PIN, gpio.HIGH)
    gpio.output(HEATER_PIN, gpio.HIGH)
    gpio.output(AC_PIN, gpio.HIGH)


def write_verbose(s, new_line=False):
    """
        helper method to only write certain things while in debug mode
    Args:
        s: a string to write
        new_line: whether or not to print the string on a new line
    """
    if app.config['DEBUG']:
        print(s)
        if new_line is True:
            print('')
