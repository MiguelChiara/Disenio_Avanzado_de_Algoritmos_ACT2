import json
import math
from .geometry import segmento_intersecta_poligono

def cargar_instancia(path):
    # Cargar datos desde un archivo JSON
    with open(path, "r") as f:
        data = json.load(f)

    # Preparar estructuras de datos
    nodos = {n["id"]: n for n in data["nodes"]}
    hub = data["hub"]
    zonas = data["no_fly_zones"]

    bateria_cap = data["battery"]["capacity"]
    consumo_km = data["battery"]["consumption_per_km"]

    # Funciones auxiliares para evaluar rutas
    def distancia(a, b):
        return math.hypot(
            nodos[a]["x"] - nodos[b]["x"],
            nodos[a]["y"] - nodos[b]["y"]
        )

    # Riesgo proporcional a la distancia
    def riesgo(a, b):
        return distancia(a, b) * 0.2

    def intersecta(a, b):
        p1 = (nodos[a]["x"], nodos[a]["y"])
        p2 = (nodos[b]["x"], nodos[b]["y"])
        for pol in zonas:
            if segmento_intersecta_poligono(p1, p2, pol):
                return True
        return False

    # Evaluar una ruta completa
    def evaluar_ruta(ruta):
        dist_total = 0.0
        riesgo_total = 0.0
        bateria = bateria_cap
        recargas = 0

        for i in range(len(ruta) - 1):
            a, b = ruta[i], ruta[i+1]

            if intersecta(a, b):
                return None

            d = distancia(a, b)
            dist_total += d
            riesgo_total += riesgo(a, b)

            bateria -= d * consumo_km
            # Verificar si es necesario recargar
            if bateria < 0:
                if nodos[a]["type"] == "recharge":
                    bateria = bateria_cap
                    recargas += 1
                else:
                    return None

        return {
            "distancia": dist_total,
            "riesgo": riesgo_total,
            "recargas": recargas
        }

    return {
        "hub": hub,
        "nodes": list(nodos.values()),
        "evaluar_ruta": evaluar_ruta
    }
