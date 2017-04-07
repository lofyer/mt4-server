#!/usr/bin/python3
import os
from flask import Flask, abort, request, jsonify, g, url_for, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_bootstrap import Bootstrap
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
    as Serializer, BadSignature, SignatureExpired)
from datetime import datetime
import hashlib
import jinja2.exceptions
import pymysql

# Initialization
db_uri = 'sqlite:///db.sqlite'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lofyer'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_FOLDER'] = 'tmp/'

# extensions
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
auth = HTTPBasicAuth()
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user

# Index
@app.route('/index', methods=['GET'])
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',current_time=datetime.utcnow())

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

# Create user
@app.route('/api/users', methods=['GET', 'POST'])
def new_user():
    if request.method == 'GET':
        return render_template("msg.html", msg="Use POST method to create user.")
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})

# 404 page
@app.errorhandler(404)
def page_not_found(e):
        return render_template('404.html'),404

# Get user name by id
@app.route('/api/users/<int:id>', methods = ['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})
    #return render_template('user.html',name=user.username)

# Get temporary token
@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})

# Get resource test
@app.route('/api/v1/health')
def get_health():
    return jsonify({"Service":"OK"})

# Get resource test
@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, {}!'.format(g.user.username)})

@app.route('/api/v1/history')
@auth.login_required
def get_history():
    data = "Trade history of {}:</br>".format(g.user.username)
    return data

@app.route('/api/v1/post_trade', methods=['GET', 'POST'])
@auth.login_required
def post_trade():
    if request.method == 'POST':
        data = "What {} post is {}".format(g.user.username,request.get_data())
        return data
    return "This is trade-posting page."

def allowed_file(filename):
    if 'username' not in session:
        return 'You must login.'
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
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
    if not os.path.exists("./db.sqlite"):
        db.create_all()
    app.run(debug=True)
