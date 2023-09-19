from pathlib import Path
import pandas as pd
import sys


from analysis_tools.transformers.imbalance_reduced_transformer import (imbalance_to_regulation_amount_per_timeslot)
from analysis_tools.transformers.imbalance_reduced_transformer import (match_all_games_transactions)
from analysis_tools.analyzers.treatment_imbalance_reduced_boxplotter import (treatment_imbalance_reduced_per_timeslot_boxplot)
from analysis_tools.analyzers.treatment_imbalance_reduced_violinplotter import (treatment_imbalance_reduced_per_timeslot_violinplot)
from analysis_tools.utility import (filter_games)

'''
    Execution file for the comparison of imbalance reduced through balancing actions of brokers between different treatments.
'''

# receive command line arguments (currently manual here, depending on requirements later)

group = "finals_2022"
tarifftype = "all"
imbalance = "up"

# set read and save path

path = '/data/passive/powertac/games/{}'.format(group)
destination = Path('/home/danguyen/data/powertac/analysis/output_all')
cwd = Path(path)
games_csv = "Power-TAC-finals-2022-csv-file.csv"

# TREATMENT 1: read games that include these brokers 

brokers = "VidyutVanika,IS3,COLDPOWER22,TUC_TAC22,Mertacor22"
list_games = filter_games(cwd, games_csv, brokers)

matched_transactions = pd.DataFrame() #initialize
matched_transactions = match_all_games_transactions(list_games, matched_transactions, cwd)

# transform the KPI
imbalance_to_regulation1 = imbalance_to_regulation_amount_per_timeslot(matched_transactions, tarifftype, imbalance)


# TREATMENT 2: read games that include these brokers 

brokers = "VidyutVanika,TUC_TAC22,Mertacor22"
list_games = filter_games(cwd, games_csv, brokers)

matched_transactions = pd.DataFrame() #initialize
matched_transactions = match_all_games_transactions(list_games, matched_transactions, cwd)

# transform the KPI
imbalance_to_regulation2 = imbalance_to_regulation_amount_per_timeslot(matched_transactions, tarifftype, imbalance)


# TREATMENT 3: read games that include these brokers 

brokers = "VidyutVanika,TUC_TAC22"
list_games = filter_games(cwd, games_csv, brokers)

matched_transactions = pd.DataFrame() #initialize
matched_transactions = match_all_games_transactions(list_games, matched_transactions, cwd)

# transform the KPI
imbalance_to_regulation3 = imbalance_to_regulation_amount_per_timeslot(matched_transactions, tarifftype, imbalance)


# plot the KPIs of the treatments
treatment_imbalance_reduced_per_timeslot_boxplot(imbalance_to_regulation1, imbalance_to_regulation2, imbalance_to_regulation3, tarifftype,imbalance, destination/"{0}_{1}_{2}_{3}_imbalance_reduced_boxplot.png".format(group, tarifftype, imbalance, brokers), group, brokers)
treatment_imbalance_reduced_per_timeslot_violinplot(imbalance_to_regulation1, imbalance_to_regulation2, imbalance_to_regulation3, tarifftype,imbalance, destination/"{0}_{1}_{2}_{3}_imbalance_reduced_violinplot.png".format(group, tarifftype, imbalance, brokers), group, brokers)
