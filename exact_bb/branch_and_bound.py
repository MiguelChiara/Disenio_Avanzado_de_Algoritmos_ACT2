from itertools import permutations

def domina(a, b):
    return (
        a["distancia"] <= b["distancia"] and
        a["riesgo"] <= b["riesgo"] and
        a["recargas"] <= b["recargas"] and
        (a["distancia"], a["riesgo"], a["recargas"]) !=
        (b["distancia"], b["riesgo"], b["recargas"])
    )

def es_dominada(sol, frente):
    return any(domina(f, sol) for f in frente)

# Algoritmo de Branch and Bound para encontrar la ruta optima
def branch_and_bound(instancia):
    # Extraer datos de la instancia
    nodos = instancia["nodes"]
    hub = instancia["hub"]
    destinos = [n["id"] for n in nodos if n["id"] != hub]

    mejor_frente = []

    # Generar todas las permutaciones posibles de destinos
    for perm in permutations(destinos):
        ruta = [hub] + list(perm) + [hub]
        evaluacion = instancia["evaluar_ruta"](ruta)
        # Si la ruta no es valida, continuar
        if evaluacion is None:
            continue

        sol = {
            "ruta": ruta,
            **evaluacion
        }

        if not es_dominada(sol, mejor_frente):
            mejor_frente = [
                f for f in mejor_frente if not domina(sol, f)
            ]
            mejor_frente.append(sol)

    return mejor_frente

def resolver(instancia):
    return branch_and_bound(instancia)
