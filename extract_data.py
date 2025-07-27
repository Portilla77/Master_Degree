import requests
import pandas as pd
import time

API_KEY = "313911fac7d0c38dbe69a0e58ee85af8"  # Sustituye con tu API Key
BASE_URL = "http://ws.audioscrobbler.com/2.0/"

# Paso 1: Obtener el top de canciones
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
    # Limita a 1000
    return pd.DataFrame([{
        "track_name": t["name"],
        "artist": t["artist"]["name"],
        "listeners": t.get("listeners"),
        "url": t.get("url")
    } for t in all_tracks[:limit]])

# Paso 2: Obtener info extra
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
        "tags": ", ".join([tag["name"] for tag in track_data.get("toptags", {}).get("tag", [])])
    }

#Paso 3: Ejecutar todo
df_top = get_top_tracks(API_KEY)

#Enriquecer con más información
extra_info = []
for i, row in df_top.iterrows():
    print(f"Procesando {i+1}/{len(df_top)}: {row['track_name']} - {row['artist']}")
    try:
        info = get_track_info(row["artist"], row["track_name"], API_KEY)
    except Exception as e:
        print("Error:", e)
        info = {"duration": None, "playcount": None, "album": None, "tags": None}
    extra_info.append(info)
    time.sleep(0.2)  # Para no saturar la API

df_extra = pd.DataFrame(extra_info)
# df_final = pd.concat([df_top, df_extra], axis=1)

# # Paso 4: Guardar CSV
# df_final.to_csv("lastfm_extended_10K.csv", index=False)
# print("CSV guardado con éxito")


# Cargar datasets
df_original = pd.read_csv("External_data/tcc_ceds_music.csv")
df_lastfm = pd.read_csv("lastfm_extended_7K.csv")


df_original["track_name_clean"] = df_original["track_name"].str.strip().str.lower()
df_lastfm["track_name_clean"] = df_lastfm["track_name"].str.strip().str.lower()

coincidencias = df_original[df_original["track_name_clean"].isin(df_lastfm["track_name_clean"])]

print(f"Coincidencias: {len(coincidencias)}")
print(coincidencias[["track_name"]].head())


