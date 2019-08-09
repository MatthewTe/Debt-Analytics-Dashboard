# Importing the necessary Packages:
import sqlite3

import requests
import bs4
import pandas as pd


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


# Creating the connection to the database:
conn = sqlite3.connect('Fundementals.db')
# Creating the cursor to interact with the database:
c = conn.cursor()


"""
MODULE NAME: db_update():
FUNCTION: This module uses the requests and bs4 packages to collect data from the stockpup.com
website and downloads all the avalible fundemental data .csv files as dataframes. It
then creates a main dataframe containing all the appended .csv files indexed by ticker.
This large, main dataframe is then stored in the 'Fundementals.db' sqlite3 database.
OUTPUT: Populates a sqlite3 database.
"""
def db_update():
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
    # Creating the main dataframe that will be used to construct the large main df:
    main_df = pd.DataFrame()
    for i in url_list:
        file_name = url_list[counter].replace("http://www.stockpup.com/data/", "")
        file_name = file_name.replace('_quarterly_financial_data', '')
        file_name = file_name.replace('.csv', '') # Removing all the values from the link that is not the ticker name
        ticker_list.append(file_name)
        df = pd.read_csv(url_list[counter]) # Pulling the .csv from each href url in the list
        # converting it to a data frame
        df.insert(0, 'Ticker', ticker_list[counter])
        counter = counter + 1

        # Appending each new dataframe to the main dataframe:
        main_df = main_df.append(df)


    # Storing the now created main_dataframe to the sqlite3 database:
    main_df.to_sql('Fundementals', con =conn, if_exists='replace')



"""
MODULE NAME: pull_request_specific():
FUNCTION: This module is used to automate the sqlite3 pull request for the data
stored in the 'Fundementals.db'. It uses the pandas .read_sql_query() function
to convert the data query directly into a pandas dataframe.
INPUT: Ticker(str), index(str), column_main(str)
OUTPUT: Returns a pandas dataframe
"""
def pull_request_specific(Ticker, index, column_main):

    """Creating the dataframe from the .read_sql_query() function and substituting
    key elements in the sql query string with input variables so that it pulls the desired
    column indexed by the desired row."""
    df = pd.read_sql_query("SELECT DISTINCT " + nest_brackets(index) + "," + "\
     " + nest_brackets(column_main) + " FROM Fundementals WHERE Ticker = " + nest_quotes(Ticker) , con = conn, index_col = index)
    return df



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
