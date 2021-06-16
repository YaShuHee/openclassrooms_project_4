#!/usr/bin/env python3
# coding: utf-8


# python standard library imports

# outside libraries imports
from tinydb import TinyDB

# local imports
from controllers import MainController


if __name__ == '__main__':
    db = TinyDB("db.json")
    controller = MainController(db)

    running = True
    while running:
        running = controller.run()
