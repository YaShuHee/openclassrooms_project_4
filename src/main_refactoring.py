#!/usr/bin/env python3
# coding: utf-8


# python standard library imports

# outside libraries imports
from tinydb import TinyDB

# local imports
from views import PlayerView, TournamentView
from controllers import SaveController, MenuController


if __name__ == '__main__':
    db = TinyDB("database/db.json")
    saver = SaveController(db)
    players = saver.load_players()
    tournaments = saver.load_tournaments()
    MenuController(players, tournaments).run()
