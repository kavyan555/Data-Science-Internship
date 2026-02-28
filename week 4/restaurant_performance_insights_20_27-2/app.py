import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import seaborn as sns

df = sns.load_dataset("tips")
df["tip_percent"] = (df["tip"] / df["total_bill"]) * 100

app = dash.Dash(__name__)
app.title = "Restaurant Dashboard"

app.layout = html.Div([

    html.H1("Restaurant Business Dashboard", style={'textAlign':'center'}),

    # FILTERS
    html.Div([

        dcc.Dropdown(
            id='day-filter',
            options=[{'label': d, 'value': d} for d in df['day'].unique()],
            multi=True,
            placeholder="Select Day"
        ),

        dcc.Dropdown(
            id='time-filter',
            options=[{'label': t, 'value': t} for t in df['time'].unique()],
            multi=True,
            placeholder="Select Time"
        )

    ], style={'display':'flex','gap':'20px','padding':'10px'}),

    # KPI CARDS
    html.Div(id='kpis', style={
        'display':'flex',
        'justifyContent':'space-around',
        'padding':'10px'
    }),

    # ROW 1
    html.Div([
        dcc.Graph(id='rev-day', style={'width':'33%'}),
        dcc.Graph(id='rev-time', style={'width':'33%'}),
        dcc.Graph(id='smoking', style={'width':'33%'})
    ], style={'display':'flex'}),

    # ROW 2
    html.Div([
        dcc.Graph(id='tip-dist', style={'width':'33%'}),
        dcc.Graph(id='bill-tip', style={'width':'33%'}),
        dcc.Graph(id='rev-gender', style={'width':'33%'})
    ], style={'display':'flex'}),

    # ROW 3
    html.Div([
        dcc.Graph(id='rev-size', style={'width':'50%'}),
        dcc.Graph(id='day-time', style={'width':'50%'})
    ], style={'display':'flex'})

])

@app.callback(
    Output('kpis','children'),
    Output('rev-day','figure'),
    Output('rev-time','figure'),
    Output('smoking','figure'),
    Output('tip-dist','figure'),
    Output('bill-tip','figure'),
    Output('rev-gender','figure'),
    Output('rev-size','figure'),
    Output('day-time','figure'),
    Input('day-filter','value'),
    Input('time-filter','value')
)
def update_dashboard(days, times):

    filtered = df.copy()

    if days:
        filtered = filtered[filtered["day"].isin(days)]

    if times:
        filtered = filtered[filtered["time"].isin(times)]

    total_revenue = filtered["total_bill"].sum()
    total_tips = filtered["tip"].sum()
    avg_tip_percent = filtered["tip_percent"].mean()
    avg_bill = filtered["total_bill"].mean()
    peak_day = filtered.groupby("day")["total_bill"].sum().idxmax()

    kpis = [
        html.Div(f"Revenue: ${total_revenue:.2f}"),
        html.Div(f"Tips: ${total_tips:.2f}"),
        html.Div(f"Avg Tip %: {avg_tip_percent:.2f}%"),
        html.Div(f"Avg Bill: ${avg_bill:.2f}"),
        html.Div(f"Peak Day: {peak_day}")
    ]

    rev_day = px.bar(filtered.groupby("day")["total_bill"].sum().reset_index(),
                     x="day", y="total_bill", title="Revenue by Day")

    rev_time = px.pie(filtered, names="time", values="total_bill",
                      title="Revenue by Time")

    smoking = px.pie(filtered, names="smoker", values="total_bill",
                     title="Smoking vs Non-Smoking")

    tip_dist = px.histogram(filtered, x="tip_percent",
                            title="Tip % Distribution")

    bill_tip = px.scatter(filtered, x="total_bill", y="tip",
                          title="Bill vs Tip")

    rev_gender = px.bar(filtered.groupby("sex")["total_bill"].sum().reset_index(),
                        x="sex", y="total_bill",
                        title="Revenue by Gender")

    rev_size = px.bar(filtered.groupby("size")["total_bill"].sum().reset_index(),
                      x="size", y="total_bill",
                      title="Revenue by Size")

    day_time = px.bar(filtered.groupby(["day","time"])["total_bill"].sum().reset_index(),
                      x="day", y="total_bill", color="time",
                      title="Day + Time Revenue")

    return kpis, rev_day, rev_time, smoking, tip_dist, bill_tip, rev_gender, rev_size, day_time

if __name__ == "__main__":
    app.run(debug=True)