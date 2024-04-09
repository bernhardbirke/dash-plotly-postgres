# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
from src.dash.config import Configuration
from src.dash.postgresql_tasks import PostgresTasks

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

config = Configuration()
yaml_data = config.yaml_config()

table_name = yaml_data["table_name"]
columns = yaml_data["columns"]


postgres_task = PostgresTasks()
df = postgres_task.psql_to_df(table_name, columns)
 


# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='Load postgresql data'),
    html.Hr(),
 #   dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='my-final-radio-item-example'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=30),
#    dcc.Graph(figure={}, id='my-final-graph-example')
])

# Add controls to build the interaction
#@callback(
   # Output(component_id='my-final-graph-example', component_property='figure'),
#    Input(component_id='my-final-radio-item-example', component_property='value')
#)
#def update_graph(col_chosen):
#    fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
#    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)