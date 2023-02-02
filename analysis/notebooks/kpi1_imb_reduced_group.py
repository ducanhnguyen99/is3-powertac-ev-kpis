from pathlib import Path
import pandas as pd
import numpy as np
import sys

from analysis_tools.transformers.ev_kpi_parser import (tf_ba_transformer)
from analysis_tools.analyzers.imbalance_reduced_plotter import (kpi1_plotter)

powertype = sys.argv[1]
imbalance = sys.argv[2]
group = sys.argv[3]

experiment_path = '/home/danguyen/data/powertac/{}'.format(group)
destination = Path('/home/danguyen/data/powertac/analysis/output')
cwd = Path(experiment_path)
games = pd.read_csv(cwd/"games.csv", skipinitialspace=True, delimiter=",")
list_games = games.iloc[:, 0].tolist()

final_df = pd.DataFrame()

for game in list_games:
    try:
        tf_transactions = pd.read_csv(cwd/"{0}/{1}.tariff-transactions.csv".format(game, game), skipinitialspace=True, delimiter=";")
        balancing_actions = pd.read_csv(cwd/"{0}/{1}.broker-balancing-actions.csv".format(game, game), skipinitialspace=True, delimiter=";", decimal = ",")
        # usually with analysis folder if automatically extracted but my manual one does not have this
        #tf_transactions = pd.read_csv(cwd/"{0}/analysis/{1}.tariff-transactions.csv".format(game, game), skipinitialspace=True, delimiter=";")
        #balancing_actions = pd.read_csv(cwd/"{0}/analysis/{1}.broker-balancing-actions.csv".format(game, game), skipinitialspace=True, delimiter=";", decimal = ".")
        final_df = pd.concat([final_df, tf_ba_transformer(tf_transactions, balancing_actions)])
    except IndexError:
        print('Game {} could not be processed due to missing csv files'.format(game))
        
kpi1_plotter(final_df, powertype,imbalance, destination/"{0}_{1}_{2}_imbalance_reduced.png".format(group, powertype, imbalance), group)