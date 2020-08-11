import csv as csv


class DataReader():
    def __init__(self):
        pass

    # format: [Team1, Team2, Team1 score, Team2 score]
    def get_formatted_row(self, row):
        formatted_row = []
        formatted_row.append(row[0][0:row[0].find(" vs")])
        formatted_row.append(row[0][row[0].find(" vs")+4:])
        formatted_row.append(row[1])
        formatted_row.append(row[2])
        return formatted_row

    # gets list of scores for a given year and returns it
    def get_scores(self, year):
        games = []
        file_name = "scores/" + str(year) + ".csv"
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file)
            row_num = 0
            for row in csv_reader:
                if row_num >= 2:
                    games.append(self.get_formatted_row(row))
                row_num = row_num+1
        return games

    # gets dictionary of scores for games from 2002 to 2019. dict['year'] = [games from year]
    def get_all_scores(self):
        start_year = 2002
        num_years = 18
        scores = {}
        for i in range(num_years):
            scores[str(start_year+i)] = self.get_scores(start_year+i)
        return scores
            