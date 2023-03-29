from pathlib import Path
import pandas as pd
import numpy as np
import sys

from analysis_tools.transformers.balancing_kpi_transformer import (tf_ba_transformer)
from analysis_tools.transformers.imbalance_reduced_transformer import (kpi1_transformer)
from analysis_tools.analyzers.imbalance_reduced_plotter import (kpi1_plotter)
from analysis_tools.utility import (filter_games)

'''
    Execution file for the analysis of imbalance reduced through balancing actions of brokers (KPI1).
'''

# receive command line arguments

tarifftype = sys.argv[1]
imbalance = sys.argv[2]
group = sys.argv[3]
brokers = sys.argv[4]

# set read and save path

path = '/data/passive/powertac/games/{}'.format(group)
destination = Path('/home/danguyen/data/powertac/analysis/output_all')
cwd = Path(path)
games_csv = "Power-TAC-finals-2022-csv-file.csv"

# read games that include our brokers

list_games = filter_games(cwd, games_csv, brokers)

final_df = pd.DataFrame() #initialize 

# aggregate data of every game into one data frame and merge tariff transactions and balancing actions

for game in list_games:
    try:
        tf_transactions = pd.read_csv(cwd/"{0}/analysis/{1}.tariff-transactions.csv".format(game, game), skipinitialspace=True, delimiter=";")
        balancing_actions = pd.read_csv(cwd/"{0}/analysis/{1}.broker-balancing-actions.csv".format(game, game), skipinitialspace=True, delimiter=";", decimal = ".")

        final_df = pd.concat([final_df, tf_ba_transformer(tf_transactions, balancing_actions)]) # apprehend and transform each game's data
    except Exception:
        print('Game {} could not be processed due to missing csv files'.format(game))
        continue

# transform and plot the kpi
kpi1_perc = kpi1_transformer(final_df, tarifftype, imbalance) 
kpi1_plotter(kpi1_perc, tarifftype,imbalance, destination/"{0}_{1}_{2}_{3}_imbalance_reduced.png".format(group, tarifftype, imbalance, brokers), group, brokers)