import os

from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from wiiboard import ServerInterface, WiiBoardThread
 

app = Flask(__name__)
socketio = SocketIO(app)
board = ServerInterface()

class WiiBoardBluetoothSync:
    def __init__(self):
        self.connection = None
    
    def setThread(self, board):
        self.connection = WiiBoardThread()
    
    def setCallback(self, func):
        self.connection.setCallback(func)
        
    def run(self):
        self.connection.run()
    
BluetoothConnection = WiiBoardBluetoothSync()    

@app.route('/')
def hello_world():
    return "Smart Scale Landing"

@app.route('/connect-board')
def show_input():
    if not os.path.exists('.wii-board-addr'):
        return "No preconfigured board here"
    
    with open('.wii-board-addr', 'r') as f:
        address = f.read()
    
    connection = board.connectToKnownAddress(address)
    
    if not connection:
        return "Board didn't connect"
    
    BluetoothConnection.setThread(board)
    BluetoothConnection.run()
        
    
    return "We're going to try to connect to the board. Make sure you click the red button on the back."

@app.route('/weight')
def displayWeight():
    render_template('weight.html')

@socketio.on('connect')
def initWeightUpdate():
    emit('sigWebSocketInit', {'connection' : 'True'})
    func = lambda weight: emit('sigUpdateWeight', {'weight' : weight})
    BluetoothConnection.setCallback(func)
    print "Callback emit initialized"
    


if __name__ == "__main__":
    app.run(host='0.0.0.0')
