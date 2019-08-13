# Importing misc packages:
import sqlite3
import pandas as pd
import numpy as np

# Importing the database management modules:
from Database import Ticker

# Importing the Dash and assosiated packages:
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Creating the app:
app = dash.Dash()

app.layout = html.Div(children=[
    # Creating the input child of the Dash app:
    dcc.Input(id ='ticker_input', value= '', type='text'),
    # The .Div Tag containing the First Debt_2_Equity_Graph:
    html.Div(id ='Debt_2_Equity_Graph_output'),
    # The .Div Tag containing the Assets/Liabilities ratio:
    html.Div(id = 'Debt_Ratio_Graph_output'),
    # The .Div Tag containing the Earnings and Earnings Volatility data:
    html.Div(id = 'Earnings_data_output')
    ])

# Generates the Debt to Equity Graph based on user input:
@app.callback(
    Output(component_id='Debt_2_Equity_Graph_output', component_property='children'),
    [Input(component_id='ticker_input', component_property='value')])
def update_debt_2_equity_ratio_graph(input_data):
    input_data = input_data.upper()

    # Creating the dataframe from the input_data variable with database call:
    try:
        df = Ticker(input_data).getFundementals()
        df = df.replace('None', 0)
        df = df.astype({'Long-term debt to equity ratio': 'float'}) # converting the df types
        # Creating the rolling average trendline for the debt_ratio: (window size = 5)
        rolling_mean = df['Long-term debt to equity ratio'].rolling(5, min_periods=4).mean()
        # Returning the dcc.Graph as a plotted figure:
        return dcc.Graph(
        id='Debt_2_Equity_Graph',
        figure = {'data':[
            {'x': df.index, 'y': df['Long-term debt to equity ratio'], 'type': 'bar', 'name': input_data + ' Debt to Equity'},
            {'x': df.index, 'y': rolling_mean, 'type': 'line', 'name':  input_data + ' Moving Average'}
                        ],
            'layout': {'title': input_data + ' Long-Term Debt to Equity Ratio'}
                })
    except:
        return ' No Data'


# Generates The Assets vs Liabilities Graph based on user input:
@app.callback(
    Output(component_id='Debt_Ratio_Graph_output', component_property='children'),
    [Input(component_id='ticker_input', component_property='value')])
def update_debt_Ratio_graph(input_data):
    input_data = input_data.upper()

    # Creating the dataframe by pulling from the sql database and formatting df:
    try:
        df = Ticker(input_data).getFundementals()
        df = df.replace('None', 0)
        df = df.astype({'Assets': 'float', 'Liabilities': 'float'})
        # Creating a new column containing the calculated value needed:
        df["Debt_ratio"] = df['Liabilities']/df['Assets']

        # Creating the .go configs for each Bar plot in the bar chart:
        trace_Assets = go.Bar(x=df.index, y=df.Assets, name= input_data + ' Assets',
         marker_color='rgb(14, 237, 40)')
        trace_Liabilities = go.Bar(x=df.index, y=df.Liabilities, name= input_data + ' Liabilities',
         marker_color='rgb(237, 14, 14)')
        trace_Debt_ratio = go.Scatter(x=df.index, y=df.Debt_ratio, name= input_data + ' Debt Ratio')

        # Creating the Figure that will be inserted into the dcc.Graph object:
        fig = make_subplots(rows=2,cols=1, subplot_titles=('Assets vs Liabilities', 'Debt Ratio'),
        row_heights=[0.7, 0.3])
        fig = fig.add_trace(trace_Assets,row=1,col=1)
        fig = fig.add_trace(trace_Liabilities,row=1,col=1)
        fig = fig.add_trace(trace_Debt_ratio, row=2,col=1)
        fig = fig.update_layout(title_text = input_data + ' Debt Ratio (Assets vs Liabilities)')

        # Creating the dcc.Graph object that will be returned:
        return dcc.Graph(
        id = 'Debt_ratio_graph',
        # Setting the figure to the fig subplot variable described above:
        figure = fig
            )
    except:
        return 'No Data'

# Generates the Earnings and Earnings volatility Graph based on user input:
@app.callback(
    Output(component_id='Earnings_data_output', component_property='children'),
    [Input(component_id='ticker_input', component_property='value')])
def update_Earnings_graphs(input_data):
    input_data = input_data.upper()

    # Creating the dataframe that will be plotted:
    try:
        df = Ticker(input_data).getFundementals()
        df = df.replace('None', 0)
        df = df.astype({'Earnings': 'float'})

        # Creating the plotly subplots to be inserted into the dcc.Graph()
        trace_Earnings = go.Bar(x=df.index, y=df.Earnings, name=input_data + ' Earnings',
         marker_color='rgb(0, 0, 0)')
        trace_Earnings_vol = go.Scatter(x=df.index, y=df.Earnings,
         name=input_data + ' Earnings Volatility ', marker_color= 'rgb(0, 0, 0)')


        # Creating the main subplot figure that will be inserted into the dcc.Graph():
        fig = make_subplots(rows=2,cols=1, subplot_titles=('Earnings Data', 'Earnings Volatility'),
        row_heights=[0.7, 0.3])
        fig = fig.add_trace(trace_Earnings,row=1,col=1)
        fig = fig.add_trace(trace_Earnings_vol,row=2,col=1)
        fig = fig.update_layout(title_text="Earnings Data with Volatility")

        # Returing the graph to the html.Div:
        return dcc.Graph(
            id = 'Earnings_data_graph',
            figure = fig
                )
    except:
        return 'No Data'


# Creating a generic function to run the server on local machine:
def server_run(bool):
    if bool == True:
        if __name__ == '__main__':
            app.run_server(debug=True)
    else:
        pass
server_run(False)
