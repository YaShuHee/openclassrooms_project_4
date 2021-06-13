#!/usr/bin/env python3
# coding: utf-8


# python standard library imports
from re import split as re_split
from datetime import date


# outside libraries imports


# local imports
# from models import Tournament, Round, Match
from models import Player


class UnstoppableTournamentController:
    """ A controller for a basic unstoppable 4 round tournament. """

    def __init__(self, view):
        self.view = view
        self.players = []
        self.tournament = None

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
        # generate pairs

    def get_round_scores(self):
        pass

    def add_a_new_player(self):
        player = {
            "first_name": None,
            "last_name": None,
            "birth_date": None,
            "gender": None,
            "rank": None,
        }
        for data in player:
            while player[data] is None:
                player[data] = self.__getattribute__(f"get_{data}")()
        self.players.append(Player(**player))

    @staticmethod
    def _name_is_valid(name):
        """ Check if a string only contains alphabetic caracters, <->, <'> or <space> symbols. """
        return name.replace(" ", "").replace("-", "").replace("'", "").isalpha()

    @staticmethod
    def _format_name(name_to_format):
        """ """
        name = ""
        split_name = re_split(r"([\-]+|[ ]+|[']+)", name_to_format)
        for word in split_name:
            if word == "":
                pass
            elif word.isalpha():
                name += word.capitalize()
            else:
                name += word[0]
        while name.startswith((" ", "-", "'")):
            name = name[1:]
        while name.endswith((" ", "-", "'")):
            name = name[0:-1]
        return name

    def _treat_name(self, name):
        if self._name_is_valid(name):
            return self._format_name(name)
        else:
            return None

    def get_first_name(self):
        name = self.view.enter_first_name()
        return self._treat_name(name)

    def get_last_name(self):
        name = self.view.enter_last_name()
        return self._treat_name(name)

    @staticmethod
    def _format_date(date_: str):
        split_date = date_.split(" ")
        return (int(time_measure) for time_measure in reversed(split_date))

    def get_birth_date(self):
        birth_date_str = self.view.enter_birth_date()
        if birth_date_str.replace(" ", "").isdecimal():
            birth_date_tuple = self._format_date(birth_date_str)
            try:
                birth_date = date(*birth_date_tuple)
            except ValueError:  # raised when the date doesn't exist
                birth_date = None
            except TypeError:    # raised when an argument is missing (1-2 number(s) instead of 3)
                birth_date = None
        else:
            birth_date = None
        return birth_date

    def get_gender(self):
        gender = self.view.enter_gender().capitalize()
        if gender in ("Homme", "Femme", "Autre"):
            return gender
        else:
            return None

    def get_rank(self):
        rank = self.view.enter_rank()
        if rank.isdecimal():
            return int(rank)
        else:
            return None


if __name__ == '__main__':
    pass
