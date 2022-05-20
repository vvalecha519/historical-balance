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
        integral_part, fractional_part = "{:.4f}".format(float(self.get_balance_with_decimal())).split(".")
        self.formatted_balance = integral_part + "." + fractional_part

