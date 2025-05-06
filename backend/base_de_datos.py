from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import MetaData

# Inicializa la extensión de SQLAlchemy para usarla con Flask
db = SQLAlchemy()

# Metadata se usa para reflejar las tablas existentes en la base de datos
metadata = MetaData()

# Automap convierte automáticamente las tablas en clases que se pueden usar en Python
Base = automap_base(metadata=metadata)

def init_models(app):
    # Se conecta la base de datos con la aplicación Flask
    db.init_app(app)
    with app.app_context():
        # Refleja solo la tabla 'usuarios' desde la base de datos
        metadata.reflect(bind=db.engine)  # Se puede quitar "only" para reflejar todas las tablas
        # Prepara las clases automapeadas para que se puedan usar como modelos
        Base.prepare()

def obtener_tablas():
    # Devuelve una lista con los nombres de las tablas reflejadas
    return list(Base.classes.keys())

def obtener_tabla(nombre):
    # Devuelve la clase correspondiente a la tabla con el nombre dado
    return Base.classes[nombre]
