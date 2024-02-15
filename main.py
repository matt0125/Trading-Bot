import alpaca_trade_api as tradeapi
import yfinance as yf
import numpy as np
import datetime
import json


class TradingBot():
    
    def __init__(self, configFile, varsFile):
        self.varFile = varsFile
        self.ReadVars()
        self.ConfigAPI(configFile)

        self.OpenMarket()

    def ReadVars(self):
        with open(self.varFile, "r") as varsFile:
            vars = json.load(varsFile)

        # Extract configuration values
        self.symbol = vars["symbol"]
        self.lookback = vars["lookback"]
        self.upperLookback = vars["lookback_upperLimit"]
        self.lowerLookback = vars["lookback_lowerLimit"]
        self.initialStopRisk = vars["stopRisk_initial"]
        self.trailingStopRisk = vars["stopRisk_trailing"]

    def ConfigAPI(self, configFile):
        # Load configuration from config.json
        with open(configFile, "r") as config_file:
            config = json.load(config_file)
        
        # Alpaca API credentials
        base_url = config["base_url_paper"]
        api_key = config["api_key_paper"]
        api_secret = config["api_secret_paper"]

        # Initialize Alpaca API
        self.api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
    

    def OpenMarket(self):
        yesterday = datetime.today().date() - datetime.timedelta(days=1)
        start_date = yesterday - datetime.timedelta(days=lookback)

        # Fetch historical data from Yahoo Finance
        data = yf.download(self.symbol, start=start_date, end=yesterday)

        close = data['Close']

        todayvol = np.std(close[1:31])
        yesterdayvol = np.std(close[0:30])
        deltavol = (todayvol - yesterdayvol) / todayvol
        lookback = round(lookback * (1 + deltavol))

        if lookback > self.upper_lookback:
            lookback = self.upper_lookback
        if lookback < self.lower_lookback:
            lookback = self.lower_lookback

        high = data['High']

        if not self.api.get_position(self.symbol).asset_id and self.api.get_last_trade(self.symbol).price >= max(high[:-1]):
            self.api.submit_order(
                symbol=self.symbol,
                qty=1,
                side='buy',
                type='limit',
                time_in_force='gtc',
                limit_price=self.api.get_last_trade(self.symbol).price
            )
            breakoutlvl = max(high[:-1])
            self.highestPrice = breakoutlvl

        if self.api.get_position(self.symbol).asset_id:
            if self.api.get_last_trade(self.symbol).price > self.highestPrice and self.initialStopRisk * breakoutlvl < self.api.get_last_trade(
                    self.symbol).price * self.trailingStopRisk:
                self.highestPrice = self.api.get_last_trade(self.symbol).price
                self.submit_trailing_stop_order()



    def submit_trailing_stop_order(self):
        if not self.api.get_position(self.symbol).asset_id:
            return

        current_price = self.api.get_last_trade(self.symbol).price
        stop_price = current_price * self.trailingStopRisk

        if stop_price > self.highestPrice:
            # Update the stop price
            self.api.submit_order(
                symbol=self.symbol,
                qty=self.api.get_position(self.symbol).qty,
                side='sell',
                type='trailing_stop',
                trail_percent=self.trailingStopRisk
            )

    def UpdateVars(self):
        
        vars = {
            "symbol": self.symbol,
            "lookback": self.lookback,
            "lookback_upperLimit": self.upperLookback,
            "lookback_lowerLimit": self.lowerLookback,
            "stopRisk_initial": self.initialStopRisk,
            "stopRisk_trailing": self.trailingStopRisk
        }

        with open(self.varFile, "w") as varsFile:
            json.dump(vars, varsFile, indent=4)





TradingBot(configFile="config.json", varsFile="vars.json")
