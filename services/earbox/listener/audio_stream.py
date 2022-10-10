import os
import pyaudio
import wave

# AUDIO INPUT
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "audio/unprocessed.wav"

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
    frames = []
    print('`frames` length, ', len(frames))
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print('`frames` length, ', len(frames))
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
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

    # #Extract Raw Audio from Wav File
    # signal = spf.readframes(-1)
    # signal = np.fromstring(signal, 'Int16')
    # copy= signal.copy()
