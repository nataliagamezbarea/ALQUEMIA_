# Importamos la función que nos permite renderizar plantillas HTML
from flask import render_template

# Importamos la base de datos y la función que nos permite obtener tablas
from backend.base_de_datos import db, obtener_tabla

def encuentranos():
    # Accedemos a la tabla 'tiendas' reflejada desde la base de datos
    Tienda = obtener_tabla("tiendas")

    # Obtenemos una lista con los países únicos registrados en las tiendas
    paises = db.session.query(Tienda.pais).distinct().all()
    
    # También sacamos las provincias únicas desde la tabla
    provincias = db.session.query(Tienda.provincia).distinct().all()
    
    # Y lo mismo con las ciudades registradas
    ciudades = db.session.query(Tienda.ciudad).distinct().all()

    # Traemos todas las tiendas disponibles 
    tiendas = db.session.query(Tienda).all()

    # Mostramos la plantilla 'encuentranos' y le pasamos los datos para que se vean en la página
    return render_template(
        'tienda/encuentranos.html',
        paises=paises,
        provincias=provincias,
        ciudades=ciudades,
        tiendas=tiendas
    )
