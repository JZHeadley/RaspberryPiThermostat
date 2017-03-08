from app import app

PORT = app.config['PORT']
IP = app.config['IP']
DEBUG = app.config['DEBUG']

# daemon = ThermostatDaemon('ThermostatDaemon.pid')
# daemon.start()
# daemon.run()


app.run(port=PORT, host=IP, debug=DEBUG)
