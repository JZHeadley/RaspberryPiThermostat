from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'super secret string'

# # TODO: write logic to read these variables from file
#
# with open('targetValues.json', 'r') as f:
#     values = json.load(f)
#
# target_temp = values['temp']
# target_mode = values['mode']

from app import views, models
from app.thermostat_controls import init_gpio

init_gpio()
# print values
#
#
# def write_target_values():
#     with open('targetValues.json', 'w') as f:
#         json.dump(dict(target_temp, target_mode), f, ensure_ascii=False)
#         print("targetValues written to file")
#
#
# atexit.register(write_target_values)
