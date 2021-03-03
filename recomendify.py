import sys
from grafo import *

class Cancion:

    def __init__(self, nombre_cancion, artista, generos = []):
        self.nombre_cancion = nombre_cancion
        self.artista = artista
        self.generos = generos

    def obtener_nombre_cancion(self):
        return self.nombre_cancion

    def obtener_artista(self):
        return self.artista

    def obtener_generos(self):
        return generos

    def __eq__(self, other):
        if type(self) is not type(other): return False
        return self.nombre_cancion == other.nombre_cancion and self.artista == other.artista

    def __hash__(self):
        return hash((self.nombre_cancion, self.artista))

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

if len(sys.argv) != 2: 
    raise ValueError("Error, cantidad de parametros distinta de 2")

canciones_usuarios, playlists = procesar_archivo(sys.argv[1])

