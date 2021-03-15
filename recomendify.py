#!/usr/bin/python3
import sys
from grafo import *
from biblioteca import recomendar, page_rank_canciones, camino_minimo, ciclo_n_canciones, canciones_en_rango, clustering_promedio, clustering_cancion, obtener_grados
from modelos import *
from comandos import comando_recomendaciones, comando_clustering, comando_camino, comando_mas_importantes, comando_canciones_rango, comando_ciclo_canciones

'''
Devuelve un grafo bipartito que relaciona un usuario con una cancion si la tiene en alguna playlsit
y un diccionario con las playlists, las keys son el id de la playlist y guarda una lista con las canciones
'''
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
            #c = Cancion(entrada[2], entrada[3])
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

'''


import csv
def _procesar_archivo(ruta_archivo):
    SEPARADOR = "\t"
    canciones_usuarios = Grafo(False) 
    playlists = {} #Guarda playlists con su nombre como key, y la instancia de la playlist como dato
    usuarios = {} #Guarda usuarios con su nombre de usuario como key, la instancia del user como dato
    with open(ruta_archivo, "r") as archivo:
        tsvreader = csv.reader(archivo, delimiter=SEPARADOR)
        for entrada in tsvreader:
            #entrada = linea.split(SEPARADOR)
            if entrada[0] == "ID": continue
            c = Cancion(entrada[2], entrada[3], entrada[6].split(","))
            #c = Cancion(entrada[2], entrada[3])
            p = Playlist(entrada[5], int(entrada[4]))
            if not canciones_usuarios.existe_vertice(c):
                canciones_usuarios.agregar_vertice(c)
            if (p.obtener_nombre(), entrada[1]) not in playlists:
                playlists[(p.obtener_nombre(), entrada[1])] = p
            playlists[(p.obtener_nombre(), entrada[1])].agregar_cancion(c)
            if entrada[1] not in usuarios:
                usuarios[entrada[1]] = Usuario(entrada[1])
            if not usuarios[entrada[1]].tiene_playlist(p.obtener_nombre()):
                usuarios[entrada[1]].agregar_playlist(p.obtener_nombre())
    for u in usuarios:
        if not canciones_usuarios.existe_vertice(u):
            canciones_usuarios.agregar_vertice(usuarios[u])
        for p in usuarios[u].obtener_nombres_playlists():
            for c in playlists[(p, u)].obtener_canciones():
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


COMANDO_CAMINO = "camino"
COMANDO_IMPORTANTES = "mas_importantes"
COMANDO_RECOMENDACION = "recomendacion"
COMANDO_CICLO = "ciclo"
COMANDO_RANGO = "rango"
COMANDO_CLUSTERING = "clustering"


if len(sys.argv) != 2:  raise ValueError("Error, cantidad de parametros distinta de 2")
grafo_completo, playlists = _procesar_archivo(sys.argv[1])
grados_completo = obtener_grados(grafo_completo)
grados_canciones = False
grafo_canciones = False
lista_rankings = False
clustering_prom = False
for linea in sys.stdin:
    comando = (linea.split(' '))[0]
    if(len(linea.split(' ')) == 1): comando = comando[:-1] #Para sacar el \n
    if comando == COMANDO_CAMINO:
        comando_camino(grafo_completo, playlists, linea)
    elif comando == COMANDO_IMPORTANTES:
        lista_rankings = comando_mas_importantes(grafo_completo, lista_rankings, linea)
    elif comando == COMANDO_RECOMENDACION:
        comando_recomendaciones(grafo_completo, grados_completo, linea)
    elif comando == COMANDO_CICLO:
        if not grafo_canciones:
            grafo_canciones = cargar_canciones_playlists(playlists)
            grados_canciones = obtener_grados(grafo_canciones)
        comando_ciclo_canciones(grafo_canciones, linea)
    elif comando == COMANDO_RANGO:
        if not grafo_canciones:
            grafo_canciones = cargar_canciones_playlists(playlists)
            grados_canciones = obtener_grados(grafo_canciones)
        comando_canciones_rango(grafo_canciones, linea)
    elif comando == COMANDO_CLUSTERING:
        if not grafo_canciones:
            grafo_canciones = cargar_canciones_playlists(playlists)
            grados_canciones = obtener_grados(grafo_canciones)
        clustering_prom = comando_clustering(grafo_canciones, grados_canciones, clustering_prom, linea)
    else:
        print("Comando invalido")





