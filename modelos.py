
'''
def mismos_generos(generos_1, generos_2):
    if len(generos_1) != len(generos_2): return False
    for g in generos_1:
        if g not in generos_2:
            return False
    return True
'''

class Cancion:

    '''
    Constructor de tipo Cancion, recibe el nombre, el artista y opcionalmente una lista con sus generos
    '''
    def __init__(self, nombre_cancion, artista, generos = []):
        self.nombre_cancion = nombre_cancion
        self.artista = artista
        self.generos = generos

    '''
    Devuelve el nombre de la cancion
    '''
    def obtener_nombre_cancion(self):
        return self.nombre_cancion


    '''
    Devuelve el artista de la cancion
    '''
    def obtener_artista(self):
        return self.artista

    '''
    Devuelve una lista con los generos de la cancion
    '''
    def obtener_generos(self):
        return self.generos

    '''
    Dos canciones son iguales si coincide el nombre de la cancion, el artista y los generos
    '''
    def __eq__(self, other):
        if not isinstance(other, Cancion): return False
        return self.nombre_cancion == other.nombre_cancion and self.artista == other.artista

    def __hash__(self):
        return hash((self.nombre_cancion, self.artista))



class Playlist:

    '''
    Constructor de tipo Playlist. Recibe el nombre de la misma y un identificador
    '''
    def __init__(self, nombre, id, usuario = None):
        self.nombre = nombre
        self.id = id
        self.usuario = usuario
        self.canciones = []

    '''
    Devuelve una lista con las canciones de la playlist
    '''
    def obtener_canciones(self):
        return self.canciones

    '''
    Devuelve el nombre de la playlist
    '''
    def obtener_nombre(self):
        return self.nombre
    
    '''
    Devuelve el id de la playlist
    '''
    def obtener_id(self):
        return self.id

    '''
    Agrega una cancion al final de la playlist
    '''
    def agregar_cancion(self, cancion):
        self.canciones.append(cancion)

    '''
    Borra la ultima cancion de la plallyist
    '''
    def borrar_ultima_cancion(self):
        self.canciones.pop()

    '''
    Borra la primera aparicion de la cancion indicada de la playlist
    '''
    def borrar_cancion(self, cancion):
        self.canciones.remove(cancion)


class Usuario:

    '''
    Constructor de la clase usuario, recibe el username del mismo
    '''
    def __init__(self, nombre):
        self.nombre = nombre
        self.playlists = [] #Lista con los nombres de las playlist del usuario

    '''
    Devuelve el username del usuario
    '''
    def obtener_nombre(self):
        return self.nombre

    '''
    Devuelve una lista con los id's de las playlists del usuarios
    '''
    '''
    def obtener_ids_playlists(self):
        return self.playlists
    '''

    def obtener_nombres_playlists(self):
        return self.playlists

    '''
    Agrega una playlist al usuario
    '''
    def agregar_playlist(self, id):
        self.playlists.append(id)

    '''
    Devuelve el id de la playlist del usuario que tiene la cancion
    En caso de no existir entre las listas del usuario, devuelve -1
    '''
    def obtener_playlist_cancion(self, cancion_buscada, playlists):
        for p in self.obtener_nombres_playlists():
            for c in playlists[(p, self.nombre)].obtener_canciones():
                if c == cancion_buscada:
                    return p
        return -1

    '''
    Devuelve True si el usuario tiene una playlist con el nombre pasado, False si no la tiene
    '''
    def tiene_playlist(self, nombre):
        for p in self.playlists:
            if nombre == p: return True
        return False


    def __eq__(self, other):
        if not isinstance(other, Usuario): return False
        return self.nombre == other.obtener_nombre()

    def __hash__(self):
        return hash(self.nombre)