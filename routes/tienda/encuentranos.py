from flask import render_template
from backend.base_de_datos import db, obtener_tabla

def encuentranos():
    try:
        # Accedemos a la tabla 'tiendas' reflejada desde la base de datos
        Tienda = obtener_tabla("tiendas")

        # Realizamos una única consulta para obtener los países, provincias y ciudades distintas
        paises = db.session.query(Tienda.pais).distinct().order_by(Tienda.pais).all()
        provincias = db.session.query(Tienda.provincia).distinct().order_by(Tienda.provincia).all()
        ciudades = db.session.query(Tienda.ciudad).distinct().order_by(Tienda.ciudad).all()

        # Obtenemos todas las tiendas ordenadas por nombre (o según sea necesario)
        tiendas = db.session.query(Tienda).order_by(Tienda.nombre).all()

        # Renderizamos la plantilla 'encuentranos.html' con los datos obtenidos
        return render_template(
            'tienda/encuentranos.html',
            paises=paises,
            provincias=provincias,
            ciudades=ciudades,
            tiendas=tiendas
        )
    
    except Exception as e:
        # Si hay algún error durante la consulta o renderización, lo gestionamos y devolvemos un mensaje
        return render_template(
            'error.html', 
            mensaje="Hubo un problema al cargar los datos de las tiendas. Inténtalo de nuevo más tarde.",
            error=str(e)
        )
