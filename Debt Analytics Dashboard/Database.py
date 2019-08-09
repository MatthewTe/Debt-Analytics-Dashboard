# Importing the necessary Packages:
import sqlite3

import requests
import bs4
import pandas as pd


# Creating the connection to the database:
conn = sqlite3.connect('Fundementals.db')
# Creating the cursor to interact with the database:
c = conn.cursor()

"""
MODULE NAME: df_main():
FUNCTION: This module uses the requests and bs4 packages to collect data from the stockpup.com
website and downloads all the avalible fundemental data .csv files as dataframes. It
then creates a main dataframe containing all the appended .csv files indexed by ticker.
This large, main dataframe is then stored in the 'Fundementals.db' sqlite3 database.
OUTPUT: Populates a sqlite3 database.
"""
def df_main():
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
        file_name = file_name.replace('.csv', '')
        ticker_list.append(file_name)
        df = pd.read_csv(url_list[counter]) # Pulling the .csv from each href url in the list
        # converting it to a data frame
        df.insert(0, 'Ticker', ticker_list[counter])
        counter = counter + 1

        # Appending each new dataframe to the main dataframe:
        main_df = main_df.append(df)


    # Storing the now created main_dataframe to the sqlite3 database:
    main_df.to_sql('Fundementals', con =conn, if_exists='replace')
