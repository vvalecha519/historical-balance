import os
import requests
import json
import urllib.parse

from datetime import datetime
from pprint import pprint
from app.TokenBalance import TokenBalance
from dotenv import load_dotenv

load_dotenv()


class Moralis:
    MORALIS_BASE_URL = os.getenv('MORALIS_BASE_URL')
    MORALIS_API_KEY = os.getenv('MORALIS_API_KEY')

    headers = {'content-type': 'application/json', 
                'Accept-Charset': 'UTF-8', 
                'X-API-Key': MORALIS_API_KEY, 
                'accept': 'application/json',
                }

    def get_all_erc20_tokens(wallet_address, chain, block_no):
        """
        Returns a list of all ERC20 tokens and balances for a given address on a given chain at given block number.
        """
        url = Moralis.MORALIS_BASE_URL + '/{}/erc20?chain={}&to_block={}'.format(wallet_address, chain, block_no)
        response = requests.get(url, headers=Moralis.headers)
        data = response.json()
        pprint(data)
            
        return data


    def get_native_balance(wallet_address, chain, block_no):
        """
        Returns native balance for a given address on a given chain at given block number.
        """
        url = Moralis.MORALIS_BASE_URL + '/{}/balance?chain={}&to_block={}'.format(wallet_address, chain, block_no)
        response = requests.get(url, headers=Moralis.headers)
        data = response.json()
        pprint(data)
            
        return data


    def get_block_number_from_datetime(datetime_input):
        """
        Returns block number closest to given datetime.
        """

        unix_datetime_ms = datetime.timestamp(datetime_input)
        print(unix_datetime_ms)

        url = Moralis.MORALIS_BASE_URL + '/dateToBlock?chain={}&date={}'.format(chain, unix_datetime_ms)
        response = requests.get(url, headers=Moralis.headers)
        data = response.json()
        pprint(data)
            
        return data['block']







old_wallet_address = '0xa9Ca3de6323145410C56D52c4fFb34a695481872'
wallet_address = '0x005EE33762b213afcea5D294B14F005B00624661'
chain = 'eth'
block_no = '14795295'
earlier_block_no = '14745551'
new_block = '14806952'

#Moralis.get_all_erc20_tokens(wallet_address, chain, block_no)

#Moralis.get_native_balance('0xF0245F6251Bef9447A08766b9DA2B07b28aD80B0', 'matic', '28521285')
#Moralis.get_native_balance('0x81b7A53FBFEfD46dc42C0b41A3B87048Ad7b2389', 'avalanche', '14914241')
#Moralis.get_native_balance('0x00c0C72A1d45Bb3704A9358282EeC06746447778', 'avalanche', '14914241')

#now = datetime.now()
#Moralis.get_block_number_from_datetime(now)

#0xF63B34710400CAd3e044cFfDcAb00a0f32E33eCf
#0xF63B34710400CAd3e044cFfDcAb00a0f32E33eCf
#0xf63b34710400cad3e044cffdcab00a0f32e33ecf

# MUST check equality of token address by setting to lower case first.

# GOTTA CHECK NATIVE BALANCE TOO E.G. ETH BALANCE