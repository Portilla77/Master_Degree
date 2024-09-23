"""Módulo de herramientas de ayuda usadas en el proyecto"""
import os
import pandas as pd
import matplotlib.pyplot as plt

def setup_data_directory() -> str:
    """ Setup the directory for storing data if it does not exist.
        Returns:
            str: The path to the data directory.
    """
    folder_path = os.path.join( os.getcwd(),'Primer_tetra' ,'Metodos_Estadisticos',
                               'Histogramas')
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def save_dataframe(data: pd.DataFrame, filename: str = 'output.xlsx',
                    index: bool = False) -> pd.DataFrame:
    """ Guarda un Dataframe en formato Excel considerando la ruta de setup_data_directory.
        Args:
            data (pandas.DataFrame): DataFrame a guardar
            filename (str, optional):Nombre del archivo que será guardado.
                                     Por default es  'output.xlsx'.
            index (bool, optional): Si es True, el índice del DataFrame se incluirá en el archivo.
                                    False implica que no considerará el indice.
        return (pd.DataFrame): Retorna un dataframe con la información guardada.
    """
    folder_path = setup_data_directory()
    file_path = os.path.join(folder_path, filename)
    data.to_excel(file_path, index=index)
    print(f'DataFrame guardado en: {file_path}')

def save_plot(fig, filename='plot.png', dpi=300, show=True):
    """ Guarda un plot usando la dirección de setup directory.
        Args:
            filename (str, optional):Nombre del archivo que será guardado.
                                     Por default es  'plot.png'.
            dpi (int, optional):Tamaño de la imagen mostrada.
            show (bool, optional): Por default muestra la imagen una vez guardada.
        return (pd.DataFrame): Retorna un dataframe con la información guardada."""
    folder_path = setup_data_directory()
    file_path = os.path.join(folder_path, filename)
    fig.savefig(file_path, dpi=dpi, bbox_inches='tight')
    if show:
        plt.show()
    plt.close(fig)
