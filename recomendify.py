import sys
from grafo import *
from biblioteca import page_rank_canciones, camino_minimo
from modelos import *

'''
Devuelve un grafo bipartito que relaciona un usuario con una cancion si la tiene en alguna playlsit
y un diccionario con las playlists, las keys son el id de la playlist y guarda una lista con las canciones
'''

def _procesar_archivo(ruta_archivo):
    SEPARADOR = "\t"
    canciones_usuarios = Grafo(False) 
    playlists = {} #Guarda playlists con su id como key, y la instancia de la playlist como dato
    usuarios = {} #Guarda usuarios con su nombre de usuario como key, la instancia del user como dato
    with open(ruta_archivo, "r") as archivo:
        for linea in archivo:
            entrada = linea.split(SEPARADOR)
            if entrada[0] == "ID": continue
            if len(entrada) != 7: continue #SACAR!!!
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
            canciones_usuarios.agregar_vertice(usuarios[u])
            for p in usuarios[u].obtener_id_playlists():
                for c in playlists[p].obtener_canciones():
                    if not canciones_usuarios.existe_arista(usuarios[u], c):
                        canciones_usuarios.agregar_arista(usuarios[u], c) 
    return canciones_usuarios, playlists


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


def cargar_playlists_2(playlists):
    grafo = Grafo(False)
    for p in playlists:
        i=0
        for c in playlists[p]:
            if not grafo.existe_vertice(c): grafo.agregar_vertice(c)
            for j in range(0, i):
                if not grafo.existe_arista((playlists[p])[i], (playlists[p])[j]):
                    grafo.agregar_arista((playlists[p])[i], (playlists[p])[j])
                else:
                    playlist_compartidas = grafo.peso_arista((playlists[p])[i], (playlists[p])[j]) + 1
                    grafo.cambiar_peso_arista((playlists[p])[i], (playlists[p])[j], playlist_compartidas)
            i += 1
    return grafo

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
        print(camino[i+1].obtener_nombre_cancion() + " - " + camino[i+1].obtener_artista())

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
        return False
    camino = camino_minimo(grafo_usuarios, cancion_origen, cancion_destino)
    if not camino: 
        print("No se encontro recorrido")
        return False
    imprimir_camino(camino, playlists)
    return True
        

if len(sys.argv) != 2:  raise ValueError("Error, cantidad de parametros distinta de 2")
grafo_usuarios, playlists = _procesar_archivo("spotify-mini.tsv")
print("Grafos cargados correctamente")

origen = Cancion("Numb", "Linkin Park")
destino = Cancion("This Is How We Do", "Katy Perry")

camino_canciones_usuarios(grafo_usuarios, origen, destino, playlists)