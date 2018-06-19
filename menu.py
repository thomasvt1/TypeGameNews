import pyglet
from pyglet.window import key

rss_list = {'Jeugdjournaal': 'https://feeds.feedburner.com/jeugdjournaal',
            'NU.nl': 'http://www.nu.nl/rss/Algemeen'
            }


class Menu:
    def __init__(self, _batch, SCREEN_W, SCREEN_H):
        global batch
        batch = _batch

        print("Menu loaded!")

        pyglet.text.Label('Kies je nieuwsbron', font_name='Arial', font_size=32, x=SCREEN_W/2, y=SCREEN_H-50,
                          anchor_x='center', anchor_y = 'center', batch = batch)

        self.entries = []

        i = 0
        for k in rss_list:
            self.entries.append(pyglet.text.Label(k, font_name='Arial', font_size=18, x=SCREEN_W / 2, y=SCREEN_H - 100 - i, anchor_x='center', anchor_y='center', batch=batch))
            i += 35

        self.location = 0
        self.entries[self.location].color = (0, 255, 0, 255)

    def move(self, change):
        if self.location+change < 0 or self.location+change is len(self.entries):
            return

        self.entries[self.location].color = (255, 255, 255, 255)
        self.location += change
        self.entries[self.location].color = (0, 255, 0, 255)

    def get_selected(self):
        return [self.entries[self.location].text, rss_list.get(self.entries[self.location].text)]

    def input(self, symbol):
        if symbol is key.DOWN:
            self.move(+1)
        elif symbol is key.UP:
            self.move(-1)
