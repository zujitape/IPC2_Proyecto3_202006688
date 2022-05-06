from Objetos.servicio import Servicio

class Empresa():
    def __init__(self, nombre):
        self.nombre = nombre
        self.servicios = []
        
    def agregarServicios(self, servicio):
        nuevo = Servicio(servicio)
        self.servicios.append(nuevo)
        return nuevo
    
        