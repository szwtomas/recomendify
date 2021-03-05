
class Nodo:

    def __init__(self, dato = None, siguiente = None):
        self.dato = dato
        self.siguiente = siguiente
    
    def obtener_siguiente(self):
        return self.siguiente
    
    def obtener_dato(self):
        return self.dato

    def asignar_siguiente(self, siguiente):
        self.siguiente = siguiente


class Cola:

    def __init__(self):
        self.cantidad = 0
        self.primero = None
        self.ultimo = None

    def esta_vacia(self):
        return self.cantidad == 0

    def cantidad(self):
        return self.cantidad

    def encolar(self, dato):
        nodo = Nodo(dato, None)
        if self.primero is None: self.primero = nodo
        if self.ultimo is not None: self.ultimo.asignar_siguiente(nodo)
        self.ultimo = nodo
        self.cantidad += 1

    def desencolar(self):
        if self.esta_vacia(): return None
        dato = self.primero.obtener_dato()
        self.primero = self.primero.obtener_siguiente()
        if self.primero is None: self.ultimo = None
        self.cantidad -= 1
        return dato
