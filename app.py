#encoding: utf-8

from model import *
from flask import request, session, redirect, render_template, url_for, jsonify, abort
import json
import hashlib, random, time

# create data tables
db.create_all()

def valid_register(username, password, jsonData):
    result = User.query.filter(User.username == username).all()
    if len(result) == 0:
        return True
    else:
        jsonData['reason'] = 'Username existed'
        return False

def register_a_user(username, password, jsonData):
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return True

def valid_login(username, password, jsonData):
    result = User.query.filter(User.username == username).first()
    if result and result.password == password:
        return True
    else:
        jsonData['reason'] = 'Invalid username/password'
        return False
def login_the_user(username, jsonData):
    result = User.query.filter(User.username == username).first()
    jsonData['avator'] = result.avator
    jsonData['nickname'] = result.nickname
    jsonData['description'] = result.description
    jsonData['money'] = result.money
    return True

@app.route('/api/users/register', methods=['POST', 'GET'])
def user_register():
    jsonData = {}
    jsonData['timestamp'] = time.time()
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            md5psw = str(hashlib.md5((salt + request.form['password']).encode()).digest())
            if valid_register(request.form['username'], md5psw, jsonData):
                register_a_user(request.form['username'], md5psw, jsonData)
                jsonData['status'] = 200
            else:
                jsonData['status'] = 0

        print(str(jsonData))
        # message = str(jsonData)
        message = json.dumps(jsonData)
        return message
    else:
        return redirect(url_for('front_end'))

@app.route('/api/users/login', methods=['POST', 'GET'])
def user_login():
    jsonData = {}
    jsonData['timestamp'] = time.time()
    if request.method == 'POST':
        if 'username' in session:
            jsonData['uid'] = session['uid']
            return redirect(url_for('front_end'))
        elif 'username' in request.form and 'password' in request.form:
            md5psw = str(hashlib.md5((salt + request.form['password']).encode()).digest())
            if valid_login(request.form['username'], md5psw, jsonData):
                login_the_user(request.form['username'], jsonData)           
                session['username'] = request.form['username']
                session['uid'] = random.randint(100000, 999999)
                jsonData['uid'] = session['uid']
                jsonData['status'] = 200
            else:
                jsonData['status'] = 0

        print(str(jsonData))
        # message = str(jsonData)
        message = json.dumps(jsonData)
        return message
    else:
        return redirect(url_for('front_end'))

@app.route('/api/user/logout', methods=['POST', 'GET'])
def user_logout():
    if request.method == 'POST':
        jsonData = {}
        jsonData['timestamp'] = time.time()
        if request.args.get('logout'):
            session.clear()
            jsonData['status'] = 200

        print(str(jsonData))
        # message = str(jsonData)
        message = json.dumps(jsonData)
        return message
    else:
        return redirect(url_for('front_end'))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def front_end(path):
    if not request.headers.get('User-Agent'):
        abort(403)

    return render_template("index.html")

# @app.route('/')
# def index():
#     return render_template('index.html')

if __name__ == '__main__':
    debug=True
    app.run(host='0.0.0.0')
