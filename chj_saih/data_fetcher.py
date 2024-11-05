import requests
from .config import BASE_URL_STATION_LIST, API_URL

def fetch_station_list(sensor_type):
    """
    Obtiene la lista de estaciones de acuerdo al tipo de sensor especificado,
    y ordena la lista alfabéticamente por el campo 'nombre'.
    
    Parámetros:
        sensor_type (str): Tipo de sensor, puede ser 'a' (aforos), 't' (temperatura),
                           'e' (embalses), o 'p' (pluviómetros).
    
    Retorna:
        list: Lista de estaciones en formato de diccionario con información estructurada,
              ordenada alfabéticamente por 'nombre'.
    """
    url = f"{BASE_URL_STATION_LIST}?t={sensor_type}&id="
    response = requests.get(url)
    
    if response.status_code == 200:
        stations_data = response.json()
        stations = []
        for s in stations_data:
            station = {
                "id": s.get("id"),
                "latitud": s.get("latitud"),
                "longitud": s.get("longitud"),
                "nombre": s.get("nombre"),
                "variable": s.get("variable"),
                "unidades": s.get("unidades"),
                "subcuenca": s.get("subcuenca"),
                "estado": s.get("estado"),
                "datoActual": s.get("datoActual"),
                "datoTotal": s.get("datoTotal"),
                "municipioNombre": s.get("municipioNombre"),
                "estadoInt": s.get("estadoInt"),
                "estadoInternal": s.get("estadoInternal")
            }
            stations.append(station)
        
        # Ordenar la lista de estaciones por el campo 'nombre'
        stations.sort(key=lambda station: station["nombre"])
        return stations
    else:
        print(f"Error: No se pudo obtener la lista de estaciones. Status code: {response.status_code}")
        return None

def fetch_all_stations():
    """
    Obtiene y combina la lista de todas las estaciones de todos los tipos de sensores,
    y ordena la lista alfabéticamente por el campo 'nombre'.
    
    Retorna:
        list: Lista de todas las estaciones, ordenada por 'nombre'.
    """
    sensor_types = ['a', 't', 'e', 'p']
    all_stations = []

    for sensor_type in sensor_types:
        stations = fetch_station_list(sensor_type)
        if stations:
            all_stations.extend(stations)

    # Ordenar la lista combinada por el campo 'nombre'
    all_stations.sort(key=lambda station: station["nombre"])
    
    return all_stations

def fetch_sensor_data(variable, period_grouping, num_values):
    """
    Obtiene datos del sensor desde la API.
    
    Args:
        variable (str): Identificador del sensor.
        period_grouping (str): Agrupación temporal (ej. 'ultimos5minutales', 'ultimashoras').
        num_values (int): Número de valores a obtener.
    
    Returns:
        dict: Datos JSON de la respuesta de la API.
    """
    url = f"{API_URL}?v={variable}&t={period_grouping}&d={num_values}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos del sensor: {e}")
        return None
