
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

class Playlist:

    def __init__(self, nombre, id):
        self.nombre = nombre
        self.id = id
        self.canciones = []

    def obtener_canciones(self):
        return self.canciones

    def obtener_nombre(self):
        return self.nombre
    
    def obtener_id(self):
        return self.id

    def agregar_cancion(self, cancion):
        self.canciones.append(cancion)

    def borrar_ultima_cancion(self):
        self.canciones.pop()

    '''
    Borra la primera aparicion de la cancion indicada de la playlist
    '''
    def borrar_cancion(self, cancion):
        self.canciones.remove(c)


class Usuario:

    def __init__(self, nombre):
        self.nombre = nombre
        self.playlists = [] #Lista con los IDs de las playlist del usuario

    def obtener_nombre(self):
        return self.nombre

    def obtener_id_playlists(self):
        return self.playlists

    def agregar_playlist(self, id):
        self.playlists.append(id)

    '''
    Devuelve el id de la playlist del usuario que tiene la cancion
    En caso de no existir entre las listas del usuario, devuelve -1
    '''
    def obtener_playlist_cancion(self, cancion_buscada, playlists):
        for p in self.obtener_id_playlists():
            for c in playlists[p].obtener_canciones():
                if c == cancion_buscada:
                    return p
        return -1

    def tiene_playlist(self, id):
        for p in self.playlists:
            if id == p: return True
        return False

    def __eq__(self, other):
        return self.nombre == other.obtener_nombre()

    def __hash__(self):
        return hash(self.nombre)