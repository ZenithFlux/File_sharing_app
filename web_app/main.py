from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
import config
import json
import threading

sem = threading.Semaphore()
# This is to prevent multiple sessions from modifying users.json at the same time

def save_users(dict):
    with open('users.json', 'w') as f:
        json.dump(dict, f)
        
def load_users():
    with open('users.json', 'r') as f:
        return json.load(f)
        

#------------------App----------------------

app = Flask(__name__)
app.config.from_object(config.Config)
socketio = SocketIO(app)

@app.route('/', methods = ['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        user = request.form['name'].strip()
        session['logged'] = 1
        sem.acquire()
        users = load_users()
        sem.release()
        
        if user in users:
            flash("Another user with same ID is currently active")
            return render_template('index.html')
        
        else: return redirect(url_for('senderpage', user = user))

    else: return render_template('index.html')
    
@app.route('/sender', methods = ['GET', 'POST'])
def senderpage():
    if request.method == 'POST':
        receiver_id = request.form['receiver'].strip()
        f = request.files['file']
        sem.acquire()
        users = load_users()
        sem.release()
        emit('sending_file', (secure_filename(f.filename), f.read(), request.form['id']), to = users[receiver_id], namespace='/')
        return render_template('sender.html', user = request.form['id'])
        
    else:
        if 'logged' in session:
            del session['logged']
            return render_template('sender.html', user = request.args.get('user'))
        else:
            return redirect(url_for("homepage"))

@socketio.on('connected')
def connected(user):
    session['id'] = user
    sem.acquire()
    users = load_users()
    users[session['id']] = request.sid
    save_users(users)
    sem.release()
    print(f'\n{session["id"]} connected!\n')
    
@socketio.on('disconnect')
def disconnection():
    sem.acquire()
    users = load_users()
    del users[session['id']]
    save_users(users)
    sem.release()
    print(f'\n{session["id"]} disconnected!\n')
    
@socketio.on('confirmation')
def confirmation(filename, sender):
    sem.acquire()
    users = load_users()
    sem.release()
    emit('alert', "'"+filename+"' is sucessfully downloaded by '"+session['id']+"'.", to = users[sender])

# To print js output in python console    
@socketio.on('print')
def print_data(text):
    print(f'\n[{session["id"]}]: {text}\n')
    
if __name__ == '__main__':
    save_users({})
    socketio.run(app, port=80)