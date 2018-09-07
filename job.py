import feedparser
from PIL import Image, ImageDraw, ImageFont

FEED_URL = 'http://feeds.feedburner.com/brainyquote/QUOTEBR'
FONT = '/home/bryandeagle/quote/media/NotoSerif.ttf'

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
    # Add Quote
    w = wrap(u'\u201c{}\u201d'.format(quote), font, draw, 980)
    line_height = 1.5 * draw.textsize('M', font=font)[1]
    height = screen_height / 2
    for q in w:
        text_width, text_height = draw.textsize(q, font=font)
        (x, y) = (screen_width - text_width) / 2, height
        draw.text((x, y), q, font=font, fill='white')
        height += line_height
    # Add Author
    a = '- {}'.format(author)
    height += line_height
    text_width, text_height = draw.textsize(a, font=font)
    (x, y) = (screen_width - text_width) / 2, height
    draw.text((x, y), a, font=font, fill='white')
    return img


def create_image(filepath):
    q = get_quote()
    img = draw(q['quote'], q['author'])
    img.save(filepath)

if __name__ == '__main__':
    create_image('/home/bryandeagle/static/quote.png')
