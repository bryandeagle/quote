from flask import Flask, send_file
import io

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'


@app.route('/image.jpg')
def logo():
    with open('/home/bryandeagle/quote/media/test.jpg', 'rb') as bites:
        return send_file(io.BytesIO(bites.read()),
                         attachment_filename='wallpaper.jpg',
                         mimetype='image/jpg')
