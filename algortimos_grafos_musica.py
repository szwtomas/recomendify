import heapq

class Heap():

    def __init__(self):
        self.heap = heapq.heapify([])
        self.cantidad = 0

    def cantidad(self):
        return self.cantidad

    def encolar(self, elemento, dato):
        heapq.heappush(self.heap, (dato, elemento))
        self.cantidad += 1

    def desencolar(self):
        elemento = heapq.heappop(self.heap)
        if elemento is not None: 
            self.cantidad += 1
        return elemento[1]

    def esta_vacia(self):
        return self.cantidad == 0    

def camino_minimo(grafo, origen):
    dist = {}
    padres = {}
    for v in grafo.obtener_vertices():
        dist[v] = float('inf') #infinito en python
    dist[origen] = 0
    padre[origen] = None
    heap = Heap()
    heap.encolar(origen, 0)
    while not heap.esta_vacia():
        v = heap.desencolar()
        for w in grafo.obtener_adyacentes(v):
            if dist[v] + grafo.peso_arista(v, w) < dist[w]:
                dist[w] = dist[v] + grafo.peso_arista(v, w)
                padre[w] = v
                heap.encolar(w, dist[w])
    return padre, distancia

