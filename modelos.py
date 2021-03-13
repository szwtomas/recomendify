
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
    Dos canciones son iguales si coincide el nombre de la cancion y del artista
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
    def __init__(self, nombre, id):
        self.nombre = nombre
        self.id = id
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
            for c in playlists[p].obtener_canciones():
                if c == cancion_buscada:
                    return p
        return -1

    '''
    Devuelve True si el usuario tiene una playlist con el id pasado, False si no la tiene
    '''
    def tiene_playlist(self, id):
        for p in self.playlists:
            if id == p: return True
        return False


    def __eq__(self, other):
        if not isinstance(other, Usuario): return False
        return self.nombre == other.obtener_nombre()

    def __hash__(self):
        return hash(self.nombre)