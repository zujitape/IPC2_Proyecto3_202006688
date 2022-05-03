from positivos import Positivos
from negativos import Negativos
from empresa import Empresa
from mensaje import Mensaje
import re
from xml.dom import minidom

class Manager():
    def __init__(self):
        #DICCIONARIO DE SOLICITUDES
        self.positivos = []
        self.negativos = []
        self.empresas = []
        self.mensajes = []
        self.noMensajes = 0
        self.noMPositivos = 0
        self.noMNegativos = 0
        self.noMNeutros = 0
    
    def agregarSPositivos(self, sentimiento):
        nuevo = Positivos(sentimiento)
        self.positivos.append(nuevo)
        return True
    
    def getSPositivos(self):
        for s in self.positivos:
            palabra = s.palabra
            palabra.strip()

    def agregarSNegativos(self, sentimiento):
        nuevo = Negativos(sentimiento)
        self.negativos.append(nuevo)
        return True

    def agregarEmpresa(self, nombre):
        nuevo = Empresa(nombre)
        self.empresas.append(nuevo)
        return nuevo

    def getTSentimiento(self, msj):
        noPositivos = 0
        noNegativos = 0
        for positivo in self.positivos:
            if(positivo.palabra in msj):
                noPositivos +=1
        
        for negativo in self.negativos:
            if(negativo.palabra in msj):
                noNegativos +=1

        if (noPositivos > noNegativos):
            tipo = 'positivo'
        elif (noNegativos > noPositivos):
            tipo = 'negativo'
        elif (noNegativos == noPositivos) or (noNegativos == 0 and noPositivos == 0):
            tipo = 'neutro'

        return tipo 
    
    def getFecha(self, msj):   
        fecha = re.findall(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", msj)
        return fecha

    def getEmpresa(self, msj, tipo):
        for empresa in self.empresas:
            if(empresa.nombre in msj):
                empresa.noMensajes += 1
                if tipo == 'positivo':
                    empresa.noMPositivos += 1
                elif tipo == 'negativo':
                    empresa.noMNegativos += 1
                else:
                    empresa.noMNeutros += 1
                return empresa
        return None
    
    def getServicio(self, msj, nombre, tipo):
        for empresa in self.empresas:
            if nombre == empresa.nombre:
                for servicio in empresa.servicios:
                    if len(servicio.alias) >0:
                        for alias in servicio.alias:
                            if (alias.alias in msj):
                                return servicio.tipo
                            elif servicio.tipo in msj:
                                servicio.noMensajes +=1
                                if tipo == 'positivo':
                                    servicio.noMPositivos += 1
                                elif tipo == 'negativo':
                                    servicio.noMNegativos += 1
                                else:
                                    servicio.noMNeutros += 1
                                return servicio.tipo
                    else:
                        return servicio.tipo

    def agregarMensaje(self, nEmpresa, tServicio, tMensaje, fecha):
        nuevo = Mensaje(nEmpresa, tServicio, tMensaje, fecha)
        self.mensajes.append(nuevo)
        return True
    
    def getFechas(self):
        lstFechas = []
        for msj in self.mensajes:
            if msj.fecha not in lstFechas:
                lstFechas.append(msj.fecha) 
        return lstFechas

    def writeXML(self, lstFechas):
        doc = minidom.Document()
        lstRespuestas = doc.createElement('lista_respuestas')
        doc.appendChild(lstRespuestas)

        respuesta = doc.createElement('respuesta')
        lstRespuestas.appendChild(respuesta)
        
        noMensajes = 0
        noMPositivos = 0
        noMNegativos = 0
        noMNeutros = 0

        noMensajes2 = 0
        noMPositivos2 = 0
        noMNegativos2 = 0
        noMNeutros2 = 0

        noMensajes3 = 0
        noMPositivos3 = 0
        noMNegativos3 = 0
        noMNeutros3 = 0


        for fecha in lstFechas:
            for msj in self.mensajes:
                if msj.fecha == fecha:
                    print(fecha)
                    print(msj.fecha)
                    noMensajes +=1
                    if msj.tMensaje == 'positivo':
                        noMPositivos += 1
                    elif msj.tMensaje == 'negativo':
                        noMNegativos += 1
                    else:
                        noMNeutros += 1
            
            date = doc.createElement('fecha')
            respuesta.appendChild(date)
            date.appendChild(doc.createTextNode(''+ fecha +''))

            mensajes = doc.createElement('mensajes')
            respuesta.appendChild(mensajes)
            
            total = doc.createElement('total')
            mensajes.appendChild(total)
            total.appendChild(doc.createTextNode(''+str(noMensajes)+''))

            positivos = doc.createElement('positivos')
            mensajes.appendChild(positivos)
            positivos.appendChild(doc.createTextNode(''+str(noMPositivos)+''))

            negativos = doc.createElement('negativos')
            mensajes.appendChild(negativos)
            negativos.appendChild(doc.createTextNode(''+str(noMNegativos)+''))

            neutros = doc.createElement('neutros')
            mensajes.appendChild(neutros)
            neutros.appendChild(doc.createTextNode(''+str(noMNeutros)+''))

            analisis = doc.createElement('analisis')
            respuesta.appendChild(analisis)

            for e in self.empresas:
                for msj in self.mensajes: 
                    if msj.fecha == fecha and e.nombre == msj.nombreEmpresa:
                        print(e.nombre)
                        print(msj.nombreEmpresa)
                        noMensajes2 +=1
                        if msj.tMensaje == 'positivo':
                            noMPositivos2 += 1
                        elif msj.tMensaje == 'negativo':
                            noMNegativos2 += 1
                        else:
                            noMNeutros2 += 1
                    nombre = e.nombre
                
                if noMensajes2 >0:
                    empresa = doc.createElement('empresa')
                    analisis.appendChild(empresa)

                    empresa.setAttribute('nombre', ''+nombre+'')

                    mensajes = doc.createElement('mensajes')
                    empresa.appendChild(mensajes)

                    total = doc.createElement('total')
                    mensajes.appendChild(total)
                    total.appendChild(doc.createTextNode(''+str(noMensajes2)+''))

                    positivos = doc.createElement('positivos')
                    mensajes.appendChild(positivos)
                    positivos.appendChild(doc.createTextNode(''+str(noMPositivos2)+''))

                    negativos = doc.createElement('negativos')
                    mensajes.appendChild(negativos)
                    negativos.appendChild(doc.createTextNode(''+str(noMNegativos2)+''))

                    neutros = doc.createElement('neutros')
                    mensajes.appendChild(neutros)
                    neutros.appendChild(doc.createTextNode(''+str(noMNeutros2)+''))

                    servicios = doc.createElement('servicios')
                    empresa.appendChild(servicios)

                    noMensajes2 = 0
                    noMPositivos2 = 0
                    noMNegativos2 = 0
                    noMNeutros2 = 0 

                for servicio in e.servicios:
                    for msj in self.mensajes: 
                        if msj.fecha == fecha and servicio.tipo == msj.tServicio and e.nombre == msj.nombreEmpresa:
                            print(servicio.tipo)
                            print(msj.tServicio)
                            noMensajes3 +=1
                            if msj.tMensaje == 'positivo':
                                noMPositivos3 += 1
                            elif msj.tMensaje == 'negativo':
                                noMNegativos3 += 1
                            else:
                                noMNeutros3 += 1
                        
                            nServicio = servicio.tipo

                    if noMensajes3 >0:
                        servicio = doc.createElement('servicio')
                        servicios.appendChild(servicio)

                        servicio.setAttribute('nombre', ''+nServicio+'')

                        mensajes = doc.createElement('mensajes')
                        servicio.appendChild(mensajes)

                        total = doc.createElement('total')
                        mensajes.appendChild(total)
                        total.appendChild(doc.createTextNode(''+str(noMensajes3)+''))

                        positivos = doc.createElement('positivos')
                        mensajes.appendChild(positivos)
                        positivos.appendChild(doc.createTextNode(''+str(noMPositivos3)+''))

                        negativos = doc.createElement('negativos')
                        mensajes.appendChild(negativos)
                        negativos.appendChild(doc.createTextNode(''+str(noMNegativos3)+''))

                        neutros = doc.createElement('neutros')
                        mensajes.appendChild(neutros)
                        neutros.appendChild(doc.createTextNode(''+str(noMNeutros3)+''))

                        noMensajes3 = 0
                        noMPositivos3 = 0
                        noMNegativos3 = 0
                        noMNeutros3 = 0 

            noMensajes = 0
            noMPositivos = 0
            noMNegativos = 0
            noMNeutros = 0
                    
                

        xml_str = doc.toprettyxml(indent ="\t") 
        
        save_path_file = "analisis.xml"
        
        with open(save_path_file, "w", encoding='utf-8') as f:
            f.write(xml_str)





        

    




