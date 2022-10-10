import wave
import whisper
import os
from pathlib import Path
from os import walk
import subprocess
import time
from datetime import datetime

UNPROCESSED = os.path.join(Path(__file__).parent.absolute(), 'audio/unprocessed')
STAGE = os.path.join(Path(__file__).parent.absolute(), 'audio/stage')
ARCHIVE = os.path.join(Path(__file__).parent.absolute(), 'audio/archive')


STAGE_FILE = os.path.join(STAGE, "sounds.wav")

TRIGGER = 'robot jones'

model = whisper.load_model("medium") # ~50 lag
model = whisper.load_model("small")
now = datetime.now().strftime("%Y%m%d_%H%M%S")
while True:
    #                                                                        GET FILES
    infiles = next(walk(UNPROCESSED), (None, None, []))[2]  # [] if no file
    if not infiles:
        print('NO FILES IN', UNPROCESSED)
        print('WAITING FOR STREAM TO START...')
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        continue
    infiles.sort()
    #                                                                        GENERATE FILE CHUNK
    print('generating file chunk')
    data = []
    for infile in infiles:
        infile = os.path.join(UNPROCESSED, infile)
        # infile = infile + '.wav'
        w = wave.open(infile, 'rb')
        data.append([w.getparams(), w.readframes(w.getnframes())])
        w.close()

    output = wave.open(STAGE_FILE, 'wb')
    output.setparams(data[0][0])
    for i in range(len(data)):
        output.writeframes(data[i][1])
    output.close()
    #                                                                        ARCHIVE FILE CHUNK
    print('archiving unprocessed files')
    for infile in infiles:
        old = os.path.join(UNPROCESSED, infile)
        new = os.path.join(ARCHIVE, infile)
        os.rename(old, new)

    #                                                                        RUN WHISPER
    LAN = 'English'
    MODEL = 'medium'

    # def execute(cmd):
        #     popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        #     for stdout_line in iter(popen.stdout.readline, ""):
        #         yield stdout_line
        #     popen.stdout.close()
        #     return_code = popen.wait()
        #     if return_code:
        #         raise subprocess.CalledProcessError(return_code, cmd)
        #
        # cmd = ["whisper", STAGE_FILE, "--model", MODEL, "--language", LAN]
        # for path in execute(cmd):
        #     print(path, end="")

    print('running transcription')
    tic = time.process_time()
    result = model.transcribe(STAGE_FILE)
    print('~'*30)
    
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

    print('~'*30)
    toc = time.process_time()
    print("executed in ", toc - tic)

    old_chunk = STAGE_FILE
    archive_chunk = os.path.join(ARCHIVE, f"archive_{now}.wav")
    # print('archiving chunk')
    # os.rename(old_chunk, archive_chunk)
