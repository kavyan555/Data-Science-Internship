import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load Dataset
df = px.data.tips()

# Prep
df['tip_pct'] = (df['tip'] / df['total_bill']) * 100

# Initialize
app = dash.Dash(__name__)
app.title = "RESTAURANT DASHBOARD"

# Layout
app.layout = html.Div([

    html.H1("RESTAURANT ANALYTICS DASHBOARD", style={'textAlign': 'center'}),

    html.Div([

        dcc.Dropdown(
            id='day-dropdown',
            options=[{'label': d, 'value': d} for d in df['day'].unique()],
            value=df['day'].unique(),
            multi=True,
            placeholder="Select Day(s)",
            style={'width': '40%', 'display': 'inline-block'}
        ),

        dcc.Dropdown(
            id='time-dropdown',
            options=[{'label': t, 'value': t} for t in df['time'].unique()],
            value=df['time'].unique(),
            multi=True,
            placeholder="Select Time(s)",
            style={'width': '40%', 'display': 'inline-block', 'marginLeft': '5%'}
        )

    ]),

    html.Br(),

    html.Div(
        id='kpi-card',
        style={
            'padding': '20px',
            'backgroundColor': '#f4f4f4',
            'width': '35%',
            'textAlign': 'center',
            'fontSize': '18px',
            'borderRadius': '10px',
            'margin': 'auto'
        }
    ),

    html.Br(),

    dcc.Graph(id='rev-day'),
    dcc.Graph(id='rev-time'),
    dcc.Graph(id='tip-dist'),
    dcc.Graph(id='bill-vs-tip'),
    dcc.Graph(id='rev-gender'),
    dcc.Graph(id='rev-size'),
    dcc.Graph(id='day-time')

])


# Callback
@app.callback(
    Output('rev-day', 'figure'),
    Output('rev-time', 'figure'),
    Output('tip-dist', 'figure'),
    Output('bill-vs-tip', 'figure'),
    Output('rev-gender', 'figure'),
    Output('rev-size', 'figure'),
    Output('day-time', 'figure'),
    Output('kpi-card', 'children'),
    Input('day-dropdown', 'value'),
    Input('time-dropdown', 'value')
)

def update_dashboard(selected_days, selected_times):

    filtered = df[
        (df['day'].isin(selected_days)) &
        (df['time'].isin(selected_times))
    ]

    # SAFE KPIs
    if len(filtered) == 0:
        return {}, {}, {}, {}, {}, {}, {}, "No Data for Selected Filters"

    total_revenue = filtered['total_bill'].sum()
    total_tips = filtered['tip'].sum()
    avg_tip_pct = filtered['tip_pct'].mean()
    avg_bill = filtered['total_bill'].mean()

    peak_day = filtered.groupby('day')['total_bill'].sum().idxmax()

    kpi_text = html.Div([
        html.H3(f"Total Revenue: {total_revenue:.2f}"),
        html.H3(f"Total Tips: {total_tips:.2f}"),
        html.H3(f"Avg Tip %: {avg_tip_pct:.2f}"),
        html.H3(f"Avg Bill: {avg_bill:.2f}"),
        html.H3(f"Peak Revenue Day: {peak_day}")
    ])

    # Charts
    rev_day = px.bar(filtered, x='day', y='total_bill', title='Revenue by Day')

    rev_time = px.bar(filtered, x='time', y='total_bill', title='Revenue by Time')

    tip_dist = px.histogram(filtered, x='tip_pct', title='Tip % Distribution')

    bill_tip = px.scatter(filtered, x='total_bill', y='tip', title='Total Bill vs Tip')

    rev_gender = px.bar(filtered, x='sex', y='total_bill', title='Revenue by Gender')

    rev_size = px.bar(filtered, x='size', y='total_bill', title='Revenue by Size')

    day_time = px.box(filtered, x='day', y='total_bill', color='time',
                      title='Day + Time Revenue')

    return rev_day, rev_time, tip_dist, bill_tip, rev_gender, rev_size, day_time, kpi_text


# Run
if __name__ == "__main__":
    app.run(debug=True)