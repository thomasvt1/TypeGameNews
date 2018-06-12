import pyaudio
import wave
import threading


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


def coin():
    Sound("resources/sound/mario_coin.wav")
    return


def error():
    Sound("resources/sound/error_sound2.wav")
    return


def coin_sound():
    t = threading.Thread(target=coin)
    # threads.append(t)
    t.start()


def error_sound():
    t = threading.Thread(target=error)
    # threads.append(t)
    t.start()
