import pyglet
from pyglet.window import key
import pyaudio
import wave
import threading

# Show FPS
fps = pyglet.clock.ClockDisplay()


class Sound:
    def __init__(self, file_location):
        chunk = 1024
        f = wave.open(file_location, "rb")
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                        channels=f.getnchannels(),
                        rate=f.getframerate(),
                        output=True)
        data = f.readframes(chunk)
        while data:
            stream.write(data)
            data = f.readframes(chunk)

            # stop stream
        stream.stop_stream()
        stream.close()

        # close PyAudio
        p.terminate()


class Game:
    def __init__(self, text, _batch, SCREEN_W, SCREEN_H):
        global batch
        batch = _batch

        self.width = SCREEN_W
        self.height = SCREEN_H

        self.shifted = False
        self.finished = False

        #TODO: This text will be obtained by polling RSS feed.
        self.typetext_text = text
        self.typetext = pyglet.text.Label(text=self.typetext_text, y=SCREEN_H/2, batch = batch)
        self.typetext.font_size = 18

        self.progress = 0  # This gives the current location of the string where the player is.
        self.typedtext = pyglet.text.Label(text=self.typetext_text, y=SCREEN_H / 2, font_size=18, batch = batch, color=(0, 255, 0, 255))

        self.fault_words=0
        self.right_words=0

        self.fault_wordsprint = pyglet.text.Label(text="Fout overgetikt: " + str(self.fault_words),  x=SCREEN_W-160, y=SCREEN_H-20, batch=batch)
        self.right_wordsprint = pyglet.text.Label(text="Juist overgetikt: " + str(self.right_words), x=SCREEN_W-160, y=SCREEN_H-40, batch=batch)

        self.update_screen()

        #Sound("resources/sound/error_sound2.wav")

    def finished_sentence(self):
        if len(self.get_short_string(self.typetext_text)) == self.progress+1:
            return True
        # if next char is ' ' return True
        return False

    def input(self, symbol):

        if self.finished:
            return

        if symbol is key.LSHIFT:
            self.shifted = True

        sym = self.parse_input(key.symbol_string(symbol))
        print(sym)
        if not self.shifted:
            sym = sym.lower()

        print(self.shifted)
        print(sym)
        print(self.typetext_text[self.progress])

        if sym == (self.typetext_text[self.progress]):
            self.progress += 1
            self.right_words += 1
        else:
            if len(key.symbol_string(symbol)) is 1:
                self.fault_words +=1
                #Sound("resources/sound/mario_coin.wav")

        if symbol is key.ENTER:
            self.progress += 1

        if self.finished_sentence():
            self.next_line()
            self.progress = 0

        self.update_screen()

    def release(self, symbol):
        if symbol is key.LSHIFT:
            self.shifted = False
            print('not shifted!')
            print(self.shifted)

    def parse_input(self, symbol):
        if symbol is 'SPACE':
            symbol = ' '
        elif symbol is 'SEMICOLON':
            symbol = ':'
        elif symbol is 'PERIOD':
            symbol = '.'
        elif symbol is 'COMMA':
            symbol = ','
        elif symbol is 'APOSTROPHE':
            symbol = "'"
        elif symbol[0] is '_':
            symbol = symbol[1]
        if self.shifted:
            if symbol is '0':
                symbol = ')'
            if symbol is '1':
                symbol = '!'
            if symbol is '2':
                symbol = '@'
            if symbol is '3':
                symbol = '#'
            if symbol is '4':
                symbol = '$'
            if symbol is '5':
                symbol = '%'
            if symbol is '6':
                symbol = '^'
            if symbol is '7':
                symbol = '&'
            if symbol is '8':
                symbol = '*'
            if symbol is '9':
                symbol = '('

        return symbol


    def update_screen(self):
        #  Copy pasta belown
        self.typetext.text = self.get_short_string(self.typetext_text)
        self.typetext.x = self.width / 2 - self.typetext.content_width / 2

        self.typedtext.text = self.typetext_text[:self.progress]
        self.typedtext.x = self.typetext.x
        #self.typedtext.x = self.width / 2 - self.typetext.content_width / 2

        self.fault_wordsprint.text = "Fout overgetikt: " + str(self.fault_words)
        self.right_wordsprint.text = "Juist overgetikt: " + str(self.right_words)
        #  End copy pasta



    def next_line(self):
        self.typetext_text = self.typetext_text.replace(self.get_short_string(self.typetext_text), "")

    def get_short_string(self, text):       #52 letters max
        splitter = text.split()
        max_words = min(9, text.count(" "))

        if max_words is 0:
            print('Oh nee!')
            self.finish()
            return text

        final = ""
        char_cur = 0
        for i in range(0, max_words):
            if (splitter[i]) is not None:
                char_cur += len(splitter[i])        # Makes sure theres not more chars than possible on screen
                if char_cur < 53:
                    final += splitter[i] + " "
        return final


    def finish(self):
        i = 0
