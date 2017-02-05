import os
from flask import Flask, session, redirect, url_for, escape, request, send_from_directory
from werkzeug import secure_filename
import hashlib

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = 'tmp/'

KEY = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"

@app.route('/')
def index():
    print session
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    else:
        return 'You have no permission.'
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        # Password is admin
        if hashlib.sha256((request.form['password']).encode('utf-8')).hexdigest() != KEY:
            return '''
                <p>ERROR: Wrong Password!</p>
            '''
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/post_trade', methods=['GET', 'POST'])
def post_trade():
    #if 'username' not in session:
    #    return 'You have no permission.'
    if request.headers.get("key") != KEY:
        return "ERROR: Wrong KEY!"
    if request.method == 'POST':
        return request.get_data()
    return "Nothing here."

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/get_all')
def get_all():
    if 'username' not in session:
        return 'You have no permission.'
    return 'All messages!'

@app.route('/get/<int:post_id>')
def get(post_id):
    if 'username' not in session:
        return 'You have no permission.'
    return 'ID: %s' % post_id

def allowed_file(filename):
    if 'username' not in session:
        return 'You have no permission.'
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'username' not in session:
        return 'You have no permission.'
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    if 'username' not in session:
        return 'You have no permission.'
    #return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    return "File %s uploaded!" % filename

if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(host='0.0.0.0', debug = True)
