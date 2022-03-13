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
            html.Div(className='col-md-12 center', children=[
                html.H1(
                    children=[
                        'You Calendar Analyzer',
                        html.I(className="fa-solid fa-calendar-days calendar-icon"),
                    ]),
                html.Hr(),
            ]),
            html.Div(className='col-md-4'),
            html.Div(
                className='col-md-4 center',
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
            html.Div(
                children=[
                    html.Hr(),
                ],
                style={'clear': 'both'},
            ),
            html.Div(className='col-md-2'),
            html.Div(
                className='col-md-8 total-events center',
                children=[
                    html.H2('Total Events'),
                    html.Hr(),
                    daq.LEDDisplay(
                        id='total-events',
                        value=len(df),
                        size=50,
                    ),
                ]
            ),
            html.Div(className='col-md-2'),
            html.Div(style={'clear': 'both'}),
            html.Div(className='col-md-2'),
            html.Div(
                className='col-md-4 center shrink',
                children=[
                    html.H2('Meetings'),
                    html.Hr(),
                    daq.Gauge(
                        id='total-meetings',
                        label="Default",
                        value=0,
                    ),
                    html.H2('Mins in Meetings'),
                    html.Hr(),
                    daq.LEDDisplay(
                        id='sum-meetings',
                        value=0,
                        size=50,
                    ),
                ]
            ),
            html.Div(
                className='col-md-4 center shrink',
                children=[
                    html.H2('Personal Events'),
                    html.Hr(),
                    daq.Gauge(
                        id='total-personal',
                        label="Default",
                        value=0,
                    ),
                    html.H2('Mins in Personal Events'),
                    html.Hr(),
                    daq.LEDDisplay(
                        id='sum-personal',
                        value=0,
                        size=50,
                    ),
                ]
            ),
            html.Div(className='col-md-2'),
            html.Div(style={'clear': 'both'}),
            html.Div(className='col-md-2'),
            html.Div(
                className='col-md-8 center shrink',
                children=[
                    html.H2('Daily Mins in Meetings Distribution'),
                    html.Hr(),
                    dcc.Graph(
                        id="distribution",
                    ),
                ]
            ),
            html.Div(className='col-md-2'),
            html.Div(style={'clear': 'both'}),
            html.Div(className='col-md-2'),
            html.Div(
                className='col-md-4 center shrink',
                children=[
                    html.H2('Top Participants'),
                    html.Hr(),
                    dash_table.DataTable(
                        id='attendees-table',
                        style_header={
                            'backgroundColor': '#161a28',
                            'color': 'white',
                            'fontWeight': 'bold'
                        },
                        style_as_list_view=True,
                        style_cell={
                            'backgroundColor': '#161a28',
                            'color': 'white'
                        },
                        style_data_conditional=[
                            {
                                "if": {"state": "selected"},
                                "backgroundColor": "inherit !important",
                                "border": "inherit !important",
                            }
                        ]
                    ),
                ]
            ),
            html.Div(
                className='col-md-4 center shrink',
                children=[
                    html.H2('Event Analysis'),
                    html.Hr(),
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
        'background-color': '#1e2130',
    })
