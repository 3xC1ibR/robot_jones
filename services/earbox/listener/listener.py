from multiprocessing import Process
import pyaudio
import wave
import signal
import sys
import whisper
import os
from pathlib import Path
from os import walk
import subprocess
import time
from datetime import datetime

# DIRS
UNPROCESSED = os.path.join(Path(__file__).parent.absolute(), 'audio/unprocessed')
STAGE = os.path.join(Path(__file__).parent.absolute(), 'audio/stage')
ARCHIVE = os.path.join(Path(__file__).parent.absolute(), 'audio/archive')

STAGE_FILE = os.path.join(STAGE, "sounds.wav")
TRIGGER = 'robot jones'

def signal_handler(sig, frame):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('bye')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


def _clean_up():
    _archive_stage()
    files = next(walk(UNPROCESSED), (None, None, []))[2]  # [] if no file
    _archive_unprocessed(files)


def _archive_stage():
    # clear STAGE, UNPROCESSED directories on startup
    print('archiving chunk')
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    if not os.path.isfile(STAGE_FILE):
        return
    old_chunk = STAGE_FILE

    archive_chunk = os.path.join(ARCHIVE, f"archive_{now}.wav")
    os.rename(old_chunk, archive_chunk)


def _archive_unprocessed(file_list):
    # clear STAGE, UNPROCESSED directories on startup
    print('archiving unprocessed files')
    for f in file_list:
        old = os.path.join(UNPROCESSED, f)
        new = os.path.join(ARCHIVE, f)
        os.rename(old, new)


def stream_reader():
    print("loading model")
    # model = whisper.load_model("tiny")
    model = whisper.load_model("base")
    # model = whisper.load_model("small")
    # model = whisper.load_model("large")
    print("model loaded")
    _clean_up()
    while True:
        infiles = next(walk(UNPROCESSED), (None, None, []))[2]  # [] if no file
        if not infiles:
            print('NO FILES IN', UNPROCESSED)
            print('WAITING FOR STREAM TO START...')
            time.sleep(1)
            # os.system('cls' if os.name == 'nt' else 'clear')
            continue
        infiles.sort()
        oldest_ts = infiles[0]
        latest_ts = infiles[-1]

        print('generating file chunk')
        data = []
        for infile in infiles:
            infile = os.path.join(UNPROCESSED, infile)
            w = wave.open(infile, 'rb')
            data.append([w.getparams(), w.readframes(w.getnframes())])
            w.close()

        output = wave.open(STAGE_FILE, 'wb')
        output.setparams(data[0][0])
        for i in range(len(data)):
            output.writeframes(data[i][1])
        output.close()
        #                                                                        ARCHIVE FILE CHUNK
        _archive_unprocessed(infiles)

        print('running transcription')
        print('for timestamps')
        print(oldest_ts, '-->', latest_ts)
        tic = time.process_time()
        result = model.transcribe(STAGE_FILE)
        print('~' * 30)

        text = result["text"]
        print(text)
        if TRIGGER in text.lower():
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('TRIGGER WORD ACTIVATED')
            print('TRIGGER WORD ACTIVATED')
            print('TRIGGER WORD ACTIVATED')
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        with open('transcription.txt', 'a') as f:
            f.write(text)
            f.write('\n')

        print('~' * 30)
        toc = time.process_time()
        print("executed in ", toc - tic)


def stream_writer():
    # AUDIO INPUT
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 3

    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    iters = 0
    while True:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")

        print(f"******[ {now} | {iters} ] recording...")
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        # print('****`frames` length, ', len(frames))
        file_name = 'audio/unprocessed/' + now + '.wav'
        wave_file = wave.open(file_name, 'wb')
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(audio.get_sample_size(FORMAT))
        wave_file.setframerate(RATE)
        wave_file.writeframes(b''.join(frames))
        wave_file.close()
        # print('wave_file closed\n')
        iters += 1


if __name__ == '__main__':
    _clean_up()
    Process(target=stream_reader).start()
    Process(target=stream_writer).start()
