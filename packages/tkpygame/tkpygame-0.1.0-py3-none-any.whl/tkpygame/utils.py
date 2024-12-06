import base64
import pygame
from io import BytesIO
from PIL import Image

from constants import *

class TerminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ERROR = '\033[91m'

    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'


def print_colored(text, color=TerminalColors.WHITE, only_if_not_debugging=True):
    result = color + str(text) + TerminalColors.ENDC
    if "New canvas " in str(text):
        result = "\n\n" + result + "\n"
    print(result)


def update_canvas_rect(canvas):
    if callable(canvas.width):
        canvas._width = canvas.width()
    else:
        canvas._width = canvas.width

    if callable(canvas.height):
        canvas._height = canvas.height()
    else:
        canvas._height = canvas.height

    if callable(canvas.x):
        canvas._x = canvas.x()
    else:
        canvas._x = canvas.x

    if callable(canvas.y):
        canvas._y = canvas.y()
    else:
        canvas._y = canvas.y


def update_rect(obj):
    if callable(obj.canvas.width):
        obj.canvas_width = obj.canvas.width()
    else:
        obj.canvas_width = obj.canvas.width

    if callable(obj.canvas.height):
        obj.canvas_height = obj.canvas.height()
    else:
        obj.canvas_height = obj.canvas.height

    if callable(obj.width):
        obj._width = obj.width()
    else:
        obj._width = obj.width

    if callable(obj.height):
        obj._height = obj.height()
    else:
        obj._height = obj.height

    try:
        if callable(obj.canvas.x):
            obj.canvas_x = obj.canvas.x()
        else:
            obj.canvas_x = obj.canvas.x

        if callable(obj.canvas.y):
            obj.canvas_y = obj.canvas.y()
        else:
            obj.canvas_y = obj.canvas.y
    except AttributeError:
        print("Error: Canvas object does not have x and y attributes")

    obj._padding = [0, 0]
    try:
        if callable(obj.padding[0]):
            obj._padding[0] = obj.padding[0]()
        else:
            obj._padding[0] = obj.padding[0]

        if callable(obj.padding[1]):
            obj._padding[1] = obj.padding[1]()
        else:
            obj._padding[1] = obj.padding[1]
    except AttributeError:
        print("Error: Canvas object does not have padding attributes")

    # Set position based on anchor
    if obj.anchor == "N":
        obj._x = obj.canvas_x - obj._width / 2 + obj.canvas._width / 2 + obj._padding[0]
        obj._y = obj.canvas_y + obj._padding[1]
    elif obj.anchor == "NE":
        obj._x = obj.canvas_x + obj.canvas_width - obj._width - obj._padding[0]
        obj._y = obj.canvas_y + obj._padding[1]
    elif obj.anchor == "E":
        obj._x = obj.canvas_x + obj.canvas_width - obj._width - obj._padding[0]
        obj._y = obj.canvas_y + obj.canvas_height / 2 - obj._height / 2 - obj._padding[1]
    elif obj.anchor == "SE":
        obj._x = obj.canvas_x + obj.canvas_width - obj._width - obj._padding[0]
        obj._y = obj.canvas_y + obj.canvas_height - obj._height - obj._padding[1]
    elif obj.anchor == "S":
        obj._x = obj.canvas_x + obj.canvas_width / 2 - obj._width / 2 + obj._padding[0]
        obj._y = obj.canvas_y + obj.canvas_height - obj._height - obj._padding[1]
    elif obj.anchor == "SW":
        obj._x = obj.canvas_x + obj.padding[0]
        obj._y = obj.canvas_y + obj.canvas_height - obj._height - obj.padding[1]
    elif obj.anchor == "W":
        obj._x = obj.canvas_x + obj.padding[0]
        obj._y = obj.canvas_y + obj.canvas_height / 2 - obj._height / 2 + obj.padding[1]
    elif obj.anchor == "NW":
        obj._x = obj.canvas_x + obj._padding[0]
        obj._y = obj.canvas_y + obj._padding[1]
    elif obj.anchor == "CENTER":
        obj._x = obj.canvas_x + obj.canvas_width / 2 - obj._width / 2 + obj._padding[0]
        obj._y = obj.canvas_y + obj.canvas_height / 2 - obj._height / 2 + obj._padding[1]


def set_icon_from_base64(base64_string):
    icon_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(icon_data))
    image = image.convert('RGBA')  # Ensure image has an alpha channel
    mode = image.mode
    size = image.size
    data = image.tobytes()

    icon_surface = pygame.image.frombuffer(data, size, mode)
    pygame.display.set_icon(icon_surface)
