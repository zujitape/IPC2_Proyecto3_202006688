from flask import Flask, request
from flask.json import jsonify
from manage import Manager
from xml.dom import minidom
from flask import Response

manage = Manager()

app = Flask(__name__)

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
                nueva = nueva.upper()
                manage.agregarSPositivos(nueva)

        snegativos = sub.getElementsByTagName('sentimientos_negativos')
        for s in snegativos:
            palabras = s.getElementsByTagName('palabra')
            for palabra in palabras:
                p = palabra.firstChild.data
                nueva = p.strip(" ")
                nueva = nueva.upper()
                manage.agregarSNegativos(nueva)


        empresasAnalizar = archivo.getElementsByTagName('empresas_analizar')
        for e in empresasAnalizar:
            empresas = e.getElementsByTagName('empresa')
            for e in empresas:
                nombre = e.getElementsByTagName('nombre')
                for n in nombre:
                    nombre = n.firstChild.data
                    nuevo = nombre.strip(" ")
                    nuevo = nuevo.upper()
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
            empresa = manage.getEmpresa(mensaje)
            if empresa != None:
                servicio = manage.getServicio(mensaje, empresa)
                if servicio != None:
                    nServicio = servicio.tipo
                    manage.agregarMensaje(empresa, nServicio, tipo, fecha)
                else:
                    manage.agregarMensaje('', '', 'neutro', fecha)
            else:
                manage.agregarMensaje('', '', 'neutro', fecha)
    
    lstFechas = manage.getFechas()
    manage.fechas = lstFechas
    cosito = manage.writeXML(lstFechas)
    print(cosito)
    return jsonify(cosito)

@app.route('/show', methods=['GET'])
def show():
    xml = manage.writeXML(manage.fechas)
    return Response(xml, mimetype='text/xml')

@app.route('/ProcesarMensaje', methods=['POST'])
def procesar():
    xml = request.data.decode('utf-8')
    archivo = minidom.parseString(xml)
    mensaje = archivo.getElementsByTagName('mensaje')
    for m in mensaje:
        mensaje = m.firstChild.data
    return manage.analizarMensaje(mensaje)

@app.route('/ConsultaFecha', methods=['GET'])
def graficaFecha():
    json = request.get_json()
    m = manage.archivoConsultaFecha(json['fecha'], json['empresas'])
    return jsonify(m), 200

@app.route('/ConsultaRangoFechas', methods = ['GET'])
def graficaRangoFechas():
    json = request.get_json()
    m = manage.archivoConsultaRangoFechas(json['fechaI'], json['fechaF'], json['empresas'])
    return jsonify(m), 200

if __name__=='__main__':
    app.run(debug=True, port=5000)


