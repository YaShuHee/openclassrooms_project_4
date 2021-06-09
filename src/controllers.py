#!/usr/bin/env python3
# coding: utf-8


# from models import Tournament, Round, Match
from models import Tournament


class UnstoppableTournamentController:
    """ A controller for a basic unstoppable 4 round tournament. """
    def __init__(self, view):
        self.view = view
        self.players = [*self.view.add_players()]
        self.tournament = Tournament(**self.view.add_tournament_informations())

    def run(self):
        while self.tournament.active_round < self.tournament.number_of_rounds:
            self.generate_new_round()
            self.get_round_scores()
            self.tournament.active_round += 1

    def generate_new_round(self):
        if self.tournament.active_round == 0:
            sorted_players = self.players.sort(key=lambda p: p.rank)
        else:
            sorted_players = self.players.sort(key=lambda p: p.score)
        print(sorted_players)
        # generate paires

    def get_round_scores(self):
        pass


if __name__ == '__main__':
    pass
