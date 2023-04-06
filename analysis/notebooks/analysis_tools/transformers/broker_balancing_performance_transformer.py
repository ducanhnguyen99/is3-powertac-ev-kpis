import pandas as pd

'''
    Transformer for KPI2 broker balancing performance with command line arguments. Returns the melted dataframes of energy and profit to 
    show for each broker the up/down-regulated energy and profit.
'''

def calculate_energy_and_profit(transactions):
    transactions = transactions[['broker', 'regUsed', 'p2', 'transaction-charge']]
    transactions = transactions.groupby(by = ['broker'], as_index = False).sum()

    transactions['regUsed'] = transactions['regUsed'].apply(lambda x: round(x, 2))
    transactions['p2'] = transactions['p2'].apply(lambda x: round(x, 2)) # payment from broker to broker
    transactions['transaction-charge'] = transactions['transaction-charge'].apply(lambda x: round(x, 2)) # payment from or to customer
    transactions['profit'] = transactions['p2'] + transactions['transaction-charge'] # payment of both customer and other broker

    return transactions


def total_energy_profit_per_broker(matched_transactions, tarifftype, tariff_transactions):
    
    # map the command line argument
    
    tarifftype_pattern = r".*" if tarifftype == 'all' else tarifftype

    # get list of all brokers to show at the end
    
    broker_list = tariff_transactions['broker-name'].unique().tolist()
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

    energy_and_profit_up = calculate_energy_and_profit(transactions_up)
    energy_and_profit_down = calculate_energy_and_profit(transactions_down)

    energy_and_profit_up.columns = ['broker', 'upReg', 'pUp_fromBroker', 'pUp_toCustomer', 'profit']
    energy_and_profit_down.columns = ['broker', 'downReg', 'pDown_toBroker', 'pDown_fromCustomer', 'profit']

    df_merge = broker_df.merge(energy_and_profit_up, on = ['broker'], how = 'left')
    df_merge = df_merge.merge(energy_and_profit_down, on = ['broker'], how = 'left')

    # use melt to reshape the dataframe
    df_melt_energy = pd.melt(df_merge, id_vars=['broker'], value_vars=['upReg', 'downReg'])
    df_melt_profit = pd.melt(df_merge, id_vars=['broker'], value_vars=['pUp_fromBroker', 'profit_x', 'pDown_toBroker', 'profit_y'])
    
    return [df_melt_energy, df_melt_profit]