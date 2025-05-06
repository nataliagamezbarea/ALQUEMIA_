from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import Table

# Inicializamos SQLAlchemy y el objeto Base para reflejar tablas
db = SQLAlchemy()
metadata = db.metadata
Base = automap_base(metadata=metadata)

def init_models(app):
    # Configuramos la base de datos con la app
    db.init_app(app)
    with app.app_context():
        # Reflejamos todas las tablas en la base de datos
        metadata.reflect(bind=db.engine, resolve_fks=True)
        
        # Aquí reflejamos la tabla específica 'productos_categorias', que es una tabla intermedia
        # Esta tabla conecta productos con categorías, y la necesitamos para las relaciones
        productos_categorias = Table('productos_categorias', metadata, autoload_with=db.engine)
        
        # Preparamos las clases reflejadas, no necesitamos autoload después
        Base.prepare()

        # Para saber qué tablas se han reflejado, lo mostramos en consola (útil para depurar)
        print("Tablas reflejadas:", list(Base.classes.keys()))

def obtener_tablas():
    # Si no hay clases reflejadas, devolvemos una lista de los nombres de las tablas reflejadas
    if not Base.classes:
        return list(Base.classes.keys())

def obtener_tabla(nombre):
    """Devuelve la tabla reflejada por su nombre o la tabla directamente de metadata si no está en las clases reflejadas."""
    try:
        return Base.classes[nombre]  # Si la tabla está reflejada, la obtenemos
    except KeyError:
        if nombre in metadata.tables:  # Si no está como clase, la buscamos en la metadata
            return metadata.tables[nombre]
        # Si no encontramos la tabla, lanzamos un error claro
        raise KeyError(f"La tabla '{nombre}' no fue encontrada. Tablas disponibles: {list(Base.classes.keys())}")
