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

    def serialized(self):
        """ Return a serialized version of the object. """
        b = self.birth_date
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": (b.year, b.month, b.day),
            "gender": self.gender,
            "rank": self.rank,
            "id_": self.id_,
        }

    def __repr__(self):
        """ Repr overloading. """
        return f"{self.first_name} {self.last_name}, {self.rank}e"


class Match(tuple):
    """ The model used to stock matches information. """
    def __new__(cls, player_1, player_2):
        """ The Match class constructor. """
        if type(player_1) is list:
            player_1, score_1 = player_1
            player_2, score_2 = player_2
            return super(Match, cls).__new__(
                cls,
                tuple([[Player(**player_1), score_1], [Player(**player_2), score_2]])
            )
        else:
            return super(Match, cls).__new__(cls, tuple([[player_1, 0], [player_2, 0]]))

    def serialized(self):
        """ Return a serialized version of the object. """
        return [self[0][0].serialized(), self[0][1]], [self[1][0].serialized(), self[1][1]]

    def __repr__(self):
        """ Repr overloading. """
        return f"{self[0][0].__repr__()} (score: {self[0][1].__repr__()})\t\t" +\
            f"<VS>\t\t{self[1][0].__repr__()} (score: {self[1][1].__repr__()})"


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

    def serialized(self):
        """ Return a serialized version of the object. """
        b = self.beginning_time
        e = self.ending_time
        return {
            "name": self.name,
            "matches": [match.serialized() for match in self.matches],
            "beginning_time": (b.year, b.month, b.day, b.hour, b.minute),
            "ending_time": (e.year, e.month, e.day, e.hour, e.minute),
        }

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
        if rounds:
            self.rounds = [Round(**kwargs) for kwargs in rounds]
        else:
            self.rounds = []
        self.players = players
        if ending_date is None:
            self.ending_date = beginning_date
        else:
            self.ending_date = ending_date

    def __repr__(self):
        """ Repr overloading. """
        return f"{self.name}, {self.place}, {self.beginning_date} - {self.ending_date}"

    def serialized(self):
        """ Return a serialized version of the object. """
        b = self.beginning_date
        e = self.ending_date
        return {
            "name": self.name,
            "place": self.place,
            "beginning_date":  (b.year, b.month, b.day),
            "ending_date":  (e.year, e.month, e.day),
            "time_control": self.time_control,
            "description": self.description,
            "number_of_rounds": self.number_of_rounds,
            "number_of_players": self.number_of_players,
            "players": self.players,
            "rounds": [round_.serialized() for round_ in self.rounds],
        }


# execution ----------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    pass
