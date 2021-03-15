from cola import Cola
from modelos import *

ITERACIONES_DEFECTO = 2
AMORTIGUACION_DEFECTO = 0.85

'''
Recibe un grafo con canciones, el coeficiente de amortiguacion a usar y un diccionario con los rankings
Devuelve el ranking de la presente iteracion de la cancion
'''
def ranking_cancion(grafo, coeficiente_amortiguacion, cancion, rankings):
    termino_amortiguacion = (1 - coeficiente_amortiguacion) / grafo.cantidad_vertices()
    termino_ranking = 0
    for w in grafo.obtener_adyacentes(cancion):
        termino_ranking += rankings[w] / grafo.cantidad_adyacentes(w)
    return termino_amortiguacion + coeficiente_amortiguacion * termino_ranking

'''
Recibe un grafo de canciones, la cantidad de iteraciones a realizar (mientras mas se hagan es mas preciso, se toma
500 como valor por defecto), y el coeficiente de amortiguacion a usar.
Devuelve una lista ordenada con las canciones rankeadas, en forma de tupla (pagerank, cancion)
'''
def page_rank_canciones(grafo, iteraciones = ITERACIONES_DEFECTO, coeficiente_amortiguacion = AMORTIGUACION_DEFECTO):
    rankings_act = {}
    for cancion in grafo.obtener_vertices():
        rankings_act[cancion] = 1 / grafo.cantidad_vertices()
    rankings_vuelta = rankings_act
    for i in range(iteraciones):
        for cancion in grafo.obtener_vertices(): 
            rankings_vuelta[cancion] = ranking_cancion(grafo, coeficiente_amortiguacion, cancion, rankings_act)
        rankings_act = rankings_vuelta
    lista_rankings = []
    for cancion in rankings_act:
        lista_rankings.append((rankings_act[cancion], cancion))
    lista_rankings.sort(key = lambda tupla: tupla[0], reverse=True)
    #lista_rankings.reverse()
    lista_rankings_final = []
    for c_u in lista_rankings:
        if isinstance(c_u[1], Cancion): lista_rankings_final.append(c_u)
    return lista_rankings_final


'''
Recibe un diccionario con padres, y el destino final del camino
Devuelve una lista con el camino reeconstruido
'''
def reecontrstruir_camino(padres, destino):
    v = destino
    camino = []
    while v is not None:
        camino.append(v)
        v = padres[v]
    camino.reverse()
    return camino

'''
Recibe un grafo con canciones y usuarios, la cancion de origen y donde se quiere llegar
Devuelve una lista con el camino minimo entre las dos canciones
'''

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
                if w == cancion_destino:
                    return reecontrstruir_camino(padres, cancion_destino)
    return False


def _ciclo_n_canciones(grafo_canciones, n, cancion_origen, cancion_actual, visitados, camino):
    visitados.add(cancion_actual)
    camino.append(cancion_actual)
    if len(camino) == n and len(camino) != 1:
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

'''
Recibe un grafo con canciones, la cancion donde se quiere comenzar y un numero n
Devuelve una lista con un camino que sea un ciclo de exactamente n canciones
'''
def ciclo_n_canciones(grafo_canciones, n, cancion_origen):
    camino = []
    visitados = set()
    if _ciclo_n_canciones(grafo_canciones, n, cancion_origen, cancion_origen, visitados, camino): return camino
    return False


'''
Recibe un grafo con canciones, un numero n y la cancion de origen
Devuelve la cantidad de canciones que estan a un rango n de la misma
'''
def canciones_en_rango(grafo_canciones, n, cancion_origen):
    visitados = set()
    visitados.add(cancion_origen)
    padres = {}
    padres[cancion_origen] = None
    cola = Cola()
    cola.encolar(cancion_origen)
    dist = {}
    dist[cancion_origen] = 0
    while not cola.esta_vacia():
        v = cola.desencolar()
        for w in grafo_canciones.obtener_adyacentes(v):
            if w not in visitados:
                visitados.add(w)
                padres[w] = v
                cola.encolar(w)
                dist[w] = dist[v] + 1
    cant_en_rango = 0
    for c in dist:
        if dist[c] == n: cant_en_rango += 1
    return cant_en_rango
    """
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
    """
    
'''
Recibe un grafo no dirigo, devuelve un diccionario con los grados de los vertices
'''
def obtener_grados(grafo):
    grados = {}
    for v in grafo.obtener_vertices():
        grados[v] = 0
    for v in grafo.obtener_vertices():
        grados[v] = len(grafo.obtener_adyacentes(v))
    return grados
'''
#Devuelve la cantidad de adyacentes de v que estan relacionados con v
def cantidad_relacionados(grafo, v):
    cant_relacionados = 0
    for w in grafo.obtener_adyacentes(v):
        for k in grafo.obtener_adyacentes(w):
            if grafo.existe_arista(v, k): cant_relacionados += 1
    return cant_relacionados
'''
def cantidad_relacionados(grafo, v):
    cant_relacionados = 0
    for w in grafo.obtener_adyacentes(v):
        for k in grafo.obtener_adyacentes(v):
            if grafo.existe_arista(w, k): 
                cant_relacionados += 1
    return cant_relacionados 

CANT_DECIMALES = 3

def clustering_cancion(grafo, grados, cancion):
    if len(grafo.obtener_adyacentes(cancion)) < 2: 
        return 0
    return round(cantidad_relacionados(grafo, cancion) / (len(grafo.obtener_adyacentes(cancion)) * (len(grafo.obtener_adyacentes(cancion)) - 1)), CANT_DECIMALES)


def clustering_promedio(grafo, grados):
    suma = 0
    for v in grafo.obtener_vertices():
        suma += clustering_cancion(grafo, grados, v)
    return round(suma / grafo.cantidad_vertices(), CANT_DECIMALES)



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
            if key not in lista_gustos: entradas_rankeadas.append((page_rank[key], key))
    entradas_rankeadas.sort(key = lambda tupla: tupla[0])
    entradas_rankeadas.reverse()
    for i in range(n):
        recomendaciones.append((entradas_rankeadas[i])[1])
    return recomendaciones
