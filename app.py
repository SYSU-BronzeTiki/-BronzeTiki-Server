#encoding: utf-8

from model import *
from flask import render_template, url_for, jsonify
from random import *

# create data tables
db.create_all()

@app.route('/api/userRegister')
def user_register():
    pass

@app.route('/api/userLogin')
def user_login():
    pass

@app.route('/api/userLogout')
def user_logout():
    pass

# @app.route('/api/random')
# def random_number():
#     response = {
#         'randomNumber': randint(1, 100)
#     }
#     return jsonify(response)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

# @app.route('/')
# def index():
#     return render_template('index.html')

if __name__ == '__main__':
    debug=True
    app.run(host='0.0.0.0')
