from WebScraper import getStats

#Data Refresh
refresh = (input('Want to Refresh the Data? y/n ') == 'y')
if refresh:
    getStats()