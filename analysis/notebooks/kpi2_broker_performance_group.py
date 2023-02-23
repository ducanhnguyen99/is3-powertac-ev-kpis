from pathlib import Path
import pandas as pd
import numpy as np
import sys

from analysis_tools.transformers.ev_kpi_parser import (tf_ba_transformer)
from analysis_tools.transformers.broker_performance_transformer_group import (kpi2_transformer)
from analysis_tools.analyzers.broker_performance_plotter_group import (kpi2_plotter)

powertype = sys.argv[1]
group = sys.argv[2]
brokers = sys.argv[3]

path = '/data/passive/powertac/games/{}'.format(group)
destination = Path('/home/danguyen/data/powertac/analysis/output_all')
cwd = Path(path)

games = pd.read_csv(cwd/"Power-TAC-finals-2022-csv-file.csv", skipinitialspace=True, delimiter=";")
games = games.fillna("na")

broker_list = brokers.split(",")
mask = games[broker_list].apply(lambda x: x.str.contains('na')).sum(axis=1) == 0
games = games[(mask) & (games["gameSize"] == len(broker_list))]
list_games = games.iloc[:, 1].tolist()

#experiment_path = '/home/danguyen/data/powertac/{}'.format(group)
#destination = Path('/home/danguyen/data/powertac/analysis/output')
#cwd = Path(experiment_path)
#games = pd.read_csv(cwd/"games.csv", skipinitialspace=True, delimiter=",")
#list_games = games.iloc[:, 0].tolist()

df_melt_energy = pd.DataFrame()
df_melt_profit = pd.DataFrame()
df_melt_perKwh = pd.DataFrame()

for game in list_games:
    try:
        
        tf_transactions = pd.read_csv(cwd/"{0}/analysis/{1}.tariff-transactions.csv".format(game, game), skipinitialspace=True, delimiter=";")
        balancing_actions = pd.read_csv(cwd/"{0}/analysis/{1}.broker-balancing-actions.csv".format(game, game), skipinitialspace=True, delimiter=";", decimal = ".")
        
        #tf_transactions = pd.read_csv(cwd/"{0}/{1}.tariff-transactions.csv".format(game, game), skipinitialspace=True, delimiter=";")
        #balancing_actions = pd.read_csv(cwd/"{0}/{1}.broker-balancing-actions.csv".format(game, game), skipinitialspace=True, delimiter=";", decimal = ",")
        # usually with analysis folder if automatically extracted but my manual one does not have this
        #tf_transactions = pd.read_csv(cwd/"{0}/analysis/{1}.tariff-transactions.csv".format(game, game), skipinitialspace=True, delimiter=";")
        #balancing_actions = pd.read_csv(cwd/"{0}/analysis/{1}.broker-balancing-actions.csv".format(game, game), skipinitialspace=True, delimiter=";", decimal = ".")
        final_df = tf_ba_transformer(tf_transactions, balancing_actions)
        list_df_melt = kpi2_transformer(final_df, powertype, game, tf_transactions)
        df_melt_energy = pd.concat([df_melt_energy, list_df_melt[0]])
        df_melt_profit = pd.concat([df_melt_profit, list_df_melt[1]])
        df_melt_perKwh = pd.concat([df_melt_perKwh, list_df_melt[2]])
    except Exception:
        print('Game {} could not be processed due to missing csv files'.format(game))
        continue
        
kpi2_plotter(df_melt_energy, df_melt_profit, df_melt_perKwh, powertype, destination/"{0}_{1}_{2}_broker_performance.png".format(group, powertype, brokers), group)
       