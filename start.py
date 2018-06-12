import pyglet
import parsefeed
from menu import Menu
from game import Game
from choose import Choose

from pyglet.window import key

SCREEN_H = 450
SCREEN_W = 720

MAX_FPS = 60

CAPTION = "Type The Game"
active_window = 0

fps = pyglet.clock.ClockDisplay()

# Create window.
mainWindow = pyglet.window.Window(SCREEN_W, SCREEN_H, caption=CAPTION)

background = pyglet.resource.image('resources/image/mountain.jpg')


def main_menu():
    """ Main menu in the game. """

    global batch, active_window

    # Reset batch for rendering.
    batch = pyglet.graphics.Batch()

    active_window = Menu(batch, SCREEN_W, SCREEN_H)


def start_game(selected):
    global batch, active_window

    batch = pyglet.graphics.Batch()
    text = selected['summary']
    print(text)
    text = 'Hallo Chris! !@#$%^&*() 0987654321'

    active_window = Game(text, batch, SCREEN_W, SCREEN_H)


def show_stories(selected):
    global batch, active_window

    feed = parsefeed.get_feed(selected)
    batch = pyglet.graphics.Batch()

    active_window = Choose(feed, batch, SCREEN_W, SCREEN_H)


@mainWindow.event
def on_key_release(symbol, modifiers):
    global active_window

    if active_window.__class__ is Game:
        active_window.release(symbol)

@mainWindow.event
def on_key_press(symbol, modifiers):
    global active_window

    if active_window.__class__ is Game:
        active_window.input(symbol)

    elif active_window.__class__ is Menu:
        if symbol is key.ENTER:
            selected = active_window.get_selected()
            if selected is not None:
                show_stories(selected)
        else:
            active_window.input(symbol)

    elif active_window.__class__ is Choose:
        if symbol is key.ENTER:
            selected = active_window.get_selected()
            if selected is not None:
                print(selected)
                start_game(selected)
        else:
            active_window.input(symbol)


@mainWindow.event
def on_draw():
    pyglet.clock.tick()  # Make sure you tick o'l the clock!
    mainWindow.clear()
    background.blit(0, 0)

    batch.draw()
    fps.draw()


def update(dt):
    i = 0


# Ruin the game.
main_menu()
#pyglet.clock.schedule_interval(update, 1.0/60.0)
pyglet.clock.set_fps_limit(MAX_FPS)
pyglet.app.run()
