"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import pandas as pd
import os
import numpy as np
import csv

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    # Cargar datos con la primera columna como índice
    archivo_entrada = "files/input/solicitudes_de_credito.csv"
    datos = pd.read_csv(archivo_entrada, sep=";", index_col=0)

    # Crear copia para manipular
    datos_limpios = datos.copy()

    # 1. Normalizar columna sexo: minúsculas y convertir a categoría
    datos_limpios["sexo"] = (
        datos_limpios["sexo"]
        .str.lower()
        .astype("category")
    )

    # 2. Procesar fechas con dos formatos posibles (dd/mm/yyyy y yyyy/mm/dd)
    columna_fecha = "fecha_de_beneficio"
    formato1 = pd.to_datetime(
        datos_limpios[columna_fecha],
        format="%d/%m/%Y",
        errors="coerce"
    )
    formato2 = pd.to_datetime(
        datos_limpios[columna_fecha],
        format="%Y/%m/%d",
        errors="coerce"
    )
    # Usar formato1 y rellenar NaT con formato2
    datos_limpios[columna_fecha] = formato1.combine_first(formato2)

    # 3. Limpiar montos: quitar símbolos y decimales, convertir a entero
    datos_limpios["monto_del_credito"] = (
        datos_limpios["monto_del_credito"]
        .str.strip()
        .str.replace(r"[$,]", "", regex=True)
        .str.replace(".00", "", regex=False)
        .astype(int)
    )

    # 4. Normalizar barrio: minúsculas y reemplazar guiones/guiones bajos
    datos_limpios["barrio"] = (
        datos_limpios["barrio"]
        .str.lower()
        .str.replace(r"[_-]", " ", regex=True)
    )

    # 5. Normalizar otras columnas de texto
    columnas_normalizar = ["idea_negocio", "línea_credito", "tipo_de_emprendimiento"]
    for col in columnas_normalizar:
        datos_limpios[col] = (
            datos_limpios[col]
            .str.lower()
            .str.replace(r"[_-]", " ", regex=True)
            .str.strip()
        )

    # 6. Eliminar duplicados y valores nulos
    datos_limpios = datos_limpios.drop_duplicates()
    datos_limpios = datos_limpios.dropna()

    # 7. Guardar archivo limpio
    directorio_salida = "files/output/"
    os.makedirs(directorio_salida, exist_ok=True)
    
    ruta_salida = os.path.join(directorio_salida, "solicitudes_de_credito.csv")
    datos_limpios.to_csv(ruta_salida, sep=";", index=True)

    return datos_limpios
    
    
    
    
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
