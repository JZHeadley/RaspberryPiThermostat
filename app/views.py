import flask
import flask_login
from flask import json
from flask import render_template

from GetTemperature import read_temp
from app import app
from app.models import User, users, login_manager
from thermostat_controls import system_off, write_verbose


@app.route('/login', methods=['GET', 'POST'])
def login():
    """

    Returns: the login view if a get request and redirects to index if given a valid login

    """
    if flask.request.method == 'GET':
        return render_template('login.html',
                               title='Login')

    email = flask.request.form['email']
    if flask.request.form['pw'] == users[email]['pw']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('index'))

    return 'Incorrect login'


@app.route('/protected')
@flask_login.login_required
def protected():
    """

    Returns: just an example protected site

    """
    return 'Logged in as: ' + flask_login.current_user.id


@app.route('/')
@app.route('/index')
def index():
    """

    Returns: Homepage of the website

    """
    return render_template('index.html',
                           title='Index')


@app.route('/logout')
def logout():
    """

    Returns: a redirect to the homepage after logging the user out

    """
    flask_login.logout_user()
    return flask.redirect(flask.url_for('index'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    """

    Returns: the view given to users that are not authenticated trying to access a restricted page

    """
    return 'Unauthorized'


@app.route('/Thermostat')
@flask_login.login_required
def thermostat():
    """

    Returns: the thermostat view

    """
    with open('settings.json', 'r') as f:
        data = json.load(f)
    return render_template('Thermostat.html',
                           title='Thermostat',
                           current_target=data['TARGET_TEMP'])


@app.route('/system/off', methods=['POST'])
@flask_login.login_required
def turn_system_off():
    """

    Returns: response from turning the thermostat system off

    """
    return system_off()


@app.route('/temp/target')
def target_temp_view():
    """

    Returns: current target temp

    """
    with open('settings.json', 'r') as f:
        data = json.load(f)
    return data['TARGET_TEMP']


@app.route('/temp/target', methods=['POST'])
def target_temp_set():
    """

    Returns: a message confirming temp has been set

    """
    target_temp = int(flask.request.form['target_temp'])

    with open('settings.json', 'r') as f:
        data = json.load(f)
    if int(60) > target_temp:
        return "That is way too cold."
    elif 85 < target_temp:
        return "That is way too hot!"
    elif (target_temp <= int(85)) and (target_temp >= int(60)):  # valid range of temps is between 60 and 85.
        data['TARGET_TEMP'] = target_temp
    else:
        return "That was an invalid operation.  Stop trying to hack my thermometer!"

    with open('settings.json', 'w') as f:
        json.dump(data, f)
    return "new temp, " + str(target_temp) + " has been set."


@app.route('/mode')
def target_temp_mode():
    """

    Returns: the current mode that should be used to reach the target

    """
    with open('settings.json', 'r') as f:
        data = json.load(f)
    return data['TARGET_MODE']


@app.route('/mode/<mode>', methods=['POST'])
def target_temp_mode_set(mode):
    """

    Args:
        mode: the new mode for the system

    Returns: a message confirming mode has been set

    """
    write_verbose("Mode has been changed to " + mode)
    with open('settings.json', 'r') as f:
        data = json.load(f)
    write_verbose(data)
    if mode == 'cool':
        data['TARGET_MODE'] = 'cool'
    elif mode == 'heat':
        data['TARGET_MODE'] = 'heat'
    elif mode == 'off':
        data['TARGET_MODE'] = 'off'
    else:
        return "that was an invalid operation.  Stop trying to hack my thermometer!"
    with open('settings.json', 'w') as f:
        json.dump(data, f)
    return "new mode, " + mode + " has been set."


@app.route('/temp/current')
def get_temp():
    """

    Returns: the current temperature of the house

    """
    return read_temp()
