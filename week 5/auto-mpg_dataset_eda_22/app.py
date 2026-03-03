import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd


# Load Dataset

columns = ["mpg","cylinders","displacement","horsepower",
           "weight","acceleration","model_year","origin","car_name"]

df = pd.read_csv("auto-mpg.data",
                 names=columns,
                 sep=r"\s+",
                 na_values="?")

df.dropna(inplace=True)

origin_map = {1: "USA", 2: "Europe", 3: "Japan"}
df["origin"] = df["origin"].map(origin_map)

# KPI Calculations

avg_mpg = round(df["mpg"].mean(), 2)
avg_hp = round(df["horsepower"].mean(), 2)
total_vehicles = df.shape[0]

mpg_year = df.groupby("model_year")["mpg"].mean().reset_index()
yoy_growth = round(((mpg_year["mpg"].iloc[-1] - mpg_year["mpg"].iloc[0])
                    / mpg_year["mpg"].iloc[0]) * 100, 2)


# Create Figures

fig_trend = px.line(mpg_year,
                    x="model_year",
                    y="mpg",
                    title="MPG Trend Over Years")

fig_origin = px.bar(df,
                    x="origin",
                    y="mpg",
                    title="Average MPG by Origin",
                    barmode="group")

fig_weight = px.scatter(df,
                        x="weight",
                        y="mpg",
                        title="MPG vs Weight")

fig_hp = px.scatter(df,
                    x="horsepower",
                    y="mpg",
                    title="MPG vs Horsepower")

fig_hist = px.histogram(df,
                        x="mpg",
                        nbins=15,
                        title="MPG Distribution")


# Initialize App

app = dash.Dash(__name__)
app.title = "Auto MPG Dashboard"


# Layout

app.layout = html.Div([

    html.H1("Auto MPG Performance Dashboard",
            style={"textAlign": "center"}),

    
    # KPI SECTION
   
    html.Div([

        html.Div([
            html.H3("Avg MPG"),
            html.H2(avg_mpg)
        ], className="card"),

        html.Div([
            html.H3("YoY Growth"),
            html.H2(f"{yoy_growth}%")
        ], className="card"),

        html.Div([
            html.H3("Avg Horsepower"),
            html.H2(avg_hp)
        ], className="card"),

        html.Div([
            html.H3("Total Vehicles"),
            html.H2(total_vehicles)
        ], className="card"),

    ], style={"display": "flex",
              "justifyContent": "space-around",
              "marginBottom": "30px"}),

    
    # MIDDLE SECTION
    
    html.Div([
        dcc.Graph(figure=fig_trend, style={"width": "65%"}),
        dcc.Graph(figure=fig_origin, style={"width": "35%"})
    ], style={"display": "flex"}),

    
    # BOTTOM SECTION
    
    html.Div([
        dcc.Graph(figure=fig_weight, style={"width": "33%"}),
        dcc.Graph(figure=fig_hp, style={"width": "33%"}),
        dcc.Graph(figure=fig_hist, style={"width": "33%"})
    ], style={"display": "flex"})

])


# Run Server

if __name__ == "__main__":
    app.run(debug=True)