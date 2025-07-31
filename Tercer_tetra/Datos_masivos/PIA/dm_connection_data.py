import requests
import pandas as pd
import numpy as np
import time

API_KEY = "313911fac7d0c38dbe69a0e58ee85af8"
BASE_URL = "http://ws.audioscrobbler.com/2.0/"

def get_top_tracks(api_key, limit=7000):
    all_tracks = []
    page = 1
    while len(all_tracks) < limit:
        params = {
            "method": "chart.gettoptracks",
            "api_key": api_key,
            "format": "json",
            "limit": 100,
            "page": page
        }
        res = requests.get(BASE_URL, params=params)
        data = res.json()
        if "tracks" not in data or "track" not in data["tracks"]:
            break
        all_tracks.extend(data["tracks"]["track"])
        page += 1
        time.sleep(0.2)

    return pd.DataFrame([{
        "track_name": t["name"],
        "artist": t["artist"]["name"],
        "listeners": t.get("listeners"),
        "url": t.get("url")
    } for t in all_tracks[:limit]])

def get_track_info(artist, track, api_key):
    params = {
        "method": "track.getInfo",
        "api_key": api_key,
        "artist": artist,
        "track": track,
        "format": "json"
    }
    res = requests.get(BASE_URL, params=params)
    data = res.json()
    track_data = data.get("track", {})
    return {
        "duration": track_data.get("duration"),
        "playcount": track_data.get("playcount"),
        "album": track_data.get("album", {}).get("title"),
        "sadness": track_data.get("sadness"),
        "valance": track_data.get("valance"),
        "age": track_data.get("age"),
        "tags": ", ".join([tag["name"] for tag in track_data.get("toptags", {}).get("tag", [])])
    }

df_top = get_top_tracks(API_KEY)

extra_info = []
for i, row in df_top.iterrows():
    print(f"Procesando {i+1}/{len(df_top)}: {row['track_name']} - {row['artist']}")
    try:
        info = get_track_info(row["artist"], row["track_name"], API_KEY)
    except Exception as e:
        print("Error:", e)
        info = {"duration": None, "playcount": None, "album": None, "tags": None}
    extra_info.append(info)
    time.sleep(0.2)

df_extra = pd.DataFrame(extra_info)

df_original = pd.read_csv("External_data/tcc_ceds_music.csv")
df_lastfm = pd.read_csv("External_data/lastfm_extended_7K.csv")

cols_original = df_original.columns.str.strip().str.lower()
cols_lastfm = df_lastfm.columns.str.strip().str.lower()

columnas_comunes = list(set(cols_original) & set(cols_lastfm))

df_original['track_name'] = df_original['track_name'].str.lower().str.strip()
df_lastfm['track_name'] = df_lastfm['track_name'].str.lower().str.strip()

common_tracks = set(df_original['track_name']) & set(df_lastfm['track_name'])

df_original_common = df_original[df_original['track_name'].isin(common_tracks)].copy()
df_lastfm_common = df_lastfm[df_lastfm['track_name'].isin(common_tracks)].copy()

cols_to_drop = [col for col in df_lastfm_common.columns if col in df_original_common.columns and col != 'track_name']
df_lastfm_common.drop(columns=cols_to_drop, inplace=True)

df_merged = pd.merge(df_original_common, df_lastfm_common, on='track_name', how='inner')

df_merged.to_csv("merged_data_music.csv", index=False)
