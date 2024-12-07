import simpleaudio as sa
import pyaudio
import wave

class AudioController:
    _instance = None

    def __init__(self):
        if not AudioController._instance:
            self.CHUNK = 2048
            self.FORMAT = pyaudio.paInt16
            self.CHANNELS = 1
            self.RATE = 44100
        else:
            raise Exception("You cannot create another AudioController class")

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = AudioController()
        return cls._instance

    def record(self, duration, filename):
        p = pyaudio.PyAudio()

        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        frames = []

        for _ in range(0, int(self.RATE / self.CHUNK *  duration)):
            data = stream.read(self.CHUNK, exception_on_overflow=False)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))

    def play(self, filename):
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        #play_obj.wait_done()       # Commented this out so that it is non-blocking - There is no time to wait, there is only time to play
        
