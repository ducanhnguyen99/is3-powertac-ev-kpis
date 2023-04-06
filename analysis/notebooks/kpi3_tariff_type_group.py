from pathlib import Path
import pandas as pd
import numpy as np
import sys

from analysis_tools.transformers.tariff_type_transformer_group import (kpi3_transformer)
from analysis_tools.analyzers.tariff_type_overview_plotter import (kpi3_plotter)
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

tf_type_count = pd.DataFrame()
tf_type_energy = pd.DataFrame()
tf_type_subs = pd.DataFrame()
tf_type_price = pd.DataFrame()

# aggregate data of every game into one data frame and transform

for game in list_games:
    try:
        
        tariff_transactions = pd.read_csv(cwd/"{0}/analysis/{1}.tariff-transactions.csv".format(game, game), skipinitialspace=True, delimiter=";")

        # transform the game's data
        
        list_df = kpi3_transformer(tariff_transactions, customers, game)
        
        # apprehend the game's data
        
        tf_type_count = pd.concat([tf_type_count, list_df[0]])
        tf_type_energy = pd.concat([tf_type_energy, list_df[1]])
        tf_type_subs = pd.concat([tf_type_subs, list_df[2]])
        tf_type_price = pd.concat([tf_type_price, list_df[3]])
    except Exception:
        print('Game {} could not be processed due to missing csv files'.format(game))
        continue

# plot and save figure

kpi3_plotter(tf_type_count, tf_type_energy, tf_type_subs, tf_type_price, destination, customers, brokers, group)
