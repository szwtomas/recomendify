from cola import Cola
from modelos import *
#import math

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


def canciones_en_rango(grafo_canciones, n, cancion_origen):
    visitados = set()
    dist = {}
    dist[cancion_origen] = 0
    visitados.add(cancion_origen)
    cola = Cola()
    cola.encolar(cancion_origen)
    cant_en_rango = 0
    while not cola.esta_vacia():
        c = cola.desencolar()
        for w in grafo_canciones.obtener_adyacentes(c):
            if w not in visitados:
                visitados.add(w)
                dist[w] = dist[c] + 1
                if dist[w] > n: break
                if dist[w] == n: cant_en_rango += 1
                cola.encolar(w) 
    return cant_en_rango
    

def obtener_grados(grafo):
    grados = {}
    for v in grafo.obtener_vertices():
        grados[v] = 0
    for v in grafo.obtener_vertices():
        grados[v] = len(grafo.obtener_adyacentes(v))
    return grados

#Devuelve la cantidad de adyacentes de v que estan relacionados con v
def cantidad_relacionados(grafo, v):
    cant_relacionados = 0
    for w in grafo.obtener_adyacentes(v):
        for k in grafo.obtener_adyacentes(w):
            if grafo.existe_arista(v, k): cant_relacionados += 1
    return cant_relacionados

CANT_DECIMALES = 3

def clustering_cancion(grafo, grados, cancion):
    if grados[cancion] == 0: return 0
    return round(((cantidad_relacionados(grafo, cancion))) / (grados[cancion] * (grados[cancion] - 1)), CANT_DECIMALES)


def clustering_promedio(grafo, grados):
    coeficientes = {}
    suma = 0
    for v in grafo.obtener_vertices():
        suma += clustering_cancion(grafo, grados, v)
    return suma / grafo.cantidad_vertices()


'''
#recibe el grafo de usuarios, una lista de canciones que le gustan y la cantidad de canciones a devolver (n)
def recomendar_canciones(grafo, lista_canciones, n):
    LARGO_CAMINO = CANT_ITERACIONES = 20
    COEFICIENTE_INICIAL = 1 / grafo.cantidad_vertices()
    page_rank = {} 
    for c in lista_canciones:
        if c not in page_rank:
            page_rank[c] = [COEFICIENTE_INICIAL, c]
        actualizar_page_rank(grafo, c, page_rank, LARGO_CAMINO, CANT_ITERACIONES)
    page_rank_ordenado = (page_rank.values()).sort(key = lambda lista: lista_canciones[0])
    page_rank_ordenado.reverse()
    cant_recomendadas = 0
    i=0
    lista_recomendadas = []
    while cant_recomendadas < n:
       if not (page_rank_ordenado[i])[1] in lista_canciones:
           lista_recomendadas.append((page_rank_ordenado[i])[1])
           cant_recomendadas += 1
        i += 1
    return lista_recomendadas


#Unica iteracion de PageRank comenzando del vertice V
def grafo_page_rank(grafo, grados, v, largo_camino, page_rank):
    if v not in page_rank: page_rank[v] = 0
    for i in range(largo_camino):
        if i == 0: valor_transmitido = 1 / grados[v]
        else: valor_transmitido = page_rank[v] / grados[v]
        v = grafo.adyacente_aleatorio(v)
        if v not in page_rank: page_rank[v] = 0
        page_rank[v] += valor_transmitido
'''

def actualizar_page_rank(grafo, v, grados, page_rank):
    LARGO_CAMINO = 30
    if v not in page_rank: page_rank[v] = 0
    for i in range(LARGO_CAMINO):
        if i == 0: valor_transmitido = 1 / grados[v]
        else: valor_transmitido = page_rank[v] / grados[v]
        v = grafo.adyacente_aleatorio(v)
        if v not in page_rank: page_rank[v] = 0
        page_rank[v] += valor_transmitido
    return page_rank


#Recibe el grafo, una lista con gustos del usuario, la cantidad de recomendaciones a recibir, y si se quieren canciones o users
def recomendar(grafo, lista_gustos, n, grados, rec_canciones = True):
    CANT_ITERACIONES = 300
    page_rank = {}
    recomendaciones = []
    for i in range(CANT_ITERACIONES):
        for gusto in lista_gustos:
            actualizar_page_rank(grafo, gusto, grados, page_rank)  
    entradas_rankeadas = []
    for key in page_rank:
        if rec_canciones and isinstance(key, Cancion): #Si quiero canciones y la entrada es una cancion
            if key not in lista_gustos: entradas_rankeadas.append((page_rank[key], key))
        elif (not rec_canciones) and isinstance(key, Usuario): #Si quiero usuarios y la entrada es un usuario
            if key not in lista_gustos: entradas_rankeadas.append((page[key], key))
    entradas_rankeadas.sort(key = lambda tupla: tupla[0])
    entradas_rankeadas.reverse()
    print(len(entradas_rankeadas))
    for i in range(n):
        recomendaciones.append((entradas_rankeadas[i])[1])
    return recomendaciones
