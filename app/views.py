import flask
import flask_login
from flask import render_template

from GetTemperature import read_temp
from app import app
from app.models import User, users, login_manager
from app.thermostat_controls import air_conditioning, heater, fan, system_off
from run import TARGET_TEMP, TARGET_MODE


@app.route('/login', methods=['GET', 'POST'])
def login():
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
    return 'Logged in as: ' + flask_login.current_user.id


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Index')


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('index'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


@app.route('/Thermostat')
@flask_login.login_required
def thermostat():
    return render_template('Thermostat.html',
                           title='Thermostat')


@app.route('/ac/<state>', methods=['POST'])
@flask_login.login_required
def toggle_ac(state):
    return air_conditioning(state)


@app.route('/fan/<state>', methods=['POST'])
@flask_login.login_required
def toggle_fan(state):
    return fan(state)


@app.route('/heater/<state>', methods=['POST'])
@flask_login.login_required
def toggle_heater(state):
    return heater(state)


@app.route('/system/off', methods=['POST'])
@flask_login.login_required
def turn_system_off():
    return system_off()


@app.route('/temp/target')
def target_temp_view():
    if flask.request.method == 'GET':
        return TARGET_TEMP
    elif flask.request.method == 'POST':
        # TODO: add this logic
        return


@app.route('/mode')
def target_temp_mode():
    if flask.request.method == 'GET':
        return TARGET_MODE
    elif flask.request.method == 'POST':
        # TODO: set the mode based on the post request
        return


@app.route('/temp/current')
def get_temp():
    return read_temp()
