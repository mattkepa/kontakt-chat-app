from flask import Flask
from flask_socketio import SocketIO
import config

# SETUP APP
# Initialize Flask core and SocketIO application
app = Flask(__name__)
app.config.from_object('config.Config')

socketio = SocketIO(app)


# ----------------------
# VIEWS

@app.route('/')
@app.route('/home')
def home():
    """
    Displays home page of chat app
    """
    return '<h1>Home Page</h1>'



if __name__ == '__main__':
    socketio.run(app, debug=True, host=config.Config.SERVER)