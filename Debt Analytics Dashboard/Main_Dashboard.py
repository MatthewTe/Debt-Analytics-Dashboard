# Importing the sqlite3 connectors:
import sqlite3
import pandas as pd

# Importing the database management modules:
from Database import pull_request_specific
from Database import pull_request_ticker

# Importing the Dash and assosiated packages:
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Creating the connection to the database:
conn = sqlite3.connect('Fundementals.db', check_same_thread=False)
# Creating the cursor to interact with the database:
c = conn.cursor()

"-------------------------------------------------------------------------------"
"""
MODULE NAME: nest_quotes()
FUNCTION: Nests the input string variable between 'single quotes' for sql query
INPUT: variable(str)
OUTPUT: returns string
"""
def nest_quotes(variable):
     string_variable = "'" + variable + "'"
     return string_variable

"""
MODULE NAME: nest_brackets()
FUNCTION: Nests the input string variable between [square brackers] for sql query
INPUT: variable(str)
OUTPUT: returns string
"""
def nest_brackets(variable):
    bracket_string = "[" + variable + "]"
    return bracket_string

"""
MODULE NAME: pull_request_ticker():
FUNCTION: This module automates the sqlite3 pull request for the data stored in
the 'Fundementals.db' database. The input variable for the function is used in the query
sql string to query all columns corresponding to the input ticker. The function that
pulls the data into a pandas dataframe is the .read_sql_query() function.
INPUT: Ticker(str)
OUTPUT: Returns a pandas dataframe
"""
def pull_request_ticker(Ticker):
    # creating the dataframe using .read_sql_query()
    df = pd.read_sql_query("SELECT * FROM Fundementals WHERE \
    Ticker = " + nest_quotes(Ticker), con = conn, index_col = 'Quarter end' )
    # Dropping the redundant 'Ticker' and 'index' sql query identifiers:
    df = df.drop(['Ticker', 'index'], axis = 1)
    return df
"-------------------------------------------------------------------------------"


# Creating the app:
app = dash.Dash()

app.layout = html.Div(children=[
    # Creating the input child of the Dash app:
    dcc.Input(id='ticker_input', value= '', type='text'),
    html.Div(id='debt_graph_output')
    ])


@app.callback(
    Output(component_id='debt_graph_output', component_property='children'),
    [Input(component_id='ticker_input', component_property='value')])
def update_debt_ratio_graph(input_data):
    input_data = input_data.upper()

    # Creating the dataframe from the input_data variable with database call:
    df = pull_request_ticker(input_data)
    df = df.replace('None', 0)
    df = df.astype({'Long-term debt to equity ratio': 'float'}) # converting the df types
    # Returning the dcc.Graph as a plotted figure:
    # TODO: Add Long term Debt to Equity Ratio trendline to dcc.Graph below:
    return dcc.Graph(
    id='Debt_Ratio_Graph',
    figure = {'data':[
        {'x': df.index, 'y': df['Long-term debt to equity ratio'], 'type': 'bar', 'name': input_data}],
        'layout': {'title': input_data + ' Long-Term Debt to Equity Ratio'}
    })

# TODO: Add graphs plotting assets, Liabilities and the ratio between them

#if __name__ == '__main__':
    #app.run_server(debug=True)
