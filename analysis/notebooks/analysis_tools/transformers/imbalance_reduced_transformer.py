from analysis.notebooks.analysis_tools.types import MatchedTransactionFrame, ImbalanceAmountFrame, RegulationAmountFrame, ImbalanceRegulationFrame

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