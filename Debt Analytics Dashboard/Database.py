# Importing the necessary Packages:
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import os
import sys
import requests
import bs4
import pandas as pd

# Creating the connection to the database:
conn = sqlite3.connect('Securities_Data.db', check_same_thread=False)
# Creating the cursor to interact with the database:
c = conn.cursor()

# Using the existing functions below to create an ORM type class structure:
class Ticker(object):
    def __init__(self, Ticker):
        self.Ticker = Ticker
        self.Ticker_fundementals = pull_request_ticker_Fundementals(Ticker)

    def getFundementals(self):
        return self.Ticker_fundementals

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
MODULE NAME: db_update_Fundementals():
FUNCTION: This module uses the requests and bs4 packages to collect data from the stockpup.com
website and downloads all the avalible fundemental data .csv files as dataframes.
It then uses the pandas.DataFrame.to_sql() function to create a sql table containing all
of the fundmental data for each ticker and write the data to the sqlite3 database.
OUTPUT: Populates a sqlite3 database.
"""
def db_update_Fundementals():
    # Dowloading the HTML data:
    url = "http://www.stockpup.com/data/"
    res = requests.get(url)
    res.raise_for_status()
    # Parsing the downloaded HTML with beautiful soup:
    stockpup = bs4.BeautifulSoup(res.text)
    # Parsing the HTML to select the elements that contain the imbeded links:
    imbeded_links = stockpup.find_all('p')


    url_list = [] # Creating the empty list to store the href links:
    counter = 7 # THe .csv href files do not start untill # 7 in the list.
    # Creating the while loop that selects the .csv href link and converts it into
    # a readable list of strings for Parsing using pandas.
    while "http://www.stockpup.com/data/ZTS_quarterly_financial_data.csv" not in url_list:
        href = imbeded_links[counter].find_all('a', href=True)[1] # Selecting the .csv href instead of the .xml
        link = "http://www.stockpup.com" + href['href'] # appending the href link to the web url.
        url_list.append(link) # appending the url to the list.
        counter = counter + 1


    # Creating the for loop that goes through each element in the url_list and converts it into a
    # data frame, then saves each data frame as a .csv file in the "stockpup_csv_database" directoty.
    ticker_list = []
    counter = 0
    for i in url_list:
        file_name = url_list[counter].replace("http://www.stockpup.com/data/", "")
        file_name = file_name.replace('_quarterly_financial_data', '')
        file_name = file_name.replace('.csv', '') # Removing all the values from the link that is not the ticker name
        ticker_list.append(file_name)
        df = pd.read_csv(url_list[counter]) # Pulling the .csv from each href url in the list
        # Creating the sqlite3 table and populating it with the dataframe:
        df.to_sql(file_name + '_Fundementals', con = conn, if_exists='replace', index=False)
        counter = counter + 1
"""
MODULE NAME: pull_request_ticker_Fundementals():
FUNCTION: This module automates the sqlite3 pull request for the data stored in
the 'Fundementals.db' database. The input variable for the function is used in the query
sql string to query all columns corresponding to the input ticker. The function that
pulls the data into a pandas dataframe is the .read_sql_query() function.
INPUT: Ticker(str)
OUTPUT: Returns a pandas dataframe
"""
def pull_request_ticker_Fundementals(Ticker):
    # creating the dataframe using .read_sql_query()
    df = pd.read_sql_query("SELECT * FROM " + Ticker + '_Fundementals', con = conn, index_col = 'Quarter end' )
    # Dropping the redundant 'Ticker' and 'index' sql query identifiers:
    #df = df.drop(['Ticker', 'index'], axis = 1)
    return df
