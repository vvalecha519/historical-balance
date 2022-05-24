class TokenBalance:
    owner_address = None

    balance = None
    decimals = None
    name = None
    symbol = None
    token_address = None
    chain = None
    block_number = None
    formatted_balance = None
    timestamp = None

    def __init__(self, owner_address=None, balance=None, decimals=None, name=None, symbol=None, token_address=None, chain=None, block_number=None, timestamp=None):
        self.owner_address = owner_address
        self.balance = balance
        self.decimals = decimals
        self.name = name
        self.symbol = symbol
        self.token_address = token_address
        self.chain = chain
        self.block_number = block_number
        self.timestamp = timestamp

        self.generate_formatted_balance()

    def to_pd_dict(self):
        return {
            'owner_address': self.owner_address,
            'token_address': self.token_address,
            'name': self.name,
            'symbol': self.symbol,
            'chain': self.chain,
            'formatted_balance': self.formatted_balance,
        }

    def get_balance_with_decimal(self):
        decimal_point_index = len(self.balance) - self.decimals
        if decimal_point_index < 0:
            return "." + self.balance
        balance = self.balance[:decimal_point_index] + "." + self.balance[decimal_point_index:]
        try: 
            float(balance)
        except:
            try:
                decimal_idx = balance.index(".", -1)
                balance = balance[:decimal_idx] + balance[decimal_idx[1]:].rstrip("0")
                return balance
            except:
                return "0"
        return self.balance[:decimal_point_index] + "." + self.balance[decimal_point_index:]

    def generate_formatted_balance(self):
        self.formatted_balance = self.get_balance_with_decimal()

