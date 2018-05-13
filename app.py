
from flask import Flask, request, url_for
app = Flask(__name__)

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
