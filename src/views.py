#!/usr/bin/env python3
# coding: utf-8


from models import Match


class UnstoppableTournamentAdminView:
    def add_players(self, number_of_players: int = 8):
        players = [self.add_players() for n in range(self.number_of_players)]
        return players

    def add_a_player(self):
        pass

    def add_tournament_informations(self):
        pass

    def add_match_scores(self, match: Match):
        pass


if __name__ == '__main__':
    pass
