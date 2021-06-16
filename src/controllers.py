#!/usr/bin/env python3
# coding: utf-8


# python standard library imports
from re import split as re_split
from datetime import date

# outside libraries imports

# local imports
from models import Player, Tournament, Round, Match
from views import PlayerView, TournamentView


class UnstoppableTournamentController:
    """ A controller for a basic unstoppable 4 round tournament. """
    def __init__(self, player_view, tournament_view, players=[], number_of_players: int = 8):
        self.player_view = player_view
        self.tournament_view = tournament_view
        self.tournament = None
        self.known_players = players
        self.players = players
        self.number_of_players = number_of_players

    def run(self):
        self.tournament = self.create_tournament()
        self.players = [self.add_new_player() for n in range(self.number_of_players)]
        while self.tournament.active_round <= self.tournament.number_of_rounds:
            self.update_scores()
            self.generate_new_round()
            self.get_round_scores()
            self.tournament.active_round += 1

    def update_scores(self):
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
        name = self.tournament_view.enter_round_name()
        if name == "":
            return "Round " + str(self.tournament.active_round + 1)
        else:
            return name

    def get_round_scores(self):
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
        try:
            treated_date = date(*(int(time_unit) for time_unit in reversed(date_str.split(" "))))
        except (ValueError, TypeError):
            treated_date = None
        return treated_date

    def get_tournament_name(self):
        name = self.tournament_view.enter_name()
        return name

    def get_tournament_place(self):
        place = self.tournament_view.enter_place()
        return place

    def get_tournament_beginning_date(self):
        beginning_date = self.tournament_view.enter_beginning_date()
        return self._treat_french_date_string(beginning_date)

    def get_tournament_ending_date(self):
        ending_date = self.tournament_view.enter_ending_date()
        if ending_date == "":
            return False
        else:
            return self._treat_french_date_string(ending_date)

    def get_tournament_time_control(self):
        time_control = self.tournament_view.enter_time_control().capitalize()
        if time_control in ("Bullet", "Blitz", "Coup rapide"):
            return time_control
        else:
            return None

    def get_tournament_number_of_rounds(self):
        number_of_rounds = self.tournament_view.enter_number_of_rounds()
        if number_of_rounds == "":
            return 4
        elif number_of_rounds.isdecimal():
            return int(number_of_rounds)
        else:
            return None

    def get_tournament_description(self):
        description = self.tournament_view.enter_description()
        return description

    def add_new_player(self):
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
        if self._player_name_is_valid(name):
            return self._format_player_name(name)
        else:
            return None

    def get_player_first_name(self):
        name = self.player_view.enter_first_name()
        return self._treat_player_name(name)

    def get_player_last_name(self):
        name = self.player_view.enter_last_name()
        return self._treat_player_name(name)

    @staticmethod
    def _format_date(date_: str):
        split_date = date_.split(" ")
        return (int(time_measure) for time_measure in reversed(split_date))

    def get_player_birth_date(self):
        birth_date_str = self.player_view.enter_birth_date()
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

    def get_player_gender(self):
        gender = self.player_view.enter_gender().capitalize()
        if gender in ("Homme", "Femme", "Autre"):
            return gender
        else:
            return None

    def get_player_rank(self):
        rank = self.player_view.enter_rank()
        if rank.isdecimal():
            return int(rank)
        else:
            return None


class MainController:
    def __init__(self, db):
        self.db = db
        self.players = self.load_players()
        self.tournaments = self.load_tournaments()
        self.player_view = PlayerView()
        self.tournament_view = TournamentView()
        self.controller = UnstoppableTournamentController(self.player_view, self.tournament_view)
        self.tournament_controllers = []

    def run(self):
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
            self.save_players()
            return True
        elif action == "2":
            print(self.players)
            self.tournament_controllers.append(UnstoppableTournamentController(self.player_view, self.tournament_view,
                                                                               players=self.players))
            self.tournament_controllers[-1].run()
            self.tournaments.append(self.tournament_controllers[-1].tournament)
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
        pass

    def reports(self):
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
        self.tournament_view.clear()
        counter = 1
        message = ""
        for player in sorted(self.players, key=lambda p: p.first_name):
            message += f"\n {counter} - {player}"
            counter += 1
        self.tournament_view.show_message(message)

    def list_players_by_rank(self):
        self.tournament_view.clear()
        counter = 1
        message = ""
        for player in sorted(self.players, key=lambda p: p.rank):
            message += f"\n {counter} - {player}"
            counter += 1
        self.tournament_view.show_message(message)

    def select_tournament(self):
        if self.tournaments:
            counter = 1
            chosen = ""
            message = "Sélectionnez le tournoi que vous voulez consulter :"
            for tournament in self.tournaments:
                message += f"\n {counter} - {tournament.__repr__()}"
            while not(chosen.isdecimal() and chosen != "0" and int(chosen) < len(self.tournaments) + 1):
                chosen = self.tournament_view.enter_information(message)
            return self.tournaments[int(chosen) - 1]
        else:
            return Tournament(None, None, None, None, None)

    def list_players_from_tournament_by_name(self):
        self.tournament_view.clear()
        tournament = self.select_tournament()
        message = ""
        for player in sorted(tournament.players, key=lambda p: p.first_name):
            message += f"\n {player.__repr__()}"
        self.tournament_view.show_message(message)

    def list_players_from_tournament_by_rank(self):
        self.tournament_view.clear()
        tournament = self.select_tournament()
        message = ""
        for player in sorted(tournament.players, key=lambda p: p.rank):
            message += f"\n {player.__repr__()}"
        self.tournament_view.show_message(message)

    def list_tournaments(self):
        self.tournament_view.clear()
        message = ""
        for tournament in self.tournaments:
            message += f"\n {tournament.__repr__()}"
        self.tournament_view.show_message(message)

    def list_rounds_from_tournament(self):
        self.tournament_view.clear()
        tournament = self.select_tournament()
        message = ""
        for round_ in tournament.rounds:
            message += f"\n\n {round_.__repr__()}"
        self.tournament_view.show_message(message)

    def list_matches_from_tournament(self):
        self.tournament_view.clear()
        tournament = self.select_tournament()
        message = ""
        for round_ in tournament.rounds:
            for match in round_.matches:
                message += f"\n {match.__repr__()}"
        self.tournament_view.show_message(message)

    def save_players(self):
        self.db.table("players").truncate()
        self.db.table("players").insert_multiple([player.serialized() for player in self.players])

    def load_players(self):
        return [Player(**kwargs) for kwargs in self.db.table("players").all()]

    def save_tournaments(self):
        self.db.table("tournament").truncate()
        self.db.table("tournament").insert_multiple([
            ctr.tournament.serialized() for ctr in self.tournament_controllers
        ])

    def load_tournaments(self):
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


if __name__ == '__main__':
    pass
