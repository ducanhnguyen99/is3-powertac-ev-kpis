from pathlib import Path
import pandas as pd
import sys

from analysis_tools.transformers.tariff_type_overview_transformer import (unique_published_tariff_count, traded_energy, subscriber_days, average_price_per_kwh)
from analysis_tools.analyzers.tariff_type_overview_plotter import (tariff_type_overview_boxplots)
from analysis_tools.utility import (filter_games)

'''
    Execution file for the analysis of tariff type KPIs (KPI3).
'''

# receive command line arguments

group = sys.argv[1]
brokers = sys.argv[2]
customers = sys.argv[3]

# set read and save path

path = '/data/passive/powertac/games/{}'.format(group)
destination = Path('/home/danguyen/data/powertac/analysis/output_all')
cwd = Path(path)
games_csv = "Power-TAC-finals-2022-csv-file.csv"

# read games that include our brokers

list_games = filter_games(cwd, games_csv, brokers)

# initialize our dataframes aggregating the games' data

counted = pd.DataFrame()
sum_energy = pd.DataFrame()
subscribers = pd.DataFrame()
price_per_kwh = pd.DataFrame()

# aggregate data of every game into one data frame and transform

for game in list_games:
    try:
        
        transactions = pd.read_csv(cwd/"{0}/analysis/{1}.tariff-transactions.csv".format(game, game), skipinitialspace=True, delimiter=";")

        # filter on customers if given

        if (customers != "any"):
            customer_list = customers.split(",")
            transactions = transactions[transactions['customer-name'].isin(customer_list)]
        
        # apprehend the game's data
        
        counted = pd.concat([counted, unique_published_tariff_count(transactions)])
        sum_energy = pd.concat([sum_energy, traded_energy(transactions)])
        subscribers = pd.concat([subscribers, subscriber_days(transactions)])
        price_per_kwh = pd.concat([price_per_kwh, average_price_per_kwh(transactions)])
    except Exception:
        print('Game {} could not be processed due to missing csv files'.format(game))
        continue

# plot and save figure

tariff_type_overview_boxplots(counted, sum_energy, subscribers, price_per_kwh, destination, customers, brokers, group)
