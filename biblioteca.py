from cola import Cola
from modelos import *

ITERACIONES_DEFECTO = 500
AMORTIGUACION_DEFECTO = 0.85

def ranking_cancion(grafo, coeficiente_amortiguacion, cancion, rankings):
    termino_amortiguacion = (1 - coeficiente_amortiguacion) / grafo.cantidad_vertices()
    termino_ranking = 0
    for ady in grafo.obtener_adyacentes(cancion):
        termino_ranking += rankings[ady] / len(grafo.obtener_adyacentes(ady))
    return termino_amortiguacion + coeficiente_amortiguacion * termino_ranking

def page_rank_canciones(grafo, iteraciones = ITERACIONES_DEFECTO, coeficiente_amortiguacion = AMORTIGUACION_DEFECTO):
    rankings = {}
    #termino_amortiguacion = (1 - coeficiente_amortiguacion) / grafo.cantidad_vertices()
    for cancion in grafo.obtener_vertices():
        rankings[cancion] = 0.99 #CAMBIAR!! Es aprox 1/vertices o mayor
    for i in range(iteraciones):
        for cancion in grafo.obtener_vertices(): 
            rankings[cancion] = ranking_cancion(grafo, coeficiente_amortiguacion, cancion, rankings)
    lista_rankings = []
    for cancion in rankings:
        lista_rankings.append((rankings[cancion], cancion))
    lista_rankings.sort(key = lambda tupla: tupla[0])
    lista_rankings.reverse()
    return lista_rankings


def bfs(grafo, origen):
    visitados = set()
    padres = {}
    padres[origen] = None
    dist = {}
    dist[origen] = 0
    visitados.add(origen)
    cola = Cola()
    cola.encolar(origen)
    while not cola.esta_vacia():
        v = cola.desencolar()
        for w in grafo.adyacentes(v):
            if w not in visitados:
                padres[w] = v
                dist[w] = dist[v] + 1
                visitados.add(w)
                cola.encolar(w)
    return padres, dist


#Recibe un grafo que tiene canciones y usuarios como vertices, y arista entre ellos si al usuario le gusta la cancion
#Devuelve una lista con el camino minimo de canciones y usuarios desde una cancion hasta otra

def reecontrstruir_camino(padres, destino):
    v = destino
    camino = []
    while v is not None:
        camino.append(v)
        v = padres[v]
    camino.reverse()
    return camino

#Recibe un grafo que tiene canciones y usuarios como vertices, y arista entre ellos si al usuario le gusta la cancion
#Devuelve una lista con el camino minimo de canciones y usuarios desde una cancion hasta otra
#Devuelve False si no existe ningun camino entre las canciones
def camino_minimo(grafo, cancion_origen, cancion_destino):
    visitados = set()
    visitados.add(cancion_origen)
    padres = {}
    padres[cancion_origen] = None
    cola = Cola()
    cola.encolar(cancion_origen)
    while not cola.esta_vacia():
        v = cola.desencolar()
        for w in grafo.obtener_adyacentes(v):
            if w not in visitados:
                visitados.add(w)
                padres[w] = v
                cola.encolar(w)
                if isinstance(w, Cancion) and w == cancion_destino:
                    return reecontrstruir_camino(padres, cancion_destino)
    return False


def _ciclo_n_canciones(grafo_canciones, n, cancion_origen, cancion_actual, visitados, camino):
    visitados.add(cancion_actual)
    camino.append(cancion_actual)
    if len(camino) == n:
        for w in grafo_canciones.obtener_adyacentes(cancion_actual):
            if w == cancion_origen:
                camino.append(w)
                return True
        camino.pop()
        visitados.remove(cancion_actual)
        return False
    for w in grafo_canciones.obtener_adyacentes(cancion_actual):
        if w not in visitados:
            if _ciclo_n_canciones(grafo_canciones, n, cancion_origen, w, visitados, camino): return True
    visitados.remove(cancion_actual)
    camino.pop()
    return False

def ciclo_n_canciones(grafo_canciones, n, cancion_origen):
    camino = []
    visitados = set()
    if _ciclo_n_canciones(grafo_canciones, n, cancion_origen, cancion_origen, visitados, camino): return camino
    return False