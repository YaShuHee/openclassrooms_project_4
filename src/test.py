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
# from views import UnstoppableTournamentAdminView
# from controllers import UnstoppableTournamentController
# from models import Player, Tournament, Round, Match
from models import Player


# Models testing functions -------------------------------------------------------------------------------------------
def test_player_method_get_information():
    """ A function to test if Player model returns information the way it is supposed to. """
    given_kwargs = {
        "first_name": "Timothé",
        "last_name": "Gélibert",
        "birth_date": date(year=1996, month=7, day=9),
        "gender": "homme",
        "rank": 42,
    }
    expected_result = {
        "first_name": "Timothé",
        "last_name": "Gélibert",
        "birth_date": date(year=1996, month=7, day=9),
        "gender": "homme",
        "rank": 42,
    }
    test_player = Player(**given_kwargs)
    test_results = test_player.get_informations()
    return test_results == expected_result


# Models testing functions -------------------------------------------------------------------------------------------


# Models testing functions -------------------------------------------------------------------------------------------


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
