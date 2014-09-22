import argparse

# Rate limit 60 seconds.
from collections import deque
import time
import requests
import logging

logging.basicConfig(filename='log.log', level=logging.DEBUG)
API_RATE_LIMIT = 60
HEADERS = {"content_type": "application/x-www-form-urlencoded"}
YO_URL = "https://api.justyo.co/yo/"


def parse_args():
    parser = argparse.ArgumentParser(description="spam YO users!")
    parser.add_argument("username", type=str, help="the user to be spammed : )")
    parser.add_argument("number_of_yos", type=int, help="the number of yo(s) to send")
    parser.add_argument("api_tokens", type=str, nargs="+", help="the api_tokens to be used")
    return parser.parse_args()


def calculate_sleep_between_yos(number_of_api_tokens):
    return 60 / number_of_api_tokens


def send_yo(api_token, username):
    payload = {"api_token": api_token, "username": username}
    r = requests.post(YO_URL, data=payload, headers=HEADERS)
    print r.text


def spam_yo(api_tokens, number_of_yos, username):
    time_between_yos = calculate_sleep_between_yos(len(api_tokens))
    print time_between_yos
    queue = deque(api_tokens)

    for n in range(number_of_yos):
        api_token = queue.popleft()
        logging.info("Sending message number %s with api_token %s", n, api_token)
        send_yo(api_token, username)
        queue.append(api_token)
        time.sleep(time_between_yos)


def main():
    args = parse_args()
    logging.info("Spamming: " + args.username)
    logging.info("Number of times: " + str(args.number_of_yos))
    logging.info("API tokens: " + str(args.api_tokens))
    spam_yo(args.api_tokens, args.number_of_yos, args.username)


if __name__ == "__main__":
    main()