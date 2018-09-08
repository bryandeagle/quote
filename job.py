import feedparser
from PIL import Image, ImageDraw, ImageFont
import os


FEED_URL = 'http://feeds.feedburner.com/brainyquote/QUOTEBR'
STATIC_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')
FONT = os.path.join(STATIC_DIR, 'NotoSerif.ttf')


def get_quote():
    rss = feedparser.parse(FEED_URL)
    return {'author': rss['entries'][0]['title'],
            'quote': rss['entries'][0]['description'].replace('\"', '')}


def wrap(text, font, draw, max_width):
    start, last = 0, ''
    words = text.split(' ')
    for i, v in enumerate(words):
        line = ' '.join(words[start:i+1])
        width, height = draw.textsize(line, font=font)
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
    img = Image.new('RGB', (screen_width, screen_height), color='black')
    draw = ImageDraw.Draw(img)
    # Get heights
    height = screen_height - 256
    line_height = 1.4 * draw.textsize('M', font=font)[1]
    # Add Author
    a = '- {}'.format(author)
    text_width, text_height = draw.textsize(a, font=font)
    (x, y) = (screen_width - text_width) / 2, height
    draw.text((x, y), a, font=font, fill='white')
    height -= 2* line_height
    # Add Quote
    w = wrap(u'\u201c{}\u201d'.format(quote), font, draw, 980)
    for q in w:
        text_width, text_height = draw.textsize(q, font=font)
        (x, y) = (screen_width - text_width) / 2, height
        draw.text((x, y), q, font=font, fill='white')
        height -= line_height

    return img


if __name__ == '__main__':
    q = get_quote()
    img = draw(q['quote'], q['author'])
    img.save(os.path.join(STATIC_DIR, 'quote.png'))
