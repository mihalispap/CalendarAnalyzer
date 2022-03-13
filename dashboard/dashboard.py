import datetime
import json

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, dash_table
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import html
import settings
from pathlib import Path
from utils import parser
import pandas as pd


def setup(app: dash.Dash):
    _setup_structure()
    _setup_layout(app)


def _setup_structure():
    Path(settings.CALENDARS_DIR).mkdir(parents=True, exist_ok=True)
    Path(settings.JSON_DIR).mkdir(parents=True, exist_ok=True)
    Path(settings.IMG_DIR).mkdir(parents=True, exist_ok=True)
    parser.iterate_through_calendars(settings.CALENDARS_DIR, settings.JSON_DIR)


def _setup_layout(app: dash.Dash):
    theme = {
        'dark': True,
        'detail': '#007439',
        'primary': '#00EA64',
        'secondary': '#6E6E6E',
    }

    df = pd.json_normalize(json.load(open(f'{settings.JSON_DIR}events.json', 'r')))
    app.title = 'Your Calendar Analyzer :)'
    root_layout = html.Div(
        id='dark-theme-container',
        className='row',
        children=[
            html.Div(className='col-md-4'),
            html.Div(
                className='col-md-4',
                children=[
                    html.Div(
                        children=[
                            dcc.DatePickerRange(
                                id='date-picker-range',
                                min_date_allowed=df['start'].min(),
                                max_date_allowed=df['end'].max(),
                                initial_visible_month=df['start'].min(),
                                display_format='Y-MM-DD',
                                start_date=pd.to_datetime(df['start'].min()),
                                end_date=datetime.datetime.now()
                            ),
                            html.Button('Apply', id='btn-submit', n_clicks=0),
                        ]),
                ]
            ),
            html.Div(className='col-md-4'),
            html.Div(style={'clear': 'both'}),
            html.Div(className='col-md-2'),
            html.Div(
                className='col-md-8',
                children=[
                    html.H2('Total Events'),
                    daq.LEDDisplay(
                        id='total-events',
                        value=len(df),
                        color='#92e0d3',
                        backgroundColor='#1e2130',
                        size=50,
                    ),
                ]
            ),
            html.Div(className='col-md-2'),
            html.Div(style={'clear': 'both'}),
            html.Div(className='col-md-2'),
            html.Div(
                className='col-md-4',
                children=[
                    html.H2('Meetings'),
                    daq.LEDDisplay(
                        id='total-meetings',
                        value=len(df),
                        color='#92e0d3',
                        backgroundColor='#1e2130',
                        size=50,
                    ),
                    daq.LEDDisplay(
                        id='avg-meetings',
                        value=len(df),
                        color='#92e0d3',
                        backgroundColor='#1e2130',
                        size=50,
                    ),
                ]
            ),
            html.Div(
                className='col-md-4',
                children=[
                    html.H2('Persoanl Events'),
                    daq.LEDDisplay(
                        id='total-personal',
                        value=len(df),
                        color='#92e0d3',
                        backgroundColor='#1e2130',
                        size=50,
                    ),
                    daq.LEDDisplay(
                        id='avg-personal',
                        value=len(df),
                        color='#92e0d3',
                        backgroundColor='#1e2130',
                        size=50,
                    ),
                ]
            ),
            html.Div(className='col-md-2'),
            html.Div(style={'clear': 'both'}),
            html.Div(className='col-md-2'),
            html.Div(
                className='col-md-8',
                children=[
                    html.H2('Distribution'),
                    dcc.Graph(
                        id="distribution",
                    ),
                ]
            ),
            html.Div(className='col-md-2'),
            html.Div(style={'clear': 'both'}),
            html.Div(className='col-md-2'),
            html.Div(
                className='col-md-4',
                children=[
                    html.H2('Attendees'),
                    dash_table.DataTable(
                        id='attendees-table',
                    ),
                ]
            ),
            html.Div(
                className='col-md-4',
                children=[
                    html.H2('Event Analysis'),
                    html.Img(id='event-analysis-wordcloud'),
                ]
            ),
            html.Div(className='col-md-2'),
        ])

    app.layout = html.Div(id='dark-theme-components', children=[
        daq.DarkThemeProvider(theme=theme, children=root_layout)
    ], style={
        'border': 'solid 1px #A2B1C6',
        'border-radius': '5px',
        'padding': '50px',
        'margin-top': '20px',
        'background-color': '#303030',
    })
