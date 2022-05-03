from servicio import Servicio

class Empresa():
    def __init__(self, nombre):
        self.nombre = nombre
        self.servicios = []
        self.noMensajes = 0
        self.noMPositivos = 0
        self.noMNegativos = 0
        self.noMNeutros = 0

    def agregarServicios(self, servicio):
        nuevo = Servicio(servicio)
        self.servicios.append(nuevo)
        return nuevo
    
        