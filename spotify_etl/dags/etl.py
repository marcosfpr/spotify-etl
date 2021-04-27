"""
    Main ETL application file.]
    Extracting all listened songs in spotify in the past 24hrs
"""

from spotify_etl.load import load
from spotify_etl.extract import extract

def run_spotify_etl():
    load(extract())


if __name__ == '__main__':
    run_spotify_etl()