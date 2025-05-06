# Importamos la función para renderizar plantillas HTML
from flask import render_template

def contacto():
    # Esta vista simplemente muestra la página de contacto general
    # No maneja formularios ni datos, solo carga el HTML correspondiente
    return render_template('contacto/contacto.html')
