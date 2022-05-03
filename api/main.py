from flask import Flask, request
from flask.json import jsonify
from manage import Manager
from xml.dom import minidom

manage = Manager()

app = Flask(__name__)

#ENDPOINTS-consumo de la aplicación
@app.route('/')
def index():
    return "API python w/Flask"

@app.route('/ConsultarDatos', methods=['POST'])
def add_solicitud():
    xml = request.data.decode('utf-8')
    archivo = minidom.parseString(xml)
    #DICCIONARIO DE INFORMACIÓN GENERAL DEL XML
    diccionario = archivo.getElementsByTagName('diccionario')
    for sub in diccionario:
        spositivos = sub.getElementsByTagName('sentimientos_positivos')
        for s in spositivos:
            palabras = s.getElementsByTagName('palabra')
            for palabra in palabras:
                p = palabra.firstChild.data
                nueva = p.strip(" ")
                nueva.lower()
                manage.agregarSPositivos(nueva)

        snegativos = sub.getElementsByTagName('sentimientos_negativos')
        for s in snegativos:
            palabras = s.getElementsByTagName('palabra')
            for palabra in palabras:
                p = palabra.firstChild.data
                nueva = p.strip(" ")
                nueva.lower()
                manage.agregarSNegativos(nueva)


        empresasAnalizar = archivo.getElementsByTagName('empresas_analizar')
        for e in empresasAnalizar:
            empresas = e.getElementsByTagName('empresa')
            for e in empresas:
                nombre = e.getElementsByTagName('nombre')
                for n in nombre:
                    nombre = n.firstChild.data
                    nuevo = nombre.strip(" ")
                    nuevo.lower()
                    nuevaEmpresa = manage.agregarEmpresa(nuevo)
                    servicios = e.getElementsByTagName('servicio')
                    for s in servicios:
                        serviceName = s.attributes['nombre'].value
                        serviceName.strip(" ")
                        serviceName.lower()
                        nuevoServicio = nuevaEmpresa.agregarServicios(serviceName)
                        alias = s.getElementsByTagName('alias')
                        for a in alias:
                            aliasName = a.firstChild.data
                            aliasName.strip(" ")
                            aliasName.lower()
                            nuevoServicio.agregarAlias(aliasName)

    lstMensajes = archivo.getElementsByTagName('lista_mensajes')
    for m in lstMensajes:
        mensajes = m.getElementsByTagName('mensaje')
        for m in mensajes:
            mensaje = m.firstChild.data
            tipo = manage.getTSentimiento(mensaje)
            fecha = manage.getFecha(mensaje)
            fecha = fecha[0]
            empresa = manage.getEmpresa(mensaje, tipo)
            nEmpresa = empresa.nombre

            servicio = manage.getServicio(mensaje, nEmpresa, tipo)
            if empresa != None:
                manage.agregarMensaje(nEmpresa, servicio, tipo, fecha)
            else:
                manage.agregarMensaje('', '', 'neutro', fecha)
    
    lstFechas = manage.getFechas()

    manage.writeXML(lstFechas)
        
    return jsonify({'msg':'Archivo XML cargado correctamente :D'}), 200

@app.route('/show', methods=['GET'])
def getSentimientos():
    manage.getSPositivos()


if __name__=='__main__':
    app.run(debug=True)


