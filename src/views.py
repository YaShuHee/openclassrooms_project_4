#!/usr/bin/env python3
# coding: utf-8


# python standard library imports
import os
# outside libraries imports

# local imports


class View:
    @staticmethod
    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def enter_information(message: str):
        return input(message)

    @staticmethod
    def show_message(message: str):
        print(message)


class PlayerView(View):
    def enter_first_name(self):
        """"""
        return self.enter_information("\nPrénom : ")

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
        return self.enter_information("\nNom du tournoi : ")

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

    def enter_round_name(self):
        return self.enter_information("\nNom du nouveau round : ")

    def show_match(self, match):
        counter = 0
        for pair in match:
            print(f"Joueur {counter+1} : {pair[0]}")
            counter += 1

    def enter_match_result(self):
        return self.enter_information("Gagnant du match ('1' pour J1, '2' pour J2 ou '0' en cas de match nul) : ")


if __name__ == '__main__':
    pass
