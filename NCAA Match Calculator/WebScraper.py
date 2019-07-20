import requests, bs4
import pandas as pd

#Will Return HashTable of Data
def getStats():
    url = "https://kenpom.com/"
    response = requests.get(url)

    soup = bs4.BeautifulSoup(response.text, 'lxml')
    table = soup.find(name='table', attrs={'id':'ratings-table'})

    dict = {}
    count = 1
    for row in table.tbody.findAll(name='tr'):
        if count == 41:
            count += 1
        elif count == 42:
            count = 1
        else:
            #Gets the Team Name for key
            key = row.find('a').text

            #Ranking on kenpom
            rank = row.find('td', attrs={'class':'hard_left'}).text

            #Win Ratio
            temp = row.find('td', attrs={'class':'wl'}).text
            win_ratio = int(temp[0: temp.index('-')]) / (int(temp[0: temp.index('-')]) + int(temp[1 + temp.index('-'):]))

            #AdjEM (Adjusted Efficiency Margin)
            adjem = row.find('td', attrs={'class':''}).text

            #AdjD (Adjusted Defensive Efficiency)
            adjd = row.find(lambda tag: tag.name == 'td' and tag.get('class') == ['td-left']).text

            # AdjO (Adjusted Offensive Efficiency), AdjT (Adjusted Tempo), Luck
            adjo = adjt = luck = 0      
            for value in row.findAll(name='td', attrs={'class':'td-left divide'}):
                if adjo == 0:
                    adjo = value.text
                elif adjt == 0:
                    adjt = value.text
                elif luck == 0:
                    luck = value.text
        
            #count increase
            count += 1

            ##Display
            #print("The name of the team is: " + key)
            #print("Stats: " +
            #      "Win Ratio: " + str(win_ratio) +
            #      " AdjeM: " + str(adjem) +
            #      " AdjO: " + str(adjo) +
            #      " AdjD: " + str(adjd) +
            #      " AdjT: " + str(adjt) +
            #      " Luck: " + str(luck))

            ##[Rank, Win Ratio, AdjEM, AdjO, AdjD, AdjT, Luck]
            stats = [rank, win_ratio, adjem, adjo, adjd, adjt, luck]
            dict[key] = stats

    return dict
            
####################################################################

statsDict = getStats()
print(statsDict)