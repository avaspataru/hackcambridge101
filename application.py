from flask import Flask
from phrase_similarity import lookup

app = Flask(__name__)

@app.route("/")
def hello():
    #result = <call-elastic-server here>
    return "hello"
    #return requests.get('http://example.com').content
    #return "pls change"
    #return flask.render_template('index.html')
    #return "Hello World!"

@app.route("/regex/<val>")
def get_code(val):
    l = lookup(val)
    return l
