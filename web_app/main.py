from flask import Flask, render_template, request, url_for, redirect
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename
import config
import os

app = Flask(__name__)
app.config.from_object(config.Config)
socketio = SocketIO(app)

@app.route('/', methods = ['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        user = request.form['name']
        return redirect(url_for('chatpage', user = user))

    else: return render_template('index.html')
    
@app.route('/sender', methods = ['GET', 'POST'])
def chatpage():
    if request.method == 'POST':
        receiver_id = request.form['receiver']
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        
    else:
        return render_template('sender.html', user = request.args.get('user'))

if __name__ == '__main__':
    socketio.run(app)