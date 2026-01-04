# Ejecucion de la actividad 2
### Para ejecutar este scrip, utilice el siguiente comando:
````shell
python main.py ./instances/instanceN10.json
````
# Explicación de la resolución de la actividad 2
### Planificación multiobjetivo de rutas de drones en entornos urbanos
Usando los algoritmos de:
- Backtracking / Branch-and-Bound con poda guiada por cotas heurísticas. (branch_and_bound.py)
- Algoritmo geométrico basado en visibilidad e intersección de segmentos (geo_heuristic.py)
- Metaheurística aleatorizada (nsga2.py)

Una vez ejecutado el script, se generará una grafica por consola por ejemplo usando el archivo instanceN10.json:
````shell
RESULTADOS
------------------------------------------------------------
No se puede calcular Exact_BB tiene demasiados nodos | 0.0000s | 0.0 KB | 0 soluciones | 0.0 hipervolumen |0.0000 diversidad
Greedy          | 0.0070s | 6.5 KB | 0 soluciones | 0.0 hipervolumen |0.0000 diversidad
NSGA2           | 0.2167s | 7.0 KB | 0 soluciones | 0.0 hipervolumen |0.0000 diversidad

TIEMPO VS N (log-scale conceptual)
No se puede calcular Exact_BB tiene demasiados nodos
N=10  tiempo=0.000000s
Greedy
N=10  tiempo=0.006989s
NSGA2
N=10  tiempo=0.216665s
````
Para poder ejecutar el algoritmo branch and bound, es necesario reducir el numero de nodos en el archivo de instancia, ya que este algoritmo es exponencial y no puede manejar muchos nodos.
por eso he creado el archivo ejemploParaBB.json con 5 nodos para poder ejecutar el algoritmo branch and bound.
````shell
python main.py ./instances/ejemploParaBB.json
````
El resultado de este algoritmo sera:
````shell

RESULTADOS
------------------------------------------------------------
Exact_BB        | 0.0030s | 10.8 KB | 2 soluciones | 0.5394737874870718 hipervolumen |0.0000 diversidad
Greedy          | 0.0007s | 3.1 KB | 0 soluciones | 0.0 hipervolumen |0.0000 diversidad
NSGA2           | 0.0047s | 7.9 KB | 4 soluciones | 0.5394737874870705 hipervolumen |0.0000 diversidad

TIEMPO VS N (log-scale conceptual)
Exact_BB
N= 5  tiempo=0.003015s
Greedy
N= 5  tiempo=0.000740s
NSGA2
N= 5  tiempo=0.004719s     
````

### Help
Existe tambien una funcion help y control de algunos errores:
````shell
python main.py ./instances/instanceN10.txt
El archivo de instancia debe ser un archivo .json

python .\main.py -h
Uso: python main.py <archivo_instancia.json>
````
# Enunciado de la actividad
## Actividad 2. Planificación multiobjetivo de rutas de drones en entornos urbanos

Competencias de la actividad

El objetivo principal de esta actividad es poner en práctica los conceptos fundamentales sobre el análisis de algoritmos de optimización multiobjetivo. El alumno será capaz de:

- Modelar el problema de distribución con drones como un problema de optimización combinatoria sobre grafos dirigidos ponderados.
- Manejar simultáneamente varios objetivos (distancia total, riesgo sobre zonas sensibles y carga de baterías) aplicando técnicas de frontera de Pareto/NSGA-II.
- Implementar y comparar tres enfoques de resolución:
  - _Backtracking_ / _Branch-and-Bound_ con poda guiada por cotas heurísticas.
  - Algoritmo geométrico basado en visibilidad e intersección de segmentos para generar caminos factibles rápidos.
  - Metaheurística aleatorizada (_simulated annealing_ o algoritmo de Monte Carlo) para refinar soluciones.
- Evaluar empíricamente el coste (tiempo, memoria), la calidad (frontera de Pareto aproximada) y la robustez estocástica de cada enfoque.
- Comunicar los resultados con visualizaciones claras y una discusión crítica de los _trade-offs._

Durante esta actividad adquirirás las siguientes competencias necesarias para el diseño y desarrollo de algoritmos eficientes:

- CT1 Competencia en comunicación, oral y escrita, como mínimo en la lengua propia y en inglés. Esta competencia incluye tanto la capacidad de análisis como síntesis del discurso.
- CT3 Utilizar estrategias para prever y resolver problemas, conflictos y cambios en el campo profesional.
- CT4 Competencia de gestión de la información, lo que implica saber adquirir capacidades de búsqueda, discriminación, gestión y uso de la información de forma autónoma en un entorno profesional.
- CT5 Saber aplicar tanto el análisis como la síntesis para organizar y planificar su propio trabajo.
- CT6 Ser capaz de utilizar y aplicar las tecnologías de la información a nivel académico y profesional con criterios éticos.
- CT8 Saber aprender de forma autónoma, actualizarse y poder profundizar en conocimientos permanentemente.
- CE1 Desarrollar y coordinar aplicaciones informáticas: análisis, especificaciones, desarrollo, integración e implementación.
- CE2 Elaborar juegos de test y evaluar la calidad de la solución.
- CE6 Resolver problemas matemáticos que puedan surgir en la ingeniería.

Para la elaboración de esta actividad es necesario estudiar los temas 4, 5 y 6, 7 y 8.

Pautas de elaboración

**Problema propuesto:**

Dispones de un mapa simplificado de la ciudad con:

- N vértices (puntos de entrega y estaciones de recarga).
- Aristas con pesos vectoriales w=⟨distancia, riesgo, consumo batería⟩.
- Zonas restringidas representadas por polígonos _(no-fly)._

Debes planificar la **ruta óptima** (circuito Hamiltoniano) que parte y termina en el _hub_ central y satisface:

- Visita todos los destinos una sola vez.
- Minimiza simultáneamente distancia y riesgo acumulado; minimiza también paradas de recarga.
- Evita intersecciones con zonas _no-fly_ (emplea los tests de intersección de segmentos del tema 7).

**Implementación:**

- Lenguaje a elección; entrega código bien documentado.
- Tres carpetas: exact_bb/, geo_heuristic/, metaheuristic/.
- El proyecto debe ejecutarse con un comando (make run, poetry run, etc.) y aceptar archivos de instancia .json.

**Experimentos:**

- Genera al menos cuatro instancias con N=10, 15, 20, 25 destinos y ≥ 3 polígonos _no-fly._
- Para cada algoritmo mide: tiempo medio (cinco réplicas), memoria pico y produce la aproximación a la frontera de Pareto (para dos objetivos y cantidad de recargas).
- Muestra resultados en gráficas:
  - Tiempo vs. N _(log-scale)._
  - Hipervolumen dominado por cada técnica.
  - Diversidad de la frontera (distancia media entre soluciones).

**Memoria técnica:**

- Máx. 7 páginas PDF excluyendo anexos.
- Secciones mínimas: Introducción, Modelado formal, Descripción de algoritmos, _Setup_ experimental, Resultados, Discusión, Conclusiones.
- Adjunta enlace a repositorio (GitHub/GitLab) con README y _dataset._

Extensión y formato

- **Extensión:** máximo de siete páginas de PDF (código y _datasets_ en anexo o repositorio).
- **Formato:** PDF, fuente legible (mayor o igual a 11 pt).
- **Entrega:** aula virtual + repositorio.

Criterios de evaluación

Especifica los criterios con los que medir los resultados obtenidos por el estudiante con la herramienta de la rúbrica.

| Planificación multiobjetivo de rutas de drones en entornos urbanos | Descripción | Peso<br><br>% |
| --- | --- | --- |
| Criterio 1 | Funcionalidad y complejidad | 55 % |
| Criterio 2 | Experimentación | 20 % |
| Criterio 3 | Calidad del código | 15 % |
| Criterio 4 | Documentación | 10 % |
| Total | **100 %** |     |