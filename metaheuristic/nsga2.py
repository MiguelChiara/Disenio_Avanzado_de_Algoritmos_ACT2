import random

# Declaracion de constantes
POP_SIZE = 4 # Tamaño de la poblacion
GENERATIONS = 5 # Numero de generaciones
MUT_RATE = 0.2 #probabilidad de mutar una ruta
MAX_INTENTOS = 1000 * POP_SIZE #maximo numero de intentos para crear la poblacion inicial

# Algoritmo NSGA-II
def nsga2(instancia):
    #Preparacion de datos
    hub = instancia["hub"]
    nodos = [n["id"] for n in instancia["nodes"] if n["id"] != hub]
    evaluar = instancia["evaluar_ruta"]
    # Un individuo es una ruta completa devuelve un objeto tal que [hub, n1, n2, n3, ..., hub]
    def crear_individuo():
        perm = nodos[:]
        random.shuffle(perm)
        return [hub] + perm + [hub]

    # Evalua un individuo y devuelve su evaluacion junto con la ruta
    def evaluar_ind(ruta):
        ev = evaluar(ruta)
        if ev is None:
            return None
        return {"ruta": ruta, **ev}

    poblacion = []
    intentos = 0

    # Crear poblacion inicial
    while len(poblacion) < POP_SIZE and intentos < MAX_INTENTOS:
        r = crear_individuo()
        ev = evaluar_ind(r)
        if ev:
            poblacion.append(ev)
        intentos += 1

    # Evolucion de la poblacion
    for _ in range(GENERATIONS):
        hijos = []
        if poblacion != []:
            # Crear hijos mediante mutacion
            while len(hijos) < POP_SIZE:
                p = random.choice(poblacion)["ruta"][:]
                if random.random() < MUT_RATE:
                    i, j = random.sample(range(1, len(p)-1), 2)
                    p[i], p[j] = p[j], p[i]

                ev = evaluar_ind(p)
                if ev:
                    hijos.append(ev)

            poblacion.extend(hijos)
            poblacion = seleccionar_pareto(poblacion, POP_SIZE)

    return poblacion

def domina(a, b):
    return (
        a["distancia"] <= b["distancia"] and
        a["riesgo"] <= b["riesgo"] and
        a["recargas"] <= b["recargas"] and
        (a["distancia"], a["riesgo"], a["recargas"]) !=
        (b["distancia"], b["riesgo"], b["recargas"])
    )

def seleccionar_pareto(poblacion, k):
    frente = []
    for p in poblacion:
        if not any(domina(o, p) for o in poblacion):
            frente.append(p)

    if len(frente) >= k:
        return frente[:k]

    resto = [p for p in poblacion if p not in frente]
    return frente + resto[:k - len(frente)]

def resolver(instancia):
    return nsga2(instancia)
