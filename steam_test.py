from steam_info import steam_info, steam_scraper
from steam_info.steam_info import Game
import steam
import os
import logging
import json
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.fields import RangeKey
from boto.dynamodb2.table import Table

from steam.apps import app_list
from steam.api import interface


def main():
    game_dict = {}
    steam.api.key.set(os.environ.get("STEAM_KEY"))
    vanity_url = steam.user.vanity_url('http://steamcommunity.com/id/maddchickenz')

    steamid = vanity_url.id64
    profile = steam.user.profile(vanity_url)

    games = interface("IPlayerService").GetOwnedGames(steamid=steamid, include_appinfo=1)

    with open("steam_games.txt", "w+") as f:
        pass
    game_list = []
    for game in games["response"]["games"]:
        game_obj = Game(game)
        game_list.append(game_obj)
        game_dict[game_obj.appid] = Game(game)
        with open("steam_games.txt", "a+") as f:
            f.write("%s\n" % game["appid"] )
    #steam_scraper.start_scraper()
    try:
        table = Table.create("random_steam_test", 
                schema=[HashKey("steam_app_id"), RangeKey("tag")],
                throughput={"read": 1, "write": 1 })
    except Exception as e:
        print e.message
        if "Table already exists" in e.message:
            table = Table("random_steam_test")
        else:
            raise
    with open("steam.json", "r") as f:
        data = json.load(f)
    for tag in data:
        appid = tag["appid"]
        game = game_dict[appid]
        game.tags = tag["tag"]
        for game_tag in game.tags:
            print game_tag
            table.put_item({"steam_app_id": game.appid, "tag": game_tag})


if __name__ == "__main__":
    main()
