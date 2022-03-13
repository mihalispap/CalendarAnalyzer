import json

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from dash import dash, Output, Input, State

import settings
import utils.analyzer
from dashboard import dashboard

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        '/assets/css/styles.css',
        '/assets/css/all.min.css'
    ],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
)

dashboard.setup(app)


@app.callback(
    [
        Output(component_id="total-events", component_property="value"),
        Output(component_id="total-meetings", component_property="value"),
        Output(component_id="total-meetings", component_property="max"),
        Output(component_id="total-personal", component_property="value"),
        Output(component_id="total-personal", component_property="max"),
        Output(component_id="sum-meetings", component_property="value"),
        Output(component_id="sum-personal", component_property="value"),
        Output(component_id="distribution", component_property="figure"),
        Output(component_id="attendees-table", component_property="data"),
        Output(component_id="event-analysis-wordcloud", component_property="src"),
    ],
    [
        Input(component_id='btn-submit', component_property='n_clicks'),
        State(component_id='date-picker-range', component_property='start_date'),
        State(component_id='date-picker-range', component_property='end_date'),
    ])
def update_charts(_, start_date, end_date):
    df = pd.json_normalize(json.load(open(f'{settings.JSON_DIR}events.json', 'r')))

    df = df[(df['start'] >= start_date) & (df['start'] <= end_date)]

    df['duration'] = (pd.to_datetime(df['end']) - pd.to_datetime(df['start'])).astype('timedelta64[m]')

    meetings_df = df[df['attendees'].notnull()]
    personal_df = df[df['attendees'].isnull()]

    cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    agg_df = meetings_df.groupby(pd.to_datetime(df['start'], utc=True).dt.day_name()).sum()
    agg_df = agg_df.reindex(cats).reset_index()

    attendees_df = df.explode('attendees').groupby(['attendees'])['belongs_to'].count().reset_index(name="count").sort_values('count', ascending=False)

    fig = px.bar(
        data_frame=agg_df,
        x='start',
        y="duration",
        color_discrete_sequence=['#2596be']
    )
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'font_color': '#fff',
    })

    return [
        len(df),
        len(meetings_df),  # meetings are events with attendees
        len(df),
        len(personal_df),  # personal events are the ones without attendees
        len(df),
        round(meetings_df['duration'].sum()),
        round(personal_df['duration'].sum()) if len(personal_df) else 0.0,
        fig,
        [record for record in attendees_df[1:settings.TOPN + 1].to_dict("records")],
        utils.analyzer.generate_wordcloud(df, 'summary')
    ]


if __name__ == '__main__':
    app.run_server()
