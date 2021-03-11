import random

class Grafo:

    #Constructor del grafo, recibe si el mismo sera dirigido. De no ser indicado, se considera dirigido
    def __init__(self, es_dirigido = True):
        self.vertices = {}
        self.es_dirigido = es_dirigido
        self.cant_vertices = 0
    
    def __len__(self):
        return self.cant_vertices

    #Devuelve una lista con los vertices
    def obtener_vertices(self):
        return self.vertices.keys()

    #Devuelve la cantidad de vertices en el grafo
    def cantidad_vertices(self):
        return self.cant_vertices

    #Devuelve True si el vertice pertenece al grafo, False si no
    def existe_vertice(self, id):
        return id in self.vertices

    #Devuelve True si existe una arista entre los vertices indicados, caso contrario devuelve False
    def existe_arista(self, id_1, id_2):
        if not self.existe_vertice(id_1) or not self.existe_vertice(id_2): return False
        return id_2 in self.vertices[id_1]

    #Agrega un vertice al grafo, donde el id es el dato a guardar
    def agregar_vertice(self, id):
        self.vertices[id] = {} #Un conjunto con los adyacentes al vertice
        self.cant_vertices += 1

    #Devuelve una lista con los vertices adyacentes
    def obtener_adyacentes(self, id):
        return self.vertices[id].keys()

    def cantidad_aristas(self, id):
        return len(self.vertices[id])

    #Agrega una arista entre los vertices pasados, si no se indica el peso es 1 por defecto
    #Devuelve False si no existe alguno de los vertices
    def agregar_arista(self, id_1, id_2, peso = 1):
        if not self.existe_vertice(id_1) or not self.existe_vertice(id_2): return False
        (self.vertices[id_1])[id_2] = peso
        if not self.es_dirigido: (self.vertices[id_2])[id_1] = peso
        return True

    #Devuelve False si no existe algun vertice o la arista
    def peso_arista(self, id_1, id_2):
        if not self.existe_vertice(id_1) or not self.existe_vertice(id_2): return False
        if not self.existe_arista(id_1, id_2): return False
        return (self.vertices[id_1])[id_2]
        
    #Cambia el peso de una arista
    def cambiar_peso_arista(self, id_1, id_2, peso_nuevo):
        if not self.existe_arista(id_1, id_2): return False
        (self.vertices[id_1])[id_2] = peso_nuevo
        if not self.es_dirigido: (self.vertices[id_2])[id_1] = peso_nuevo
        return True

    #Devuelve una lista con tuplas de la forma (origen, destino, peso)
    def obtener_aristas(self):
        aristas_enlistadas = set() #Conjunto para no repetir aristas en grafos no dirigidos
        aristas = []
        for v in self.obtener_vertices():
            for w in self.vertices[v]: #Para cada key en los adyacentes de v
                if (self.es_dirigido) or (not self.es_dirigido and not (w, v) in aristas_enlistadas):
                    aristas.append((v, w, self.peso_arista(v, w)))
                    aristas_enlistadas.add((v, w))
        return aristas

    #Devuelve un vertice aleatorio, o False si el grafo no tiene vertices
    def vertice_aleatorio(self):
        if self.cant_vertices == 0: return False
        return random.choice(list(self.vertices))

    #Devuelve un vertice aleatorio que sea adyacente a v
    def adyacente_aleatorio(self, v):
        return random.choice(list(self.obtener_adyacentes(v)))

    #Elimina un vertice del grafo, devuelve False si no existe el vertice o True si lo borra correctamente
    def eliminar_vertice(self, id):
        if not self.existe_vertice(id): return False
        del self.vertices[id]
        self.cant_vertices -= 1
        return True

    #Elimina una arista entre los vertices indicados
    #En caso de no existir alguno de los vertices o la arista, devuelve False. Si se elimina correctamente devuelve True
    def eliminar_arista(self, id_1, id_2):
        if not self.existe_vertice(id_1) or not self.existe_vertice(id_2): return False
        if not self.existe_arista(id_1, id_2): return False
        del (self.vertices[id_1])[id_2]
        if not self.es_dirigido: del (self.vertices[id_2])[id_1]
        return True
