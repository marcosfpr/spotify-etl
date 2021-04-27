"""
    Main ETL application file.]
    Extracting all listened songs in spotify in the past 24hrs
"""

from spotify_etl.load import load
from spotify_etl.extract import extract

load(extract())