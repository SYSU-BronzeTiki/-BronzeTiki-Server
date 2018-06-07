#encoding: utf-8

from model import *
from flask import render_template, url_for

# create data tables
db.create_all()

# import os
# indexFilePath = os.getcwd()
# indexFilePath = os.path.join(indexFilePath, 'templates\index.html')

@app.route('/')
def index():
    return render_template('index.html')
    # indexStr = ''
    # with open(indexFilePath, 'r') as f:
    #     indexStr = f.read()''
    # return indexStr

if __name__ == '__main__':
    debug=True
    app.run(host='0.0.0.0')
