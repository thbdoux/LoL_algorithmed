from riotwatcher import LolWatcher, ApiError
import time
import csv
import json
from datetime import datetime


settings_file = open("API_key.json")
API_KEY = json.load(settings_file)["API_key"]
settings_file.close()

REGION = 'euw1'
CONTINENT = 'EUROPE'
SLEEPING_TIME = 2
MATCHS_SIZE = 500

lol_watcher = LolWatcher(API_KEY)


def getSummonerByName(name):
    summoner = lol_watcher.summoner.by_name(REGION, name)
    return summoner

def getRankedStatsBySummoner(summoner):
    my_ranked_stats = lol_watcher.league.by_summoner(REGION, summoner['id'])
    return my_ranked_stats

def getAllMatchsFromSummoner(summoner):
    for x in range(0, MATCHS_SIZE/100):
        all_matchs = lol_watcher.match.matchlist_by_puuid(
            "europe", summoner['puuid'], count=100, start=x*100, queue=420)

        all_x_matchs = all_matchs + all_x_matchs
        time.sleep(SLEEPING_TIME)
    return all_x_matchs

def getDetailedMatchFromMatchId(match_id):
    detailed_match = lol_watcher.match.by_id(CONTINENT, match_id)

    return detailed_match

def getAllMatchsFromASummonerName(name):
    summoner = getSummonerByName(name)
    all_matchs = getAllMatchsFromSummoner(summoner)
    return all_matchs

    
