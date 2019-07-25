import requests, bs4
import pandas as pd

def getStats():
    #Hard Coded Max for Each Year (Ascending)
    year = range(2002, 2020, 1)
    year_max = [252, 283, 266, 278, 271, 254, 306, 213, 231, 227, 237, 266, 259, 251, 285, 218, 316, 303]

    #Method Call
    for i in range(0, 18, 1):
        print("Loading Stats From " + str(year[i]) + "...")
        yearlyStats(year[i], year_max[i])

#Make csv file of specific year's regular season stats for all march madness teams
def yearlyStats(year, max):
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

def getScores():
    #Hard Coded Max for Each Year (Ascending)
    year = range(2002, 2020, 1)

    #Method Call
    for i in range(0, 18, 1):
        print("Loading Scores From " + str(year[i]) + "...")
        yearlyScores(year[i])


def yearlyScores(year):
    url = "https://en.wikipedia.org/wiki/" + str(year) + "_NCAA_Division_I_Men%27s_Basketball_Tournament" 
    response = requests.get(url)

    soup = bs4.BeautifulSoup(response.text, 'lxml')
    tds = soup.findAll(name='td', attrs={'rowspan':'2'})

    twoThousandTwoCities = ["Washington, D.C.", "St. Louis", "Chicago", "Dallas", "Sacramento", "Greenville", "Pittsburgh", "Albuquerque"]
    twoThousandThreeCities = ["Oklahoma City", "Birmingham", "Boston", "Tampa", "Spokane", "Nashville", "Indianapolis", "Salt Lake City"]
    twoThousandFourCities = ["Buffalo", "Raleigh", "Milwaukee", "Kansas City", "Columbus", "Seattle", "Denver", "Orlando"]
    twoThousandFiveCities = ["Indianapolis", "Cleveland", "Boise", "Oklahoma City", "Nashville", "Tucson", "Charlotte", "Worcester"]
    twoThousandSixCities = ["Greensboro", "Jacksonville", "Auburn Hills", "Dallas", "Salt Lake City", "San Diego", "Philadelphia", "Dayton"]
    twoThousandSevenCities = ["New Orleans", "Buffalo", "Spokane", "Chicago", "Columbus", "Sacramento", "Winston-Salem", "Lexington"]
    twoThousandEightCities = ["Raleigh", "Denver", "Birmingham", "Omaha", "Tampa", "North Little Rock", "Anaheim", "Washington, D.C."]
    twoThousandNineCities = ["Dayton", "Miami", "Minneapolis", "Philadelphia", "Portland", "Boise", "Kansas City", "Greensboro"]
    twoThousandTenCities = ["Oklahoma City", "Spokane", "Providence", "Milwaukee", "Buffalo", "San Jose", "Jacksonville", "New Orleans"]

    game = []
    allGames = {}
    allGames["Teams"] = ["Left", "Right"]
    for td in tds:
        if td.text.isspace() or "/" in td.text or "#" in td.text or ":" in td.text:
            x = 1#Empty Line

        elif year == 2002 and any(x == td.text.rstrip("\r\n*–") for x in twoThousandTwoCities):
            if td.text.rstrip("\r\n*–") == "Pittsburgh" and (len(game) == 0 or len(game) == 2):
                if len(game) == 0:
                    game.append(td.text.rstrip("\r\n*–"))
                elif len(game) == 2 and game[0] != "Cincinnati":
                    game.append(td.text.rstrip("\r\n*–"))
        elif year == 2003 and any(x == td.text.rstrip("\r\n*–") for x in twoThousandThreeCities) :
            x = 1#Empty Line

        elif year == 2004 and any(x == td.text.rstrip("\r\n*–") for x in twoThousandFourCities):
            x = 1#Empty Line

        elif year == 2005 and (any(x == td.text.rstrip("\r\n*–") for x in twoThousandFiveCities) or td.text.rstrip("\r\n*–") == "Oakland advances to 16 seed in Syracuse"):
            if td.text.rstrip("\r\n*–") == "Charlotte" and len(allGames) == 43:
                game.append(td.text.rstrip("\r\n*–"))

        elif year == 2006 and any(x == td.text.rstrip("\r\n*–") for x in twoThousandSixCities):
            x = 1#Empty Line

        elif year == 2007 and any(x == td.text.rstrip("\r\n*–") for x in twoThousandSevenCities):
            x = 1#Empty Line

        elif year == 2008 and any(x == td.text.rstrip("\r\n*–") for x in twoThousandEightCities):
            x = 1#Empty Line

        elif year == 2009 and any(x == td.text.rstrip("\r\n*–") for x in twoThousandNineCities):
            x = 1#Empty Line

        elif year == 2010 and any(x == td.text.rstrip("\r\n*–") for x in twoThousandTenCities):
            x = 1#Empty Line

        elif len(td.text) > 0 and (td.text[0:1]).isalpha():

            if not td.text[len(td.text) - 2 : len(td.text) ].rstrip("\r\n*–").isdigit():
                game.append(td.text.rstrip("\r\n*–"))

        elif len(td.text) > 0 and (int(td.text[0:2]) > 16 or td.text[0:3].isdigit()):
            game.append(td.text.rstrip("\r\n*–"))

        if len(game) == 4:
            if str(game[0]) == "Loyola–Chicago":
                allGames["Loyola Chicago" + " vs " + str(game[2])] = [game[1],game[3]]
            elif str(game[2]) == "Loyola–Chicago":
                allGames[str(game[0]) + " vs " + "Loyola Chicago"] = [game[1],game[3]]
            else:
                allGames[str(game[0]) + " vs " + str(game[2])] = [game[1],game[3]]

            game.clear()

    #Put into csv file
    df = pd.DataFrame(allGames).T
    df.to_csv('./scores/' + str(year) + '.csv')
    
    ##Display
    #for key, val in allGames.items():
    #    print(key + " =>")
    #    for i in val:
    #        print(i, end=" ")
