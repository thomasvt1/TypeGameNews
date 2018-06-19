import pyglet
from pyglet.window import key
import pyaudio
import wave
import threading
import audio

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
        self.batch = _batch

        self.width = SCREEN_W
        self.height = SCREEN_H

        self.shifted = False
        self.finished = False

        self.typetext_text = text
        self.typetext = pyglet.text.Label(text=self.typetext_text, y=SCREEN_H/2, batch=batch)
        self.typetext.font_size = 18

        self.progress = 0  # This gives the current location of the string where the player is.
        self.typedtext = pyglet.text.Label(text=self.typetext_text, y=SCREEN_H / 2, font_size=18,
                                           batch=batch, color=(0, 255, 0, 255))

        self.fault_words=0
        self.right_words=0

        self.fault_wordsprint = pyglet.text.Label(text="Fout overgetikt: " + str(self.fault_words),
                                                  x=SCREEN_W-160, y=SCREEN_H-20, batch=batch)
        self.right_wordsprint = pyglet.text.Label(text="Juist overgetikt: " + str(self.right_words),
                                                  x=SCREEN_W-160, y=SCREEN_H-40, batch=batch)
        #self.end_screen_right = pyglet.text.Label(text="Juist overgetikt: " + str(self.right_words), x=SCREEN_W-400, y=SCREEN_H-200, batch=batch)
        #self.end_screen_fault = pyglet.text.Label(text="Fout overgetikt: " + str(self.fault_words), x=SCREEN_W - 400,
        #                                          y=SCREEN_H - 250, batch=batch)

        self.update_screen()

        #Sound("resources/sound/error_sound2.wav")
        #audio

    def finished_sentence(self):
        if self.get_short_string(self.typetext_text)[-1:] == ' ':
            if len(self.get_short_string(self.typetext_text)) == self.progress+1:
                return True
        # if next char is ' ' return True
        return False

    def input(self, symbol):
        if self.finished:
            print('Finished!')
            #return "FINISHED"
            return [self.right_words, self.fault_words]

        if symbol is key.LSHIFT:
            self.shifted = True

        sym = self.parse_input(symbol)
        print('-------')
        print(key.symbol_string(symbol))
        print(sym)
        print(self.typetext_text[self.progress])

        if not self.shifted:
            sym = sym.lower()

        if sym == (self.typetext_text[self.progress]):
            self.progress += 1
            self.right_words += 1
            if sym == " ":
                audio.coin_sound()    # play coin sound
        else:
            if len(key.symbol_string(symbol)) is 1:
                self.fault_words += 1
                audio.error_sound()     # play error sound

        if symbol is key.ENTER:
            self.progress += 1

        if self.finished_sentence():
            self.next_line()
            self.progress = 0
            audio.coin_sound()  # play coin sound

        self.update_screen()

    def release(self, symbol):
        if symbol is key.LSHIFT:
            self.shifted = False
            print('not shifted!')
            print(self.shifted)

    def parse_input(self, symbol):
        sym = key.symbol_string(symbol)
        if symbol is key.SPACE:
            sym = ' '
        elif symbol is key.SEMICOLON:
            sym = ':'
        elif symbol is key.PERIOD:
            sym = '.'
        elif symbol is key.COMMA:
            sym = ','
        elif symbol is key.MINUS:
            sym = '-'
        elif symbol is key.APOSTROPHE:
            sym = "'"
        elif 'user_key(de)' in sym:
            sym = "'"
        elif sym[0] is '_':
            sym = sym[1]
        if self.shifted:
            if sym is '0':
                sym = ')'
            if sym is '1':
                sym = '!'
            if sym is '2':
                sym = '@'
            if sym is '3':
                sym = '#'
            if sym is '4':
                sym = '$'
            if sym is '5':
                sym = '%'
            if sym is '6':
                sym = '^'
            if sym is '7':
                sym = '&'
            if sym is '8':
                sym = '*'
            if sym is '9':
                sym = '('

        return sym


    def update_screen(self):
        if self.finished is False:
            #  Copy pasta belown
            self.typetext.text = self.get_short_string(self.typetext_text)
            self.typetext.x = self.width / 2 - self.typetext.content_width / 2

            self.typedtext.text = self.typetext_text[:self.progress]
            self.typedtext.x = self.typetext.x
            #self.typedtext.x = self.width / 2 - self.typedtext.content_width / 2

            self.fault_wordsprint.text = "Fout overgetikt: " + str(self.fault_words)
            self.right_wordsprint.text = "Juist overgetikt: " + str(self.right_words)
            #  End copy pasta
        elif self.finished is True:
            i = 0
            self.batch = pyglet.graphics.Batch()


            #self.end_screen_right.text = "Juist overgetikt: " + str(self.right_words)
            #self.end_screen_fault.text = "Fout overgetikt: " + str(self.fault_words)

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
        self.finished = True
