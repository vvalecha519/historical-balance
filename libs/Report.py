import os
import csv
import time
import pandas as pd

from libs.Moralis import Moralis
from app.TokenBalance import TokenBalance
from datetime import datetime, timedelta


GENERATED_REPORT_PATH = 'generated_reports'


CHAINS = [{'id': 'eth', 'name': 'Native Ethereum', 'symbol': 'Native ETH', 'avg_blocks_per_day': 6300},
            {'id': 'matic','name': 'Native Polygon (Matic)', 'symbol': 'Native MATIC', 'avg_blocks_per_day': 24 * 60 * 60 / 3},
            {'id': 'avalanche', 'name': 'Native Avalanche', 'symbol': 'Native AVAX', 'avg_blocks_per_day': 24 * 60 * 60 / 3}]


class Report:
    wallet_sheet = None
    contracts = None

    def __init__(self, filepath):
        xls = pd.ExcelFile(filepath)
        self.wallet_sheet = pd.read_excel(xls, 0)
        self.contracts = pd.read_excel(xls, 1).iloc[:, 0]

    # Inclusive range
    def generate_token_balance_report_in_date_range(self, start_date, end_date):
        date_range = [start_date + timedelta(days=x) for x in range(0, (end_date-start_date).days + 1)]
        output_data = []
        for date in date_range:
            block_no = Moralis.get_block_number_from_datetime(date)
            time.sleep(1)  # sleep for 1 second to avoid rate limit
            output_data.extend(self.generate_token_balance_report(block_no))
        return output_data


    # Inclusive range
    def generate_token_balance_report_in_block_range(self, start_block, end_block):
        output_data = []
        for block_no in range(start_block, end_block + 1):
            output_data.extend(self.generate_token_balance_report(block_no))
        return output_data



    def generate_token_balance_report(self, block_no):
        output_data = []
        
        for wallet_data in self.wallet_sheet.itertuples():
            print(wallet_data)
            wallet_address = wallet_data.address

            chain_data = None
            for chain in CHAINS:
                if chain.get('id') == wallet_data.chain:
                    chain_data = chain

            native_balance = Moralis.get_native_balance(wallet_address, chain_data.get('id'), block_no)
            token_balance = TokenBalance()
            token_balance.owner_address = wallet_address
            token_balance.balance = native_balance['balance']
            token_balance.decimals = 18
            token_balance.name = chain_data.get('name')
            token_balance.symbol = chain_data.get('symbol')
            token_balance.token_address = 'NATIVE'  # not applicable for native tokens
            token_balance.chain = chain_data.get('id')
            token_balance.block_number = block_no

            token_balance.generate_formatted_balance()

            output_data.append(token_balance)

            time.sleep(1)  # sleep for 1 second to avoid rate limit

            data = Moralis.get_all_erc20_tokens(wallet_address, chain_data.get('id'), block_no)
            for balance_data in data:
                token_address = balance_data['token_address']

                in_contracts = len([x for x in self.contracts if x.lower() == token_address.lower()]) > 0

                if in_contracts:
                    token_balance = TokenBalance()
                    token_balance.owner_address = wallet_address
                    token_balance.balance = balance_data['balance']
                    token_balance.decimals = balance_data['decimals']
                    token_balance.name = balance_data['name']
                    token_balance.symbol = balance_data['symbol']
                    token_balance.token_address = balance_data['token_address']
                    token_balance.chain = chain_data.get('id')
                    token_balance.block_number = block_no

                    token_balance.generate_formatted_balance()
                    print(token_balance.formatted_balance)

                    output_data.append(token_balance)

            time.sleep(1)  # sleep for 1 second to avoid rate limit
                
        return output_data



    def output_report(self, output_data):
        if not os.path.exists(GENERATED_REPORT_PATH):
            os.makedirs(GENERATED_REPORT_PATH)  # create the directory if it doesn't exist

        output_filename = 'token_balance_report_' + str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) + '.csv'

        with open(os.path.join(GENERATED_REPORT_PATH, output_filename), mode='w') as output_file:
            output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            output_writer.writerow(['Wallet Address', 'Contract Address','Name', 'Symbol', 'Balance', 'Chain', 'Block Number'])
            for entry in output_data:
                output_writer.writerow([entry.owner_address, entry.token_address, entry.name, entry.symbol, entry.formatted_balance, entry.chain, entry.block_number])


        return output_filename

