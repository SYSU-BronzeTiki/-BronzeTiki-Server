#encoding: utf-8

from model import *
from flask import request, session, redirect, render_template, url_for, jsonify, abort
import json
import hashlib, random, time

# create data tables
db.create_all()

def register_a_user(username, password, jsonData):
    result = User.query.filter(User.username == username).all()
    if len(result) == 0:
        try:
            md5psw = str(hashlib.md5((salt + password).encode()).digest())
            user = User(username=username, password=md5psw)
            db.session.add(user)
            db.session.commit()
            jsonData['message'] = 'Register succeeded'
            return True
        except:
            jsonData['message'] = 'Register failed'
            return False
    else:
        jsonData['message'] = 'Username existed'
        return False

@app.route('/api/users/register', methods=['POST', 'GET'])
def user_register():
    if request.method == 'POST':
        jsonData = {}
        jsonData['timestamp'] = time.time()
        # print(str(request.form))
        if 'username' not in request.form:
            jsonData['status'] = '0'
            jsonData['message'] = 'No username'
        elif 'password' not in request.form:
            jsonData['status'] = '0'
            jsonData['message'] = 'No password'
        else:
            # validate and register
            if register_a_user(request.form['username'], request.form['password'], jsonData):
                jsonData['status'] = 200
            else:
                jsonData['status'] = 0

        print(str(jsonData))           # debug the message
        message = json.dumps(jsonData) # convert to json
        return message
    # GET
    return redirect(url_for('front_end'))

def login_the_user(username, password, jsonData):
    result = User.query.filter(User.username == username).first()
    md5psw = str(hashlib.md5((salt + password).encode()).digest())
    if result:
        if result.password == md5psw:
            try:
                result = User.query.filter(User.username == username).first()
                jsonData['avator'] = result.avator
                jsonData['nickname'] = result.nickname
                jsonData['description'] = result.description
                jsonData['money'] = result.money
                jsonData['message'] = 'Login succeeded'
                return True
            except:
                jsonData['message'] = 'Login failed'
                return False
        else:
            jsonData['message'] = 'Invalid password'
            return False
    else:
        jsonData['message'] = 'Invalid username'
        return False

@app.route('/api/users/login', methods=['POST', 'GET'])
def user_login():
    # POST
    if request.method == 'POST':
        jsonData = {}
        jsonData['timestamp'] = time.time()

        if 'username' not in request.form:
            jsonData['status'] = '0'
            jsonData['message'] = 'No username'
        elif 'password' not in request.form:
            jsonData['status'] = '0'
            jsonData['message'] = 'No password'
        else:
            # validate and login
            if login_the_user(request.form['username'], request.form['password'], jsonData):
                session['username'] = request.form['username']
                session['avator'] = jsonData['avator']
                session['nickname'] = jsonData['nickname']
                session['description'] = jsonData['description']
                session['money'] = jsonData['money']
                session.permanent = True
                # session['uid'] = (random.randint(1000000, 9999999) + (int)(time.time())) % 1000000
                # jsonData['uid'] = session['uid']
                jsonData['status'] = 200
            else:
                jsonData['status'] = 0

        print(str(jsonData))           # debug the message
        message = json.dumps(jsonData) # convert to json
        return message
    # GET
    if 'username' in session:
        if request.args.get('logout'):
            print(session.get('username', 'none') + " logout")
            session.clear()
        return redirect(url_for('front_end'))
    # GET
    return redirect(url_for('front_end'))

@app.route('/api/movies', methods=['POST', 'GET'])
def movies():
    pass

@app.route('/api/orders', methods=['POST', 'GET'])
def orders():
    pass

@app.route('/api/state', methods=['GET', 'POST'])
def state():
    jsonData = {}
    jsonData['timestamp'] = time.time()
    if 'username' not in session:
        jsonData['message'] = 'Offline'
        jsonData['status'] = 0
    elif 'username' in session:
        # jsonData['uid'] = jsonData['uid']
        jsonData['username'] = session.get('username', 'none')
        jsonData['avator'] = session.get('avator', 'none')
        jsonData['nickname'] = session.get('nickname', 'none')
        jsonData['description'] = session.get('description', 'none')
        jsonData['money'] = session.get('money', 'none')
        jsonData['message'] = 'Online'
        jsonData['status'] = 200
    print(str(jsonData))           # debug the message
    message = json.dumps(jsonData) # convert to json
    return message


@app.route('/', defaults={'path': ''})  # root dir
@app.route('/<path:path>')              # any path
def front_end(path):
    if not request.headers.get('User-Agent'):
        abort(403)

    paths = path.split('/')
    print([x for x in paths])
    return render_template("index.html")

if __name__ == '__main__':
    debug=True
    app.run(host='0.0.0.0')
