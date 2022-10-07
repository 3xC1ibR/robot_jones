import os
import logging
import openai
import argparse

from pathlib import Path

TOKEN = os.getenv('OPENAI_API_KEY')
PROMPT_PATH = '/opt/projects/robot_jones/services/wordbox/gpt/prompt'

LOGDIR = '/opt/projects/.logs'
LOGSUBDIR = os.path.join(LOGDIR, __file__.replace('/opt/projects/robot_jones/', ''))
Path(LOGSUBDIR).mkdir(parents=True, exist_ok=True)
LOGFILE = os.path.join(LOGSUBDIR, f"{os.path.basename(__file__)}.log")

logging.basicConfig(
    format='[%(asctime)s] [%(filename)s:%(lineno)s :: %(funcName)s :: %(levelname)-8s] %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler(LOGFILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)

def main(prompt: str):
    logger.info(f"prompt: \n{prompt}\n")
    logger.warning(f"prompt: {prompt}")
    model="text-davinci-002"
    temp=0.6
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temp,
        max_tokens=100,
    )
    logger.debug(f"model {model}, temp: {temp}")
    logger.info(f"response: \n{response}\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='speak with the oracle')
    parser.add_argument('-p', '--prompt',required=False, type=str, help='message to send to the oracle')
    parser.add_argument('-f', '--from-file', required=False, type=bool,default=False, help='message to send to the oracle, from a file')
    args = vars(parser.parse_args())

    print(args)
    if args['from_file']:
        with open(PROMPT_PATH, 'r') as f:
            prompt = f.read()
    elif args['prompt']:
        prompt = args['prompt']

    main(prompt)
