import os
import pyaudio
import wave
from datetime import datetime
import pyaudio
import wave
from pathlib import Path


# AUDIO INPUT
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "audio/unprocessed.wav"
# WAVE_OUTPUT_FILENAME_1 = "audio/unprocessed_1.wav"
# WAVE_OUTPUT_FILENAME_2 = "audio/unprocessed_2.wav"

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print(type(stream))

iters = 0
while True:
    print("recording...")
    print(iters)

UNPROCESSED_DIR = os.path.join(Path(__file__).parent.absolute(), 'audio/unprocessed')


iters = 0
while True:
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    # os.system('cls' if os.name == 'nt' else 'clear')
    print(f"[ {now} | {iters} ] recording...")
    frames = []
    print('`frames` length, ', len(frames))
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print('`frames` length, ', len(frames))
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')

    file_name = 'audio/unprocessed/' + now + '.wav'
    waveFile = wave.open(file_name, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    print(iters)
    print(iters)
    print(iters)
    print(iters)
    print('waveFile closed\n')
    spf = wave.open(WAVE_OUTPUT_FILENAME, 'r')
    iters += 1
    os.system('cls' if os.name == 'nt' else 'clear')
    print('waveFile closed\n')
    # spf = wave.open(WAVE_OUTPUT_FILENAME_1, 'r')
    iters += 1

    # #Extract Raw Audio from Wav File
    # signal = spf.readframes(-1)
    # signal = np.fromstring(signal, 'Int16')
    # copy= signal.copy()
