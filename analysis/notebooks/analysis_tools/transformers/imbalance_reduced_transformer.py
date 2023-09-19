from ..types import MatchedTransactionFrame, ImbalanceAmountFrame, RegulationAmountFrame, ImbalanceRegulationFrame
from typing import List
import os
import typing
import pandas as pd
from analysis_tools.transformers.balancing_transactions_merger import (matched_balancing_transactions)

'''
    Transformer for KPI1 imbalance reduced through balancing actions with command line arguments. Returns the dataframe showing the % share of 
    imbalance reduced through balancing action in each timeslot.
'''

def imbalance_amount_per_timeslot(matched_transactions: MatchedTransactionFrame, imb_pattern: str) -> ImbalanceAmountFrame:
    imbalance_amount = matched_transactions[(matched_transactions['transaction-type'].str.match(imb_pattern)) ][['ts', 'totalImbalance']].copy()
    imbalance_amount['totalImbalance'] = abs(imbalance_amount['totalImbalance'].astype(int))
    imbalance_amount = imbalance_amount.groupby(by = ['ts'], as_index = False).sum()
    return imbalance_amount
def regulation_amount_per_timeslot(matched_transactions: MatchedTransactionFrame, imb_pattern: str, tarifftype_pattern: str)-> RegulationAmountFrame:
    regulation_amount = matched_transactions[(matched_transactions['transaction-type'].str.match(imb_pattern))
                                       & (matched_transactions['tariff-type'].str.match(tarifftype_pattern))][['ts', 'regUsed']].copy()
    regulation_amount['regUsed'] = abs(regulation_amount['regUsed'])
    regulation_amount = regulation_amount.groupby(by = ['ts'], as_index = False).sum()
    return regulation_amount


def imbalance_to_regulation_amount_per_timeslot(matched_transactions: MatchedTransactionFrame, tarifftype: str, imbalance: str) -> ImbalanceRegulationFrame:
    
    # map the command line arguments and aggregate per timeslot
    
    imb_pattern = r".*" if imbalance == 'both' else 'PRODUCE' if imbalance == 'up' else 'CONSUME'
    tarifftype_pattern = r".*" if tarifftype == 'all' else tarifftype

    imbalance_amount = imbalance_amount_per_timeslot(matched_transactions, imb_pattern)
    regulation_amount = regulation_amount_per_timeslot(matched_transactions, imb_pattern, tarifftype_pattern)
    
    imbalance_to_regulation = imbalance_amount.merge(regulation_amount, on = ['ts'], how = 'left')

    # calculate the percentage of imbalance reduced in all timeslots reduced to a 24-hour interval
    imbalance_to_regulation['hour'] = imbalance_to_regulation['ts'] % 24
    imbalance_to_regulation['perc'] = imbalance_to_regulation['regUsed'] / imbalance_to_regulation['totalImbalance']
    
    return imbalance_to_regulation


# aggregate data of every game into one data frame and merge tariff transactions and balancing actions
def match_all_games_transactions(list_games: List[str], matched_transactions: MatchedTransactionFrame, cwd: typing.Union[str, os.PathLike]) -> MatchedTransactionFrame:
    for game in list_games:
        try:
            transactions = pd.read_csv(cwd/"{0}/analysis/{1}.tariff-transactions.csv".format(game, game), skipinitialspace=True, delimiter=";")
            balancing_actions = pd.read_csv(cwd/"{0}/analysis/{1}.broker-balancing-actions.csv".format(game, game), skipinitialspace=True, delimiter=";", decimal = ".")
            matched_transactions = pd.concat([matched_transactions, matched_balancing_transactions(transactions, balancing_actions)]) # apprehend and transform each game's data
        except Exception:
            print('Game {} could not be processed due to missing csv files'.format(game))
            continue
    return matched_transactions