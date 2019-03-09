import logging
import os.path
from util import Bot

TOKEN_PATH = 'token'


def main():
    if not os.path.isfile(TOKEN_PATH):
        with open(TOKEN_PATH, "w"):
            pass
    with open(TOKEN_PATH, "r") as token_file:
        token = token_file.readline().strip()
        if not token:
            print(f"Please, put token into the '{TOKEN_PATH}' file")
            return

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s '
                               '- %(levelname)s - %(message)s')

    bot = Bot(token,
              request_kwargs={'proxy_url': 'https://66.82.123.234:8080/',
                              'urllib3_proxy_kwargs': {}})
    bot.idle()


if __name__ == '__main__':
    main()
