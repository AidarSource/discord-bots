# do manipulation with cfg of bot
from json import dumps, loads


def get_data():
    with open('channels.json', 'r') as file:
        return loads(file.read())


def set_data(chan):
    with open('channels.json', 'w') as file:
        file.write(dumps(chan, indent=2))


def get_block():
    with open('blocked.json', 'r') as file:
        return loads(file.read())


def set_block(chan):
    with open('blocked.json', 'w') as file:
        file.write(dumps(chan, indent=2))


def get_exception():
    with open('exception_words.json', 'r') as file:
        return loads(file.read())


def set_exception(chan):
    with open('exception_words.json', 'w') as file:
        file.write(dumps(chan, indent=2))
