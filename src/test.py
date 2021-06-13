#!/usr/bin/env python3
# coding: utf-8


"""
This file is used to test the project code.
"""


# python standard library imports
from datetime import date
from sys import modules
from inspect import isfunction


# outside libraries imports


# local imports
from models import Player
from controllers import UnstoppableTournamentController


# Class to implement tests -------------------------------------------------------------------------------------------
class PassTestView:
    """A class used to test interfaces bypassing users input. """
    def __init__(self):
        for method, return_ in {
            "first_name": "TiMoThé",
            "last_name": "  GélibeRt ",
            "birth_date": "09 07 1996",
            "gender": "homMe",
            "rank": "42",
        }.items():
            setattr(self, f"enter_{method}", lambda r=return_: r)


# Models testing functions -------------------------------------------------------------------------------------------
def test_player_get_information():
    """ A function to test if Player model returns information the way it is supposed to. """
    given_kwargs = {
        "first_name": "Timothé",
        "last_name": "Gélibert",
        "birth_date": date(year=1996, month=7, day=9),
        "gender": "Homme",
        "rank": 42,
    }
    expected_result = {
        "first_name": "Timothé",
        "last_name": "Gélibert",
        "birth_date": date(year=1996, month=7, day=9),
        "gender": "Homme",
        "rank": 42,
    }
    test_player = Player(**given_kwargs)
    test_results = test_player.get_information()
    return test_results == expected_result


# Controllers testing functions --------------------------------------------------------------------------------------
def test_controller_add_a_new_player():
    expected_result = {
        "first_name": "Timothé",
        "last_name": "Gélibert",
        "birth_date": date(year=1996, month=7, day=9),
        "gender": "Homme",
        "rank": 42,
    }
    view = PassTestView()
    controller = UnstoppableTournamentController(view)
    controller.add_a_new_player()
    return controller.players[0].get_information() == expected_result


# Views testing functions --------------------------------------------------------------------------------------------


# Tests execution ----------------------------------------------------------------------------------------------------
def run_tests(strings_to_test: list):
    """ A function seeking and calling every function in this file which name starts with 'test_'. """
    passed_tests = 0
    number_of_tests = 0

    for string in strings_to_test:
        test = getattr(modules['__main__'], string)
        if isfunction(test):
            number_of_tests += 1
            if test():
                passed_tests += 1
                print(f"[✔] {test.__name__} : PASSED.")
            else:
                print(f"[✘] {test.__name__} : FAILED.")
    print(f"-------------------\nPASSED TESTS: {passed_tests}\nFAILED TESTS: {number_of_tests-passed_tests}")


if __name__ == '__main__':
    run_tests((string for string in dir() if string.startswith("test_")))
