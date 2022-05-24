import pandas as pd


from app.TokenBalance import TokenBalance
from datetime import datetime


now = datetime.now()
token1 = TokenBalance(owner_address='0x0', balance='1', decimals=18, name='test', symbol='test', token_address='0x0', chain='test', block_number=1, timestamp=now)
token2 = TokenBalance(owner_address='0x1', balance='1', decimals=18, name='test2', symbol='test', token_address='0x1', chain='test', block_number=2, timestamp=now)
token3 = TokenBalance(owner_address='0x1', balance='1', decimals=18, name='test2', symbol='test', token_address='0x1', chain='test', block_number=2, timestamp=now)

token1 


input_data = [token1, token2, token3]


def adapt_data_to_pd(data):
    df = pd.DataFrame()

    for token_balance in data:
        if df.empty:
            match = []
        else:
            match = df[(df['owner_address'] == token_balance.owner_address) & (df['token_address'] == token_balance.token_address) & (df['chain'] == token_balance.chain)]

        column_header = str(token_balance.block_number)
        if token_balance.timestamp:
            column_header += "\n" + token_balance.timestamp.strftime("%Y-%m-%d %H:%M:%S")

        if len(match) == 0: # add if no match
            df2 = pd.DataFrame(token_balance.to_pd_dict(), index=[0])
            df = pd.concat([df, df2], ignore_index=True)
        else:
            df.loc[match.index, column_header] = token_balance.formatted_balance
            match.iloc[0][column_header] = token_balance.formatted_balance


    print(df)
    df.to_csv('test.csv')





adapt_data_to_pd(input_data)