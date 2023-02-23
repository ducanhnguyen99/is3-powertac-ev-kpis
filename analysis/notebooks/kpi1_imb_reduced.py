from pathlib import Path
import pandas as pd
import sys

from analysis_tools.transformers.ev_kpi_parser import (tf_ba_transformer)
from analysis_tools.analyzers.imbalance_reduced_plotter import (kpi1_plotter)

# analyzes via boxplot the hourly reduction of imbalances through balancing actions of certain tariff types
# command line arguments passed to the script

powertype = sys.argv[1] # tariff type e.g. BATTERY_STORAGE, THERMAL_STORAGE_CONSUMPTION etc.
imbalance = sys.argv[2] # regulation type e.g imbalance = shortage of energy -> up, imbalance = excess of energy -> down
group = sys.argv[3] # group/folder of games to analyze e.g. finals_2022

# in the future specify the number of games here, e.g. games 4 6 7 8 9 then create a csv with these games or take that input instead of reading all games from games.csv

cwd = Path('/home/danguyen/data/powertac/{}'.format(group))
games = pd.read_csv(cwd/"games.csv", skipinitialspace=True, delimiter=",")
list_games = games.iloc[:, 0].tolist()

# for each game id create a boxplot and save it to the destination
for game in list_games:
    try:
        tf_transactions = pd.read_csv(cwd/"{0}/{1}.tariff-transactions.csv".format(game, game), skipinitialspace=True, delimiter=";")
        balancing_actions = pd.read_csv(cwd/"{0}/{1}.broker-balancing-actions.csv".format(game, game), skipinitialspace=True, delimiter=";", decimal = ",")
        # usually with analysis folder if automatically extracted but my manual one does not have this
        #tf_transactions = pd.read_csv(cwd/"{0}/analysis/{1}.tariff-transactions.csv".format(game, game), skipinitialspace=True, delimiter=";")
        #balancing_actions = pd.read_csv(cwd/"{0}/analysis/{1}.broker-balancing-actions.csv".format(game, game), skipinitialspace=True, delimiter=";", decimal = ".")
        final_df = tf_ba_transformer(tf_transactions, balancing_actions)
        destination = Path('/home/danguyen/data/powertac/analysis/output')
        kpi1_plotter(final_df, powertype,imbalance, destination/"{0}_{1}_{2}_imbalance_reduced.png".format(game, powertype, imbalance), game)
    except Exception:
        print('Game {} could not be processed due to missing csv files'.format(game))
        continue
        
       

