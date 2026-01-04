from loader import loader
from rendimiento import gestionDatos
from exact_bb import branch_and_bound as bb
from geo_heuristic import greedy
from metaheuristic import nsga2
import sys

if len(sys.argv) != 2:
    print("Uso: python main.py <archivo_instancia.json>")
    sys.exit(1)

if sys.argv[1]  == "--help" or sys.argv[1] == "-h":
    print("Uso: python main.py <archivo_instancia.json>")
    sys.exit(0)

if not sys.argv[1].endswith(".json"):
    print("El archivo de instancia debe ser un archivo .json")
    sys.exit(1)

#Definicion de los algoritmos a evaluar
algoritmos = [
    ("Exact_BB", bb),
    ("Greedy", greedy),
    ("NSGA2", nsga2),
]
#Cargar la instancia desde el archivo proporcionado como argumento
instancia = loader.cargar_instancia(sys.argv[1])

def main():
    # Calculamos el numero de nodos
    n=sum(1 for node in instancia["nodes"] if node["type"] == "delivery" or node["type"] == "hub")
    resultados = []
    repeticiones = 5
    for nombre, modulo in algoritmos:
        if (n<=8 and nombre=="Exact_BB") or nombre!="Exact_BB":
            res = gestionDatos.medir_rendimiento(
                modulo.resolver,
                nombre,
                instancia,
                repeticiones
            )
        else:
            res={
            "algoritmo": f"No se puede calcular {nombre} tiene demasiados nodos",
            "tiempo_medio": 0.0,
            "memoria_pico": 0.0,
            "soluciones": [],
            "hipervolumen" : 0.0,
            "diversidad": 0.0
            }
        resultados.append(res)

    gestionDatos.imprimir_tabla(resultados)
    gestionDatos.tiempo_vs_n(resultados,n)

if __name__ == "__main__":
    main()