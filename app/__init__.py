from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'super secret string'


from app import views, models
from app.thermostat_controls import init_gpio

init_gpio()
