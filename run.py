from app import app

PORT = app.config['PORT']
IP = app.config['IP']
DEBUG = app.config['DEBUG']
# TARGET_TEMP = app.config['TARGET_TEMP']
# TARGET_MODE = app.config['TARGET_MODE']

app.run(port=PORT, host=IP, debug=DEBUG)
