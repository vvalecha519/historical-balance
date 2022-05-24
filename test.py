import os
import pandas as pd


from app.TokenBalance import TokenBalance
from datetime import datetime


now = datetime.now()
token1 = TokenBalance(owner_address='0x0', balance='1', decimals=18, name='test', symbol='test', token_address='0x0', chain='test', block_number=1, timestamp=now)
token2 = TokenBalance(owner_address='0x1', balance='1', decimals=18, name='test2', symbol='test', token_address='0x1', chain='test', block_number=2, timestamp=now)
token3 = TokenBalance(owner_address='0x1', balance='1', decimals=18, name='test2', symbol='test', token_address='0x1', chain='test', block_number=2, timestamp=now)


GENERATED_REPORT_PATH = 'generated_reports'


input_data = [token1, token2, token3]


def adapt_to_pd_and_output(data):
    df = pd.DataFrame()

    for token_balance in data:
        if df.empty:
            match = []
        else:
            match = df[(df['owner_address'] == token_balance.owner_address) & (df['token_address'] == token_balance.token_address) & (df['chain'] == token_balance.chain)]

        column_header = 'Block Number: ' + str(token_balance.block_number)
        if token_balance.timestamp:
            column_header += "\n" + token_balance.timestamp.strftime("%Y-%m-%d %H:%M:%S")

        if len(match) == 0: # add if no match
            df2 = pd.DataFrame(token_balance.to_pd_dict(), index=[0])
            df2.loc[0, column_header] = token_balance.formatted_balance 
            df = pd.concat([df, df2], ignore_index=True)
        else:
            df.loc[match.index, column_header] = token_balance.formatted_balance


    df.rename(columns={'owner_address': 'Owner Address', 'token_address': 'Token Address', 'name': 'Name', 'symbol': 'Symbol', 'chain': 'Chain'}, inplace=True)
    
    if not os.path.exists(GENERATED_REPORT_PATH):
            os.makedirs(GENERATED_REPORT_PATH)  # create the directory if it doesn't exist

    output_filename = 'token_balance_report_' + str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) + '.csv'
    
    df.to_csv(os.path.join(GENERATED_REPORT_PATH, output_filename), index=False)





adapt_to_pd_and_output(input_data)