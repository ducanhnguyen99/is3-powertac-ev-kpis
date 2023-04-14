import pandas as pd
from ..types import TariffTransactionFrame, TariffRegulationTransactionFrame, BalancingActionFrame, PivotBalancingActionFrame, MatchedTransactionFrame

'''
    Transformer to create a merged dataset to identify the tariff/transaction type of the balancing action and the balancing charge for the 
    customer.
'''

def regulation_transactions(transactions: TariffTransactionFrame) -> TariffRegulationTransactionFrame:
    # aggregate tariff transactions corresponding to regulation
    transactions_for_regulation = transactions[transactions['transaction-regulation'] == 1].copy()

    transactions_for_regulation = transactions_for_regulation[['timeslot'
        , 'broker-name'
        , 'tariff-type'
        , 'transaction-type'
        , 'transaction-kWh'
        , 'transaction-charge']]
    regulation_transactions_agg = transactions_for_regulation.groupby(by = ['timeslot'
        , 'broker-name'
        , 'tariff-type'
        , 'transaction-type'], as_index=False).sum().copy()
    regulation_transactions_agg = regulation_transactions_agg[regulation_transactions_agg['transaction-kWh'] != 0]
    return regulation_transactions_agg

def pivot_balancing_actions(balancing_actions: BalancingActionFrame) -> PivotBalancingActionFrame:
    # pivot balancing actions longer to have one broker column with the respective loads and payments
    iterations = range(int((len(balancing_actions.columns)-6)/7))

    pivoted_balancing_actions = pd.DataFrame()

    # for the i the number of brokers pivot the required columns
    for i in iterations:
        common_columns = balancing_actions.iloc[:, [0,3]]
        broker_columns = balancing_actions.iloc[:, 6+i*7:(i+1)*7+6]
        broker_columns.columns = ['broker', 'netLoad', 'regOffered', 'regUsed', 'baseCost', 'p1', 'p2']
        df_merge = pd.concat([common_columns,broker_columns], axis=1)
        pivoted_balancing_actions = pd.concat([pivoted_balancing_actions, df_merge])

    pivoted_balancing_actions = pivoted_balancing_actions[pivoted_balancing_actions["regUsed"] != 0 ]
    return pivoted_balancing_actions
def matched_balancing_transactions(transactions: TariffTransactionFrame, balancing_actions: BalancingActionFrame) -> MatchedTransactionFrame:
    pivoted_balancing_actions = pivot_balancing_actions(balancing_actions)
    regulation_transactions_agg = regulation_transactions(transactions)
    
    # merge datasets
    matched_transactions = pivoted_balancing_actions.merge(regulation_transactions_agg, left_on=['ts', 'broker'], right_on=['timeslot', 'broker-name'])
    
    return matched_transactions
