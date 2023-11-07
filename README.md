
# 
<div align="center">
  
[![CircleCI](https://img.shields.io/circleci/project/github/bitpay/wallet/master.svg)](https://circleci.com/gh/bitpay/wallet/)
[![Codecov](https://img.shields.io/codecov/c/github/bitpay/wallet.svg)](https://codecov.io/gh/bitpay/wallet/)
[![Crowdin](https://d322cqt584bo4o.cloudfront.net/copay/localized.png)](https://crowdin.com/project/copay)
![Download Count](https://img.shields.io/github/downloads/Snowflake-coin/snowflake-frost-wallet/total.svg)
![Version](https://img.shields.io/github/v/release/Snowflake-coin/snowflake-frost-wallet)
![Windows Build Status](https://github.com/Snowflake-coin/snowflake-frost-wallet/workflows/Windows%20Build/badge.svg?branch=main)
[![Documentation](https://readthedocs.org/projects/freqtrade/badge/)](https://www.freqtrade.io)
![docker](https://img.shields.io/docker/pulls/edeng23/binance-trade-bot)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/edeng23/binance-trade-bot)

[![Deploy to DO](https://mp-assets1.sfo2.digitaloceanspaces.com/deploy-to-do/do-btn-blue.svg)](https://cloud.digitalocean.com/apps/new?repo=https://github.com/coinbookbrasil/binance-trade-bot/tree/master&refcode=a076ff7a9a6a)




</div>

# CryptoAlert: Crypto Signal Trading Bot

CryptoAlert is an open-source trading bot that helps you automatically follow and trade signals when trading cryptocurrencies. This project is designed for developers who want to further analyse data and develop trading strategies in the cryptocurrency markets.

# Information
This project was inspired by the observation that all cryptocurrencies pretty much behave in the same way. When one spikes, they all spike, and when one takes a dive, they all do. Pretty much. Moreover, all coins follow Bitcoin's lead; the difference is their phase offset.

So, if coins are basically oscillating with respect to each other, it seems smart to trade the rising coin for the falling coin, and then trade back when the ratio is reversed.




## Features

- [x] Integration of APIs with cryptocurrency exchanges for seamless interaction.
- [x] Proficiency in real-time market data monitoring and analysis.
- [x] Capability to implement customizable trading strategies tailored to your preferences.
- [x] Automated signal processing and efficient position management.
- [x] Intuitive user interface and a comprehensive reporting system for user convenience.
- [x] Utilization of Python 3.9+ as the programming foundation, ensuring compatibility across Windows, macOS, and Linux operating systems.
- [x] Establishment of data persistence through the use of sqlite.
- [x] Provision for a dry-run mode, enabling users to run the bot without risking actual funds.
- [x] Implementation of backtesting functionality, facilitating the simulation of buy/sell strategies.
- [X] Integration of machine learning for optimizing buy/sell strategy parameters using real exchange data.
- [x] Incorporation of adaptive prediction modeling via FreqAI, a smart strategy that self-trains in response to market dynamics.
- [x] Introduction of edge position sizing, allowing for the calculation of win rates, risk-reward ratios, optimal stop-loss levels, and position size adjustments tailored to specific markets.
- [x] Ability to create whitelists of preferred cryptocurrencies for trading or implement dynamic whitelists.
- [x] Option to blacklist specific cryptocurrencies, avoiding unwanted trades.
- [x] Inclusion of a built-in web UI for seamless bot management.
- [x] Convenient bot management via Telegram for real-time control.
- [x] Display of profit and loss in fiat currency for clear financial tracking.
- [x] Provision of performance status reports, offering insights into the current state of your trades.

![0](https://github.com/MuckPro/REDME/assets/138373919/42d740e8-e358-4e86-9124-e81d7127cbf6)





# The Methodology Unveiled


The modus operandi unfolds within the Binance market platform, which, in all fairness, lacks markets catering to every conceivable altcoin pair. A clever stratagem to circumvent this limitation involves the employment of an intermediary currency, one that can seamlessly bridge the gap left by the absence of certain pairs. The default choice for such a bridge currency rests upon Tether (USDT), a currency esteemed for its inherent stability and universal compatibility across the platform's coin spectrum.

The underlying principle that guides the bot's operations capitalizes on the observed behavioral dynamics of these coins. It entails a continuous transition from the "dominant" coin to its "vulnerable" counterpart, operating under the underlying presumption that the tides of fortune will eventually shift. Subsequently, the bot retraces its steps back to the original coin, ultimately amassing a greater quantity than it initially held. This intricate maneuver is conducted with meticulous consideration of the accompanying trading fees.

The bot jumps between a configured set of coins on the condition that it does not return to a coin unless it is profitable in respect to the amount held last. This means that we will never end up having less of a certain coin. The risk is that one of the coins may freefall relative to the others all of a sudden, attracting our reverse greedy algorithm.



## Supported Exchange marketplaces

Please read the [exchange specific notes](docs/exchanges.md) to learn about eventual, special configurations needed for each exchange.

- [X] [Binance](https://www.binance.com/)
- [X] [Bittrex](https://bittrex.com/)
- [X] [Gate.io](https://www.gate.io/ref/6266643)
- [X] [Huobi](http://huobi.com/)
- [X] [Kraken](https://kraken.com/)
- [X] [OKX](https://okx.com/) (Former OKEX)
- [ ] [potentially many others](https://github.com/ccxt/ccxt/). _(We cannot guarantee they will work)_

### Supported Futures Exchanges (experimental)

- [X] [Binance](https://www.binance.com/)
- [X] [Gate.io](https://www.gate.io/ref/6266643)
- [X] [OKX](https://okx.com/)
- [X] [Bybit](https://bybit.com/)



### Bot commands

```
usage: freqtrade [-h] [-V]
                 {trade,create-userdir,new-config,new-strategy,download-data,convert-data,convert-trade-data,list-data,backtesting,edge,hyperopt,hyperopt-list,hyperopt-show,list-exchanges,list-hyperopts,list-markets,list-pairs,list-strategies,list-timeframes,show-trades,test-pairlist,install-ui,plot-dataframe,plot-profit,webserver}
                 ...

Free, open source crypto trading bot

positional arguments:
  {trade,create-userdir,new-config,new-strategy,download-data,convert-data,convert-trade-data,list-data,backtesting,edge,hyperopt,hyperopt-list,hyperopt-show,list-exchanges,list-hyperopts,list-markets,list-pairs,list-strategies,list-timeframes,show-trades,test-pairlist,install-ui,plot-dataframe,plot-profit,webserver}
    trade               Trade module.
    create-userdir      Create user-data directory.
    new-config          Create new config
    new-strategy        Create new strategy
    download-data       Download backtesting data.
    convert-data        Convert candle (OHLCV) data from one format to
                        another.
    convert-trade-data  Convert trade data from one format to another.
    list-data           List downloaded data.
    backtesting         Backtesting module.
    edge                Edge module.
    hyperopt            Hyperopt module.
    hyperopt-list       List Hyperopt results
    hyperopt-show       Show details of Hyperopt results
    list-exchanges      Print available exchanges.
    list-hyperopts      Print available hyperopt classes.
    list-markets        Print markets on exchange.
    list-pairs          Print pairs on exchange.
    list-strategies     Print available strategies.
    list-timeframes     Print available timeframes for the exchange.
    show-trades         Show trades.
    test-pairlist       Test your pairlist configuration.
    install-ui          Install FreqUI
    plot-dataframe      Plot candles with indicators.
    plot-profit         Generate plot showing profits.
    webserver           Webserver module.

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit

```


## Contributing

We welcome contributions from the community. To contribute to BlockchainBridge, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes.
4. Submit a pull request. 

<h2> License </h2>

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<h3> Disclaimer </h3>

This project is for informational purposes only. You should not construe any such information or other material as legal, tax, investment, financial, or other advice. Nothing contained here constitutes a solicitation, recommendation, endorsement, or offer by me or any third party service provider to buy or sell any securities or other financial instruments in this or in any other jurisdiction in which such solicitation or offer would be unlawful under the securities laws of such jurisdiction.

If you plan to use real money, USE AT YOUR OWN RISK.

Under no circumstances will I be held responsible or liable in any way for any claims, damages, losses, expenses, costs, or liabilities whatsoever, including, without limitation, any direct or indirect damages for loss of profits.

---