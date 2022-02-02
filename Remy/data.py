from riotwatcher import LolWatcher, ApiError
import time
import csv
from datetime import datetime

file = open("data.csv", "w", newline='')

lol_watcher = LolWatcher('TODO')

my_region = 'euw1'

me = lol_watcher.summoner.by_name(my_region, 'BobyV2')
print(me)

my_ranked_stats = lol_watcher.league.by_summoner(my_region, me['id'])
# print(my_ranked_stats)

all_500_matchs = []

for x in range(0, 5):
    all_matchs = lol_watcher.match.matchlist_by_puuid(
        "europe", me['puuid'], count=100, start=x*100, queue=420)
    all_500_matchs = all_matchs + all_500_matchs
    # print(all_matchs)
    time.sleep(2)


print(len(all_500_matchs))


i = 0

writer = csv.writer(file, delimiter=';')
writer.writerow(["puuid","date", "lane", "win", "match_id", "championname"])

for match_id in all_500_matchs:
    try:
        detailed_match = lol_watcher.match.by_id("europe", match_id)
        rank = detailed_match['metadata']['participants'].index(me['puuid'])
        gamemode = detailed_match['info']['gameMode']
        gametype = detailed_match['info']['gameType']

        win = detailed_match['info']['participants'][rank]['win']
        lane = detailed_match['info']['participants'][rank]['lane']
        individualPosition = detailed_match['info']['participants'][rank]['individualPosition']
        championname = detailed_match['info']['participants'][rank]['championName']

        timestamp = detailed_match['info']['gameCreation'] / 1000
        dt_object = datetime.utcfromtimestamp(timestamp)

        #print("Lane : " + lane + "; IndividualPosition : " + individualPosition + "; Win : " + str(win) + "; Gamemode : " + gamemode)

        row = [me['puuid'], dt_object, lane, str(win), match_id, championname]
        writer.writerow(row)

        time.sleep(1.5)
        print(i)
        i += 1

    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(
                err.response.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
        elif err.response.status_code == 404:
            print('Error 404.')
        else:
            raise
