import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import seaborn as sns

# Load & clean data
df = sns.load_dataset("penguins").dropna()

app = dash.Dash(__name__)

app.layout = html.Div([

    html.H1("Penguin Executive Dashboard", style={'textAlign':'center'}),

    # FILTERS
    html.Div([
        dcc.Dropdown(df['species'].unique(), multi=True, placeholder="Species", id='species_filter'),
        dcc.Dropdown(df['island'].unique(), multi=True, placeholder="Island", id='island_filter'),
        dcc.Dropdown(df['sex'].unique(), multi=True, placeholder="Gender", id='gender_filter')
    ], style={'display':'flex','gap':'15px','margin':'10px'}),

    # KPI CARDS
    html.Div([
        html.Div(id='total_penguins'),
        html.Div(id='avg_body_mass'),
        html.Div(id='avg_flipper'),
        html.Div(id='avg_bill'),
        html.Div(id='gender_split')
    ], style={'display':'flex','justifyContent':'space-around','margin':'20px'}),

    # CHART GRID
    html.Div([
        html.Div(dcc.Graph(id='distribution_chart'), style={'width':'48%'}),
        html.Div(dcc.Graph(id='comparison_chart'), style={'width':'48%'})
    ], style={'display':'flex','justifyContent':'space-between'}),

    html.Div([
        html.Div(dcc.Graph(id='relationship_chart'), style={'width':'48%'}),
        html.Div(dcc.Graph(id='correlation_chart'), style={'width':'48%'})
    ], style={'display':'flex','justifyContent':'space-between'})

])

@app.callback(
[
Output('total_penguins','children'),
Output('avg_body_mass','children'),
Output('avg_flipper','children'),
Output('avg_bill','children'),
Output('gender_split','children'),
Output('distribution_chart','figure'),
Output('comparison_chart','figure'),
Output('relationship_chart','figure'),
Output('correlation_chart','figure')
],
[
Input('species_filter','value'),
Input('island_filter','value'),
Input('gender_filter','value')
]
)
def update_dashboard(species, island, gender):

    dff = df.copy()

    if species:
        dff = dff[dff['species'].isin(species)]
    if island:
        dff = dff[dff['island'].isin(island)]
    if gender:
        dff = dff[dff['sex'].isin(gender)]

    total = f"Total Penguins: {len(dff)}"
    avg_mass = f"Avg Body Mass: {round(dff['body_mass_g'].mean(),2)}"
    avg_flipper = f"Avg Flipper Length: {round(dff['flipper_length_mm'].mean(),2)}"
    avg_bill = f"Avg Bill Length: {round(dff['bill_length_mm'].mean(),2)}"

    gender_pct = dff['sex'].value_counts(normalize=True)*100
    gender_split = f"Male %: {round(gender_pct.get('Male',0),1)} | Female %: {round(gender_pct.get('Female',0),1)}"

    dist = px.bar(dff, x='species', title="Species Distribution")

    comp = px.bar(
        dff.groupby('species')['body_mass_g'].mean().reset_index(),
        x='species', y='body_mass_g',
        title="Avg Body Mass by Species"
    )

    rel = px.scatter(
        dff, x='flipper_length_mm', y='body_mass_g',
        color='species',
        title="Flipper vs Body Mass"
    )

    corr = px.imshow(
        dff.corr(numeric_only=True),
        text_auto=True,
        title="Correlation Heatmap"
    )

    return total, avg_mass, avg_flipper, avg_bill, gender_split, dist, comp, rel, corr

if __name__ == '__main__':
    app.run(debug=True)