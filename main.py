from flask import Flask, render_template, url_for, redirect, request, Response, make_response, session, jsonify
from flask_socketio import SocketIO
from flask_cors import cross_origin
import config
from uuid import uuid4


# SETUP APP
# Initialize Flask core and SocketIO application
app = Flask(__name__)
app.config.from_object('config.Config')

socketio = SocketIO(app)


# ----------------------
# APP CONSTANTS
NAME_KEY = 'user'

# APP VARIABLES
users = []


# ----------------------
# VIEWS

@app.route('/')
@app.route('/home')
def home():
    """
    Displays home page of chat app if user is logged in
    """
    if NAME_KEY not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Displays login page
    """
    if request.method == 'POST':
        # create and save new active user
        user = { 'id': str(uuid4()), 'username': request.form['username'] }
        users.append(user)
        session[NAME_KEY] = user
        return redirect(url_for('home'))
    return render_template('LoginPage.html')


# ----------------------
# API FUNCTIONS

@app.route('/api/logout', methods=['POST'])
def logout():
    """
    Handles logging the current user out by popping user from session
    and removing from active users list
    """
    if request.method == 'POST':
        usr = request.get_json()
        usr_id = usr['uid']
        for i, usr in enumerate(users):
            if users[i]['id'] == usr_id:
                del users[i]

        session.pop(NAME_KEY, None)
        return usr


@app.route('/api/user')
def get_user():
    """
    Called only from frontend axios to get current logged in user
    """
    if NAME_KEY in session:
        return jsonify(session[NAME_KEY])
    return {}



if __name__ == '__main__':
    socketio.run(app, debug=True, host=config.Config.SERVER)