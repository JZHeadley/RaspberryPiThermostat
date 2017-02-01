from app import app

PORT = app.config['PORT']
IP = app.config['IP']
DEBUG = app.config['DEBUG']
app.run(port=PORT, host=IP, debug=DEBUG)
