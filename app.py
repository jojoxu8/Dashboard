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


### App Layout und Callbacks ###

#####################  Importieren aller libraries   #####################
import dash
import flask
import dash_html_components as html
import plotly.graph_objs as go
import dash_core_components as dcc
import funktionen as f
import numpy as np
import pandas as pd
import dash_table

exec(open("data_preparation.py").read())

##########################    App Layout  ###########################
app.layout = html.Div([
# Erster Tab: Kurze Einleitung, Statistiken
    dcc.Tabs([
        dcc.Tab(label='Dashboard', children=[
        # Banner
        html.Div(
            id="banner",
            className="banner",
            children=[html.Img(src=app.get_asset_url("race.png"))],
        ),
        html.Div(
            id="banner_tab1",
            style={'margin-right': 200},
            className="four columns",
            children=[f.description_card()]
            + [
                html.Div(
                    ["initial child"], id="output-clientside", style={"display": "none"}
                ),
            ],
        ),
        html.Br(),
        html.Br(),
        html.H2("*    Spiel-Statistik     *"),
        html.Br(),
        html.H5("Meiste Spiele gespielt:"),
            html.H1(top.iloc[0]),
            html.H5("Beliebteste Strecke:"),
            html.H1(top_tracks.iloc[0]),
            html.H5("Häufigste Wetterbedinung:"),
            html.H1(top_wetter.iloc[0]),

        ]),
        # Tab 2, gewinnraten für Spieler analysieren
        dcc.Tab(label='Gewinnrate', children=[
        # Banner
        html.Div(
            id="banner_g",
            className="banner",
            children=[html.Img(src=app.get_asset_url("winner.png"))],
        ),
        html.Div(
            id="banner:tabgewinn",
            style={'margin-right': 60},
            className="four columns",
            children=[f.description_card2()],
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.H6("Gewinnrate mit Wilson Score Intervall als lower und upper bound."),
        html.I("Wählen Sie hier die Spieler aus:"),
        dcc.RangeSlider(
            id='play',
            min=1,
            max=14664,
            step=2,
            marks={
        0: '0',
        1000: '1000',
        2000: '2000',
        3000: '3000',
        4000: '4000',
        5000: '5000',
        6000: '6000',
        7000: '7000',
        8000: '8000',
        9000: '9000',
        10000: '10000',
        11000: '11000',
        12000: '12000',
        13000: '13000',
        14000: '14000',
        15000: '15000',
        16000: '16000',
        17000: '17000',
        18000: '18000'
        },
            value=[1, 10]
    ),
        html.Br(),
        html.Br(),
        dcc.Graph("player"),
        html.Br(),
        html.H3("In dieser Tabelle können Sie mit gängigen Operationen nach Werten filtern."),
        dash_table.DataTable(
    columns=[
        {"name": i, "id": i} for i in final.columns
    ],
    data=final.to_dict('records'),
    filter_action="native",
    )

        ]),

    # Tab 3, Analyse der Trackbenutzung nach Spielern
        dcc.Tab(label='Trackbenutzung', children=[
        # Banner
        html.Div(
            id="banner5",
            className="banner",
            children=[html.Img(src=app.get_asset_url("car.png"))],

        ),
        html.Div(
            id="banner:tab23",
            style={'margin-right': 60},
            className="four columns",
            children=[f.description_card4()]

        ),
        html.Br(),
    html.Div(children=[
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),

        html.I("Wählen Sie einen Spieler aus:"),
        dcc.Dropdown(
            style={'margin-right': 60},
                id="spieler",
                options=[{
                    'label': i,
                    'value': i
                } for i in spieler_options],
                value=43),
        html.Br(),
        html.Br(),
        dcc.Graph("gewinn_rate"),
        ]),
                        ]),
        # Tab 4, analyse ob die Wetterbedinung von den Tracks abhängt
        dcc.Tab(label='Wetterbedinung', children=[
        # Banner
        html.Div(
            id="banner_f",
            className="banner",
            children=[html.Img(src=app.get_asset_url("weather.png"))],
        ),
        html.Div(
            id="banner:tabwetter",
            style={'margin-right': 60},
            className="four columns",
            children=[f.description_card5()],
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.I("Track id Auswählen:"),
                html.Br(),
            html.Div(children=[
        dcc.Dropdown(
            style={'margin-right': 60},
                id="track",
                options=[{
                    'label': i,
                    'value': i
                } for i in mgr_options],
                value='None'),
        html.Br(),
        html.Br(),
        dcc.Graph("graph"),
        ]),
     ]),
    # Tab 5, Voraussage über zukünftige Rennen
        dcc.Tab(label='Prediction', children=[
        html.Div(
            id="banner_prediction",
            className="banner",
            children=[html.Img(src=app.get_asset_url("prediction.png"))],

        ),
        html.Div(
            id="banner:tab236",
            style={'margin-right': 60},
            className="four columns",
            children=[f.description_card3()]

        ),
        html.Br(),
        html.Div(children=[
        dcc.Dropdown(
            style={'margin-right': 60},
                id="challenger",
                options=[{
                    'label': i,
                    'value': i
                } for i in spieler_options],
                value='None'),
        dcc.Dropdown(
            style={'margin-right': 60},
                id="opponent",
                options=[{
                    'label': i,
                    'value': i
                } for i in spieler_options],
                value='None'),
                html.Br(),
        html.I("Wählen Sie die Track id aus:"),
        html.Br(),
        dcc.Input(
            id="input_id", type="number", placeholder="None",
            min=3, max=14, step=1,
        ),
        ]),
        html.Div(id="number-out"),
        html.H6("Prediction:", className='two columns', style={'display': 'inline-block'}),
        html.Br(),
        html.Div(id='predict', className='two columns', style={'display': 'inline-block'}),
        ]),
    ])
])


##########################    App Callbacks  ###########################

#### Tab Gewinnrate ####
@app.callback(
    dash.dependencies.Output('player', 'figure'),
    [dash.dependencies.Input('play', 'value')])
def update_graph(play):
    if (play == "All") or (play is None):
        None

    else:
        graph_top = final[(final['Spieler'] > play[0]) & (final['Spieler'] < play[1])]
        bar = go.Bar(x=pd.Series(range(1,len(graph_top["Gewonnene Spiele"]))), y=final["Gewinnrate"], name='Lower bound')
        bar2 = go.Bar(x=pd.Series(range(1,len(graph_top["Gewonnene Spiele"]))), y=final["lower_bound"], name='Gewinnrate')
        bar3 = go.Bar(x=pd.Series(range(1,len(graph_top["Gewonnene Spiele"]))), y=final["upper_bound"], name='Upper bound')
        return {
        'data': [bar, bar2, bar3],
        'layout':
        go.Layout(
            title='Hier sehen Sie die Gewinnrate von Spieler {} bis {}'.format(play[0], play[1]),
            barmode='stack')
    }



#### Tab Trackbenutzung ####
@app.callback(
    dash.dependencies.Output('gewinn_rate', 'figure'),
    [dash.dependencies.Input('spieler', 'value')])
def update_graph(spieler):
    if spieler is None:
       None
    else:
        chall = races_finished[races_finished['challenger'] == spieler]
        opp = races_finished[races_finished['opponent'] == spieler]
        df = pd.concat([chall , opp])
        df = df.counter.groupby(df.track_id).count()
        df = df.reset_index()
        df = df.sort_values(by="track_id")

        trace1 = go.Pie(labels=df.track_id,
                                values=round(df.counter),
                                hoverinfo='label+value+percent', textinfo='value+percent',
                                )

    return {
        'data': [trace1],
        'layout':
        go.Layout(
            title='Tracks nach Häufigkeit Spieler {}'.format(spieler))
    }



#### Tab Wetterbedinung ####
@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('track', 'value')])
def update_graph2(track):
    if (track == "None") or (track is None):
     track1 = go.Pie(labels=races_finished_weather.index.values,
                                values=round(races_finished.counter.groupby(races_finished.weather).sum()),
                                hoverinfo='label+value+percent', textinfo="label",
                                )
     return {
            'data': [track1],
            'layout':
             go.Layout(
                title='Relative Wetterbedinung insgesamt',
                barmode='stack')
        }
    else:
        df_plot = races_finished[races_finished['track_id'] == track]

    track1 = go.Pie(labels=races_finished_weather.index.values,
                                values=round(df_plot.counter.groupby(races_finished.weather).sum()),
                                hoverinfo='label+value+percent', textinfo='label+percent',
                                )
    return {
        'data': [track1],
        'layout':
        go.Layout(
            title='Wetterbedinung Track {}'.format(track),
            barmode='stack')
    }




#### Tab Prediction ####
@app.callback(
    dash.dependencies.Output('predict', 'children'),
    [dash.dependencies.Input('challenger', 'value'),
    dash.dependencies.Input('opponent', 'value'),
    dash.dependencies.Input('input_id', 'value')
    ])

def update_prediction(challenger, opponent, input_id):
    if (challenger == "None") or (opponent == "None") or (input_id == "None"):
        x = []
        None
    else:
        df_model_prep = pd.DataFrame([[input_id, challenger,opponent]], columns=("track_id", 'challenger' ,"opponent"))
        x = model.predict(df_model_prep)
    return html.H5(x)





if __name__ == '__main__':
    app.run_server(debug=False)