from app import app

PORT = app.config['PORT']
IP = app.config['IP']
DEBUG = app.config['DEBUG']
TARGET_TEMP = app.config['TARGET_TEMP']
TARGET_MODE = app.config['TARGET_MODE']

app.run(port=PORT, host=IP, debug=DEBUG)

# TODO: instead of using at exit just write to config whenever these values are modified weird things happening with
#  atexit

# def on_exit(): app.config['TARGET_TEMP'] = TARGET_TEMP app.config['TARGET_MODE'] = TARGET_MODE print
# "exiting"
#
#
# atexit.register(on_exit)
