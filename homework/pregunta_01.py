"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd
import re

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """

    def titulo(head):
        # Fomato titulos
        return head.lower().replace(" ", "_")

    # Leer el archivo ignorando las líneas en blanco al inicio
    with open("files/input/clusters_report.txt", "r", encoding="utf-8") as file:
        lineas = file.readlines()
    
    # Limpieza titulos
    t1 = re.sub(r"\s{2,}", "-", lineas[0]).strip().split("-")
    t2 = re.sub(r"\s{2,}", "-", lineas[1]).strip().split("-")
    t1.pop()
    t2.pop(0)

    cabeceras = [
        t1[0],  
        f"{t1[1]} {t2[0]}",  
        f"{t1[2]} {t2[1]}",
        t1[3], 
    ]    

    # Aplicar formato
    cabeceras = [titulo(t) for t in cabeceras]

    # Crear la data
    df = pd.read_fwf("files/input/clusters_report.txt", widths = [9, 16, 16, 80], 
        header = None, names = cabeceras, skip_blank_lines = False,
        converters = {cabeceras[2]: lambda x: x.rstrip(" %").replace(",", ".")},
    ).iloc[4:] 

    # Limpiar palabras clave
    palabras_clave = df[cabeceras[3]]
    df = df[df[cabeceras[0]].notna()].drop(columns=[cabeceras[3]])
    df = df.astype({
        cabeceras[0]: int,
        cabeceras[1]: int,
        cabeceras[2]: float,
    })

    # Guardar palabras clave
    claves = []
    texto = ""
    for p in palabras_clave:
        if isinstance(p, str): 
            if p.endswith("."): 
                p = p[:-1]
            p = re.sub(r'\s+', ' ', p).strip()
            texto += p + " "
        elif texto: 
            claves.append(", ".join(re.split(r'\s*,\s*', texto.strip())))
            texto = ""
    if texto:
        claves.append(", ".join(re.split(r'\s*,\s*', texto.strip())))

    df[cabeceras[3]] = claves

    return df  

print(pregunta_01())
