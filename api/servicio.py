from aliasServicio import AliasServicio

class Servicio():
    def __init__(self, tipo):
        self.tipo = tipo
        self.alias = []

    def agregarAlias(self, alias):
        nuevo = AliasServicio(alias)
        self.alias.append(nuevo)
        return nuevo
   
