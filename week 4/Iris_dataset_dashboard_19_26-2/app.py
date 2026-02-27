# IMPORT LIBRARIES
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
from sklearn.datasets import load_iris

# LOAD DATA
iris = load_iris()

df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df['species'] = iris.target
df['species'] = df['species'].map({0:'Setosa',1:'Versicolor',2:'Virginica'})

# APP INITIALIZE
app = Dash(__name__)

# LAYOUT
app.layout = html.Div([

    html.H1("Interactive Iris Dashboard", style={'textAlign':'center'}),

    html.H3("Filter by Species"),

    dcc.Dropdown(
        id='species-filter',
        options=[{'label':s, 'value':s} for s in df['species'].unique()],
        value=df['species'].unique().tolist(),
        multi=True
    ),

    html.Br(),

    html.Div(id='kpi-output'),

    dcc.Graph(id='pie-chart'),
    dcc.Graph(id='box-plot'),
    dcc.Graph(id='pair-plot'),
    dcc.Graph(id='heatmap')

])

# CALLBACK
@app.callback(
    Output('kpi-output','children'),
    Output('pie-chart','figure'),
    Output('box-plot','figure'),
    Output('pair-plot','figure'),
    Output('heatmap','figure'),
    Input('species-filter','value')
)

def update_dashboard(selected_species):

    filtered_df = df[df['species'].isin(selected_species)]

    # KPI
    total_records = len(filtered_df)

    species_count = filtered_df['species'].value_counts().reset_index()
    species_count.columns = ['species','count']

    # PIE
    pie = px.pie(
        species_count,
        names='species',
        values='count',
        title='Species Distribution'
    )

    # BOX
    box = px.box(
        filtered_df,
        x='species',
        y='petal length (cm)',
        title='Petal Length by Species'
    )

    # PAIR PLOT
    pair = px.scatter_matrix(
        filtered_df,
        dimensions=filtered_df.columns[:-1],
        color='species',
        title='Pair Plot'
    )

    # HEATMAP
    if len(filtered_df) > 1:
       corr = filtered_df.drop('species',axis=1).corr()
       heat = px.imshow(corr, text_auto=True, title='Correlation Heatmap')
    else:
       heat = px.imshow([[0]], text_auto=True, title='Not enough data for correlation')
       
    # KPI DISPLAY
    kpi = html.H3(f"Total Records: {total_records}")

    return kpi, pie, box, pair, heat


# RUN APP
if __name__ == '__main__':
    app.run(debug=True)
