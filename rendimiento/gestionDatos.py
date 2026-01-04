import time
import tracemalloc
import math


def medir_rendimiento(func, nombre, instancia, repeticiones=5):

    tiempos = []
    memorias = []
    frentes = []

    for _ in range(repeticiones):
        tracemalloc.start()
        inicio = time.perf_counter()
        soluciones = func(instancia)
        tiempo = time.perf_counter() - inicio
        memoria = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        maxDistancia = 0
        maximoRiesgo = 0
        for solucion in soluciones:
            if solucion["distancia"] > maxDistancia:
                maxDistancia = solucion["distancia"]
            if solucion["riesgo"] > maximoRiesgo:
                maximoRiesgo = solucion["riesgo"]
        ref = {
            "distancia": maxDistancia * 1.1,
            "riesgo": maximoRiesgo * 1.1
        }
        tiempos.append(tiempo)
        memorias.append(memoria)
        frentes.append(soluciones)

    return {
        "algoritmo": nombre,
        "tiempo_medio": sum(tiempos) / repeticiones,
        "memoria_pico": max(memorias),
        "soluciones": frentes[tiempos.index(min(tiempos))],
        "hipervolumen" : hipervolumen_2d(frentes[tiempos.index(min(tiempos))], ref),
        "diversidad": diversidad_frontera(frentes[tiempos.index(min(tiempos))])

    }


def imprimir_tabla(resultados):
    print("\nRESULTADOS")
    print("-" * 60)
    for r in resultados:
        print(
            f"{r['algoritmo']:15} | "
            f"{r['tiempo_medio']:.4f}s | "
            f"{r['memoria_pico']/1024:.1f} KB | "
            f"{len(r['soluciones'])} soluciones | "
            f"{r['hipervolumen']} hipervolumen |"
            f"{r['diversidad']:.4f} diversidad"
        )

def tiempo_vs_n(resultados,n):
    tabla = {}
    for r in resultados:
        tabla.setdefault(r["algoritmo"], []).append(
            (n, r["tiempo_medio"])
        )

    print("\nTIEMPO VS N (log-scale conceptual)")
    for alg, datos in tabla.items():
        print(f"{alg}")
        for n, t in sorted(datos):
            print(f"N={n:2d}  tiempo={t:.6f}s")


def hipervolumen_2d(frente, ref):
    puntos = sorted(
        [(s["distancia"], s["riesgo"]) for s in frente],
        key=lambda x: x[0]
    )

    hv = 0.0
    prev_d = ref["distancia"]

    for d, r in reversed(puntos):
        ancho = prev_d - d
        alto = ref["riesgo"] - r
        if ancho > 0 and alto > 0:
            hv += ancho * alto
            prev_d = d

    return hv


def distancia(a, b):
    return math.sqrt(
        (a["distancia"] - b["distancia"])**2 +
        (a["riesgo"] - b["riesgo"])**2 +
        (a["recargas"] - b["recargas"])**2
    )

def diversidad_frontera(frente):
    if len(frente) < 2:
        return 0.0

    dists = []
    for i in range(len(frente)):
        for j in range(i+1, len(frente)):
            dists.append(distancia(frente[i], frente[j]))

    return sum(dists) / len(dists)
