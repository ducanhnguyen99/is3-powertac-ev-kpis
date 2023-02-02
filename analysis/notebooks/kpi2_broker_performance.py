from pathlib import Path
import pandas as pd
import numpy as np
import sys

from analysis_tools.transformers.ev_kpi_parser import (tf_ba_transformer)
from analysis_tools.analyzers.broker_performance_plotter import (kpi2_plotter)

power_type = sys.argv[1]
group = sys.argv[2]

experiment_path = '/home/danguyen/data/powertac/{}'.format(group)
cwd = Path(experiment_path)
games = pd.read_csv(cwd/"games.csv", skipinitialspace=True, delimiter=",")
list_games = games.iloc[:, 0].tolist()

for game in list_games:
    try:
        tf_transactions = pd.read_csv(cwd/"{0}/{1}.tariff-transactions.csv".format(game, game), skipinitialspace=True, delimiter=";")
        balancing_actions = pd.read_csv(cwd/"{0}/{1}.broker-balancing-actions.csv".format(game, game), skipinitialspace=True, delimiter=";", decimal = ",")
        # usually with analysis folder if automatically extracted but my manual one does not have this
        #tf_transactions = pd.read_csv(cwd/"{0}/analysis/{1}.tariff-transactions.csv".format(game, game), skipinitialspace=True, delimiter=";")
        #balancing_actions = pd.read_csv(cwd/"{0}/analysis/{1}.broker-balancing-actions.csv".format(game, game), skipinitialspace=True, delimiter=";", decimal = ".")
        final_df = tf_ba_transformer(tf_transactions, balancing_actions)
        destination = Path('/home/danguyen/data/powertac/analysis/output')
        kpi2_plotter(final_df, power_type, destination/"{0}_{1}_broker_performance.png".format(game, power_type), game, tf_transactions)
    except IndexError:
        print('Game {} could not be processed due to missing csv files'.format(game))
        
        