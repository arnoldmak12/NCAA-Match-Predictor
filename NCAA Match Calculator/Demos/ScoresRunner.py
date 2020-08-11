from DataReader import DataReader

reader = DataReader()
scores = reader.get_all_scores()

print(scores['2002'])
