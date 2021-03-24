from flask import Flask
app = Flask(__name__)

@app.route('/')
def root():
    return app.send_static_file('map.html')


@app.route('/parking')
def hello_park():
    return 'Find a garage!'
