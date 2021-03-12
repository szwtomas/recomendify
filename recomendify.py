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
            #if len(entrada) != 7: continue #SACAR!!!
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
        if i != (len(camino) - 2): print(camino[i+1].obtener_nombre_cancion() + " - " + camino[i+1].obtener_artista(), end=' --> ')
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
        return False
    camino = camino_minimo(grafo_usuarios, cancion_origen, cancion_destino)
    if not camino: 
        print("No se encontro recorrido")
        return False
    imprimir_camino(camino, playlists)
    return True
        


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
grafo_canciones = False
lista_rankings = False
#camino Don't Go Away - Oasis >>>> Quitter - Eminem
#ciclo 7 By The Way - Red Hot Chili Peppers

#CAMBIAR ID POR V EN GRAFO.PY
for linea in sys.stdin:
    comando = (linea.split(' '))[0]
    if comando == COMANDO_CAMINO:
        str_canciones = linea[7:-1]
        canciones = str_canciones.split(' >>>> ')
        cancion_leida = canciones[0].split(' - ')
        cancion_origen = Cancion(cancion_leida[0], cancion_leida[1])
        cancion_leida = canciones[1].split(' - ')
        cancion_destino = Cancion(cancion_leida[0], cancion_leida[1]) 
        camino_canciones_usuarios(grafo_completo, cancion_origen, cancion_destino, playlists)
    elif comando == COMANDO_IMPORTANTES:
        str_importantes = linea.split(' ')
        n = int(str_importantes[1])
        if not grafo_canciones: grafo_canciones = cargar_canciones_playlists(playlists)
        if not lista_rankings: lista_rankings = page_rank_canciones(grafo_canciones)
        for i in range(n):
            c = (lista_rankings[i])[1]
            if i != (n - 1): print(c.obtener_nombre_cancion() + ' - ' + c.obtener_artista(), end = '; ')
            else: print(c.obtener_nombre_cancion() + ' - ' + c.obtener_artista())
    elif comando == COMANDO_RECOMENDACION:
        pass
    elif comando == COMANDO_CICLO:
        if not grafo_canciones: grafo_canciones = cargar_canciones_playlists(playlists)
        str_ciclo = linea.split(' ')
        n = str_ciclo[1]
        str_cancion = linea[(7+len(n)): -1]
        n = int(n)
        cancion_artista = str_cancion.split(' - ')
        c = Cancion(cancion_artista[0], cancion_artista[1])
        mostrar_ciclo(grafo_canciones, n, c)
    elif comando == COMANDO_RANGO:
        pass
    elif comando == COMANDO_CLUSTERING:
        pass
    else:
        print("Comando invalido")





