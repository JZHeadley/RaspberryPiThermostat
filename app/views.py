import flask
import flask_login
from flask import render_template

from app import app
from app.models import User, users, login_manager
from app.thermostat_controls import air_conditioning, heater, fan


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
    return 'Logged out'


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


@app.route('/Thermostat')
@flask_login.login_required
def thermostat():
    return render_template('Thermostat.html',
                           title='Thermostat')


@app.route('/ac/<state>')
@flask_login.login_required
def toggle_ac(state):
    return air_conditioning(state)


@app.route('/fan/<state>')
@flask_login.login_required
def toggle_fan(state):
    return fan(state)


@app.route('/heater/<state>')
@flask_login.login_required
def toggle_heater(state):
    return heater(state)
