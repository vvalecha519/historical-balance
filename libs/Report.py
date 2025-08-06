import os
import csv
import time
import pandas as pd
import io

from libs.Moralis import Moralis
from app.TokenBalance import TokenBalance
from datetime import datetime, timedelta
from itertools import groupby
from flask import make_response


GENERATED_REPORT_PATH = 'generated_reports'


CHAINS = [{'id': 'eth', 'name': 'Ethereum', 'symbol': 'ETH', 'avg_blocks_per_day': 6300},
            {'id': 'matic','name': 'Polygon (Matic)', 'symbol': 'MATIC', 'avg_blocks_per_day': 24 * 60 * 60 / 3},
            {'id': 'avalanche', 'name': 'Avalanche', 'symbol': 'AVAX', 'avg_blocks_per_day': 24 * 60 * 60 / 3}]


class Report:
    wallet_sheet = None
    contracts = None

    output_data = []

    def __init__(self, file_obj_or_path):
        # Handle both file objects (from memory) and file paths
        if hasattr(file_obj_or_path, 'read'):
            # It's a file object
            xls = pd.ExcelFile(file_obj_or_path)
        else:
            # It's a file path (for backward compatibility)
            xls = pd.ExcelFile(file_obj_or_path)
        
        self.wallet_sheet = pd.read_excel(xls, 0)
        try:
            self.contracts = pd.read_excel(xls, 1).iloc[:, 0]
        except:
            self.contracts = None

    # Inclusive range
    def generate_token_balance_report_in_date_range(self, start_date, end_date):
        date_range = [start_date + timedelta(days=x) for x in range(0, (end_date-start_date).days + 1)]
        output_data = []
        for date in date_range:
            block_no = Moralis.get_block_number_from_datetime(date)
            time.sleep(1)  # sleep for 1 second to avoid rate limit
            output_data.extend(self.generate_token_balance_report(block_no, date))
        return output_data


    # Inclusive range
    def generate_token_balance_report_in_block_range(self, start_block, end_block):
        output_data = []
        start_block = int(start_block)
        end_block = int(end_block)
        for block_no in range(start_block, end_block + 1):
            output_data.extend(self.generate_token_balance_report(block_no))
        return output_data



    def generate_token_balance_report(self, block_no, timestamp=None):
        output_data = []
        #hardcode wallet address    
        wallet_address = '0x0000000000000000000000000000000000000000'
        
        for wallet_data in self.wallet_sheet.itertuples():
            print(wallet_data)
            wallet_address = wallet_data.address

            chain_data = None
            for chain in CHAINS:
                if chain.get('id') == wallet_data.chain.lower():
                    chain_data = chain

            native_balance = Moralis.get_native_balance(wallet_address, chain_data.get('id'), block_no)
            token_balance = TokenBalance()
            token_balance.owner_address = wallet_address
            token_balance.balance = native_balance['balance']
            token_balance.decimals = 18
            token_balance.name = chain_data.get('name')
            token_balance.symbol = chain_data.get('symbol')
            token_balance.token_address = 'NATIVE ' + chain_data.get('symbol')
            token_balance.chain = chain_data.get('id')
            token_balance.block_number = block_no
            token_balance.timestamp = timestamp

            token_balance.generate_formatted_balance()

            output_data.append(token_balance)

            time.sleep(1)  # sleep for 1 second to avoid rate limit

            data = Moralis.get_all_erc20_tokens(wallet_address, chain_data.get('id'), block_no)
            for balance_data in data:
                token_address = balance_data['token_address']

                in_contracts = False

                if self.contracts is None:
                    in_contracts = True
                else:
                    in_contracts = len([x for x in self.contracts if x.lower() == token_address.lower()]) > 0

                if in_contracts:
                    try:
                        token_balance = TokenBalance()
                        token_balance.owner_address = wallet_address
                        token_balance.balance = balance_data['balance']
                        token_balance.decimals = balance_data['decimals']
                        token_balance.name = balance_data['name']
                        token_balance.symbol = balance_data['symbol']
                        token_balance.token_address = balance_data['token_address']
                        token_balance.chain = chain_data.get('id')
                        token_balance.block_number = block_no
                        token_balance.timestamp = timestamp

                        print('')
                        print(token_balance.balance)
                        print(token_balance.decimals)
                        print(token_balance.name)

                        token_balance.generate_formatted_balance()

                        output_data.append(token_balance)
                    except:
                        continue

            time.sleep(1)  # sleep for 1 second to avoid rate limit
                
        return output_data


    def adapt_to_pd_and_output(self, data):
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
        
        # Create CSV in memory instead of saving to file
        output_filename = 'token_balance_report_' + str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) + '.csv'
        
        # Convert DataFrame to CSV string
        csv_string = df.to_csv(index=False)
        
        # Create a response with the CSV data
        response = make_response(csv_string)
        response.headers["Content-Disposition"] = f"attachment; filename={output_filename}"
        response.headers["Content-type"] = "text/csv"
        
        return response

    

'''

    def output_report(self, output_data):
        if not os.path.exists(GENERATED_REPORT_PATH):
            os.makedirs(GENERATED_REPORT_PATH)  # create the directory if it doesn't exist

        output_filename = 'token_balance_report_' + str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) + '.csv'

        with open(os.path.join(GENERATED_REPORT_PATH, output_filename), mode='w') as output_file:
            output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if output_data[1].timestamp is None:
                output_writer.writerow(['Wallet Address', 'Contract Address','Name', 'Symbol', 'Balance', 'Chain', 'Block Number'])
                for entry in output_data:
                    output_writer.writerow([entry.owner_address, entry.token_address, entry.name, entry.symbol, entry.formatted_balance, entry.chain.upper(), entry.block_number])
            else:
                output_writer.writerow(['Wallet Address', 'Contract Address','Name', 'Symbol', 'Balance', 'Chain', 'Block Number', 'Timestamp'])
                for entry in output_data:
                    output_writer.writerow([entry.owner_address, entry.token_address, entry.name, entry.symbol, entry.formatted_balance, entry.chain.upper(), entry.block_number, entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')])


        return output_filename
'''
