# Importamos la función 'render_template' de Flask, que nos permite cargar archivos HTML
from flask import render_template

# Esta función muestra la página "nosotros" dentro del directorio de la tienda
def nosotros():
    # Aquí se devuelve la plantilla HTML para que se muestre en el navegador
    return render_template('tienda/nosotros.html')
