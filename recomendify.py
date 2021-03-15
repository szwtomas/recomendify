#!/usr/bin/python3
import sys
import csv
from grafo import *
from modelos import *
from comandos import comando_recomendaciones, comando_clustering, comando_camino, comando_mas_importantes, comando_canciones_rango, comando_ciclo_canciones
from biblioteca import obtener_grados

'''
Devuelve un grafo bipartito que relaciona un usuario con una cancion si la tiene en alguna playlsit
y un diccionario con las playlists, las keys son de la forma (nombre_playlist, usuario)
y guarda como dato la instancia de playlist
'''
def procesar_archivo(ruta_archivo):
    SEPARADOR = "\t"
    canciones_usuarios = Grafo(False) 
    playlists = {} #Guarda playlists con su nombre como key, y la instancia de la playlist como dato
    usuarios = {} #Guarda usuarios con su nombre de usuario como key, la instancia del user como dato
    with open(ruta_archivo, "r") as archivo:
        tsvreader = csv.reader(archivo, delimiter=SEPARADOR)
        for entrada in tsvreader:
            if entrada[0] == "ID": continue
            c = Cancion(entrada[2], entrada[3], entrada[6].split(","))
            p = Playlist(entrada[5], entrada[4])
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


'''
Recibe un diccionario con todas las playlists, devuelve un grafo no dirigido y no pesado donde un par
de canciones tienen una arista si comparten al menos una playlist.
'''
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
grafo_completo, playlists = procesar_archivo(sys.argv[1])
grados_completo = obtener_grados(grafo_completo)
grados_canciones = False
grafo_canciones = False
lista_rankings = False
clustering_prom = False
for linea in sys.stdin:
    linea = linea.strip()
    comando = (linea.split(' '))[0]
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





