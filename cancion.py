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
