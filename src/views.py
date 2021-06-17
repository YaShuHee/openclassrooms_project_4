#!/usr/bin/env python3
# coding: utf-8


# imports ------------------------------------------------------------------------------------------------------------
# python standard library imports
import os

# outside libraries imports
# local imports


# views classes ------------------------------------------------------------------------------------------------------
class View:
    """ A parent for Views classes. """
    @staticmethod
    def clear():
        """ A method to clear the view (here, it is the screen). """
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def enter_information(message: str):
        """ A method to get user inputs. """
        return input(message + "\n>>> ")

    @staticmethod
    def display_message(message: str):
        """ A method to display a message/information to the user. """
        print(message)


class PlayerView(View):
    """ A view for the player model. """
    def enter_first_name(self):
        """ A method to get the player first name. """
        return self.enter_information("\nPrénom : ")

    def enter_last_name(self):
        """ A method to get the player last name. """
        return self.enter_information("Nom de famille : ")

    def enter_birth_date(self):
        """ A method to get the player birth date. """
        return self.enter_information("Date de naissance (format jj/mm/aaaa) : ")

    def enter_gender(self):
        """ A method to get the player gender. """
        return self.enter_information("Genre ('H' pour homme, 'F' pour femme et 'A' pour autre) : ")

    def enter_rank(self):
        """ A method to get the player rank. """
        return self.enter_information("Classement : ")

    @staticmethod
    def list_players(players, show_index: bool = False):
        """ A method to display a list of players. """
        if show_index:
            index = 1
            for player in players:
                print(f" {index} - {player.first_name} {player.last_name} ({player.birth_date}), {player.rank}e")
                index += 1
        else:
            for player in players:
                print(f"{player.first_name} {player.last_name} ({player.birth_date}), {player.rank}e")


class TournamentView(View):
    """ A view for the tournament model. """
    def enter_name(self):
        """ A method to get the tournament name. """
        return self.enter_information("\nNom du tournoi : ")

    def enter_place(self):
        """ A method to get the tournament location. """
        return self.enter_information("Lieu du tournoi : ")

    def enter_beginning_date(self):
        """ A method to get the tournament beginning date. """
        return self.enter_information("Date de début du tournoi (format jj/mm/aaaa) :")

    def enter_ending_date(self):
        """ A method to get the tournament ending date. """
        return self.enter_information(
            "Date de fin du tournoi "
            "(laisser vide si le tournoi se déroule seulement sur un jour) : "
        )

    def enter_time_control(self):
        """ A method to get the tournament time control. """
        return self.enter_information("Gestion du temps ('blitz', 'bullet' ou 'coup rapide') : ")

    def enter_number_of_rounds(self):
        """ A method to get the tournament number of rounds. """
        return self.enter_information("Nombre de round (4 par défaut) : ")

    def enter_number_of_players(self):
        """ A method to get the tournament number of players. """
        return self.enter_information("Nombre de round (8 par défaut) : ")

    def enter_description(self):
        """ A method to get the tournament description. """
        return self.enter_information("Description et commentaires sur le tournoi : ")

    def enter_round_name(self):
        """ A method to get a tournament round name. """
        return self.enter_information("\nNom du nouveau round : ")

    def show_match(self, match):
        """ A method to display a match. """
        counter = 0
        for pair in match:
            print(f"Joueur {counter+1} : {pair[0]}")
            counter += 1

    def enter_match_result(self):
        """ A method to get a match result. """
        return self.enter_information("Gagnant du match ('1' pour J1, '2' pour J2 ou '0' en cas de match nul) : ")

    @staticmethod
    def list_tournaments(tournaments, show_index: bool = False):
        """ A method to display a list of tournaments. """
        if show_index:
            index = 1
            for tournament in tournaments:
                print(f" {index} - {tournament.name}, {tournament.place} "
                      f"({tournament.beginning_date} - {tournament.ending_date})")
                index += 1
        else:
            for tournament in tournaments:
                print(f"{tournament.name}, {tournament.place} "
                      f"({tournament.beginning_date} - {tournament.ending_date})")


# execution ----------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    pass
