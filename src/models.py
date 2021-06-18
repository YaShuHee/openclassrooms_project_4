#!/usr/bin/env python3
# coding: utf-8


# python standard library imports
from datetime import date, datetime
from typing import List


# outside libraries imports
# local imports


class Player:
    uid = 0
    """ The model used to stock players information. """

    def __init__(
            self,
            first_name: str,
            last_name: str,
            birth_date: date,
            gender: str,
            rank: int,
            uid=None,
    ):
        """ The Player class initiator. """
        self.first_name = first_name
        self.last_name = last_name
        if type(birth_date) in (tuple, list):
            birth_date = date(*birth_date)
        self.birth_date = birth_date
        self.gender = gender
        self.rank = rank
        self.score = 0
        if uid is not None:
            self.uid = uid
        else:
            self.uid = Player.uid
        Player.uid += 1

    def __repr__(self):
        """ Repr overloading. """
        return f"{self.first_name} {self.last_name}, {self.rank}e"


class Match(tuple):
    """ The model used to stock matches information. """

    def __new__(cls, player_1, player_2, score_1: int = 0, score_2: int = 0):
        """ The Match class constructor. """
        return super(Match, cls).__new__(cls, tuple([[player_1, score_1], [player_2, score_2]]))

    def __repr__(self):
        """ __repr__ overloading. """
        return f"< {self.p1.first_name} {self.p1.last_name} : {self.s1}pt\t"\
               f"---<VS>---\t{self.p2.first_name} {self.p2.last_name} : {self.s2}pt >"

    @property
    def p1(self):
        """ Return the player 1 instance. """
        return self[0][0]

    @property
    def p2(self):
        """ Return the player 2 instance. """
        return self[1][0]

    @property
    def s1(self):
        """ Return the player 1 score. """
        return self[0][1]

    @property
    def s2(self):
        """ Return the player 2 score. """
        return self[1][1]


class Round:
    """ The model used to stock rounds information. """

    def __init__(
            self,
            name: str,
            matches: List[Match],
            beginning_time=None,
            ending_time=None,

    ):
        """ The round class initiator. """
        self.name = name
        self.matches = matches
        if beginning_time is not None:
            self.beginning_time = beginning_time
        else:
            self.beginning_time = datetime.now()
        self.ending_time = ending_time

    def close(self):
        """ The method used to finish a round, auto-report the ending time."""
        self.ending_time = datetime.now()

    def __repr__(self):
        """ Repr overloading. """
        string = f"{self.name} :\n{'-' * (len(self.name) + 2)}"
        for match in self.matches:
            string += f"\n {match.__repr__()}"
        return string


class Tournament:
    """ The model used to stock tournament information. """

    def __init__(
            self,
            name: str,
            place: str,
            beginning_date: date,
            time_control: str,
            description: str,
            number_of_rounds: int = 4,
            number_of_players: int = 8,
            players=[],
            ending_date: date = None,
            rounds=[],
    ):
        """ The tournament initiator. """
        self.name = name
        self.place = place
        self.beginning_date = beginning_date
        self.time_control = time_control
        self.description = description
        self.number_of_rounds = number_of_rounds
        self.number_of_players = number_of_players
        self.active_round = 0
        # if loading saved object
        self.rounds = rounds
        self.players = players
        if ending_date is None:
            self.ending_date = beginning_date
        else:
            self.ending_date = ending_date

    def __repr__(self):
        """ Repr overloading. """
        return f"{self.name}, {self.place}, {self.beginning_date} - {self.ending_date}"


# execution ----------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    pass
