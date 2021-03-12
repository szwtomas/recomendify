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

    #Devuelve la cantidad de aristas del grafo
    def cantidad_aristas(self):
        cant_aristas = 0
        for v in self.obtener_vertices():
            cant_aristas += len(self.obtener_adyacentes(v))
        if not self.es_dirigido:
            cant_aristas = cant_aristas // 2
        return cant_aristas

    #Devuelve True si el vertice pertenece al grafo, False si no
    def existe_vertice(self, v):
        return v in self.vertices

    #Devuelve True si existe una arista entre los vertices indicados, caso contrario devuelve False
    def existe_arista(self, v, w):
        if not self.existe_vertice(v) or not self.existe_vertice(w): return False
        return w in self.vertices[v]

    #Agrega un vertice al grafo, donde el id es el dato a guardar
    def agregar_vertice(self, v):
        self.vertices[v] = {} #Un conjunto con los adyacentes al vertice
        self.cant_vertices += 1

    #Devuelve una lista con los vertices adyacentes
    def obtener_adyacentes(self, v):
        return self.vertices[v].keys()

    def cantidad_adyacentes(self, v):
        return len(self.vertices[v])

    #Agrega una arista entre los vertices pasados, si no se indica el peso es 1 por defecto
    #Devuelve False si no existe alguno de los vertices
    def agregar_arista(self, v, w, peso = 1):
        if not self.existe_vertice(v) or not self.existe_vertice(w): return False
        (self.vertices[v])[w] = peso
        if not self.es_dirigido: (self.vertices[w])[v] = peso
        return True

    #Devuelve False si no existe algun vertice o la arista
    def peso_arista(self, v, w):
        if not self.existe_vertice(v) or not self.existe_vertice(w): return False
        if not self.existe_arista(v, w): return False
        return (self.vertices[v])[w]
        
    #Cambia el peso de una arista
    def cambiar_peso_arista(self, v, w, peso_nuevo):
        if not self.existe_arista(v, w): return False
        (self.vertices[v])[w] = peso_nuevo
        if not self.es_dirigido: (self.vertices[w])[v] = peso_nuevo
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
    def eliminar_vertice(self, v):
        if not self.existe_vertice(v): return False
        del self.vertices[v]
        self.cant_vertices -= 1
        return True

    #Elimina una arista entre los vertices indicados
    #En caso de no existir alguno de los vertices o la arista, devuelve False. Si se elimina correctamente devuelve True
    def eliminar_arista(self, v, w):
        if not self.existe_vertice(v) or not self.existe_vertice(w): return False
        if not self.existe_arista(v, w): return False
        del (self.vertices[v])[w]
        if not self.es_dirigido: del (self.vertices[w])[v]
        return True
