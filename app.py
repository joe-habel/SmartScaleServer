import os

from flask import Flask, render_template, copy_current_request_context, redirect, url_for
from flask_socketio import SocketIO, emit
from wiiboard import ServerInterface, WiiBoardThread
 
import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
board = ServerInterface()

class WiiBoardBluetoothSync:
    def __init__(self):
        self.connection = None
        self.callback = None

    def setThread(self, board):
        self.connection = WiiBoardThread(board)
        print "Thread set"
        if self.callback is not None:
            print "We already had our callback"
            self.connection.setCallback(self.callback)
            self.start()

    def setCallback(self, func):
        print "Setting Callback"
        if self.connection is None:
            print "No connection thread"
            self.callback = func
        else:
            print "Connection thread established"
            self.connection.setCallback(func)
            self.start()

    def start(self):
        print "Start receive thread"
        self.connection.start()
    
BluetoothConnection = WiiBoardBluetoothSync()    

@app.route('/')
def hello_world():
    return "Smart Scale Landing"

@app.route('/connect-board')
def show_input():
    board.discoverBoard()
    
    print "Init Thread"
    BluetoothConnection.setThread(board)
        
    
    return redirect(url_for('displayWeight'))

@app.route('/weight')
def displayWeight():
    return render_template('weight.html')

@socketio.on('connect')
def initWeightUpdate():
    emit('sigWebSocketInit', {'connection' : 'True'})
    @copy_current_request_context
    def func(weight):
        emit('sigUpdateWeight', {'weight' : weight})
        socketio.sleep(0)
    BluetoothConnection.setCallback(func)
    print "Callback emit initialized"
    


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', debug=True)
