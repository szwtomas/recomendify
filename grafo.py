import random

class Vertice():

    def __init__(self, dato, id):
        self.adyacentes = {}
        self.dato = dato
        self.id = id

    def obtener_adyacentes(self):
        return self.adyacentes

    def obtener_id(self):
        return self.id

class Grafo():

    def __init__(self, es_dirigido = True):
        self.vertices = {}
        self.es_dirigido = es_dirigido
        self.cantidad = 0 #ver si la usamos
    
    def agregar_vertice(self, id, dato = None):
        v = Vertice(dato, id)
        self.cantidad += 1
        self.vertices[id] = v

    def eliminar_vertice(self, id):
        if id not in self.vertices: return False
        for id_v in self.vertices:
            v = self.vertices[id_v]
            if id in v.adyacentes:
                v.adyacentes.pop(id)
        self.vertices.pop(id)
        return True
                    
    def agregar_arista(self, id_1, id_2, peso = 0):
        if id_1 not in self.vertices or id_2 not in self.vertices: return False
        self.vertices[id_1].adyacentes[id_2] = (self.vertices[id_2], peso)
        if not self.es_dirigido:
            self.vertices[id_2].adyacentes[id_1] = (self.vertices[id_1], peso)

    def estan_unidos(self, id_1, id_2):
        if id_1 not in self.vertices or id_2 not in self.vertices: return False
        return id_2 in self.vertices[id_1].adyacentes

    def peso_arista(self, v1, v2):
        if not self.estan_unidos(v1.obtener_id(), v2.obtener_id()): return None
        ady = self.vertices[v1.obtener_id()].obtener_adyacentes()
        return ady[v2.obtener_id()][1]

    def existe_vertice(self, id):
        return id in self.vertices

    def vertice_aleatorio(self):
        if self.cantidad == 0: return False
        return random.choice(self.vertices.values())

    def obtener_vertices(self):
        return self.vertices

    def obtener_adyacentes(self, id):
        if id not in self.vertices return False
        return self.vertices[id].obtener_adyacentes()

    