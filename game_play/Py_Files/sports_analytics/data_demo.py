import pandas as pd

prem_data_path = 'Premier League Player Stats.csv'
prem_data = pd.read_csv(prem_data_path)
print(prem_data.describe)