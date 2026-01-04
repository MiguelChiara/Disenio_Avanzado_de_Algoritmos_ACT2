# implementacion de un algoritmo para la heuristica geo
def greedy(instancia):
    # Extraer datos de la instancia
    hub = instancia["hub"]
    nodos = instancia["nodes"]
    evaluar = instancia["evaluar_ruta"]

    soluciones = []

    # Probar diferentes valores de alpha para combinar distancia y riesgo
    for alpha in [0.2, 0.5, 0.8]:
        no_visitados = {n["id"] for n in nodos if n["id"] != hub}
        ruta = [hub]
        # Construir la ruta
        while no_visitados:
            mejor = None
            mejor_coste = float("inf")
            # Evaluar cada candidato no visitado
            for candidato in no_visitados:
                eval_parcial = evaluar(ruta + [candidato])
                if eval_parcial is None:
                    continue

                coste = (
                    alpha * eval_parcial["distancia"] +
                    (1 - alpha) * eval_parcial["riesgo"]
                )

                if coste < mejor_coste:
                    mejor = candidato
                    mejor_coste = coste
            # Si no hay candidato valido, terminar la construccion
            if mejor is None:
                break
            # Aniadir el mejor candidato a la ruta
            ruta.append(mejor)
            no_visitados.remove(mejor)

        ruta.append(hub)
        evaluacion = evaluar(ruta)
        # Si la ruta es valida, guardarla
        if evaluacion:
            soluciones.append({
                "ruta": ruta,
                **evaluacion
            })

    return soluciones

def resolver(instancia):
    return greedy(instancia)
