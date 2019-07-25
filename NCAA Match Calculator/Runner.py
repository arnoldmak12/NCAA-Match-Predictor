from WebScraper import *

#Data Refresh
refreshStats = (input('Want to Refresh the Stats Data? y/n ') == 'y')
if refreshStats:
    getStats()

#Data Refresh
refreshScores = (input('Want to Refresh the Scores Data? y/n ') == 'y')
if refreshScores:
    getScores()