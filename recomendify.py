import sys
from grafo import *
from algortimos_grafos_musica import page_rank_canciones
from cancion import *

'''
Devuelve un grafo bipartito que relaciona un usuario con una cancion si la tiene en alguna playlsit
y un diccionario con las playlists, las keys son el id de la playlist y guarda una lista con las canciones
'''

def procesar_archivo(ruta_archivo):
    SEPARADOR = "\t"
    canciones_usuarios = Grafo(False) 
    playlists = {}
    with open(ruta_archivo, "r") as archivo:
        for linea in archivo:
            entrada = linea.split(SEPARADOR)
            if entrada[0] == "ID": continue
            if len(entrada) != 7: continue #SACAR!!!
            if not canciones_usuarios.existe_vertice(entrada[1]):
                canciones_usuarios.agregar_vertice(entrada[1])
            cancion = Cancion(entrada[2], entrada[3], entrada[6].split(","))
            if not canciones_usuarios.existe_vertice(cancion):
                canciones_usuarios.agregar_vertice(cancion)
            canciones_usuarios.agregar_arista(entrada[1], cancion)
            if not entrada[4] in playlists:
                playlists[entrada[4]] = []
            playlists[entrada[4]].append(cancion)
    return canciones_usuarios, playlists

def _cargar_playlists(playlists):
    canciones_playlist = Grafo(False)
    for p in playlists:
        i=1
        for cancion in playlists[p]:
            if not canciones_playlist.existe_vertice(cancion):
                canciones_playlist.agregar_vertice(cancion)           
            for j in range(i, len(playlists[p])):
                cancion_2 = (playlists[p])[j]
                if not canciones_playlist.existe_vertice(cancion):
                    canciones_playlist.agregar_vertice(cancion_2)
                if cancion != cancion_2 and not canciones_playlist.existe_arista(cancion, cancion_2):
                    canciones_playlist.agregar_arista(cancion, cancion_2)
            i += 1
    return canciones_playlist            

def cargar_playlists(playlists):
    canciones_playlist = Grafo(False)
    for p in playlists:
        for cancion in playlists[p]: 
            if not canciones_playlist.existe_vertice(cancion):
                canciones_playlist.agregar_vertice(cancion)
                for cancion_2 in playlists[p]:
                    if cancion != cancion_2 and not canciones_playlist.existe_arista(cancion, cancion_2):
                        canciones_playlist.agregar_arista(cancion, cancion_2)
    return canciones_playlist
'''
if len(sys.argv) != 2: 
    raise ValueError("Error, cantidad de parametros distinta de 2")
'''
#canciones_usuarios, playlists = procesar_archivo(sys.argv[1])
canciones_usuarios, playlists = procesar_archivo("spotify-mini.tsv")
print(len(playlists))
for p in playlists:
    print(len(playlists[p]))
print("Grafo canciones y usuarios cargado")
canciones_playlist = _cargar_playlists(playlists)

for c in canciones_playlist.obtener_vertices():
    print(c.obtener_nombre_cancion())

print("Grafo playlists cargado")

rankings = page_rank_canciones(canciones_playlist, 10, 0.85)

for i in range(0, len(rankings)):
    print("Cancion " + str(i+1) + ": " + ((rankings[i])[1]).obtener_nombre_cancion() + " PR: " + str((rankings[i])[0]))



