# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Dahsboard Rennspiel
# Purpose:     Klausurvorbereitung Python Einführung
#
# Author:      jolanda Duenner
#
# Created:     30.01.2020
# Copyright:   (c) jolan 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------


####################  Importiere benötigte Packages  ####################
import dash
import funktionen as f
import numpy as np
import pandas as pd
import pathlib
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
################  Einlesen des Datensatzes (seperator = ;) #################
# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()

dtypes = {'status': 'str','weather':'str'}
parse_dates = ['race_created', 'race_driven', 'forecast']
races = pd.read_csv(DATA_PATH.joinpath("races.csv"), sep = ";", dtype=dtypes, parse_dates=parse_dates)

##########################    Data Preperation   ###########################

## Neuer Datensatz mit allen "finished" races
races_mask = (races["status"] == "finished")   # Maske, um nur finished races zu berücksichtigen
races_finished = races[races_mask]
races_finished.loc[:,"counter"] = 1
races_finished_weather = races_finished.groupby("weather").size().round(1)
df = races_finished


##########################    Tab 1 (Statistik)   ###########################
# Welche Strecke kommt wie oft vor
race_number = races_finished.counter.groupby(races_finished.track_id).sum()
race_number = race_number.sort_values(ascending=False)
modified = race_number.reset_index()

# Welcher Spieler ist wie oft challenger
challenger = races_finished.counter.groupby(races_finished.challenger).count()
challenger = challenger.reset_index()

# Welcher Spieler ist wie oft opponent
opponent = races_finished.counter.groupby(races_finished.opponent).count()
opponent = opponent.reset_index()

# Total gespielte Spiele pro Spieler
merged = pd.merge(challenger, opponent, how='outer',  left_on="challenger", right_on="opponent")
merged["total"] = merged.counter_x + merged.counter_y

## Berechne die Gewinnrate
winner = races_finished.counter.groupby(races_finished.winner).count()
winner = winner.reset_index()
winner_rate = pd.merge(merged, winner, how="outer", left_on="challenger", right_on="winner")
winner_rate["counter"].sum()
winner_rate = winner_rate.drop(['opponent', 'winner'], axis=1)
winner_rate = winner_rate.rename(columns={"challenger": "Spieler", "counter_x": "Anzahl Challenger", "counter_y":"Anzahl Opponent", "total":"Total", "counter":"Gewonnene Spiele"})

### Gewinnerrate hängt von Anzahl gespielter Spiele ab (Wilson interval)
z = 1.96
winner_rate["Gewinnrate"] = (winner_rate["Gewonnene Spiele"]/winner_rate["Total"])
winner_rate["denominator"] = 1 + z**2/winner_rate["Total"]
winner_rate["centre_adjusted_probability"] = winner_rate["Gewinnrate"] + z*z / (2*winner_rate["Total"])
winner_rate["adjusted_stand"] = np.sqrt((winner_rate["Gewinnrate"]*(1 - winner_rate["Gewinnrate"]) + z*z / (4*winner_rate["Total"])) / winner_rate["Total"])
winner_rate["lower_bound"] = (((winner_rate["centre_adjusted_probability"] - z*winner_rate["adjusted_stand"] ) / winner_rate["denominator"])*100).round(2)
winner_rate["upper_bound"] = (((winner_rate["centre_adjusted_probability"] + z*winner_rate["adjusted_stand"] ) / winner_rate["denominator"])*100).round(2)
winner_rate["Gewinnrate"]  = (winner_rate["Gewinnrate"]*100).round(2)
final = winner_rate.drop(["Anzahl Challenger", "Anzahl Opponent", "denominator", "centre_adjusted_probability", "adjusted_stand"], axis=1)
final = final.sort_values(by=['Gewonnene Spiele'], ascending=False)
final = final.dropna()
###### Spieler mit den meisten gespielten Spielen
top = final.iloc[0]

###### Beliebteste Strecke
races_finished.loc[:,'COUNTER'] =1       #initially, set that counter to 1.
top_tracks =  races_finished.groupby(['track_id'])['COUNTER'].sum()
top_tracks = top_tracks.reset_index()
top_tracks = top_tracks.sort_values(by ='COUNTER' , ascending=False)
top_tracks = top_tracks.iloc[0]
###### Häufigste Wetterbedinung
top_wetter =  races_finished.groupby(['weather'])['COUNTER'].sum()
top_wetter = top_wetter.reset_index()
top_wetter = top_wetter.sort_values(by ='COUNTER' , ascending=False)
top_wetter = top_wetter.iloc[0]
##########################    Visualisierung   ###########################

# Labels für das Wetterdiagramm

races_finished_weather = races_finished.groupby("weather").size().round(1)
label = [races_finished_weather.index.values]
value = [races_finished.counter.groupby(races_finished.weather).sum()]
data = []
n = 5
# Dataframe für die Funktion "Update Graph"
df = races_finished

# Dropdown menu für die Tracks
mgr_options = races_finished["track_id"].unique()



##########################    Prediction   ###########################

# Lade das trainierte Model ("predictor.py")
model = f.entpickler("model.pck")
x = []
# Drop down menu für die Spieler
spieler_options = np.sort(races_finished["challenger"].unique())
