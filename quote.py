import feedparser
from PIL import Image, ImageDraw, ImageFont
import os


FEED_URL = 'http://feeds.feedburner.com/brainyquote/QUOTEBR'
STATIC_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')
FONT = 'NotoSerif.ttf'


def get_quote():
    rss = feedparser.parse(FEED_URL)
    return {'author': rss['entries'][0]['title'],
            'quote': rss['entries'][0]['description'].replace('\"', '')}


def wrap(text, font, drawing, max_width):
    start, last = 0, ''
    words = text.split(' ')
    for i, v in enumerate(words):
        line = ' '.join(words[start:i+1])
        width, height = drawing.textsize(line, font=font)
        if width < max_width:
            last = line
        else:
            start = i
            yield last
    yield ' '.join(words[start:])


def draw(quote, author):
    # Create image
    screen_width, screen_height = (1080, 1920)
    font = ImageFont.truetype(FONT, 72)
    image = Image.new('RGB', (screen_width, screen_height), color='black')
    drawing = ImageDraw.Draw(image)
    # Get heights
    line_height = 1.4 * drawing.textsize('M', font=font)[1]
    height = screen_height - 256 - line_height
    # Add Author
    a = '- {}'.format(author)
    text_width, text_height = drawing.textsize(a, font=font)
    (x, y) = (screen_width - text_width) / 2, height
    drawing.text((x, y), a, font=font, fill='white')
    height -= 2 * line_height
    # Add Quote
    w = wrap(u'\u201c{}\u201d'.format(quote), font, drawing, screen_width-100)
    for line in reversed(list(w)):
        text_width, text_height = drawing.textsize(line, font=font)
        (x, y) = (screen_width - text_width) / 2, height
        drawing.text((x, y), line, font=font, fill='white')
        height -= line_height

    return image


if __name__ == '__main__':
    q = get_quote()
    img = draw(q['quote'], q['author'])
    img.save(os.path.join(STATIC_DIR, 'quote.png'))
