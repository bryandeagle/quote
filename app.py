from flask import Flask, redirect
app = Flask(__name__)


@app.route('/')
def hello_world():
    return redirect('/quote.png')
