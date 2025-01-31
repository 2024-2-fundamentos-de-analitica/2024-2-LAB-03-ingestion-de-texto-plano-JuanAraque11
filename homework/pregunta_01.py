"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd
import re

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'.
    """
    
    # Leer el archivo ignorando las líneas en blanco al inicio
    with open("files/input/clusters_report.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    # Determinar la línea donde inician los datos
    start_index = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("Cluster"):  # Encontrar el encabezado de las columnas
            start_index = i + 1
            break
    
    # Extraer el contenido de datos sin encabezado
    data_lines = lines[start_index:]
    
    # Lista para almacenar las filas procesadas
    data = []
    
    # Variables auxiliares para unir líneas de palabras clave
    current_cluster = None
    current_count = None
    current_percentage = None
    current_keywords = ""
    
    for line in data_lines:
        line = line.rstrip()
        if not line:
            continue  # Saltar líneas vacías
        
        # Intentar capturar una nueva línea de cluster
        match = re.match(r"(\d+)\s+(\d+)\s+([\d\.]+)%\s+(.*)", line)
        
        if match:
            # Si ya se estaba construyendo una fila, agregarla a la lista
            if current_cluster is not None:
                data.append([current_cluster, current_count, current_percentage, current_keywords.strip()])
            
            # Capturar nuevos valores
            current_cluster = int(match.group(1))
            current_count = int(match.group(2))
            current_percentage = float(match.group(3))
            current_keywords = match.group(4)
        else:
            # Línea de continuación de palabras clave
            current_keywords += " " + line.strip()
    
    # Agregar la última fila procesada
    if current_cluster is not None:
        data.append([current_cluster, current_count, current_percentage, current_keywords.strip()])
    
    # Crear DataFrame
    df = pd.DataFrame(data, columns=["cluster", "cantidad_de_palabras_clave", "porcentaje_de_palabras_clave", "principales_palabras_clave"])
    
    # Normalizar las palabras clave (quitar espacios extra y separar por coma correctamente)
    df["principales_palabras_clave"] = df["principales_palabras_clave"].apply(lambda x: re.sub(r"\s*,\s*", ", ", x))
    
    return df
