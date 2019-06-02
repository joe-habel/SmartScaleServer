import os

from flask import Flask
from wiiboard import ServerInterface
 

app = Flask(__name__)
board = ServerInterface()

@app.route('/')
def hello_world():
    return "Smart Scale Landing"

@app.route('/connect-board')
def show_input():
    if not os.path.exists('.wii-board-addr'):
        return "No preconfigured board here"
    
    with open('.wii-board-addr', 'r') as f:
        address = f.read()
    
    board.connectToKnownAddress(address)
    print "what happen here????"
    
    return "We're going to try to connect to the board. Make sure you click the red button on the back. If it connects, move to /weight route"

@app.route('/weight')
def displayWeight():
    return "Last Weight: %s"%board.getWeight()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
