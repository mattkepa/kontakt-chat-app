from flask import Flask, render_template
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
    return render_template('index.html')



if __name__ == '__main__':
    socketio.run(app, debug=True, host=config.Config.SERVER)