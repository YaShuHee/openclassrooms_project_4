#!/usr/bin/env python3
# coding: utf-8


# imports ------------------------------------------------------------------------------------------------------------
# python standard library imports
import re
from datetime import date

# outside libraries imports
from tinydb import TinyDB

# local imports
from models import Player, Tournament, Round, Match
from views import View, PlayerView, TournamentView


# controllers classes -------------------------------------------------------------------------------------------------
class BasicCreator:
    """ A basic class to control Player and Tournament creation. """
    def __init__(self, view: View):
        """ The class initiatior. It just needs a View. """
        self.view = view

    def run(self, cls, kwargs: dict, default_values: bool = False):
        """ The main method which needs to be called to execute a Player/Tournament creation.
        It calls self.view.get_<attribute>() for each given attribute in kwargs attribute, while the returned value
        is None. If the return of this call is False, then the attribute will take a default value. """
        for data in kwargs:
            while kwargs[data] is None:
                kwargs[data] = self.__getattribute__(f"get_{data}")()
        # delete 'key: False' items, so they take default value when given to Player/Tournament initiator
        kwargs = {key: value for key, value in kwargs.items() if value is not False}
        return cls(**kwargs)

    @staticmethod
    def _french_date_string_to_python_date(date_str: str):
        """ A method to control and transform a french date string "jj/mm/aaaa" into a python date object. """
        if re.match(r"\d{2}/\d{2}/\d{4}", date_str):
            try:
                treated_date = date(*(int(time_unit) for time_unit in reversed(date_str.split("/"))))
            except (ValueError, TypeError):
                treated_date = None
        else:
            treated_date = None
        return treated_date


class TournamentCreator(BasicCreator):
    """ A class to create Tournament objects. To create a Tournament instance, you must call the 'run' method. """
    def __init__(self, view: TournamentView):
        """ The class initiatior. It just needs a TournamentView. """
        super().__init__(view)

    def run(self):
        """" Return a Tournament instance (without players). """
        tournament_kwargs = {
            "name": None,
            "place": None,
            "beginning_date": None,
            "ending_date": None,
            "time_control": None,
            "description": None,
            "number_of_rounds": None,
            "number_of_players": None,
        }
        return super().run(Tournament, tournament_kwargs)

    def get_name(self):
        """ A method to control a tournament name entry. """
        name = self.view.enter_name()
        if name == "":
            return None
        else:
            return name
        return name

    def get_place(self):
        """ A method to control a tournament place entry. """
        place = self.view.enter_place()
        if place == "":
            return None
        else:
            return place

    def get_beginning_date(self):
        """ A method to control a tournament beginning date entry. """
        beginning_date = self.view.enter_beginning_date()
        return self._french_date_string_to_python_date(beginning_date)

    def get_ending_date(self):
        """ A method to control a tournament ending date entry. """
        ending_date = self.view.enter_ending_date()
        if ending_date == "":
            return False
        else:
            return self._french_date_string_to_python_date(ending_date)

    def get_time_control(self):
        """ A method to control a tournament time control entry. """
        time_control = self.view.enter_time_control().capitalize()
        if time_control in ("Bullet", "Blitz", "Coup rapide"):
            return time_control
        else:
            return None

    def get_number_of_rounds(self):
        """ A method to control a tournament number of round entry. """
        number_of_rounds = self.view.enter_number_of_rounds()
        if number_of_rounds == "":
            return 4
        elif number_of_rounds.isdecimal():
            return int(number_of_rounds)
        else:
            return None

    def get_number_of_players(self):
        """ A method to control a tournament number of players entry. """
        number_of_players = self.view.enter_number_of_players()
        if number_of_players == "":
            return 8
        elif number_of_players.isdecimal():
            return int(number_of_players)
        else:
            return None

    def get_description(self):
        """ A method to control a tournament description entry. """
        description = self.view.enter_description()
        return description


class PlayerCreator(BasicCreator):
    """ A class to create Player objects. To create a Player instance, you must call the 'run' method. """
    id_ = 1

    def __init__(self, view: PlayerView):
        """ The class initiatior. It just needs a PlayerView. """
        super().__init__(view)

    def run(self):
        """" Return a Player instance. """
        player_kwargs = {
            "first_name": None,
            "last_name": None,
            "birth_date": None,
            "gender": None,
            "rank": None,
            "id_": Player.id_,
        }
        Player.id_ += 1
        return super().run(Player, player_kwargs)

    @staticmethod
    def _name_is_valid(name):
        """ Check if a string only contains alphabetic caracters, <->, <'> or <space> symbols. """
        return name.replace(" ", "").replace("-", "").replace("'", "").isalpha()

    @staticmethod
    def _format_name(name_to_format):
        """ A method to control and format a player name entry. """
        name = ""
        split_name = re.split(r"([\-]+|[ ]+|[']+)", name_to_format)
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
        """ A method to coordinate several controls on a name entry. """
        if self._name_is_valid(name):
            return self._format_name(name)
        else:
            return None

    def get_first_name(self):
        """ A method to control a player first name entry. """
        name = self.view.enter_first_name()
        return self._treat_name(name)

    def get_last_name(self):
        """ A method to control a player last name entry. """
        name = self.view.enter_last_name()
        return self._treat_name(name)

    def get_birth_date(self):
        """ A method to control a player birth date. """
        birth_date = self.view.enter_birth_date()
        return self._french_date_string_to_python_date(birth_date)

    def get_gender(self):
        """ A method to control a player gender. """
        gender = self.view.enter_gender().upper()
        if gender in ("H", "F", "A"):
            return {"H": "Homme", "F": "Femme", "A": "Autre"}[gender]
        else:
            return None

    def get_rank(self):
        """ A method to control a player rank. """
        rank = self.view.enter_rank()
        if rank.isdecimal() and rank != "0":
            return int(rank)
        else:
            return None


class TournamentRunner:
    def __init__(self, view: View, tournament: Tournament, player_creator: PlayerCreator, known_players: list):
        self.view = view
        self.tournament = tournament
        self.player_creator = player_creator
        self.known_players = known_players

    def run(self):
        # add players
        self.add_players()
        # run the tournament with added players
        self._run()

    def add_players(self):
        while len(self.tournament.players) < self.tournament.number_of_players:
            number_of_players = len(self.tournament.players)
            self.view.display_message(f"Votre tournoi compte actuellement {number_of_players} joueur"
                                      f"{'s' * (number_of_players > 1)} sur {self.tournament.number_of_players}.")
            answer = ""
            while answer not in ("1", "2", "/list"):
                answer = self.view.enter_information(
                    "Voulez-vous :"
                    "\n 1 - Ajouter un joueur (tapez '/list' pour voir les joueurs) ?"
                    "\n 2 - Créer un nouveau joueur ?"
                ).lower()
            if answer == "1" and number_of_players != 0:
                player = self.select_a_known_player()
                if player in self.tournament.players:
                    self.view.display_message("Ce joueur est déjà dans le tournoi !")
                else:
                    self.tournament.players.append(player)
            elif answer == "2":
                new_player = self.player_creator.run()
                self.known_players.append(new_player)
                self.tournament.players.append(new_player)
            elif answer == "/list":
                self.player_creator.view.list_players(self.known_players)

    def select_a_known_player(self):
        number_of_players = len(self.known_players)
        player_range = ""
        while not(player_range.isdecimal() and player_range != "0" and int(player_range) <= number_of_players):
            self.player_creator.view.list_players(self.known_players, show_index=True)
            player_range = self.view.enter_information(f"Sélectionner le joueur que vous voulez ajouter "
                                                       f"(1-{number_of_players})")
        return self.known_players[int(player_range) - 1]

    def _run(self):
        print("run tournament with :")
        for player in self.tournament.players:
            print(player)


class MainController:
    def __init__(self):
        # attributes
        self.players = []
        self.tournaments = []
        # views initialisation
        self.view = View()
        self.player_view = PlayerView()
        self.tournament_view = TournamentView()
        # creation controller initialisation
        self.player_creator = PlayerCreator(self.player_view)
        self.tournament_creator = TournamentCreator(self.tournament_view)

    def run(self):
        """ A method to execute the controller and its menu. """
        running = True
        while running:
            action = self.tournament_view.enter_information(
                "\n--------------------------------------------------------"
                "\nVoulez-vous :"
                "\n 1 - Ajouter un joueur à la base de données ?"
                "\n 2 - Créer, exécuter et sauvegarder un tournoi ?"
                "\n 3 - Consulter la liste des joueurs ou des tournois ?"
                "\n 4 - Modifier le classement d'un joueur ?"
                "\n 5 - Quitter."
                "\n"
            )

            if action == "1":
                self.players.append(self.player_creator.run())
                self.save_players()

            elif action == "2":
                self.tournaments.append(self.tournament_creator.run())
                TournamentRunner(self.view, self.tournaments[-1], self.player_creator, self.players).run()
                self.save_players()
                self.save_tournaments()
                running = True

            elif action == "3":
                self.reports()
                running = True

            elif action == "4":
                self.modify_rank()
                self.save_players()
                running = True

            elif action == "5":
                running = False

            else:
                running = True

    def save_players(self):
        print("Save players")

    def save_tournaments(self):
        print("Save tournaments")

    def load_players(self):
        print("Load players")

    def load_tournaments(self):
        print("Load tournaments")

    def reports(self):
        """ A method to execute the reports. """
        self.view.clear()
        action = self.view.enter_information(
            "Voulez-vous consulter la liste de :"
            "\n 1 - Tous les joueurs, triés par nom ?"
            "\n 2 - Tous les joueurs, triés par classement ?"
            "\n 3 - Les joueurs d'un tournoi, triés par nom ?"
            "\n 4 - Les joueurs d'un tournoi, triés par classement ?"
            "\n 5 - Les tournois ?"
            "\n 6 - Les tours d'un tournoi ?"
            "\n 7 - Les matchs d'un tournoi ?"
            "\n"
        )
        self.view.clear()
        if action == "1":
            "Liste des joueurs, triés par nom :"
            self.player_view.list_players(sorted(self.players, key=lambda p: p.first_name))
        elif action == "2":
            "Liste des joueurs, triés par classement :"
            self.player_view.list_players(sorted(self.players, key=lambda p: p.rank))
        elif action == "3":
            pass
        elif action == "4":
            pass
        elif action == "5":
            pass
        elif action == "6":
            pass
        elif action == "7":
            pass


# OLD IMPLEMENTATION #################################################################################################
class OldUnstoppableTournamentController:
    """ A controller for a basic unstoppable 4 round tournament. """
    def __init__(self, player_view, tournament_view, players=[], number_of_players: int = 8):
        self.player_view = player_view
        self.tournament_view = tournament_view
        self.tournament = None
        self.known_players = players
        self.players = players
        self.number_of_players = number_of_players

    def run(self):
        """ A method to execute the tournament. """
        self.tournament = self.create_tournament()
        while len(self.players) < self.number_of_players:
            self.players.append(self.add_new_player())
        while self.tournament.active_round < self.tournament.number_of_rounds:
            self.update_scores()
            self.generate_new_round()
            self.get_round_scores()
            self.tournament.active_round += 1

    def update_scores(self):
        """ A method to enter and control scores. """
        for player in self.players:
            player.score = 0
        for round_ in self.tournament.rounds:
            for match in round_.matches:
                for pair in match:
                    pair[0].score += pair[1]
                    if int(pair[0].score) == pair[0].score:
                        pair[0].score = int(pair[0].score)
        if len(self.tournament.rounds) != 0:
            message = f"\nScores après {self.tournament.rounds[-1].name}"
            for player in reversed(sorted(self.players, key=lambda p: p.score)):
                message += f"\n {player} -> score: {player.score} "
            self.tournament_view.show_message(message)

    def generate_new_round(self):
        """ A method to generate a new round. """
        round_name = self.get_round_name()
        if self.tournament.active_round == 0:
            sorted_players_iterator = iter(sorted(self.players, key=lambda p: p.rank))
        else:
            # TODO : sort players by rank when they have the same score
            # TODO : avoid playing several times against the same player
            sorted_players_iterator = iter(sorted(self.players, key=lambda p: p.score, reverse=True))
        matches = [Match(player, next(sorted_players_iterator)) for player in sorted_players_iterator]
        self.tournament.rounds.append(Round(round_name, matches))

    def get_round_name(self):
        """ A method to control a round name. """
        name = self.tournament_view.enter_round_name()
        if name == "":
            return "Round " + str(self.tournament.active_round + 1)
        else:
            return name

    def get_round_scores(self):
        """ A method to control a round scores. """
        for match in self.tournament.rounds[-1].matches:
            self.tournament_view.show_match(match)
            match_winner_range = ""
            while match_winner_range not in ("0", "1", "2"):
                match_winner_range = self.tournament_view.enter_match_result()
            if match_winner_range == "0":
                match[0][1] = 0.5
                match[1][1] = 0.5
            else:
                match[int(match_winner_range) - 1][1] = 1
        self.tournament.rounds[-1].close()

    def create_tournament(self):
        """ A method to return a tournament object. """
        tournament = {
            "name": None,
            "place": None,
            "beginning_date": None,
            "ending_date": None,
            "time_control": None,
            "number_of_rounds": None,
            "description": None,
        }
        for data in tournament:
            while tournament[data] is None:
                tournament[data] = self.__getattribute__(f"get_tournament_{data}")()
            # if data == False, the default value will be used by 'Tournament' class
        tournament = {key: value for key, value in tournament.items() if value is not False}
        return Tournament(**tournament)

    @staticmethod
    def _treat_french_date_string(date_str: str):
        """ A method to check a date entry and to format it. """
        try:
            treated_date = date(*(int(time_unit) for time_unit in reversed(date_str.split("/"))))
        except (ValueError, TypeError):
            treated_date = None
        return treated_date

    def get_tournament_name(self):
        """ A method to control a tournament name entry. """
        name = self.tournament_view.enter_name()
        return name

    def get_tournament_place(self):
        """ A method to control a tournament place entry. """
        place = self.tournament_view.enter_place()
        return place

    def get_tournament_beginning_date(self):
        """ A method to control a tournament beginning date entry. """
        beginning_date = self.tournament_view.enter_beginning_date()
        return self._treat_french_date_string(beginning_date)

    def get_tournament_ending_date(self):
        """ A method to control a tournament ending date entry. """
        ending_date = self.tournament_view.enter_ending_date()
        if ending_date == "":
            return False
        else:
            return self._treat_french_date_string(ending_date)

    def get_tournament_time_control(self):
        """ A method to control a tournament time control entry. """
        time_control = self.tournament_view.enter_time_control().capitalize()
        if time_control in ("Bullet", "Blitz", "Coup rapide"):
            return time_control
        else:
            return None

    def get_tournament_number_of_rounds(self):
        """ A method to control a tournament number of round entry. """
        number_of_rounds = self.tournament_view.enter_number_of_rounds()
        if number_of_rounds == "":
            return 4
        elif number_of_rounds.isdecimal():
            return int(number_of_rounds)
        else:
            return None

    def get_tournament_description(self):
        """ A method to control a tournament description entry. """
        description = self.tournament_view.enter_description()
        return description

    def add_new_player(self):
        """ A method to add a player to a tournament (the player may already exist). """
        action = self.tournament_view.enter_information(
            "Voulez-vous ajouter :"
            "\n 1 - Un utilisateur existant ?"
            "\n 2 - Un nouvel utilisateur ?"
        )
        if action == "1":
            chosen = ""
            while not(chosen.isdecimal() and int(chosen) < len(self.known_players)):
                message = "Indiquez le numéro du joueur à ajouter :"
                for player in self.known_players:
                    message += f"\n {player.id_} - {player.__repr__()}"
                chosen = self.tournament_view.enter_information(message)
            return self.known_players[int(chosen)]
        elif action == "2":
            return self.create_new_player()
        else:
            return self.add_new_player()

    def create_new_player(self):
        """ A method to create a new player. """
        player = {
            "first_name": None,
            "last_name": None,
            "birth_date": None,
            "gender": None,
            "rank": None,
        }
        for data in player:
            while player[data] is None:
                player[data] = self.__getattribute__(f"get_player_{data}")()
        return Player(**player)

    @staticmethod
    def _player_name_is_valid(name):
        """ Check if a string only contains alphabetic caracters, <->, <'> or <space> symbols. """
        return name.replace(" ", "").replace("-", "").replace("'", "").isalpha()

    @staticmethod
    def _format_player_name(name_to_format):
        """ A method to control and format a player name entry. """
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

    def _treat_player_name(self, name):
        """ A method to coordinate several controls on a name entry. """
        if self._player_name_is_valid(name):
            return self._format_player_name(name)
        else:
            return None

    def get_player_first_name(self):
        """ A method to control a player first name entry. """
        name = self.player_view.enter_first_name()
        return self._treat_player_name(name)

    def get_player_last_name(self):
        """ A method to control a player last name entry. """
        name = self.player_view.enter_last_name()
        return self._treat_player_name(name)

    @staticmethod
    def _format_date(date_: str):
        """ A method to format a date. """
        split_date = date_.split("/")
        return (int(time_measure) for time_measure in reversed(split_date))

    def get_player_birth_date(self):
        """ A method to control a player birth date. """
        birth_date_str = self.player_view.enter_birth_date()
        if birth_date_str.replace("/", "").isdecimal():
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

    def get_player_gender(self):
        """ A method to control a player gender. """
        gender = self.player_view.enter_gender().upper()
        if gender in ("H", "F", "A"):
            return {"H": "Homme", "F": "Femme", "A": "Autre"}[gender]
        else:
            return None

    def get_player_rank(self):
        """ A method to control a player rank. """
        rank = self.player_view.enter_rank()
        if rank.isdecimal():
            return int(rank)
        else:
            return None


class OldMainController:
    """ The main controller class. """
    def __init__(self, db):
        """ The MainController initiator. """
        self.db = db
        self.players = self.load_players()
        self.tournaments = self.load_tournaments()
        self.player_view = PlayerView()
        self.tournament_view = TournamentView()
        # used to access UTC class methods and attributes
        self.controller = UnstoppableTournamentController(self.player_view, self.tournament_view)
        # used to control tournaments
        self.active_tournament_controller = None

    def run(self):
        """ A method to execute the controller and its menu. """
        action = self.tournament_view.enter_information(
            "\n--------------------------------------------------------"
            "\nVoulez-vous :"
            "\n 1 - Ajouter un joueur à la base de données ?"
            "\n 2 - Créer, exécuter et sauvegarder un tournoi ?"
            "\n 3 - Consulter la liste des joueurs ou des tournois ?"
            "\n 4 - Modifier le classement d'un joueur ?"
            "\n 5 - Quitter."
            "\n"
        )
        if action == "1":
            self.players.append(self.controller.create_new_player())
            print(self.players)
            self.save_players()
            print(self.players)
            return True
        elif action == "2":
            print(self.players)
            self.active_tournament_controller = UnstoppableTournamentController(
                self.player_view,
                self.tournament_view,
                players=self.players,
            )
            self.active_tournament_controller.run()
            self.tournaments.append(copy(self.active_tournament_controller.tournament))
            self.players = self.players + copy(self.active_tournament_controller.players)
            self.save_players()
            self.save_tournaments()
            return True
        elif action == "3":
            self.reports()
            return True
        elif action == "4":
            self.modify_rank()
            self.save_players()
            return True
        elif action == "5":
            return False
        else:
            return self.run()

    def modify_rank(self):
        """ A method to modify rank outside from player creation. """
        self.tournament_view.clear()
        if len(self.players) != 0:
            counter = 1
            message = "Le classement de quel joueur voulez-vous modifier ?"
            for player in self.players:
                message += f"\n {counter} - {player}"
                counter += 1
            player_range = ""
            while not(player_range.isdecimal() and player_range != 0 and int(player_range) < len(self.players) + 1):
                player_range = self.tournament_view.enter_information(message)
            new_rank = None
            while new_rank is None:
                new_rank = self.controller.get_player_rank()
            self.players[int(player_range) - 1].rank = new_rank
        else:
            print("Vous devez d'abord ajouter des joueurs.")

    def reports(self):
        """ A method to execute the reports. """
        self.tournament_view.clear()
        action = self.tournament_view.enter_information(
            "Voulez-vous consulter la liste de :"
            "\n 1 - Tous les joueurs, triés par nom ?"
            "\n 2 - Tous les joueurs, triés par classement ?"
            "\n 3 - Les joueurs d'un tournoi, triés par nom ?"
            "\n 4 - Les joueurs d'un tournoi, triés par classement ?"
            "\n 5 - Les tournois ?"
            "\n 6 - Les tours d'un tournoi ?"
            "\n 7 - Les matchs d'un tournoi ?"
            "\n"
        )
        if action == "1":
            self.list_players_by_name()
        elif action == "2":
            self.list_players_by_rank()
        elif action == "3":
            self.list_players_from_tournament_by_name()
        elif action == "4":
            self.list_players_from_tournament_by_rank()
        elif action == "5":
            self.list_tournaments()
        elif action == "6":
            self.list_rounds_from_tournament()
        elif action == "7":
            self.list_matches_from_tournament()

    def list_players_by_name(self):
        """ A report method to list players sorted by name."""
        self.tournament_view.clear()
        counter = 1
        message = ""
        for player in sorted(self.players, key=lambda p: p.first_name):
            message += f"\n {counter} - {player}"
            counter += 1
        self.tournament_view.show_message(message)

    def list_players_by_rank(self):
        """ A report method to list players sorted by rank."""
        self.tournament_view.clear()
        counter = 1
        message = ""
        for player in sorted(self.players, key=lambda p: p.rank):
            message += f"\n {counter} - {player}"
            counter += 1
        self.tournament_view.show_message(message)

    def select_tournament(self):
        """ A method to select a to tournament on which user will see reports.."""
        if self.tournaments:
            counter = 1
            chosen = ""
            message = "Sélectionnez le tournoi que vous voulez consulter :"
            for tournament in self.tournaments:
                message += f"\n {counter} - {tournament.__repr__()}"
                counter += 1
            while not(chosen.isdecimal() and chosen != "0" and int(chosen) < len(self.tournaments) + 1):
                chosen = self.tournament_view.enter_information(message)
            return self.tournaments[int(chosen) - 1]
        else:
            return Tournament(None, None, None, None, None)

    def list_players_from_tournament_by_name(self):
        """ A report method to list a tournament players sorted by name."""
        self.tournament_view.clear()
        tournament = self.select_tournament()
        message = ""
        for player in sorted(tournament.players, key=lambda p: p.first_name):
            message += f"\n {player.__repr__()}"
        self.tournament_view.show_message(message)

    def list_players_from_tournament_by_rank(self):
        """ A report method to list a tournament players sorted by rank."""
        self.tournament_view.clear()
        tournament = self.select_tournament()
        message = ""
        for player in sorted(tournament.players, key=lambda p: p.rank):
            message += f"\n {player.__repr__()}"
        self.tournament_view.show_message(message)

    def list_tournaments(self):
        """ A report method to list tournaments."""
        self.tournament_view.clear()
        message = ""
        for tournament in self.tournaments:
            message += f"\n {tournament.__repr__()}"
        self.tournament_view.show_message(message)

    def list_rounds_from_tournament(self):
        """ A report method to list rounds from a tournament."""
        self.tournament_view.clear()
        tournament = self.select_tournament()
        message = ""
        for round_ in tournament.rounds:
            message += f"\n\n {round_.__repr__()}"
        self.tournament_view.show_message(message)

    def list_matches_from_tournament(self):
        """ A report method to list matches from a tournament."""
        self.tournament_view.clear()
        tournament = self.select_tournament()
        message = ""
        for round_ in tournament.rounds:
            for match in round_.matches:
                message += f"\n {match.__repr__()}"
        self.tournament_view.show_message(message)

    def save_players(self):
        """ A method to save serialized versions of player objects in a .JSON."""
        self.db.table("players").truncate()
        self.db.table("players").insert_multiple([player.serialized() for player in self.players])

    def load_players(self):
        """ A method to load serialized versions of player objects from a .JSON and to extract them."""
        return [Player(**kwargs) for kwargs in self.db.table("players").all()]

    def save_tournaments(self):
        """ A method to save serialized versions of tournament objects in a .JSON."""
        self.db.table("tournament").truncate()
        self.db.table("tournament").insert_multiple([tournament.serialized() for tournament in self.tournaments])

    def load_tournaments(self):
        """ A method to load serialized versions of tournament objects from a .JSON and to extract them."""
        tournaments = self.db.table("tournament").all()
        unserialized_tournament = []
        for tournament in tournaments:
            unserialized_rounds = []
            unserialized_players = []
            for round_ in tournament["rounds"]:
                unserialized_matches = []
                for match in round_["matches"]:
                    unserialized_matches.append(Match(*match))
                round_["matches"] = unserialized_matches
                unserialized_rounds.append(round_)
            for player in tournament["players"]:
                unserialized_players.append(Player(**player))
            tournament["rounds"] = unserialized_rounds
            tournament["players"] = unserialized_players
            unserialized_tournament.append(Tournament(**tournament))
        return unserialized_tournament


# execution ----------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    pass
