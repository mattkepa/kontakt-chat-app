from flask import Flask, render_template, url_for, redirect, request, session, jsonify
from flask_cors import CORS
from flask_session import Session
from flask_socketio import SocketIO, emit
import config
from uuid import uuid4
from utils import convert_timestamp_to_timestr


# SETUP APP
# Initialize Flask core application
app = Flask(__name__)
app.config.from_object('config.Config')
# Congifure CORS and server side sessions
Session(app)
CORS(app)
# Initialize Flask SocketIO application
socketio = SocketIO(app)


# ----------------------
# APP CONSTANTS
NAME_KEY = 'user'

# APP VARIABLES
users = {}


# ----------------------
# SOCKET COMMUNICATION FUNCTIONS

@socketio.on('ehlo')
def handle_connect(user):
    users[request.sid] = user
    message = { 'content': f'{user["username"]} joined the chat' }
    emit('broadcast', message, broadcast=True)
    emit('user-connected', users, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    user = users.pop(request.sid)
    message = { 'content': f'{user["username"]} left the chat' }
    emit('broadcast', message, broadcast=True)
    emit('user-disconnected', users, broadcast=True)
    session.pop(NAME_KEY, None)

@socketio.on('message-sent')
def handle_message(message):
    message['time'] = convert_timestamp_to_timestr(message['time'])
    emit('broadcast', message, broadcast=True)


# ----------------------
# VIEWS

@app.route('/')
@app.route('/home')
def home():
    """
    Displays home page of chat app if user is logged in (session is created),
    otherwise redirect to login page
    """
    if NAME_KEY not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Displays login page and saves session
    """
    if request.method == 'POST':
        # create and save new active user
        user = { 'id': str(uuid4()), 'username': request.form['username'] }
        session[NAME_KEY] = user
        return redirect(url_for('home'))
    return render_template('LoginPage.html')


# ----------------------
# API FUNCTIONS

@app.route('/api/user')
def get_user():
    """
    Returns current logged in user from session. Called only from frontend
    """
    if NAME_KEY in session:
        return jsonify(session[NAME_KEY])
    return {}


@app.route('/api/users')
def get_users():
    """
    Returns active users list. Called only from frontend
    """
    return users



if __name__ == '__main__':
    socketio.run(app, debug=True, host=config.Config.SERVER)