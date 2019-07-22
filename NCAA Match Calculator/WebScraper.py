import requests, bs4
import pandas as pd

#Will Return HashTable of Data
def getStats(year, max):
    url = "https://kenpom.com/index.php?y=" + str(year)
    response = requests.get(url)

    soup = bs4.BeautifulSoup(response.text, 'lxml')
    table = soup.find(name='table', attrs={'id':'ratings-table'})

    dict = {}
    total_count = 0
    count = 1
    dict["Columns"] = ["Rank", "Win Ratio", "AdjEM", "AdjO", "AdjD", "AdjT", "Luck"]
    for row in table.tbody.findAll(name='tr'):
        if total_count == max:
            break;
        elif count == 41:
            count += 1
        elif count == 42:
            count = 1
        elif row.find(lambda tag: tag.name == 'span' and tag.get('class') == ['seed-nit']) is None and int(row.find(lambda tag: tag.name == 'span' and tag.get('class') == ['seed']).text) <= 16:
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
            total_count += 1

            ##Display
            #print(row.find(lambda tag: tag.name == 'span' and tag.get('class') == ['seed']).text + "The name of the team is: " + key + " Rank: " + str(rank))
            #print("Stats: " +
            #      "Win Ratio: " + str(win_ratio) +
            #      " AdjeM: " + str(adjem) +
            #      " AdjO: " + str(adjo) +
            #      " AdjD: " + str(adjd) +
            #      " AdjT: " + str(adjt) +
            #      " Luck: " + str(luck))

            #[Rank, Win Ratio, AdjEM, AdjO, AdjD, AdjT, Luck]
            stats = [rank, win_ratio, adjem, adjo, adjd, adjt, luck]
            dict[key] = stats
        else: 
            count += 1
            total_count += 1

    #Put into csv file
    df = pd.DataFrame(dict).T
    df.to_csv('./stats/' + str(year) + '.csv')
            
####################################################################

#Hard Coded Max for Each Year (Ascending)
year = range(2002, 2020, 1)
year_max = [252, 283, 266, 278, 271, 254, 306, 213, 231, 227, 237, 266, 259, 251, 285, 218, 316, 303]

#Store All Data
statsDict = {}
for i in range(0, 18, 1):
    getStats(year[i], year_max[i])