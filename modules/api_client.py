"""
Módulo cliente para la API de pensiones
Maneja todas las comunicaciones con la API backend
"""

import requests
import streamlit as st

# URL base de la API
API_BASE_URL = "https://pension-bases-api-e707c1384c99.herokuapp.com"


def check_api_health():
    """
    Verificar el estado de la API
    
    Returns:
        tuple: (is_healthy: bool, response_data: dict)
    """
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        return response.status_code == 200, response.json() if response.status_code == 200 else None
    except Exception as e:
        return False, str(e)


def extract_bases(file):
    """
    Extraer bases de cotización de un PDF
    
    Args:
        file: Archivo PDF subido
        
    Returns:
        tuple: (success: bool, result: dict)
    """
    try:
        files = {"file": file}
        response = requests.post(f"{API_BASE_URL}/api/extract", files=files, timeout=60)
        return response.status_code == 200, response.json()
    except Exception as e:
        return False, {"error": str(e)}


def process_complete(file, fecha_jubilacion, regimen_acceso, sexo):
    """
    Procesar PDF completo (extraer + simular)
    
    Args:
        file: Archivo PDF subido
        fecha_jubilacion (str): Fecha en formato MM/YYYY
        regimen_acceso (str): GENERAL o AUTONOMO
        sexo (str): MASCULINO o FEMENINO
        
    Returns:
        tuple: (success: bool, result: dict)
    """
    try:
        files = {"file": file}
        data = {
            "fecha_jubilacion": fecha_jubilacion,
            "regimen_acceso": regimen_acceso,
            "sexo": sexo
        }
        response = requests.post(f"{API_BASE_URL}/api/process", files=files, data=data, timeout=120)
        return response.status_code == 200, response.json()
    except Exception as e:
        return False, {"error": str(e)}


def get_configuration():
    """
    Obtener configuración de la API
    
    Returns:
        tuple: (success: bool, configs: dict)
    """
    try:
        configs = {}
        
        # Parámetros de cómputo
        response = requests.get(f"{API_BASE_URL}/api/config/parametros", timeout=10)
        if response.status_code == 200:
            configs["parametros"] = response.json()
        
        # Índices de revalorización
        response = requests.get(f"{API_BASE_URL}/api/config/indices", timeout=10)
        if response.status_code == 200:
            configs["indices"] = response.json()
        
        # Topes de cotización
        response = requests.get(f"{API_BASE_URL}/api/config/topes", timeout=10)
        if response.status_code == 200:
            configs["topes"] = response.json()
        
        return True, configs
    except Exception as e:
        return False, {"error": str(e)}


@st.cache_data
def check_api_health_cached():
    """Versión cacheada de check_api_health para mejorar rendimiento"""
    return check_api_health() 