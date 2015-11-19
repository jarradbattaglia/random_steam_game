import steam
from steam.apps import app_list
from steam.api import interface
import os

class Game():

    def __init__(self, game_info):
        self.name = game_info["name"]
        self.hours_played = game_info["playtime_forever"] / 60.0
        #self.last_two_week = game_info["playtime_2weeks"]
        self.appid = str(game_info["appid"])
        self.tags = []

    def __str__(self):
        return "(Name: %s, Hours: %s, Id: %s)" % (self.name, self.hours_played, self.appid)

def find_longest_played_game(games):
    longest_game = None
    for game in games:
        if not longest_game:
            longest_game = game
        elif longest_game.hours_played < game.hours_played:
            longest_game = game

    return longest_game

