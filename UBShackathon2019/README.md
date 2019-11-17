# UBS Quant Hackathon 2019

## Overview

UBS Quant Hackathon 2019 is an online Hackathon organized and administered by UBS. The first round has four tasks to choose from. Each involves some kind of trading strategies using the data provided by the Refinitv platform ([link](https://www.refinitiv.com)). Each team has to write a report explaining their strategy, implement it and back-test the strategy against historical data. The second round is by invitation only.

Out of 1000 registered participants, only 80 teams submitted their proposals. Due to our lack of technical knowledge in the finance field, our team was not invited for the second round.

Our code and explanation of strategy are provided in the Jupyter notebook. The chosen task is reproduced below.

## Chosen task

__4. FX Value Strategy__:

- __Objective__: To explore a trading strategy which take long/short position in G10 currencies (against USD) in order to extract value premium. In another words: to buy under-valued currency and to sell over-valued currency expecting price will revert to fair value.
- __Trading instrument__: G10 FX forwards (can use 1w to 3month depending on trading frequency).
- __Trading frequency__: Can be as frequent as once a day trading or less frequent.
- __Modeling inputs__: FX spot/FX implied vol; rates; government bond yields in relevant jurisdiction, commodity price (oil, gold, etc); economic data (GDP, CPI etc) only if it is available.

__NOTE__: API access token to the Refinitiv platform is removed. Pricing data won't be available without the access token.