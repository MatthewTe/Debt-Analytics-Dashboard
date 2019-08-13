# Importing the Sqlite3 and the sqlalchemy packages:
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

# Importing other packages:
import os
import sys
import requests
import bs4
import pandas as pd

Base = declarative_base()

# Creating the ORM for Ticker Fundemental data scraped by stockpup.com:
class Ticker_fundementals(Base):
    # Defining the table name based on a string input:
    __tablename__ = ticker_name
    # Defining the column names and types based on the stockpup .csv format:
    Quarter = Column(Date, nullable = False, primary_key = True)
    Shares = Column(Integer)
    Shares_split_adjusted = Column(Integer)
    Split_factor = Column(Integer)
    Assets = Column(Integer)
    Current_Assets = Column(Integer)
    Liabilities = Column(Integer)
    Current_Liabilities = Column(Integer)
    Shareholders_equity = Column(Integer)
    Non_controlling_interest = Column(Integer)
    Preferred_equity = Column(Integer)
    Goodwill_and_intangibles = Column(Integer)
    Long_term_debt = Column(Integer)
    Revenue = Column(Integer)
    Earnings = Column(Integer)
    Earnings_available_for_common_stockholders = Column(Integer)
    EPS_basic = Column(Integer)
    EPS_diluted = Column(Integer)
    Dividend_per_share = Column(Integer)
    Cash_from_operating_activities = Column(Integer)
    Cash_from_investing_activities = Column(Integer)
    Cash_from_financing_activities = Column(Integer)
    Cash_change_during_period = Column(Integer)
    Cash_at_end_of_period = Column(Integer)
    Capital_expenditures = Column(Integer)
    Price = Column(String(250))
    Price_high = Column(String(250))
    Price_low = Column(String(250))
    ROE = Column(String(250))
    ROA = Column(String(250))
    Book_value = Column(String(250))
    P_2_B_ratio = Column(String(250))
    P_2_E_ratio = Column(String(250))
    Cumulative_dividends_per_share = Column(Integer)
    Dividend_payout_ratio = Column(Integer, nullable = True)
    Long_term_debt_to_equity_ratio = Column(String(250))
    Equity_to_assets_ratio = Column(String(250))
    Net_margin = Column(String(250))
    Asset_turnover = Column(String(250))
    Free_cash_flow_per_share = Column(String(250))
    Current_ratio = Column(String(250))



engine = create_engine('sqlite:///ORM_Database_Test.db')
Base.metadata.create_all(engine)
