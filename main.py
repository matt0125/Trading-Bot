import alpaca_trade_api as tradeapi
import json

class Alpaca:
    def __init__(self, configFile="config.json"):

        with open(configFile, 'r') as config_file:
            self.config = json.load(config_file)

        self.api_key = self.config["api_key"]
        self.api_secret = self.config["api_secret"]
        self.short_window = self.config["short_window"]
        self.long_window = self.config["long_window"]
        self.polling_interval_seconds = self.config["polling_interval_seconds"]
        self.base_url = self.config["base_url"]

        self.api = tradeapi.REST(self.api_key, self.api_secret, base_url = self.base_url)
        print("a")


    def placeOrder(self, symbol, qty):

        order = self.api.submit_order(
            symbol=symbol,
            qty=qty,
            side='buy',
            type='market',
            time_in_force='gtc'
        )

        return order
    
    def getEquity(self):
        print(self.api.get_account().equity)

# Usage:
alpaca = Alpaca()  # Load configuration from "config.json" by default

alpaca.getEquity()