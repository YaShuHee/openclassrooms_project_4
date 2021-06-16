#!/usr/bin/env python3
# coding: utf-8


# python standard library imports


# outside libraries imports


# local imports
from views import PlayerView, TournamentView
from controllers import UnstoppableTournamentController


if __name__ == '__main__':
    player_view = PlayerView()
    tournament_view = TournamentView()
    controller = UnstoppableTournamentController(player_view, tournament_view)
    controller.run()
