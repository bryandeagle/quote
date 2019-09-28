from PIL import Image, ImageDraw, ImageFont
import feedparser
import os


def _get_quote():
    """ Parses quote from brainyquote's RSS feed """
    rss = feedparser.parse('http://feeds.feedburner.com/brainyquote/QUOTEBR')
    return {'author': rss['entries'][0]['title'],
            'quote': rss['entries'][0]['description'].replace('\"', '')}


def _wrap_text(text, font, drawing, max_width):
    """ Wrap text appropriately """
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


def _draw(quotation, author):
    """ Create the image from the given quote """
    # Phone-specific constants
    screen_width, screen_height = 1080, 1920
    font_name, font_size = 'NotoSerif.ttf', 72
    bottom_margin = 256  # Leave 256 pixels free

    # Create image
    font_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), font_name)
    font = ImageFont.truetype(font_file, font_size)
    image = Image.new('RGB', (screen_width, screen_height), color='black')
    drawing = ImageDraw.Draw(image)

    # Get heights
    line_height = 1.4 * drawing.textsize('M', font=font)[1]
    height = screen_height - bottom_margin - line_height

    # Add Author
    a = '- {}'.format(author)
    text_width, text_height = drawing.textsize(a, font=font)
    (x, y) = (screen_width - text_width) / 2, height
    drawing.text((x, y), a, font=font, fill='white')
    height -= 2 * line_height

    # Add Quote
    w = _wrap_text(u'\u201c{}\u201d'.format(quotation), font, drawing, screen_width - 100)
    for line in reversed(list(w)):
        text_width, text_height = drawing.textsize(line, font=font)
        (x, y) = (screen_width - text_width) / 2, height
        drawing.text((x, y), line, font=font, fill='white')
        height -= line_height
    return image


def quote(output_directory):
    new_quote = _get_quote()
    img = _draw(new_quote['quote'], new_quote['author'])
    img.save(os.path.join(output_directory, 'quote.png'))


if __name__ == '__main__':
    quote(os.path.dirname(os.path.realpath(__file__)))
