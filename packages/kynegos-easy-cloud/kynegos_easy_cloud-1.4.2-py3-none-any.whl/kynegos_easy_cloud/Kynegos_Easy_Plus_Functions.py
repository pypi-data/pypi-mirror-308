import geopandas as gpd
import os
from .Kynegos_functions import list_files_in_gcs_folder, download_file_from_gcs, save_file_temporarily, insert_geometry_to_bigquery
from .Kynegos_GIS_functions import process_gdf_for_bigquery

def create_big_query_geometry_table_from_bucket(bucket_name, folder_path, bigquery_dataset, bigquery_table):
    """
    Descarga archivos de un bucket de Google Cloud Storage, los procesa con geopandas y los sube a una tabla de BigQuery.

    Args:
        bucket_name (str): Nombre del bucket de Google Cloud Storage donde están los archivos.
        folder_path (str): Ruta de la carpeta dentro del bucket desde donde se descargarán los archivos.
        bigquery_dataset (str): Nombre del dataset de BigQuery donde se insertarán los datos procesados.
        bigquery_table (str): Nombre de la tabla en BigQuery donde se subirá el GeoDataFrame.

    Returns:
        None
    """
    print(f"Iniciando el proceso para el bucket '{bucket_name}' y carpeta '{folder_path}'.")

    archivos = list_files_in_gcs_folder(bucket_name, folder_path)
    print(f"Archivos encontrados: {archivos}")

    for archivo in archivos:
        print(f"\nProcesando archivo: {archivo}")
        
        # Descargar el archivo en formato bytes
        file_bytes = download_file_from_gcs(bucket_name, archivo, return_bytes=True)
        print(f"Archivo descargado: {archivo}")

        # Guardar temporalmente el archivo y obtener la ruta local
        local_path = save_file_temporarily(archivo)
        print(f"Archivo guardado temporalmente en: {local_path}")
        
        # Leer el archivo con geopandas
        gdf = gpd.read_file(local_path)
        print(f"GeoDataFrame creado, número de registros: {len(gdf)}")

        # Procesar el GeoDataFrame para BigQuery
        gdf = process_gdf_for_bigquery(gdf)
        print("GeoDataFrame procesado para BigQuery.")

        # Insertar en BigQuery
        insert_geometry_to_bigquery(gdf, bigquery_dataset, bigquery_table)
        print(f"GeoDataFrame insertado en BigQuery en {bigquery_dataset}.{bigquery_table}")

        # Eliminar el archivo local después de procesarlo
        os.remove(local_path)
        print(f"Archivo temporal eliminado: {local_path}")

    print("Proceso completado.")
