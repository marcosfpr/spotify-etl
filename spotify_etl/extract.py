"""
    Extraction of my Spotify recently played musics.
"""

import os
import sys

from datetime import datetime
import datetime

import pandas as pd

import spotipy
from spotipy.oauth2 import SpotifyOAuth


USER_ID = os.environ.get('SPOTIFY_CLIENT_ID')
USER_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')


class InvalidSongError(RuntimeError):
    pass


def validate_song(song: pd.DataFrame) -> bool:
    if song.empty:
        print("[WARNING] No songs downloaded.")
        return False

    if not pd.Series(song["played_at"]).is_unique:
        raise InvalidSongError("[ERROR] Primary key check is violated")

    if song.isnull().values.any():
        raise InvalidSongError("[ERROR] Null song found!")

    # checking timestamps
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    timestamps = song["timestamp"].tolist()
    for timestamp in timestamps:
        if datetime.datetime.strptime(timestamp, '%Y-%m-%d') < yesterday:
            raise InvalidSongError(
                "[ERROR] At least one of the returned songs does not have a yesterday's timestamp: {t} != {y}".format(t=timestamp, y=yesterday))

    return True


def one_day_unix_timestamp():
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000
    return yesterday_unix_timestamp


def extract():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=USER_ID,
                                                    client_secret=USER_SECRET,
                                                    redirect_uri="http://localhost:8888/callback",
                                                    scope="user-read-recently-played"))

    data = sp.current_user_recently_played(limit=50, after=one_day_unix_timestamp())
    #if the length of recently_played is 0 for some reason just exit the program
    if len(data) ==0:
        sys.exit("[WARNING] Any song found: {data}".format(data=data))
        

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []


    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at_list,
        "timestamp": timestamps
    }

    print(song_dict)

    song_dataframe = pd.DataFrame(
        song_dict, columns=["song_name", "artist_name", "played_at", "timestamp"])

    if validate_song(song_dataframe):
        print("[INFO] Data is valid, proceeding to Load stage.")

    return song_dataframe
