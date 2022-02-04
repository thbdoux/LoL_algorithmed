from riotwatcher import LolWatcher, ApiError
import time
import csv
import json
from datetime import datetime
from methods import methods as m

import os
cwd = os.path.dirname(os.path.realpath(__file__))

#----INIT----#

CONTINENT = 'EUROPE'
SLEEPING_TIME = 0

settings_file = open(cwd + "\methods\settings.json", "r")
API_KEY = json.load(settings_file)["API_key"]
settings_file.close()

file = open("data.csv", "w", newline='')
writer = csv.writer(file, delimiter=',')
writer.writerow(["puuid", "date", "lane", "individualPosition",
                "win", "match_id", "championname"])

lol_watcher = LolWatcher(API_KEY)

#names = ['WAO RANK 1', 'Reym', 'Pied à coulisse', 'BobyV2','Tarek Boudali', 'Philippe Lacheau']
names = []

challengers = m.getChallengers()

for challenger in challengers['entries']:
    challengerName = challenger['summonerName']
    print(challengerName)
    names.append(challengerName)

for name in names:
    print(name)
    executed_times = 0
    summoner = m.getSummonerByName(name)
    all_matchs = m.getAllMatchsFromSummoner(summoner)

    for match_id in all_matchs:
        try:
            detailed_match = lol_watcher.match.by_id(CONTINENT, match_id)

            # Not used yet
            rank = detailed_match['metadata']['participants'].index(
                summoner['puuid'])
            gamemode = detailed_match['info']['gameMode']
            gametype = detailed_match['info']['gameType']
            #

            individualPosition = detailed_match['info']['participants'][rank]['individualPosition']
            timestamp = detailed_match['info']['gameCreation'] / 1000
            dt_object = datetime.utcfromtimestamp(timestamp)
            lane = detailed_match['info']['participants'][rank]['lane']
            win = detailed_match['info']['participants'][rank]['win']
            championname = detailed_match['info']['participants'][rank]['championName']

            row = [summoner['puuid'], dt_object, lane, individualPosition,
                   str(win), match_id, championname]
            writer.writerow(row)

            time.sleep(SLEEPING_TIME)
            print(executed_times)
            executed_times += 1

        except ApiError as err:
            if err.response.status_code == 429:
                print('We should retry in {} seconds.'.format(
                    err.response.headers['Retry-After']))
                print(
                    'this retry-after is handled by default by the RiotWatcher library')
                print('future requests wait until the retry-after time passes')
            elif err.response.status_code == 404:
                print('Error 404.')
            elif err.response.status_code == 503:
                print('Error 503.')
            else:
                raise
        except Exception as error:
            print(error)
