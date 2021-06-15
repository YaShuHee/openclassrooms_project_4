#!/usr/bin/env python3
# coding: utf-8


# python standard library imports
import os


# outside libraries imports


# local imports
from models import Match


class View:
    @staticmethod
    def clear_view():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def enter_information(self, message: str):
        return input(message)


class PlayerView(View):
    def enter_first_name(self):
        """"""
        return self.enter_information("Prénom : ")

    def enter_last_name(self):
        """"""
        return self.enter_information("Nom de famille : ")

    def enter_birth_date(self):
        """"""
        return self.enter_information("Date de naissance (format <jj> <mm> <aaaa>) : ")

    def enter_gender(self):
        """"""
        return self.enter_information("Genre ('homme', 'femme' ou 'autre') : ")

    def enter_rank(self):
        return self.enter_information("Classement : ")


class TournamentView(View):
    def enter_name(self):
        return self.enter_information("Nom du tournoi : ")

    def enter_place(self):
        return self.enter_information("Lieu du tournoi : ")

    def enter_beginning_date(self):
        return self.enter_information("Date de début du tournoi :")

    def enter_ending_date(self):
        return self.enter_information(
            "Date de fin du tournoi"
            "(laisser vide si le tournoi se déroule seulement sur un jour) : "
        )

    def enter_time_control(self):
        return self.enter_information("Gestion du temps ('blitz', 'bullet' ou 'coup rapide') : ")

    def enter_number_of_rounds(self):
        return self.enter_information("Nombre de round (4 par défaut) : ")

    def enter_description(self):
        return self.enter_information("Description et commentaires sur le tournoi : ")


class UnstoppableTournamentAdminView:
    def enter_player_player_information(self, number_of_players: int = 8):
        players = [self.enter_player_a_player_information() for n in range(self.number_of_players)]
        return players

    def enter_player_a_player_information(self):
        pass

    def enter_player_tournament_informations(self):
        pass

    def enter_player_match_scores(self, match: Match):
        pass


if __name__ == '__main__':
    pass
