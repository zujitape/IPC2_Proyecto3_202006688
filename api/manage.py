from positivos import Positivos
from negativos import Negativos
from empresa import Empresa
from mensaje import Mensaje
import re
from xml.dom import minidom
from datetime import datetime

def normalize(s):
        replacements = (
            ("á", "a"),
            ("é", "e"),
            ("í", "i"),
            ("ó", "o"),
            ("ú", "u"),
        )
        for a, b in replacements:
            s = s.replace(a, b).replace(a.upper(), b.upper())
        return s

class Manager():
    def __init__(self):
        #DICCIONARIO DE SOLICITUDES
        self.positivos = []
        self.negativos = []
        self.empresas = []
        self.mensajes = []
        self.fechas = []
    
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
        msj = normalize(msj)
        msj = msj.upper()
        for positivo in self.positivos:
            pPositiva = normalize(positivo.palabra)
            if(pPositiva in msj):
                noPositivos +=1
        for negativo in self.negativos:
            pNegativa = normalize(negativo.palabra)
            if(pNegativa in msj):
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

    def getEmpresa(self, msj):
        msj = msj.split(" ")
        for e in self.empresas:
            for m in msj:
                m = normalize(m)
                res = re.match(e.nombre, m, flags = re.IGNORECASE)
                if res != None:
                    return e.nombre
                else:
                    pass

    def getServicio(self, msj, nombre):
        msj = msj.upper()
        msj = normalize(msj)
        for empresa in self.empresas:
            if nombre == empresa.nombre:
                for servicio in empresa.servicios:
                    nServicio = servicio.tipo
                    nServicio = nServicio.upper()
                    nServicio = normalize(nServicio)
                    if len(servicio.alias) >0:
                        for alias in servicio.alias:
                            nAlias = alias.alias
                            nAlias = normalize(nAlias)
                            nAlias = nAlias.upper()
                            if (nAlias in msj):
                                return servicio
                            elif nServicio in msj:
                                return servicio
                    else:
                        return servicio

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
        
        noMensajes, noMPositivos, noMNegativos, noMNeutros = 0, 0, 0, 0
        noMensajes2, noMPositivos2, noMNegativos2, noMNeutros2 = 0, 0, 0, 0
        noMensajes3, noMPositivos3, noMNegativos3, noMNeutros3 = 0, 0, 0, 0
    
        for fecha in lstFechas:
            for msj in self.mensajes:
                if msj.fecha == fecha:
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

                    noMensajes2, noMPositivos2, noMNegativos2, noMNeutros2 = 0, 0, 0, 0

                for servicio in e.servicios:
                    for msj in self.mensajes: 
                        if msj.fecha == fecha and servicio.tipo == msj.tServicio and e.nombre == msj.nombreEmpresa:
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

                        noMensajes3, noMPositivos3, noMNegativos3, noMNeutros3 = 0, 0, 0, 0

            noMensajes, noMPositivos, noMNegativos, noMNeutros = 0, 0, 0, 0
                    
        xml_str = doc.toprettyxml(indent ="\t") 
        
        save_path_file = "analisis.xml"
        
        with open(save_path_file, "w", encoding='utf-8') as f:
            f.write(xml_str)
        
        return xml_str

    def analizarMensaje(self, mensaje):
        #fecha:
        fecha = re.search(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", mensaje)
        dateMsj = fecha.group(0)

        #lugar / red social:
        aa = re.findall(r' *:(?: *([\w.-]+))?', mensaje)
        redSocial = aa[3]

        #username:
        user = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', mensaje)

        if user != None:
            userMsj = user.group(0)
        else:
            userMsj = aa[2]

        nm = normalize(mensaje)
        nm = nm.upper()

        #empresa:
        lstEmpresas = []
        msj = mensaje.split(" ")
        for e in self.empresas:
            for m in msj:
                res = re.match(e.nombre, m, flags = re.IGNORECASE)
                if res != None:
                    lstEmpresas.append(e.nombre)
                else:
                    pass

        
        #servicio:
        lstServicios = []
        if len(lstEmpresas) > 0:
            for l in lstEmpresas:
                tServicio = self.getServicio(nm, l)
                lstServicios.append(tServicio.tipo)
                print(tServicio.tipo)


        #Definir sentimiento/número de palabras
        noPositivos = 0
        noNegativos = 0
        noTotal = 0
        lstSentimientos = []
        for positivo in self.positivos:
            pPositiva = (positivo.palabra)
            if(pPositiva in nm):
                noPositivos += 1
                noTotal += 1

        for negativo in self.negativos:
            pNegativa = (negativo.palabra)
            if(pNegativa in nm):
                noNegativos +=1
                noTotal += 1
        
        if noTotal>0:
            sPositivo = int((noPositivos/noTotal)*100)
            sNegativo = int((noNegativos/noTotal)*100)
        else:
            sPositivo = 0
            sNegativo = 0

        if noPositivos > 0:
            lstSentimientos.append('positivo')
        elif noNegativos > 0:
            lstSentimientos.append('negativo')
        else:
            lstSentimientos.append('no sentimiento encontrado')

        doc = minidom.Document()
        respuesta = doc.createElement('respuesta')
        doc.appendChild(respuesta)

        fecha = doc.createElement('fecha')
        respuesta.appendChild(fecha)
        fecha.appendChild(doc.createTextNode(''+ dateMsj +''))

        social = doc.createElement('red_social')
        respuesta.appendChild(social)
        social.appendChild(doc.createTextNode(''+ redSocial +''))

        usuario = doc.createElement('usuario')
        respuesta.appendChild(usuario)
        usuario.appendChild(doc.createTextNode(''+userMsj+''))

        empresas = doc.createElement('empresas')
        respuesta.appendChild(empresas)
        
        for e in lstEmpresas:
            empresa = doc.createElement('empresa')
            empresas.appendChild(empresa)
            empresa.setAttribute('nombre', ''+e+'')
        
        for s in lstServicios:
            servicio = doc.createElement('servicio')
            empresa.appendChild(servicio)
            servicio.appendChild(doc.createTextNode(''+s+''))  
        
        positivas = doc.createElement('palabras_positivas')
        respuesta.appendChild(positivas)
        positivas.appendChild(doc.createTextNode(''+ str(noPositivos) +''))

        negativos = doc.createElement('palabras_negativas')
        respuesta.appendChild(negativos)
        negativos.appendChild(doc.createTextNode(''+str(noNegativos)+''))

        sPositivoxml = doc.createElement('sentimiento_positivo')
        respuesta.appendChild(sPositivoxml)
        sPositivoxml.appendChild(doc.createTextNode(''+str(sPositivo)+'%'))

        sNegativoxml = doc.createElement('sentimiento_negativo')
        respuesta.appendChild(sNegativoxml)
        sNegativoxml.appendChild(doc.createTextNode(''+str(sNegativo)+'%'))

        for s in lstSentimientos:
            sAnalizado = doc.createElement('sentimiento_analizado')
            respuesta.appendChild(sAnalizado)
            sAnalizado.appendChild(doc.createTextNode(''+s+''))

        xml_str = doc.toprettyxml(indent ="\t") 
        
        save_path_file = "analisisMensaje.xml"
        
        with open(save_path_file, "w", encoding='utf-8') as f:
            f.write(xml_str)
        
        return xml_str

    def archivoConsultaFecha(self, fecha, empresas):
        noTotal, noPositivos, noNegativos, noNeutros =0, 0, 0, 0
        total, positivos, negativos, neutros = 0, 0, 0, 0

        json = []

        for e in empresas:
            for m in self.mensajes:
                if m.nombreEmpresa == e and m.fecha == fecha:
                    noTotal +=1
                    total += 1
                    if m.tMensaje == 'positivo':
                        noPositivos += 1
                        positivos += 1
                    elif m.tMensaje == 'negativo':
                        noNegativos += 1
                        negativos += 1
                    elif m.tMensaje == 'neutro':
                        noNeutros += 1
                        neutros += 1
        
            if noTotal >0:
                datos = {
                        'empresa': e,
                        'total': noTotal,
                        'positivos': noPositivos,
                        'negativos': noNegativos,
                        'neutros': noNeutros
                    }
                json.append(datos)
            else: 
                pass

            noTotal = 0
            noPositivos = 0
            noNegativos = 0
            noNeutros = 0

        datosG = {
            'totalG': total,
            'positivosG': positivos,
            'negativosG': negativos,
            'neutrosG': neutros
        }
        json.append(datosG)

        return json

    def archivoConsultaRangoFechas(self, fechaI, fechaF, empresas):
        inicio = datetime.strptime(fechaI, '%d/%m/%Y')
        final = datetime.strptime(fechaF, '%d/%m/%Y')
        inicio = inicio.date()
        final = final.date()
        noTotal, noPositivos, noNegativos, noNeutros =0, 0, 0, 0
        total, positivos, negativos, neutros = 0, 0, 0, 0

        json = []

        for e in empresas:
            for m in self.mensajes:
                fecha = datetime.strptime(m.fecha, '%d/%m/%Y')
                fecha = fecha.date()
                if fecha >= inicio and fecha <= final and m.nombreEmpresa == e:
                    noTotal +=1
                    total += 1
                    if m.tMensaje == 'positivo':
                        noPositivos += 1
                        positivos += 1
                    elif m.tMensaje == 'negativo':
                        noNegativos += 1
                        negativos += 1
                    elif m.tMensaje == 'neutro':
                        noNeutros += 1
                        neutros += 1
        
            if noTotal >0:
                datos = {
                        'fecha': fecha,
                        'empresa': e,
                        'total': noTotal,
                        'positivos': noPositivos,
                        'negativos': noNegativos,
                        'neutros': noNeutros
                    }
                json.append(datos)
            else: 
                pass

            noTotal = 0
            noPositivos = 0
            noNegativos = 0
            noNeutros = 0

        datosG = {
            'totalG': total,
            'positivosG': positivos,
            'negativosG': negativos,
            'neutrosG': neutros
        }
        json.append(datosG)

        return json
    



                



    
        












        

    




