from pathlib import Path
import pandas as pd
import sys

from analysis_tools.transformers.balancing_transactions_merger import (matched_balancing_transactions)
from analysis_tools.transformers.broker_balancing_performance_transformer import (total_energy_profit_per_broker)
from analysis_tools.analyzers.broker_balancing_performance_plotter import (broker_balancing_performance_boxplot)
from analysis_tools.utility import (filter_games)

'''
    Execution file for the analysis of brokers balancing actions (KPI2).
'''

# receive command line arguments

tarifftype = sys.argv[1]
group = sys.argv[2]
brokers = sys.argv[3]

# set read and save path

path = '/data/passive/powertac/games/{}'.format(group)
destination = Path('/home/danguyen/data/powertac/analysis/output_all')
cwd = Path(path)
games_csv = "Power-TAC-finals-2022-csv-file.csv"

# read games that include our brokers

list_games = filter_games(cwd, games_csv, brokers)

# initialize our dataframes aggregating the games' data

df_melt_energy = pd.DataFrame()
df_melt_profit = pd.DataFrame()

# aggregate data of every game into one data frame and transform

for game in list_games:
    try:
        
        tariff_transactions = pd.read_csv(cwd/"{0}/analysis/{1}.tariff-transactions.csv".format(game, game), skipinitialspace=True, delimiter=";")
        balancing_actions = pd.read_csv(cwd/"{0}/analysis/{1}.broker-balancing-actions.csv".format(game, game), skipinitialspace=True, delimiter=";", decimal = ".")
        
        # transform the game's data
    
        final_df = matched_balancing_transactions(tariff_transactions, balancing_actions)
        list_df_melt = total_energy_profit_per_broker(final_df, tarifftype, tariff_transactions)
        
         # apprehend the game's data
        
        df_melt_energy = pd.concat([df_melt_energy, list_df_melt[0]])
        df_melt_profit = pd.concat([df_melt_profit, list_df_melt[1]])
    except Exception:
        print('Game {} could not be processed due to missing csv files'.format(game))
        continue
        
# plot the kpi
        
broker_balancing_performance_boxplot(df_melt_energy, df_melt_profit, tarifftype, destination/"{0}_{1}_{2}_broker_performance.png".format(group, tarifftype, brokers), group)
       