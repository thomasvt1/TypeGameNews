import pyglet
import urllib.request
import feedparser
import re
from pyglet.window import key

# Show FPS
fps = pyglet.clock.ClockDisplay()

python_wiki_rss_url = "https://feeds.feedburner.com/jeugdjournaal"


class Background:
    def __init__(self):
        self.background = pyglet.resource.image('resources/image/mountain.jpg')

    def draw(self):
        self.background.blit(0, 0)


class Window(pyglet.window.Window):
    def __init__(self):
        print("Started!")

        super(Window, self).__init__(vsync=False, height=451, width=720)
        self.set_caption("Type the game!")  # Insert pretty cool name here!

        self.max_fps = 60
        pyglet.clock.schedule(self.update)
        pyglet.clock.set_fps_limit(self.max_fps)

        self.typetext_text = ""
        self.typetext = pyglet.text.Label(text=self.typetext_text, y=self.height/2)
        self.typetext.font_size = 18

        self.typedtext_text = ""
        self.typedtext = pyglet.text.Label(text=self.typetext_text, y=self.height / 2, font_size= 18, color=(0, 255, 0, 255))

        self.background = Background()
        self.fault_words = pyglet.text.Label(text = "Fout overgetikt: 0", x=self.width-160, y=self.height-20)
        self.right_words = pyglet.text.Label(text = "Juist overgetikt: 0", x=self.width-160, y=self.height-40)

    def on_draw(self):
        pyglet.clock.tick()  # Make sure you tick o'l the clock!
        self.clear()
        self.background.draw()
        self.fault_words.draw()
        self.right_words.draw()

        self.typetext.draw()
        self.typedtext.draw()

        fps.draw()

    def get_enter_string(self, text):
        splitter = text.split()

        max = min(9, text.count(" ") + 1)

        final = ""
        for i in range(0, max):
            if (splitter[i]) is not None:
                final += splitter[i] + " "

        return final


    def update(self, dt):
        self.typetext.text = self.get_enter_string("De vulkaan met de naam Kilauea barstte in april uit en daarna zijn er ook nog kleinere uitbarstingen en aardbevingen geweest. Huis uit")
        self.typetext.x = self.width / 2 - self.typetext.content_width / 2

        self.typedtext.text = self.get_enter_string("De vulkaan met de naam Kila")
        self.typedtext.x = self.width / 2 - self.typetext.content_width / 2


# Create a window and run
win = Window()
pyglet.app.run()




feed = feedparser.parse( python_wiki_rss_url )
for x in range(0, 20):
    feed['entries'][x]['summary'] = re.sub('<[^>]+>', '', feed['entries'][x]['summary'])

for x in range(0, 20):
    print(feed['entries'][x]['summary'])

