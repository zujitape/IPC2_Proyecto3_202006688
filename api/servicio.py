from aliasServicio import AliasServicio

class Servicio():
    def __init__(self, tipo):
        self.tipo = tipo
        self.alias = []
        self.noMensajes = 0
        self.noMPositivos = 0
        self.noMNegativos = 0
        self.noMNeutros = 0

    def agregarAlias(self, alias):
        nuevo = AliasServicio(alias)
        self.alias.append(nuevo)
        return nuevo
   
