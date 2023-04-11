import pandas as pd

'''
    Transformer for KPI2 broker balancing performance with command line arguments. Returns the melted dataframes of energy and profit to 
    show for each broker the up/down-regulated energy and profit.
'''

def calculate_energy_and_profit_per_broker(transactions):
    transactions_per_broker = transactions[['broker', 'regUsed', 'p2', 'transaction-charge']].groupby(by = ['broker'], as_index = False).sum()

    transactions_per_broker['regUsed'] = transactions_per_broker['regUsed'].apply(lambda x: round(x, 2))
    transactions_per_broker['p2'] = transactions_per_broker['p2'].apply(lambda x: round(x, 2)) # payment from broker to broker
    transactions_per_broker['transaction-charge'] = transactions_per_broker['transaction-charge'].apply(lambda x: round(x, 2)) # payment from or to customer
    transactions_per_broker['profit'] = transactions_per_broker['p2'] + transactions_per_broker['transaction-charge'] # payment of both customer and other broker

    return transactions_per_broker


def total_energy_profit_per_broker(matched_transactions, tarifftype, transactions):
    
    # map the command line argument
    
    tarifftype_pattern = r".*" if tarifftype == 'all' else tarifftype

    # get list of all brokers to show at the end
    
    broker_list = transactions['broker-name'].unique().tolist()
    final_broker_list = [x for x in broker_list if x != 'default broker'] # exclude default broker
    broker_df = pd.DataFrame(final_broker_list, columns = ['broker'])
    
    # divide into up and down regulation
    transactions_up = matched_transactions[(matched_transactions['transaction-type'] == 'PRODUCE') 
                     & (matched_transactions['tariff-type'].str.match(tarifftype_pattern))][['broker'
                                                                                , 'regUsed', 'p2', 'transaction-charge', 'tariff-type']].copy()
    transactions_down = matched_transactions[(matched_transactions['transaction-type'] == 'CONSUME') 
                       & (matched_transactions['tariff-type'].str.match(tarifftype_pattern))][['broker'
                                                                                  , 'regUsed', 'p2', 'transaction-charge', 'tariff-type']].copy()
    # get KPIs by grouping and manipulating data

    energy_and_profit_up = calculate_energy_and_profit_per_broker(transactions_up)
    energy_and_profit_down = calculate_energy_and_profit_per_broker(transactions_down)

    energy_and_profit_up.columns = ['broker', 'upReg', 'pUp_fromBroker', 'pUp_toCustomer', 'profit']
    energy_and_profit_down.columns = ['broker', 'downReg', 'pDown_toBroker', 'pDown_fromCustomer', 'profit']

    energy_and_profit_up_and_down = broker_df.merge(energy_and_profit_up, on = ['broker'], how = 'left')
    energy_and_profit_up_and_down = energy_and_profit_up_and_down.merge(energy_and_profit_down, on = ['broker'], how = 'left')

    # use melt to reshape the dataframe
    melt_energy_up_and_down_per_broker = pd.melt(energy_and_profit_up_and_down, id_vars=['broker'], value_vars=['upReg', 'downReg'])
    melt_profit_up_and_down_per_broker = pd.melt(energy_and_profit_up_and_down, id_vars=['broker'], value_vars=['pUp_fromBroker', 'profit_x', 'pDown_toBroker', 'profit_y'])
    
    return [melt_energy_up_and_down_per_broker, melt_profit_up_and_down_per_broker]