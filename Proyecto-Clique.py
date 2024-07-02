import random
import networkx as nx
import matplotlib.pyplot as plt

# Configuraciones generales
tamaño_poblacion = 20
tasa_mutacion = 0.01
tasa_cruza = 0.9
generaciones = 50
semilla_aleatoria = 50

# Establecer semilla para la generación de números aleatorios
random.seed(semilla_aleatoria)

# Función para inicializar la población
def inicializar_poblacion(tamaño_poblacion, num_vertices):
    poblacion = []
    for _ in range(tamaño_poblacion):
        individuo = [random.randint(0, 1) for _ in range(num_vertices)]
        poblacion.append(individuo)
    return poblacion

# Función de aptitud
def evaluar_individuo(individuo, grafo):
    nodos_seleccionados = [i for i, gen in enumerate(individuo) if gen == 1]
    for i in range(len(nodos_seleccionados)):
        for j in range(i + 1, len(nodos_seleccionados)):
            if not grafo[nodos_seleccionados[i]][nodos_seleccionados[j]]:
                return 0  # No es una clique válida
    return len(nodos_seleccionados)

# Evaluar toda la población
def evaluar_poblacion(poblacion, grafo):
    return [evaluar_individuo(individuo, grafo) for individuo in poblacion]

# Selección por torneo
def seleccion(poblacion, valores_aptitud):
    seleccionados = []
    for _ in range(len(poblacion)):
        torneo = random.sample(list(zip(poblacion, valores_aptitud)), k=3)
        ganador = max(torneo, key=lambda x: x[1])
        seleccionados.append(ganador[0])
    return seleccionados

# Cruza de un punto con tasa de cruza
def cruza(padre1, padre2):
    if random.random() < tasa_cruza:
        punto_cruza = random.randint(1, len(padre1) - 1)
        hijo1 = padre1[:punto_cruza] + padre2[punto_cruza:]
        hijo2 = padre2[:punto_cruza] + padre1[punto_cruza:]
    else:
        hijo1, hijo2 = padre1, padre2
    return hijo1, hijo2

# Mutación bit a bit
def mutar(individuo, tasa_mutacion):
    return [1 - gen if random.random() < tasa_mutacion else gen for gen in individuo]

# Reemplazo de la población
def reemplazar_poblacion(poblacion, descendencia):
    return descendencia

# Seleccionar el mejor individuo
def seleccionar_mejor_individuo(poblacion, valores_aptitud):
    mejor_indice = valores_aptitud.index(max(valores_aptitud))
    return poblacion[mejor_indice]

# Algoritmo genético completo
def algoritmo_genetico(tamaño_poblacion, tasa_mutacion, tasa_cruza, generaciones, grafo):
    num_vertices = len(grafo)
    poblacion = inicializar_poblacion(tamaño_poblacion, num_vertices)
    
    for _ in range(generaciones):
        valores_aptitud = evaluar_poblacion(poblacion, grafo)
        seleccionados = seleccion(poblacion, valores_aptitud)
        descendencia = []
        for i in range(0, len(seleccionados), 2):
            padre1, padre2 = seleccionados[i], seleccionados[i + 1]
            hijo1, hijo2 = cruza(padre1, padre2)
            descendencia.append(mutar(hijo1, tasa_mutacion))
            descendencia.append(mutar(hijo2, tasa_mutacion))
        poblacion = reemplazar_poblacion(poblacion, descendencia)
    
    valores_aptitud = evaluar_poblacion(poblacion, grafo)
    mejor_individuo = seleccionar_mejor_individuo(poblacion, valores_aptitud)
    return mejor_individuo

# Crear grafo
def crear_grafo(num_nodos, probabilidad_arista, semilla):
    random.seed(semilla)
    grafo = nx.erdos_renyi_graph(num_nodos, probabilidad_arista, seed=semilla)
    matriz_adyacencia = nx.adjacency_matrix(grafo).todense().tolist()
    return grafo, matriz_adyacencia

# Representación visual del grafo
def representar_grafo(grafo):
    pos = nx.spring_layout(grafo)
    nx.draw(grafo, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
    plt.show()

# Encontrar cliques máximas exactas usando NetworkX
def encontrar_clique_maxima_exacta(grafo):
    cliques = list(nx.find_cliques(grafo))
    tamaño_maximo = max(len(clique) for clique in cliques)
    cliques_maximas = [clique for clique in cliques if len(clique) == tamaño_maximo]
    return cliques_maximas, tamaño_maximo

# Crear y mostrar el grafo
num_nodos = 10
probabilidad_arista = 0.5
grafo, matriz_adyacencia = crear_grafo(num_nodos, probabilidad_arista, semilla_aleatoria)
representar_grafo(grafo)

# Comparar cliques hallados
def comparar (cliques_maximas, mejor_clique, tamaño_maximo):
    aux2 = []
    aux = [i for i, val in enumerate(mejor_clique) if val == 1]
    if len(aux) == len(cliques_maximas[0]):
        for i in range(len(cliques_maximas)):
            dc = 0
            for j in range (tamaño_maximo):
                if cliques_maximas[i][dc] == aux[j]:
                    aux2.append(aux[j])
                else:
                    break
                dc = dc+1
        return print("Los cliques coinciden")
    else:
        print("No coincide el tamaño del clique")
    
# Encontrar cliques máximas exactas
cliques_maximas, tamaño_maximo = encontrar_clique_maxima_exacta(grafo)
print("Cliques máximas exactas encontradas:", cliques_maximas)
for i, clique in enumerate(cliques_maximas):
        print(f"Clique máxima {i+1}: {clique}")

# Ejecutar el algoritmo genético
mejor_clique = algoritmo_genetico(tamaño_poblacion, tasa_mutacion, tasa_cruza, generaciones, matriz_adyacencia)

# Mostrar el resultado del algoritmo genético
print("Mejor clique encontrada por el algoritmo genético:", mejor_clique)
print("Tamaño de la clique:", sum(mejor_clique))
print("Nodos que forman la clique máxima:", [i for i, val in enumerate(mejor_clique) if val == 1])

comparar(cliques_maximas, mejor_clique, tamaño_maximo)
