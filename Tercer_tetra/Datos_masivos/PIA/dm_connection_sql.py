import pandas as pd
import pyodbc

class DatabaseConnection:
    def __init__(self, server, database, username, password, driver='{ODBC Driver 17 for SQL Server}'):
        self.conn_str = (
            f'DRIVER={driver};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password}'
        )
        self.connection = None

    def connect(self):
        try:
            self.connection = pyodbc.connect(self.conn_str)
            print('[INFO] Conexión exitosa a la base de datos MSSQL.')
        except Exception as e:
            print(f'[ERROR] No se pudo conectar a la base de datos: {e}')
            self.connection = None

    def fetch_song_table(self, table='song'):
        if self.connection is None:
            self.connect()
        if self.connection is None:
            raise Exception('No hay conexión a la base de datos.')
        query = f'SELECT id, communication,obscene,music,movement_places,light_visual_perceptions,family_spiritual,like_girls,sadness,feelings,danceability,loudness,acousticness,instrumentalness,valence,energy,topic,age FROM {table}'
        df = pd.read_sql(query, self.connection)
        print(f'[INFO] Se leyeron {len(df)} filas de la tabla {table}.')
        return df

class DatasetBySql:
    def get_allSongs():
        server = 'LUISRODRIGUEZ\BD'
        database = 'BigData_finalProject'
        username = 'main_user'
        password = '123456789'
        db = DatabaseConnection(server, database, username, password)
        db.connect()
        df = db.fetch_song_table()
        return df

DatasetBySql.get_allSongs()