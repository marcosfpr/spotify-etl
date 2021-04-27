"""
    Load extracted songs to database
"""
import sqlalchemy
import pandas as pd

from spotify_etl.db import with_connection, get_url

def load(songs: pd.DataFrame):
    if songs is not None:
        @with_connection
        def create_table(cnn):
            cur = cnn.cursor()

            sql_query = """
            CREATE TABLE IF NOT EXISTS tracks(
                song_name   VARCHAR(200),
                played_at   VARCHAR(200),
                artist_name VARCHAR(200),
                timestamp   VARCHAR(200),
                CONSTRAINT pk_played_at PRIMARY KEY (played_at))
            """

            cur.execute(sql_query)
            
            print("[INFO] Opened database successfully!")
                    
        create_table()

        engine = sqlalchemy.create_engine(get_url())

        try:
            songs.to_sql("tracks", engine, index=False, if_exists='append')
        except:
            print("[WARNING] Data already exists in database")
        
    