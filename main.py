import alpaca_trade_api as tradeapi
import json


class TradingBot():
    
    def __init__(self, configFile, varsFile):
        self.varFile = varsFile
        self.ReadVars()
        self.ConfigAPI(configFile)

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

bot = TradingBot(configFile="config.json", varsFile="vars.json")


bot.UpdateVars()