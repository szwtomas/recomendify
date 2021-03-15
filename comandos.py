from modelos import *
from biblioteca import *
from grafo import *

'''
CAMINO MINIMO
'''
'''
Recibe el grafo de usuarios, la cancion en la cual empieza el camino, la cancion a la que se quiere llegar
y un diccionario con todas las playlists por id
'''
def camino_canciones_usuarios(grafo_usuarios, cancion_origen, cancion_destino):
    existe_origen = False
    existe_destino = False
    for v in grafo_usuarios.obtener_vertices():
        if not isinstance(v, Cancion): continue
        if v == cancion_origen: existe_origen = True
        if v == cancion_destino: existe_destino = True
    if not existe_destino or not existe_origen:
        print("Tanto el origen como el destino deben ser canciones")
        raise ValueError(("No existe la cancion"))
        return False, False
    camino = camino_minimo(grafo_usuarios, cancion_origen, cancion_destino)
    if not camino: 
        print("No se encontro recorrido")
        return False, False
    return True, camino
        
def imprimir_camino(camino, playlists):
    print(camino[0].obtener_nombre_cancion() + " - " + camino[0].obtener_artista(), end=" --> ")
    for i in range(1, len(camino) - 1):
        if isinstance(camino[i], Cancion): continue
        print("aparece en playlist", end=" --> ")
        print(playlists[(camino[i].obtener_playlist_cancion(camino[i-1], playlists), camino[i].obtener_nombre())].obtener_nombre(), end=" --> ")
        print("de", end=" --> ")
        print(camino[i].obtener_nombre(), end=" --> ")
        print("tiene una playlist", end = " --> ")
        print(playlists[(camino[i].obtener_playlist_cancion(camino[i+1], playlists), camino[i].obtener_nombre())].obtener_nombre(), end=" --> ")
        print("donde aparece", end=" --> ")
        if i != (len(camino) - 2): print(camino[i+1].obtener_nombre_cancion() + " - " + camino[i+1].obtener_artista(), end=" --> ")
        else: print(camino[i+1].obtener_nombre_cancion() + " - " + camino[i+1].obtener_artista())


def comando_camino(grafo_completo, playlists, linea):
    str_canciones = linea[7:-1]
    canciones = str_canciones.split(' >>>> ')
    if len(canciones) != 2:
        print("Se deben ingresar 2 canciones")
        return
    cancion_leida = canciones[0].split(' - ')
    if len(cancion_leida) != 2: 
        print("Tanto el origen como el destino deben ser canciones")
        return
    cancion_origen = Cancion(cancion_leida[0], cancion_leida[1])
    cancion_leida = canciones[1].split(' - ')
    if len(cancion_leida) != 2: 
        print("Tanto el origen como el destino deben ser canciones")
        return
    cancion_destino = Cancion(cancion_leida[0], cancion_leida[1]) 
    existe_camino, camino = camino_canciones_usuarios(grafo_completo, cancion_origen, cancion_destino)
    if existe_camino: 
        imprimir_camino(camino, playlists)


'''
CANCIONES MAS IMPORTANTES
'''
def comando_mas_importantes(grafo_completo, lista_rankings, linea):
    str_importantes = linea.split(' ')
    n = int(str_importantes[1])
    if not lista_rankings: lista_rankings = page_rank_canciones(grafo_completo)
    for i in range(n):
        c = (lista_rankings[i])[1]
        if i != (n - 1): print(c.obtener_nombre_cancion() + ' - ' + c.obtener_artista(), end = '; ')
        else: print(c.obtener_nombre_cancion() + ' - ' + c.obtener_artista())
    return lista_rankings

'''
CANCIONES EN RANGO
'''
def comando_canciones_rango(grafo_canciones, linea):
    str_rango = linea.split(' ')
    n = str_rango[1]
    str_cancion = linea[(7+len(n)):-1]
    n = int(n)
    cancion_artista = str_cancion.split(' - ')
    c = Cancion(cancion_artista[0], cancion_artista[1])
    print(canciones_en_rango(grafo_canciones, n, c))


'''
CICLO N CANCIONES
'''
def mostrar_ciclo(grafo_canciones, n, cancion_origen):
    if not grafo_canciones.existe_vertice(cancion_origen):
        print("No existe la cancion")
        return None
    camino = ciclo_n_canciones(grafo_canciones, n, cancion_origen)
    if not camino:
        print("No se encontro recorrido")
        return None
    for i in range(0, len(camino) - 1):
        print(camino[i].obtener_nombre_cancion() + " - " + camino[i].obtener_artista(), end = " --> ")
    print(cancion_origen.obtener_nombre_cancion() + " - " + cancion_origen.obtener_artista())


def comando_ciclo_canciones(grafo_canciones, linea):
    str_ciclo = linea.split(' ')
    n = str_ciclo[1]
    str_cancion = linea[(7+len(n)): -1]
    n = int(n)
    cancion_artista = str_cancion.split(' - ')
    c = Cancion(cancion_artista[0], cancion_artista[1])
    mostrar_ciclo(grafo_canciones, n, c)


'''
RECOMENDACIONES
'''

def mostrar_recomendaciones_canciones(lista_recomendaciones, n):
    for i in range(n):
        c = lista_recomendaciones[i]
        if i != (n - 1): print(c.obtener_nombre_cancion() + ' - ' + c.obtener_artista(), end = '; ')
        else: print(c.obtener_nombre_cancion() + ' - ' + c.obtener_artista())

def mostrar_recomendaciones_usuarios(lista_recomendaciones, n):
    for i in range(n):
        u = lista_recomendaciones[i]
        if i != (n - 1): print(u.obtener_nombre(), end="; ")
        else: print(u.obtener_nombre())    

def comando_recomendaciones(grafo_completo, grados_completo, linea):
    str_linea = linea.split(' ')
    es_cancion = str_linea[1]
    n = str_linea[2]
    str_linea = linea[16 + len(es_cancion) + len(n):-1]
    str_canciones = str_linea.split(' >>>> ')
    canciones = []
    for s in str_canciones:
        canciones_artista = s.split(' - ')
        canciones.append(Cancion(canciones_artista[0], canciones_artista[1]))
    n = int(n)
    if es_cancion == "canciones": es_cancion = True
    elif es_cancion == "usuarios": es_cancion = False
    else: 
        print("Comando invalido")
        return
    lista_recomendaciones = recomendar(grafo_completo, canciones, n, grados_completo, es_cancion)
    if es_cancion: mostrar_recomendaciones_canciones(lista_recomendaciones, n)
    else: mostrar_recomendaciones_usuarios(lista_recomendaciones, n)

'''
COEFICIENTE DE CLUSTERING
'''

def comando_clustering(grafo_canciones, grados_canciones, clustering_prom, linea):
    if len(linea.split(' ')) == 1:
        if not clustering_prom: clustering_prom = clustering_promedio(grafo_canciones, grados_canciones)
        print(clustering_prom)
        return clustering_prom
    str_cancion = linea[11:-1]
    cancion_artista = str_cancion.split(' - ')
    c = Cancion(cancion_artista[0], cancion_artista[1])
    if not grafo_canciones.existe_vertice(c): 
        print("0000") # No esta encontrando la cancion
        raise ValueError("No esta en el grafo canciones")
    else: print(clustering_cancion(grafo_canciones, grados_canciones, c))
    return clustering_prom