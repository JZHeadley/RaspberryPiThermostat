import flask
import flask_login
from flask import render_template

from GetTemperature import read_temp
from app import app
from app.models import User, users, login_manager
from app.thermostat_controls import system_off


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
    return render_template('Thermostat.html',
                           title='Thermostat')


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
    # TODO: return current target temp here.  read from json file
    return


@app.route('/temp/target/<target_temp>', methods=['POST'])
def target_temp_set(target_temp):
    """

    Args:
        target_temp: the target temp you want to reach

    Returns: a message confirming temp has been set

    """
    # else:
    #     return "that was an invalid operation.  Stop trying to hack my thermometer!"
    # TODO: set the target temp in a json file here
    return "new temp, " + target_temp + " has been set."


@app.route('/mode')
def target_temp_mode():
    """

    Returns: the current mode that should be used to reach the target

    """
    # TODO: get the current mode from the json file here
    return


@app.route('/mode/<mode>', methods=['POST'])
def target_temp_mode_set(mode):
    """

    Args:
        mode: the new mode for the system

    Returns: a message confirming mode has been set

    """
    print mode
    # TODO: set the target mode in the json file here

    if mode == 'cool':
        return
    elif mode == 'heat':
        return
    elif mode == 'off':
        return
    else:
        return "that was an invalid operation.  Stop trying to hack my thermometer!"

        # return "new mode, " + mode + " has been set."


@app.route('/temp/current')
def get_temp():
    """

    Returns: the current temperature of the house

    """
    return read_temp()
