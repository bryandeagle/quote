import cStringIO as StringIO
from flask import Flask, send_file
from skimage.io import imsave


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/image')
def image():
    """
    Return a generated image as a png by
    saving it into a StringIO and using send_file.
    """
    num_tiles = 20
    tile_size = 30
    arr = np.random.randint(0, 255, (num_tiles, num_tiles, 3))
    arr = arr.repeat(tile_size, axis=0).repeat(tile_size, axis=1)

    # We make sure to use the PIL plugin here because not all skimage.io plugins
    # support writing to a file object.
    strIO = StringIO.StringIO()
    imsave(strIO, arr, plugin='pil', format_str='png')
    strIO.seek(0)
    return send_file(strIO, mimetype='image/png')