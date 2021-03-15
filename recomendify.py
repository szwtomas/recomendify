#!/usr/bin/python3
import sys
from grafo import *
from biblioteca import recomendar, page_rank_canciones, camino_minimo, ciclo_n_canciones, canciones_en_rango, clustering_promedio, clustering_cancion, obtener_grados
from modelos import *

'''
Devuelve un grafo bipartito que relaciona un usuario con una cancion si la tiene en alguna playlsit
y un diccionario con las playlists, las keys son el id de la playlist y guarda una lista con las canciones
'''
def procesar_archivo(ruta_archivo):
    SEPARADOR = "\t"
    canciones_usuarios = Grafo(False) 
    playlists = {} #Guarda playlists con su id como key, y la instancia de la playlist como dato
    usuarios = {} #Guarda usuarios con su nombre de usuario como key, la instancia del user como dato
    with open(ruta_archivo, "r") as archivo:
        for linea in archivo:
            entrada = linea.split(SEPARADOR)
            if entrada[0] == "ID": continue
            c = Cancion(entrada[2], entrada[3], entrada[6].split(","))
            p = Playlist(entrada[5], int(entrada[4]))
            if not canciones_usuarios.existe_vertice(c):
                canciones_usuarios.agregar_vertice(c)
            if p.obtener_id() not in playlists:
                playlists[p.obtener_id()] = p
            playlists[p.obtener_id()].agregar_cancion(c)
            if entrada[1] not in usuarios:
                usuarios[entrada[1]] = Usuario(entrada[1])
            if not usuarios[entrada[1]].tiene_playlist(p.obtener_id()):
                usuarios[entrada[1]].agregar_playlist(p.obtener_id())
        for u in usuarios:
            if not canciones_usuarios.existe_vertice(u):
                canciones_usuarios.agregar_vertice(usuarios[u])
            for p in usuarios[u].obtener_ids_playlists():
                for c in playlists[p].obtener_canciones():
                    if not canciones_usuarios.existe_arista(usuarios[u], c):
                        canciones_usuarios.agregar_arista(usuarios[u], c) 
    return canciones_usuarios, playlists


def cargar_canciones_playlists(playlists):
    grafo_playlists = Grafo(False)
    for p in playlists:
        canciones_playlist = playlists[p].obtener_canciones()
        for i in range(0, len(canciones_playlist)):
            if not grafo_playlists.existe_vertice(canciones_playlist[i]):
                grafo_playlists.agregar_vertice(canciones_playlist[i]) 
            for j in range(0, i):
                if not grafo_playlists.existe_arista(canciones_playlist[i], canciones_playlist[j]):
                    grafo_playlists.agregar_arista(canciones_playlist[i], canciones_playlist[j])
    return grafo_playlists

'''
def cargar_canciones_playlists(playlist):
    grafo_playlists = Grafo(False)
    for p in playlists:
        canciones_playlist = playlists[p].obtener_canciones()   
'''

def imprimir_camino(camino, playlists):
    print(camino[0].obtener_nombre_cancion() + " - " + camino[0].obtener_artista(), end=" --> ")
    for i in range(1, len(camino) - 1):
        if isinstance(camino[i], Cancion): continue
        print("aparece en playlist", end=" --> ")
        print(playlists[camino[i].obtener_playlist_cancion(camino[i-1], playlists)].obtener_nombre(), end=" --> ")
        print("de", end=" --> ")
        print(camino[i].obtener_nombre(), end=" --> ")
        print("tiene una playlist", end = " --> ")
        print(playlists[camino[i].obtener_playlist_cancion(camino[i+1], playlists)].obtener_nombre(), end=" --> ")
        print("donde aparece", end=" --> ")
        if i != (len(camino) - 2): print(camino[i+1].obtener_nombre_cancion() + " - " + camino[i+1].obtener_artista(), end=" --> ")
        else: print(camino[i+1].obtener_nombre_cancion() + " - " + camino[i+1].obtener_artista())

'''
Recibe el grafo de usuarios, la cancion en la cual empieza el camino, la cancion a la que se quiere llegar
y un diccionario con todas las playlists por id
'''
def camino_canciones_usuarios(grafo_usuarios, cancion_origen, cancion_destino, playlists):
    existe_origen = False
    existe_destino = False
    for v in grafo_usuarios.obtener_vertices():
        if not isinstance(v, Cancion): continue
        if v == cancion_origen: existe_origen = True
        if v == cancion_destino: existe_destino = True
    if not existe_destino or not existe_origen:
        print("Tanto el origen como el destino deben ser canciones")
        return False, False
    camino = camino_minimo(grafo_usuarios, cancion_origen, cancion_destino)
    if not camino: 
        print("No se encontro recorrido")
        return False, False
    return True, camino
        


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



COMANDO_CAMINO = "camino"
COMANDO_IMPORTANTES = "mas_importantes"
COMANDO_RECOMENDACION = "recomendacion"
COMANDO_CICLO = "ciclo"
COMANDO_RANGO = "rango"
COMANDO_CLUSTERING = "clustering"


if len(sys.argv) != 2:  raise ValueError("Error, cantidad de parametros distinta de 2")
grafo_completo, playlists = procesar_archivo(sys.argv[1])
grados_completo = obtener_grados(grafo_completo)
grados_canciones = False
grafo_canciones = False
lista_rankings = False
clustering_prom = False



for linea in sys.stdin:
    comando = (linea.split(' '))[0]
    if(len(linea.split(' ')) == 1): comando = comando[:-1] #Para sacar el \n
    if comando == COMANDO_CAMINO:
        str_canciones = linea[7:-1]
        canciones = str_canciones.split(' >>>> ')
        if len(canciones) != 2:
            print("Se deben ingresar 2 canciones")
            continue
        cancion_leida = canciones[0].split(' - ')
        if len(cancion_leida) != 2: 
            print("Tanto el origen como el destino deben ser canciones")
            continue
        cancion_origen = Cancion(cancion_leida[0], cancion_leida[1])
        cancion_leida = canciones[1].split(' - ')
        if len(cancion_leida) != 2: 
            print("Tanto el origen como el destino deben ser canciones")
            continue
        cancion_destino = Cancion(cancion_leida[0], cancion_leida[1]) 
        existe_camino, camino = camino_canciones_usuarios(grafo_completo, cancion_origen, cancion_destino, playlists)
        if existe_camino: 
            imprimir_camino(camino, playlists)
    elif comando == COMANDO_IMPORTANTES:
        str_importantes = linea.split(' ')
        n = int(str_importantes[1])
        if not grafo_canciones:
            grafo_canciones = cargar_canciones_playlists(playlists)
            #grados_canciones = obtener_grados(grafo_canciones)
        if not lista_rankings: lista_rankings = page_rank_canciones(grafo_completo)
        for i in range(n):
            c = (lista_rankings[i])[1]
            if i != (n - 1): print(c.obtener_nombre_cancion() + ' - ' + c.obtener_artista(), end = '; ')
            else: print(c.obtener_nombre_cancion() + ' - ' + c.obtener_artista())
    elif comando == COMANDO_RECOMENDACION:
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
            continue
        lista_recomendaciones = recomendar(grafo_completo, canciones, n, grados_completo, es_cancion)
        if es_cancion:
            for i in range(n):
                c = lista_recomendaciones[i]
                if i != (n - 1): print(c.obtener_nombre_cancion() + ' - ' + c.obtener_artista(), end = '; ')
                else: print(c.obtener_nombre_cancion() + ' - ' + c.obtener_artista())
        else:
            for i in range(n):
                u = lista_recomendaciones[i]
                if i != (n - 1): print(u.obtener_nombre(), end="; ")
                else: print(u.obtener_nombre())
    elif comando == COMANDO_CICLO:
        if not grafo_canciones:
            grafo_canciones = cargar_canciones_playlists(playlists)
            grados_canciones = obtener_grados(grafo_canciones)
        str_ciclo = linea.split(' ')
        n = str_ciclo[1]
        str_cancion = linea[(7+len(n)): -1]
        n = int(n)
        cancion_artista = str_cancion.split(' - ')
        c = Cancion(cancion_artista[0], cancion_artista[1])
        mostrar_ciclo(grafo_canciones, n, c)
    elif comando == COMANDO_RANGO:
        if not grafo_canciones:
            grafo_canciones = cargar_canciones_playlists(playlists)
            grados_canciones = obtener_grados(grafo_canciones)
        str_rango = linea.split(' ')
        n = str_rango[1]
        str_cancion = linea[(7+len(n)):-1]
        n = int(n)
        cancion_artista = str_cancion.split(' - ')
        c = Cancion(cancion_artista[0], cancion_artista[1])
        print(canciones_en_rango(grafo_canciones, n, c))
    elif comando == COMANDO_CLUSTERING:
        if not grafo_canciones:
            grafo_canciones = cargar_canciones_playlists(playlists)
            grados_canciones = obtener_grados(grafo_canciones)
        if len(linea.split(' ')) == 1:
            if not clustering_prom: clustering_prom = clustering_promedio(grafo_canciones, grados_canciones)
            print(clustering_prom)
            continue
        str_cancion = linea[11:-1]
        cancion_artista = str_cancion.split(' - ')
        c = Cancion(cancion_artista[0], cancion_artista[1])
        if not grafo_canciones.existe_vertice(c): print("0000") # No esta encontrando la cancion
        else: print(clustering_cancion(grafo_canciones, grados_canciones, c)) # Sacar len(adyacentes)
    else:
        print("Comando invalido")





