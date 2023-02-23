from pathlib import Path
import pandas as pd
import numpy as np
import sys

from analysis_tools.transformers.ev_kpi_parser import (tf_ba_transformer)
from analysis_tools.analyzers.imbalance_reduced_plotter import (kpi1_plotter)

powertype = sys.argv[1]
imbalance = sys.argv[2]
group = sys.argv[3]
brokers = sys.argv[4]

path = '/data/passive/powertac/games/{}'.format(group)
destination = Path('/home/danguyen/data/powertac/analysis/output_all')
cwd = Path(path)

games = pd.read_csv(cwd/"Power-TAC-finals-2022-csv-file.csv", skipinitialspace=True, delimiter=";")
games = games.fillna("na")

broker_list = brokers.split(",")
mask = games[broker_list].apply(lambda x: x.str.contains('na')).sum(axis=1) == 0
games = games[(mask) & (games["gameSize"] == len(broker_list))]
list_games = games.iloc[:, 1].tolist()


final_df = pd.DataFrame()

for game in list_games:
    try:
        tf_transactions = pd.read_csv(cwd/"{0}/analysis/{1}.tariff-transactions.csv".format(game, game), skipinitialspace=True, delimiter=";")
        balancing_actions = pd.read_csv(cwd/"{0}/analysis/{1}.broker-balancing-actions.csv".format(game, game), skipinitialspace=True, delimiter=";", decimal = ".")
        
        #tf_transactions = pd.read_csv(cwd/"{0}/{1}.tariff-transactions.csv".format(game, game), skipinitialspace=True, delimiter=";")
        #balancing_actions = pd.read_csv(cwd/"{0}/{1}.broker-balancing-actions.csv".format(game, game), skipinitialspace=True, delimiter=";", decimal = ",")
        final_df = pd.concat([final_df, tf_ba_transformer(tf_transactions, balancing_actions)])
    except Exception:
        print('Game {} could not be processed due to missing csv files'.format(game))
        continue
        
kpi1_plotter(final_df, powertype,imbalance, destination/"{0}_{1}_{2}_{3}_imbalance_reduced.png".format(group, powertype, imbalance, brokers), group)