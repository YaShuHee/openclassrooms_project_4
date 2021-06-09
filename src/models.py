#!/usr/bin/env python3
# coding: utf-8


from datetime import date, datetime
from typing import List


class Player:
    """ The model used to stock players information. """
    def __init__(
            self,
            first_name: str,
            last_name: str,
            birth_date: date,
            gender: str,
            rank: int,
    ):
        """ The Player class constructor. """
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.gender = gender
        self.rank = rank
        self.score = 0

    def get_information(self):
        """ Return a player information as a dict. """
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date,
            "gender": self.gender,
            "rank": self.rank,
        }


class Match:
    """ The model used to stock matches information. """
    def __init__(
            self,
            player_1,
            player_2,
    ):
        """ The match class constructor. """
        self.player_1 = player_1
        self.player_2 = player_2
        self.score_of_player_1 = 0
        self.score_of_player_2 = 0


class Round:
    """ The model used to stock rounds information. """
    def __init__(
            self,
            name: str,
            matches: List[Match],
    ):
        """ The round class constructor. """
        self.name = name
        self.matches = matches
        self.beginning_time = datetime.now()
        self.ending_time = None

    def close(self):
        """ The method used to finish a round, auto-report the ending time."""
        self.ending_time = datetime.now()


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
            ending_date: date = None,
    ):
        """ The tournament constructor. """
        self.name = name
        self.place = place
        self.beginning_date = beginning_date
        self.time_control = time_control
        self.description = description
        self.active_round = 0
        self.number_of_rounds = number_of_rounds
        if ending_date is None:
            self.ending_date = beginning_date
        else:
            self.ending_date = ending_date


if __name__ == '__main__':
    pass
