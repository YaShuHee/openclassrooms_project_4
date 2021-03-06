#!/usr/bin/env python3
# coding: utf-8


# imports ------------------------------------------------------------------------------------------------------------
# python standard library imports
import re
import os
from os.path import join, dirname, abspath
from datetime import date, datetime

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
        }
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
    """ The controller to add players to and to execute a tournament."""
    def __init__(self, view: TournamentView, tournament: Tournament, player_creator: PlayerCreator,
                 known_players: list):
        """ The class initiator. """
        self.view = view
        self.tournament = tournament
        self.tournament.players = []
        self.player_creator = player_creator
        self.known_players = known_players

    def run(self):
        """ Execution method from the TournamentRunner class. It first fill the self.tournament.player list, and then
        execute the tournament and the scores entries. """
        # add players
        self.add_players()
        # run the tournament with added players
        self._run()

    def add_players(self):
        """ A method to fill self.tournament.players list. """
        while len(self.tournament.players) < self.tournament.number_of_players:
            number_of_players = len(self.tournament.players)
            self.view.display_message(f"Votre tournoi compte actuellement {number_of_players} joueur"
                                      f"{'s' * (number_of_players > 1)} sur {self.tournament.number_of_players}.")
            answer = ""
            while answer not in ("1", "2", "/list"):
                answer = self.view.enter_information(
                    "Voulez-vous :"
                    "\n 1 - Ajouter un joueur (tapez '/list' pour voir les joueurs) ?"
                    "\n 2 - Cr??er un nouveau joueur ?"
                ).lower()
            if answer == "1" and self.known_players != 0:
                player = self.select_a_known_player()
                if player in self.tournament.players:
                    self.view.display_message("Ce joueur est d??j?? dans le tournoi !")
                else:
                    self.tournament.players.append(player)
            elif answer == "2":
                new_player = self.player_creator.run()
                self.known_players.append(new_player)
                self.tournament.players.append(new_player)
            elif answer == "/list":
                self.player_creator.view.list_players(self.known_players)

    def select_a_known_player(self):
        """ Return a player chosen by the user. """
        number_of_players = len(self.known_players)
        player_range = ""
        while not(player_range.isdecimal() and player_range != "0" and int(player_range) <= number_of_players):
            self.player_creator.view.list_players(self.known_players, show_index=True)
            player_range = self.view.enter_information(f"S??lectionner le joueur que vous voulez ajouter "
                                                       f"(1-{number_of_players}).")
        return self.known_players[int(player_range) - 1]

    def _run(self):
        """ Run the tournament operation. """
        while self.tournament.active_round < self.tournament.number_of_rounds:
            self.update_scores()
            self.generate_new_round()
            self.get_round_scores()
            self.tournament.active_round += 1

    def update_scores(self):
        """ Display scores and reset them for next round. """
        active_round = self.tournament.active_round
        # reset all players scores (from previous sessions, tournaments and matches)
        for player in self.tournament.players:
            player.score = 0
        # make a cumulative sum of scores for this tournament
        for round_ in self.tournament.rounds:
            for match in round_.matches:
                match.p1.score += match.s1
                match.p2.score += match.s2
        # display scores
        if active_round != 0:
            message = f"Scores apr??s {self.tournament.rounds[active_round - 1].name}"
            for player in reversed(sorted(self.tournament.players, key=lambda p: p.score)):
                # keep score int type (instead of float) for in scores -> avoid 1.0 or 2.0 scores
                if int(player.score) == player.score:
                    player.score = int(player.score)
                message += f"\n {player} -> score: {player.score} "
            self.view.display_message(message)

    def generate_new_round(self):
        """ Generate new round and avoid players to compete several times against the same player. """
        round_name = self.get_round_name()
        players = self.tournament.players
        if self.tournament.active_round == 0:
            sorted_players = sorted(players, key=lambda p: p.rank)
            best_sorted_players = sorted_players[:len(sorted_players)//2]
            worst_sorted_players = sorted_players[len(sorted_players)//2:]
            matches = [Match(best, worst) for best, worst in zip(best_sorted_players, worst_sorted_players)]
        else:
            # 1 - sort by rank
            sorted_players = sorted(players, key=lambda p: p.rank)
            # 2 - over sort by score => list is now sorted by score, and items with equal scores are sorted by rank
            sorted_players = sorted(sorted_players, key=lambda p: p.score, reverse=True)
            already_met = False
            # check if 1st and 2nd player already met
            for round_ in self.tournament.rounds:
                for match in round_.matches:
                    first_players = (sorted_players[0], sorted_players[1])
                    already_met = (first_players == (match.p1, match.p2) or first_players == (match.p2, match.p2))
                    if already_met:
                        break
                if already_met:
                    break
            if already_met:
                sorted_players[0], sorted_players[2] = sorted_players[2], sorted_players[0]
            player_iterator = iter(sorted_players)
            matches = [Match(player, next(player_iterator)) for player in player_iterator]
        self.tournament.rounds.append(Round(round_name, matches))

    def get_round_name(self):
        """ Get a round name. """
        default_name = "Round " + str(self.tournament.active_round + 1)
        entry = self.view.enter_information(f"\n\nVeuillez saisir le nom du round (par d??faut : '{default_name}').")
        if entry == "":
            return default_name
        else:
            return entry

    def get_round_scores(self):
        """ Ask the winner of the round and attribute the scores. """
        for match in self.tournament.rounds[-1].matches:
            self.view.display_message(match.__repr__())
            winner_number = ""
            while winner_number not in ("0", "1", "2"):
                winner_number = self.view.enter_match_result()
            if winner_number == "0":
                match[0][1] = 0.5
                match[1][1] = 0.5
            else:
                match[int(winner_number) - 1][1] = 1
        self.tournament.rounds[-1].close()


class Loader:
    """ A class to manage players and tournaments, independently from any controller. """
    def __init__(self, players, tournaments):
        self.players = players
        self.tournaments = tournaments

        # db initialisation
        root_path = dirname(dirname(abspath(__file__)))
        database_directory = join(root_path, "database")
        if not os.path.exists(database_directory):
            os.mkdir(database_directory)
        self.db = TinyDB(join(database_directory, "db.json"))

    def serialized_player(self, player) -> dict:
        """ Return a serialized version of the player object. """
        b = player.birth_date
        return {
            "first_name": player.first_name,
            "last_name": player.last_name,
            "birth_date": (b.year, b.month, b.day),
            "gender": player.gender,
            "rank": player.rank,
            "uid": player.uid,
        }

    def unserialized_player(self, player) -> Player:
        """ Return an Player instance from a serialized instance saved in a previous session. """
        clean_kwargs = {
            "first_name": player["first_name"],
            "last_name": player["last_name"],
            "birth_date": date(*player["birth_date"]),
            "gender": player["gender"],
            "rank": player["rank"],
            "uid": player["uid"],
        }
        return Player(**clean_kwargs)

    def serialized_tournament(self, tournament) -> dict:
        """ Return a serialized version of a Tournament object. """
        b = tournament.beginning_date
        e = tournament.ending_date
        return {
            "name": tournament.name,
            "place": tournament.place,
            "beginning_date": (b.year, b.month, b.day),
            "ending_date": (e.year, e.month, e.day),
            "time_control": tournament.time_control,
            "description": tournament.description,
            "number_of_rounds": tournament.number_of_rounds,
            "number_of_players": tournament.number_of_players,
            "players": [player.uid for player in tournament.players],
            "rounds": [self.serialized_round(round_) for round_ in tournament.rounds],
        }

    def unserialized_tournament(self, tournament) -> Tournament:
        """ Return an Tournament instance from a serialized instance saved in a previous session. """
        clean_kwargs = {
            "name": tournament["name"],
            "place": tournament["place"],
            "beginning_date": date(*tournament["beginning_date"]),
            "ending_date": date(*tournament["ending_date"]),
            "time_control": tournament["time_control"],
            "description": tournament["description"],
            "number_of_rounds": tournament["number_of_rounds"],
            "number_of_players": tournament["number_of_players"],
            "players": [self.players[uid] for uid in tournament["players"]],
            "rounds": [self.unserialized_round(round_) for round_ in tournament["rounds"]],
        }
        return Tournament(**clean_kwargs)

    def serialized_round(self, round_: Round) -> dict:
        """ Return a serialized version of a Round object."""
        b = round_.beginning_time
        e = round_.ending_time
        return {
            "name": round_.name,
            "matches": [self.serialized_match(match) for match in round_.matches],
            "beginning_time": (b.year, b.month, b.day, b.hour, b.minute),
            "ending_time": (e.year, e.month, e.day, e.hour, e.minute),
        }

    def unserialized_round(self, round_: dict) -> Round:
        """ Return an unserialized version of a previously saved Round object."""
        clean_kwargs = {
            "name": round_["name"],
            "matches": [self.unserialized_match(match) for match in round_["matches"]],
            "beginning_time": datetime(*round_["beginning_time"]),
            "ending_time": datetime(*round_["ending_time"]),
        }
        return Round(**clean_kwargs)

    def serialized_match(self, match: Match) -> tuple[list, list]:
        """ Return a serialized version of a Match object. Instead of the player, it's the player UID that is saved.
        """
        return [match.p1.uid, match.s1], [match.p2.uid, match.s2]

    def unserialized_match(self, match: dict):
        """ Return a Match object referencing to Players objects from a previously serialized Match. """
        player_1 = self.players[match[0][0]]
        player_2 = self.players[match[1][0]]
        score_1 = match[0][1]
        score_2 = match[1][1]
        return Match(player_1, player_2, score_1, score_2)

    def save_players(self):
        """ Saves the self.players list in a .JSON file after serializing objects. """
        self.db.table("players").truncate()
        self.db.table("players").insert_multiple([self.serialized_player(player) for player in self.players])

    def save_tournaments(self):
        """ Saves the self.tournaments list in a .JSON file after serializing objects. """
        self.db.table("tournaments").truncate()
        self.db.table("tournaments").insert_multiple([self.serialized_tournament(tournament)
                                                      for tournament in self.tournaments])

    def load_players(self):
        """ Unserialize and reinstanciate saved Players objects from previous sessions.
        /!\\ Should not create any player or tournament, by hand  before the call of this method.
        /!\\ Must be called before self.load_tournaments. """
        Player.uid = 0
        for player in self.db.table("players").all():
            self.players.append(self.unserialized_player(player))

    def load_tournaments(self):
        """ Unserialize and reinstanciate saved Tournaments objects from previous sessions.
        /!\\ Should not create any player or tournament, by hand  before the call of this method.
        /!\\ Must be called after self.load_players, because it uses Player.uid to reference Match objects. """
        for tournament in self.db.table("tournaments").all():
            self.tournaments.append(self.unserialized_tournament(tournament))


class MainController:
    """ The main controller managing and calling the other subcontrollers. """
    def __init__(self):
        """ The class initiator. """
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
        # db initialisation
        self.loader = Loader(self.players, self.tournaments)
        self.loader.load_players()
        self.loader.load_tournaments()

    def run(self):
        """ A method to execute the controller and its menu. """
        running = True
        while running:
            action = self.tournament_view.enter_information(
                "\n--------------------------------------------------------"
                "\nVoulez-vous :"
                "\n 1 - Ajouter un joueur ?? la base de donn??es ?"
                "\n 2 - Cr??er, ex??cuter et sauvegarder un tournoi ?"
                "\n 3 - Consulter la liste des joueurs ou des tournois ?"
                "\n 4 - Modifier le classement d'un joueur ?"
                "\n 5 - Quitter."
                "\n"
            )

            if action == "1":
                self.players.append(self.player_creator.run())
                self.loader.save_players()

            elif action == "2":
                self.tournaments.append(self.tournament_creator.run())
                TournamentRunner(self.tournament_view, self.tournaments[-1], self.player_creator, self.players).run()
                self.loader.save_players()
                self.loader.save_tournaments()
                running = True

            elif action == "3":
                self.reports()
                running = True

            elif action == "4":
                self.modify_rank()
                self.loader.save_players()
                running = True

            elif action == "5":
                running = False

            else:
                running = True

    def modify_rank(self):
        """ A method to control a player rank modification. """
        if len(self.players) == 0:
            self.view.display_message("Aucun joueur pour le moment.")
        else:
            player = self.select_player()
            rank = None
            while rank is None:
                rank = self.player_creator.get_rank()
            player.rank = rank
            self.view.display_message(f"{player.first_name} {player.last_name} est maintenant class??"
                                      f"{'-' * (player.gender == 'Autre')}"
                                      f"{'e' * (player.gender in ('Femme', 'Autre'))} "
                                      f"{player.rank}e.")

    def select_player(self):
        """ This method let the user chose a player on which to do actions.
        /!\\ This method must not be called when self.players is empty. """
        number_of_players = len(self.players)
        player_range = ""
        while not(player_range.isdecimal() and player_range != "0" and int(player_range) <= number_of_players):
            self.player_view.list_players(self.players, show_index=True)
            player_range = self.view.enter_information(f"S??lectionner un joueur (1-{number_of_players}).")
        return self.players[int(player_range) - 1]

    def select_tournament(self):
        """ This method let the user chose a tournament on which to do actions.
        /!\\ This method must not be called when self.tournaments is empty. """
        number_of_tournaments = len(self.tournaments)
        tournament_range = ""
        while not(tournament_range.isdecimal() and tournament_range != "0"
                  and int(tournament_range) <= number_of_tournaments):
            self.tournament_view.list_tournaments(self.tournaments, show_index=True)
            tournament_range = self.view.enter_information(f"S??lectionner tournoi (1-{number_of_tournaments}).")
        return self.tournaments[int(tournament_range) - 1]

    def reports(self):
        """ A method to execute the reports. """
        self.view.clear()
        action = self.view.enter_information(
            "Voulez-vous consulter la liste de :"
            "\n 1 - Tous les joueurs, tri??s par nom ?"
            "\n 2 - Tous les joueurs, tri??s par classement ?"
            "\n 3 - Les joueurs d'un tournoi, tri??s par nom ?"
            "\n 4 - Les joueurs d'un tournoi, tri??s par classement ?"
            "\n 5 - Les tournois ?"
            "\n 6 - Les tours d'un tournoi ?"
            "\n 7 - Les matchs d'un tournoi ?"
            "\n"
        )
        self.view.clear()
        if action == "1":
            "Liste des joueurs, tri??s par nom :"
            self.player_view.list_players(sorted(self.players, key=lambda p: p.first_name))
        elif action == "2":
            "Liste des joueurs, tri??s par classement :"
            self.player_view.list_players(sorted(self.players, key=lambda p: p.rank))
        elif action == "3":
            if self.tournaments:
                self.player_view.list_players(sorted(self.select_tournament().players, key=lambda p: p.first_name))
        elif action == "4":
            if self.tournaments:
                self.player_view.list_players(sorted(self.select_tournament().players, key=lambda p: p.rank))
        elif action == "5":
            self.tournament_view.list_tournaments(self.tournaments)
        elif action == "6":
            if self.tournaments:
                self.tournament_view.list_rounds(self.select_tournament())
        elif action == "7":
            if self.tournaments:
                self.tournament_view.list_matches(self.select_tournament())


# execution ----------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    pass
