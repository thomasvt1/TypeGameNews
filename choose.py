import pyglet
from pyglet.window import key


class Choose:
    def __init__(self, feed, _batch, SCREEN_W, SCREEN_H):
        global batch
        batch = _batch

        print("Choose loaded!")

        pyglet.text.Label('Kies je artikel', font_name='Arial', font_size=32, x=SCREEN_W/2, y=SCREEN_H-50,
                          anchor_x='center', anchor_y='center', batch=batch)

        self.entries = []

        max_show = min(len(feed), 15)
        self.feed = feed

        for i in range (0, max_show):
            text = feed[i]['title']
            self.entries.append(
                pyglet.text.Label(text, font_name='Arial', font_size=13, x=SCREEN_W / 2, y=SCREEN_H - 100 - i*20,
                                  anchor_x='center', anchor_y='center', batch=batch))

        self.location = 0
        self.entries[self.location].color = (0, 255, 0, 255)

    def move(self, change):
        if self.location+change < 0 or self.location+change is len(self.entries):
            return

        self.entries[self.location].color = (255, 255, 255, 255)
        self.location += change
        self.entries[self.location].color = (0, 255, 0, 255)

    def get_selected(self):
        return self.feed[self.location]

    def input(self, symbol):
        if symbol is key.DOWN:
            self.move(+1)
        elif symbol is key.UP:
            self.move(-1)
