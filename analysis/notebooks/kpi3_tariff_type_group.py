from pathlib import Path
import pandas as pd
import numpy as np
import sys

from analysis_tools.transformers.tariff_type_transformer_group import (kpi3_transformer)
from analysis_tools.analyzers.tariff_type_plotter_group import (kpi3_plotter)

group = sys.argv[1]
brokers = sys.argv[2]

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

df_melt_count = pd.DataFrame()
df_melt_energy = pd.DataFrame()
df_melt_subs = pd.DataFrame()

for game in list_games:
    try:
        
        tf_transactions = pd.read_csv(cwd/"{0}/analysis/{1}.tariff-transactions.csv".format(game, game), skipinitialspace=True, delimiter=";")

        list_df_melt = kpi3_transformer(tf_transactions, game)
        df_melt_count = pd.concat([df_melt_count, list_df_melt[0]])
        df_melt_energy = pd.concat([df_melt_energy, list_df_melt[1]])
        df_melt_subs = pd.concat([df_melt_subs, list_df_melt[2]])
    except Exception:
        print('Game {} could not be processed due to missing csv files'.format(game))
        continue
        
kpi3_plotter(df_melt_count, df_melt_energy, df_melt_subs, destination/"{0}_{1}_tariff_type.png".format(group, brokers), group)
       