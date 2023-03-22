from pathlib import Path
import pandas as pd
import numpy as np
import sys

from analysis_tools.transformers.tariff_type_transformer_group import (kpi3_transformer)
from analysis_tools.analyzers.tariff_type_plotter_group import (kpi3_plotter)

# receive command line arguments

group = sys.argv[1]
brokers = sys.argv[2]

# set read and save path

path = '/data/passive/powertac/games/{}'.format(group)
destination = Path('/home/danguyen/data/powertac/analysis/output_all')
cwd = Path(path)

# read games that include our brokers

games = pd.read_csv(cwd/"Power-TAC-finals-2022-csv-file.csv", skipinitialspace=True, delimiter=";")
games = games.fillna("na") # used for masking

broker_list = brokers.split(",")
mask = games[broker_list].apply(lambda x: x.str.contains('na')).sum(axis=1) == 0 # mask filters all games where the desired brokers exist therefore the broker columns should contain no na's
games = games[(mask) & (games["gameSize"] == len(broker_list))] # check that it is this exact number of brokers only
list_games = games.iloc[:, 1].tolist() # collect identified game ids

# initialize our dataframes aggregating the games' data

tf_type_count = pd.DataFrame()
tf_type_energy = pd.DataFrame()
tf_type_subs = pd.DataFrame()
tf_type_price = pd.DataFrame()

# aggregate data of every game and transform

for game in list_games:
    try:
        
        tf_transactions = pd.read_csv(cwd/"{0}/analysis/{1}.tariff-transactions.csv".format(game, game), skipinitialspace=True, delimiter=";")

        # transform the game's data
        
        list_df = kpi3_transformer(tf_transactions, game)
        
        # apprehend the game's data
        
        tf_type_count = pd.concat([tf_type_count, list_df[0]])
        tf_type_energy = pd.concat([tf_type_energy, list_df[1]])
        tf_type_subs = pd.concat([tf_type_subs, list_df[2]])
        tf_type_price = pd.concat([tf_type_price, list_df[3]])
    except Exception:
        print('Game {} could not be processed due to missing csv files'.format(game))
        continue

# plot and save figure

kpi3_plotter(tf_type_count, tf_type_energy, tf_type_subs, tf_type_price, destination, brokers, group)
