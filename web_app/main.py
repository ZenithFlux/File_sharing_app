from flask import Flask, render_template, request, session, send_from_directory, url_for, redirect
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
import config
import os
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
        
save_users({})

#------------------App----------------------

app = Flask(__name__)
app.config.from_object(config.Config)
socketio = SocketIO(app)

@app.route('/', methods = ['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        user = request.form['name']
        return redirect(url_for('senderpage', user = user))

    else: return render_template('index.html')
    
@app.route('/sender', methods = ['GET', 'POST'])
def senderpage():
    if request.method == 'POST':
        receiver_id = request.form['receiver']
        f = request.files['file']
        #path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
        #f.save(path)
        users = load_users()
        emit('sending_file', (secure_filename(f.filename), f.read()), to = users[receiver_id], namespace='/')
        return render_template('sender.html', user = request.form['id'])
        
    else:
        return render_template('sender.html', user = request.args.get('user'))

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
    
@socketio.on('print')
def print_data(text):
    print(f'\n[{session["id"]}]: {text}\n')
    #send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    #os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
if __name__ == '__main__':
    socketio.run(app)