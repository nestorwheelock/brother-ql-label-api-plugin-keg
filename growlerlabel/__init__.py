"""
### Name Badge Plugin

## Guillaume Libersat <guillaume@singe-savant.com>
## Brasserie du Singe Savant

Fonts distributed with this plugin:

* Roboto (License: Apache 2.0)
"""

import os
from PIL import Image, ImageDraw, ImageFont

BROTHER_QL_LABEL = "62"

ARGUMENTS = {
    'product_name': {'help': 'Name of product', 'type': str, 'default': 'Anonymous Beer'},
    'abv': {'help': 'Alochol content', 'type': str, 'default': '?.?'},
    'volume': {'help': 'Volume of product', 'type': str, 'default': '75cl'},
    'batch': {'help': 'Batch number', 'type': str, 'default': '???????'},
    'expires': {'help': 'Expire date', 'type': str, 'default': '???????'},
    'allergens': {'help': 'List of allergens', 'type': str, 'default': 'malt d\'orge'},
    'beer_description': {'help': 'Description of beer', 'type': str, 'default': 'Bière pur malt.'},
    'repacked_by': {'help': 'Repacked_by', 'type': str, 'default': '?????'},
}

FONT_REGULAR = "Roboto-Regular.ttf"
FONT_MEDIUM = "Roboto-Medium.ttf"
FONT_BOLD  = "Roboto-Bold.ttf"

LABEL_SIZE = (732, 320)
FONT_SCALING = 4.2

BROTHER_QL_CONVERT_KWARGS = {
}

def resource_path(rel_path):
    return os.path.join(os.path.dirname(__file__), rel_path)

def create_label(product_name=None, abv=None, volume=None, batch=None, repacked_by=None, expires=None, allergens=None, beer_description=None):
    if not product_name: product_name = ARGUMENTS['product_name']['default']
    if not abv: abv = ARGUMENTS['abv']['default']
    if not volume: volume = ARGUMENTS['volume']['default']
    if not batch: batch = ARGUMENTS['batch']['default']
    if not expires: expires = ARGUMENTS['expires']['default']
    if not allergens: allergens = ARGUMENTS['allergens']['default']
    if not beer_description: beer_description = ARGUMENTS['beer_description']['default']
    if not repacked_by: beer_description = ARGUMENTS['repacked_by']['default']

    im = Image.new("L", LABEL_SIZE, 255)
    draw = ImageDraw.Draw(im)

    # brand LOGO
    logo = Image.open(resource_path("logo.png"))
    logo.thumbnail((255, 255), Image.ANTIALIAS)
    im.paste(logo, box=(10, 20), mask=logo.split()[1])

    ## PREGNANT LOGO
    pregnant_logo = Image.open(resource_path("pregnant.png"))
    im.paste(pregnant_logo, box=(580, 170), mask=pregnant_logo.split()[3])

    ## Product name
    x_pos, y_pos = (270, 10)
    font_path = resource_path(FONT_MEDIUM)
    ifs = int(12*FONT_SCALING) # initial font size
    font = fit_text(product_name, LABEL_SIZE[0], font_path, ifs)
    draw.text((x_pos, y_pos), product_name, font=font, fill=0)

    ## ABV + VOL
    txt = "Growler {0} - Alc. {1}% vol".format(volume, abv)
    y_pos += font.size * 1.2
    font_path = resource_path(FONT_REGULAR)
    ifs = int(7*FONT_SCALING) # initial font size
    font = fit_text(txt, LABEL_SIZE[0], font_path, ifs, break_func=break_text_whitespace, max_lines=2)
    line_spacing = int(font.size * 1.15)
    for i, line in enumerate(break_text_whitespace(txt, font, LABEL_SIZE[0])):
        draw.text((x_pos, y_pos+line_spacing*i), line, font=font)

    ## lot
    txt = "Lot : {0}".format(batch)
    y_pos += 40
    font_path = resource_path(FONT_REGULAR)
    ifs = int(7*FONT_SCALING) # initial font size
    font = fit_text(txt, LABEL_SIZE[0], font_path, ifs, break_func=break_text_whitespace, max_lines=2)
    line_spacing = int(font.size * 1.15)
    for i, line in enumerate(break_text_whitespace(txt, font, LABEL_SIZE[0])):
        draw.text((x_pos, y_pos+line_spacing*i), line, font=font)

    txt = "DDM : {0}".format(expires)
    y_pos += 30
    font_path = resource_path(FONT_REGULAR)
    ifs = int(7*FONT_SCALING) # initial font size
    font = fit_text(txt, LABEL_SIZE[0], font_path, ifs, break_func=break_text_whitespace, max_lines=2)
    line_spacing = int(font.size * 1.15)
    for i, line in enumerate(break_text_whitespace(txt, font, LABEL_SIZE[0])):
        draw.text((x_pos, y_pos+line_spacing*i), line, font=font)

    txt = "Mis en Growler par : {0}".format(repacked_by)
    y_pos += 40
    font_path = resource_path(FONT_REGULAR)
    ifs = int(4*FONT_SCALING) # initial font size
    font = fit_text(txt, LABEL_SIZE[0], font_path, ifs, break_func=break_text_whitespace, max_lines=2)
    line_spacing = int(font.size * 1.15)
    for i, line in enumerate(break_text_whitespace(txt, font, LABEL_SIZE[0])):
        draw.text((x_pos, y_pos+line_spacing*i), line, font=font)


    y_pos += 40
    font_path = resource_path(FONT_REGULAR)
    ifs = int(5*FONT_SCALING) # initial font size
    font = fit_text(beer_description, LABEL_SIZE[0], font_path, ifs, break_func=break_text_whitespace, max_lines=2)
    line_spacing = int(font.size * 1.15)
    for i, line in enumerate(break_text_whitespace(beer_description, font, LABEL_SIZE[0])):
        draw.text((x_pos, y_pos+line_spacing*i), line, font=font)



    txt = "Contient :"
    x_pos = 10
    y_pos += 70
    font_path = resource_path(FONT_REGULAR)
    ifs = int(5*FONT_SCALING) # initial font size
    font = fit_text(txt, LABEL_SIZE[0], font_path, ifs, break_func=break_text_whitespace, max_lines=2)
    line_spacing = int(font.size * 1.15)
    for i, line in enumerate(break_text_whitespace(txt, font, LABEL_SIZE[0])):
        draw.text((x_pos, y_pos+line_spacing*i), line, font=font)


    txt = "{0}.".format(allergens)
    x_pos += 95
    font_path = resource_path(FONT_BOLD)
    ifs = int(5*FONT_SCALING) # initial font size
    font = fit_text(txt, LABEL_SIZE[0], font_path, ifs, break_func=break_text_whitespace, max_lines=2)
    line_spacing = int(font.size * 1.15)
    for i, line in enumerate(break_text_whitespace(txt, font, LABEL_SIZE[0])):
        draw.text((x_pos, y_pos+line_spacing*i), line, font=font)

    return im

def break_text_any(txt, font, max_width):
    """
    break text at any character
    https://stackoverflow.com/a/43828315/183995
    """

    # We share the subset to remember the last finest guess over 
    # the text breakpoint and make it faster
    subset = len(txt)
    letter_size = None

    text_size = len(txt)
    while text_size > 0:

        subsets_tried = []
        # Let's find the appropriate subset size
        while True:
            width, height = font.getsize(txt[:subset])
            letter_size = width / subset

            # min/max(..., subset +/- 1) are to avoid looping infinitely over a wrong value
            if width < max_width - letter_size and text_size >= subset: # Too short
                subset = max(int(max_width * subset / width), subset + 1)
            elif width > max_width: # Too large
                subset = min(int(max_width * subset / width), subset - 1)
            else: # Subset fits, we exit
                break

            if subset in subsets_tried:
                break
            else:
                subsets_tried.append(subset)

        yield txt[:subset]
        txt = txt[subset:]
        text_size = len(txt)

def break_text_whitespace(txt, font, max_width):
    """
    break text at whitespace
    https://stackoverflow.com/a/43830313/183995
    """

    line = ""
    width_of_line = 0
    # break string into multi-lines that fit max_width
    for token in txt.split():
        token = token+' '
        token_width = font.getsize(token)[0]
        if width_of_line + token_width < max_width:
            line += token
            width_of_line += token_width
        else:
            yield line
            width_of_line = 0
            line = ""
            line += token
            width_of_line += token_width
    if line:
        yield line

def fit_text(txt, max_width, font_path, initial_font_size, max_lines=1, delta=-1, break_func=break_text_any):
    """
    Tries to fit the given text in the given
    max_width with the given max_lines.
    Adjusts the font size until it fits.
    Returns the font with the adjusted size.
    """
    font_size = initial_font_size
    font = ImageFont.truetype(font_path, font_size)

    while len(list(break_func(txt, font, max_width))) > max_lines:
        font_size += delta
        if font_size == 5: return font
        font = ImageFont.truetype(font_path, font_size)
    return font
