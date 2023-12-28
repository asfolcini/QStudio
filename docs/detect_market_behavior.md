# QStudio - Detect Market Behavior

[Home](index.md)

### Table of Contents
- [Introduction](#introduction)
- [Market behaviors](#market-behaviors)
- [Hurst Exponent](#hurst-exponent)
- [5% Threshold on Hurst Exponent](#5-threshold-on-hurst-exponent)
- [Usage](#usage)



## Introduction

Empowers users to analyze a set of symbols and determine their market behavior. It categorizes symbols into **mean-reverting**, **trending**, or **random-walk**, offering insights that are crucial for making informed decisions in financial markets. This feature is particularly valuable for traders seeking to adapt their strategies based on prevailing market trends.

## Market behaviors

1. **Mean-Reverting:**
    - **Characteristics:**
        - **Mean-Reversion:** These strategies assume that asset prices will tend to revert to their historical average or mean over time.
        - **Counter-Trend Trading:** Traders using mean-reverting strategies take positions against the prevailing trend, expecting prices to reverse direction.
        - **Bounded Price Movement:** Mean-reverting assets are expected to stay within certain price boundaries, making it suitable for range-bound markets.
    - **Trading Approach:**
        - Identify overbought or oversold conditions through technical indicators or statistical measures.
        - Enter trades when prices deviate significantly from their historical mean.
        - Exit positions when prices approach the mean or show signs of reversing.


2. **Trend-Following:**
    - **Characteristics:**
        - **Trend Continuation:** Trend-following strategies assume that asset prices will continue in the direction of the prevailing trend.
        - **Momentum Trading:** Traders following trends aim to capture gains during strong price movements.
        - **Unbounded Price Movement:** Trend-following strategies are suitable for markets experiencing prolonged trends.
    - **Trading Approach:**
        - Identify and confirm existing trends using technical indicators, moving averages, or trendlines.
        - Enter trades in the direction of the trend to capture potential gains.
        - Use risk management techniques to protect against sudden reversals.


3. **Random Walk:**
    - **Characteristics:**
        - **Efficient Market Hypothesis (EMH):** Random walk strategies are based on the belief that asset prices follow a random path, and historical price movements cannot be used to predict future movements.
        - **No Predictive Patterns:** Traders using random walk strategies do not rely on technical analysis or historical data to make trading decisions.
        - **Market Efficiency:** Random walk strategies align with the concept of market efficiency, suggesting that all available information is already reflected in asset prices.
    - **Trading Approach:**
        - Accept the idea that price movements are unpredictable and follow a random path.
        - Avoid relying on technical analysis patterns or historical trends for trading decisions.
        - May focus on fundamental analysis or external factors affecting the market.


Understanding the main characteristic of a market is crucial in trading because it allows traders to adapt their strategies appropriately.
The `detect-trend` function in QStudio becomes crucial because it automates the process of identifying the main characteristic of a market. This helps traders make more informed decisions about the type of strategy to implement, enhancing adaptability to the specific market conditions at a given moment.

## Hurst Exponent
The Hurst Exponent is a tool used in financial analysis to assess the nature of a stochastic process, such as the behavior of a financial market over time. In QStudio, the Hurst Exponent is employed to determine market behavior. Here's how you can use the Hurst Exponent to assess and adapt your trading strategy:

**Definition of the Hurst Exponent:**

- The Hurst Exponent is an index that ranges from 0 to 1.
- A Hurst Exponent value in the range of 0.5-1.0 suggests a "trend" behavior, where current trends are more likely to persist in the future.
- A value in the range of 0.0-0.5 suggests a "mean-reverting" behavior, where current variations are more likely to reverse direction in the future.

**Interpretation of the Hurst Exponent:**

- Values above 0.5 suggest a "trend" behavior, indicating that the market is more likely to follow persistent trends.
- Values below 0.5 suggest a "mean-reverting" behavior, indicating that the market is more likely to revert to the mean over time.

**Application in Trading Strategy:**

- Trend Following: If the Hurst Exponent indicates a "trend" behavior, trend-following strategies can be considered where one seeks to exploit current trends.
- Mean-Reversion: If the Hurst Exponent suggests a "mean-reverting" behavior, mean-reversion strategies can be considered, where one seeks to exploit trend reversals.

## 5% Threshold on Hurst Exponent
By applying this 5% margin to the Hurst Exponent, QStudio provides a threshold for distinguishing between mean-reverting, random-walk or trend-following market behaviors.

**Note:** The 5% margin is a default setting, but users can customize this margin through code, providing flexibility in adjusting the sensitivity of the classification.


## Usage

Detect market behavior for configured symbols or specific symbols. Below are the usage options:

1. **Detect Market Behavior for Configured Symbols:**
   ```textmate
   python qstudio.py --detect_market_behavior 
   ```
   Example:
   ```pythonregexp
   python qstudio.py ----detect_market_behavior 
   ```
   output:
   ~~~textmate
   ------------------------------------------------------------------------------------------------------------------------
   Q S t u d i o   v0.3.5
   2023 (c) Alberto Sfolcini <a.sfolcini@gmail.com>
   www.surprisalx.com
   ------------------------------------------------------------------------------------------------------------------------
   FTSEMIB.MI is likely a RANDOM WALK  (Hurst=0.4930269577647605) using margin of 5.0 %
   ^GDAXI is likely a MEAN-REVERTING  (Hurst=0.47010834232220483) using margin of 5.0 %
   ENI.MI is likely a MEAN-REVERTING  (Hurst=0.4417712547303772) using margin of 5.0 %
   RACE.MI is likely a MEAN-REVERTING  (Hurst=0.4208084406156848) using margin of 5.0 %
   CPR.MI is likely a RANDOM WALK  (Hurst=0.5103345149597034) using margin of 5.0 %
   PST.MI is likely a MEAN-REVERTING  (Hurst=0.46852963966297184) using margin of 5.0 %
   G.MI is likely a MEAN-REVERTING  (Hurst=0.46285110340519564) using margin of 5.0 %
   BAMI.MI is likely a MEAN-REVERTING  (Hurst=0.4615018175590222) using margin of 5.0 %
   AZM.MI is likely a RANDOM WALK  (Hurst=0.5152094961869939) using margin of 5.0 %
   LDO.MI is likely a RANDOM WALK  (Hurst=0.5054944585835435) using margin of 5.0 %
   STLAM.MI is likely a MEAN-REVERTING  (Hurst=0.4670049839463649) using margin of 5.0 %
   ISP.MI is likely a MEAN-REVERTING  (Hurst=0.47176027577454227) using margin of 5.0 %
   BGN.MI is likely a MEAN-REVERTING  (Hurst=0.4668449262705132) using margin of 5.0 %
   IF.MI is likely a MEAN-REVERTING  (Hurst=0.4398256829136585) using margin of 5.0 %
   ~~~

2. **Detect Market Behavior for Given Symbols:**
   ```textmate
   python qstudio.py --detect_market_behavior --symbols [symbols]
   ```
   Example:
   ```pythonregexp
   python qstudio.py --detect_market_behavior --symbols AAPL,SPY
   ```
   output:
   ~~~textmate
   ------------------------------------------------------------------------------------------------------------------------
    Q S t u d i o   v0.3.5
    2023 (c) Alberto Sfolcini <a.sfolcini@gmail.com>
    www.surprisalx.com
   ------------------------------------------------------------------------------------------------------------------------
   AAPL is likely a MEAN-REVERTING  (Hurst=0.46515677325822913) using margin of 5.0 %
   SPY is likely a MEAN-REVERTING  (Hurst=0.426289094140744) using margin of 5.0 %
   ~~~


[Top](#qstudio---detect-market-behavior)