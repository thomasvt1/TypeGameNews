import pyglet
from pyglet.window import key


class Finished:
    def __init__(self, _batch, SCREEN_W, SCREEN_H, array):
        global batch
        batch = _batch

        print("Menu loaded!")

        pyglet.text.Label('Goed gedaan!', font_name='Arial', font_size=32, x=SCREEN_W/2, y=SCREEN_H-50,
                          anchor_x='center', anchor_y = 'center', batch = batch)

        pyglet.text.Label('Klik op ENTER op opnieuw te starten', font_name='Arial', font_size=20, x=SCREEN_W / 2, y=SCREEN_H - 400,
                          anchor_x='center', anchor_y='center', batch=batch)

        print(array[0])
        s = ""
        seq = (str(array[0]), " / ", str(array[1]))
        string = s.join(seq)

        pyglet.text.Label("Goed /  Fout", font_name='Arial', font_size=32, x=SCREEN_W / 2, y=SCREEN_H - 150,
                          anchor_x='center', anchor_y='center', batch=batch)

        pyglet.text.Label(string, font_name='Arial', font_size=32, x=SCREEN_W / 2, y=SCREEN_H - 200,
                          anchor_x='center', anchor_y='center', batch=batch)




    def input(self, symbol):
        i = 0
