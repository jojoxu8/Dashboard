#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      jolan
#
# Created:     28.01.2020
# Copyright:   (c) jolan 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#####################  Importieren aller libraries   #####################
import dash_html_components as html
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd
import pickle
import re

##########################    Funktionen    ###########################

### Funktionen zum pickeln und entpicklen des ML-models ###
def pickler(datName, input):
    import pickle
    dateiS = open(datName, "wb")
    pickle.dump(input, dateiS)
    dateiS.close()


def  entpickler(datName):
    import pickle
    dateiL = open(datName, "rb")
    name = pickle.load(dateiL)
    dateiL.close()
    return name


### Description card für die einzelnen Tabs (insgesamt 5) ###
def description_card():
    return html.Div(
        id="description-card",
        children=[
            html.H2("Rennspiel Dashboard"),
            html.H3("Programmierwettbewerb by MATERNA: Big Data Predictions"),
            html.Div(
                id="intro",
                children="Dashboard von Jolanda Dünner",
            ),
            html.H4("Auf diesem Dashboard werden Daten von einem Rennspiel analysiert und visualisiert"),
            html.Br(),
            html.H4("Im letzten Tab wird eine Voraussage gegeben, ob der Challenger oder der Opponent gewinnt."),
                    ],
    )

def description_card2():
    return html.Div(
        id="description-card2",
        children=[
            html.H2("Rennspiel Dashboard"),
            html.H3("Hier können Sie die Gewinnrate jedes Spielers analysieren."),
        ],
    )

def description_card4():
    return html.Div(
        id="description-card4",
        children=[
            html.H2("Rennspiel Dashboard"),
            html.H3("Hier können Sie die Benutzung der Tracks nach Spieler analysieren"),
        ],
    )
def description_card5():
    return html.Div(
        id="description-card5",
        children=[
            html.H2("Rennspiel Dashboard"),
            html.H3("Hier können Sie die Wetterbedinungen auf den Strecken analysieren"),
        ],
    )



def description_card3():
    return html.Div(
        id="description-card3",
        children=[
            html.H2("Rennspiel Dashboard"),
            html.H3("Prediction"),
            html.Div(
                id="intro3",
                children="Auf diesem Tab wird eine Voraussage getroffen, ob der Challenger gegen den Opponent gewinnt. Das trainierte Model basiert auf einem Random Forest classifier."
            ),
            html.I("Wählen Sie dazu einen Challenger, einen Opponent und die Track id aus:"),
        ],
    )



