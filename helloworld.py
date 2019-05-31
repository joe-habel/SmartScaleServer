from flask import Flask
app = Flask(__name__)

@app.route('/hi')
def hello_world():
    return "Hi From the Pi!"

@app.route('/input/<val>')
def show_input(val):
    return "The route was input/%s"%val


if __name__ == "__main__":
    app.run(host='0.0.0.0')
