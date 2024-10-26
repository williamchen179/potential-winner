import pandas as pd
import numpy as np
import os

print(os.getcwd())

odds = pd.read_csv("EPLWinLossOdds.csv")
print(odds.head())

print(odds.columns)
odds = odds.drop(['Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12', 'Unnamed: 13', 'Unnamed: 14', 'Date Refreshed'], axis = 1)

print(odds.head())

odds['Distinct_Match'] = odds['Home Team'] + odds['Away Team']
odds['Risk_Margin'] = (1/odds['Win'] + 1/odds['Draw'] + 1/odds['Loss'])-1

# Strategy 1: Arbitrage
distinctmatches = odds['Distinct_Match'].unique()

for match in distinctmatches:
    filtered_odds = odds[odds['Distinct_Match'] == match]
    max_win = filtered_odds['Win'].max()
    max_draw = filtered_odds['Draw'].max()
    max_loss = filtered_odds['Loss'].max()
    implied_probability = 1/max_win + 1/max_draw + 1/max_loss
    
    if implied_probability < 1:
        print("The " + match + " match has an arbitrage opportunity")


# Strategy 2: Averages with a risk margin
distinctmatches = odds['Distinct_Match'].unique()

for match in distinctmatches:

    filtered_odds = odds[odds['Distinct_Match'] == match]
    filtered_odds_excluding_betfair = filtered_odds[filtered_odds['Betting Agency'] != 'BetFair -5% (UK,Aus)']
    betfair_odds = filtered_odds[filtered_odds['Betting Agency'] == 'BetFair -5% (UK,Aus)']

    average_risk_margin = filtered_odds_excluding_betfair['Risk_Margin'].mean()
    average_win_odds_risk_margin = filtered_odds_excluding_betfair['Win'].mean() * (1+average_risk_margin)
    average_draw_odds_risk_margin = filtered_odds_excluding_betfair['Draw'].mean() * (1+average_risk_margin)
    average_loss_odds_risk_margin = filtered_odds_excluding_betfair['Loss'].mean() * (1+average_risk_margin)

    filtered_win_df = filtered_odds[filtered_odds['Win'] > average_win_odds_risk_margin][['Betting Agency', 'Home Team', 'Away Team', 'Win']]
    filtered_draw_df = filtered_odds[filtered_odds['Draw'] > average_draw_odds_risk_margin][['Betting Agency', 'Home Team', 'Away Team', 'Draw']]
    filtered_loss_df = filtered_odds[filtered_odds['Loss'] > average_loss_odds_risk_margin][['Betting Agency', 'Home Team', 'Away Team', 'Loss']]

    if(len(filtered_win_df) > 0):
        print(filtered_win_df)
    if(len(filtered_draw_df) > 0):
        print(filtered_draw_df)
    if(len(filtered_loss_df) > 0):
        print(filtered_loss_df)


