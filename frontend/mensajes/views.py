from django.shortcuts import render
from mensajes.forms import FileForm
import requests

# Create your views here.

endpoint = 'http://127.0.0.1:5000/' 
def home(request):
    response = requests.post(endpoint)
    analisis = response.json()
    return render(request, 'carga.html')

def cargaMasiva(request):
    ctx = {
        'content':None,
        'response':None
    }
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            xml_binary = f.read()
            xml = xml_binary.decode('utf-8')
            ctx['content'] = xml
            response = requests.post(endpoint + 'ConsultarDatos', data=xml_binary)
            if response.ok:
                ctx['response'] = response.json()
            else:
                ctx['response'] = 'El archivo se envio, pero hubo un error en el servidor'
    else:
        return render(request, 'carga.html')
        
    return render(request, 'carga.html', ctx)


def consultarFecha(request):
    response = requests.get(endpoint + 'ConsultaFecha')
    mensajes = response.json()
    context = {
        'mensajes': mensajes
    }
    return render(request, 'index.html', context)