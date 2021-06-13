#!/usr/bin/env python3
# coding: utf-8


# python standard library imports


# outside libraries imports


# local imports
from models import Match


class PlayerInformationView:
    @staticmethod
    def enter_first_name():
        """"""
        return input("Prénom :")

    @staticmethod
    def enter_last_name():
        """"""
        return input("Nom de famille :")

    @staticmethod
    def enter_birth_date():
        """"""
        return input("Date de naissance (format <jj> <mm> <aaaa>) :")

    @staticmethod
    def enter_gender():
        """"""
        return input("Genre ('homme', 'femme' ou 'autre') :")

    @staticmethod
    def enter_rank():
        return input("Classement :")


class UnstoppableTournamentAdminView:
    def enter_player_information(self, number_of_players: int = 8):
        players = [self.enter_a_player_information() for n in range(self.number_of_players)]
        return players

    def enter_a_player_information(self):
        pass

    def enter_tournament_informations(self):
        pass

    def enter_match_scores(self, match: Match):
        pass


if __name__ == '__main__':
    pass
