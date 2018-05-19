#encoding: utf-8

from flask import Flask, request, url_for
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

# test the SQLAlchemy configuration
db.create_all()

import os
indexFilePath = os.getcwd()
indexFilePath = os.path.join(indexFilePath, 'templates\index.html')

@app.route('/')
def index():
    indexStr = ''
    with open(indexFilePath, 'r') as f:
        indexStr = f.read()
    return indexStr

debug=True

if __name__ == '__main__':
    app.run(host='0.0.0.0')
