from flask import Flask, send_file
import io

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'


@app.route('/image')
def image():
    redirect(url_for('static', filename='test.jpg'))