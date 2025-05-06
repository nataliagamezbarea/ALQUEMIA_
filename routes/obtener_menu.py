from flask import url_for
import random
from backend.base_de_datos import db, obtener_tabla
from sqlalchemy.orm import Session
from sqlalchemy import func

def obtener_menu():
    # Este método centraliza la obtención de categorías e imágenes para el menú,
    # organizadas según la sección de hombre y mujer.

    # Reflejamos las tablas necesarias desde la base de datos
    Producto = obtener_tabla('productos')
    Categoria = obtener_tabla('categorias')
    ProductoCategoria = obtener_tabla('productos_categorias')
    Seccion = obtener_tabla('secciones')
    ImagenColor = obtener_tabla('productos_imagenes_colores')

    # Iniciamos una sesión para ejecutar las consultas
    sesion = Session(db.engine)

    # Recuperamos todas las categorías disponibles
    categorias = sesion.query(Categoria).all()

    # Función auxiliar para obtener categorías aleatorias de una sección específica
    def categorias_aleatorias(nombre_seccion, limite=3):
        # Construimos la consulta filtrando por sección y obteniendo resultados únicos
        consulta = (
            sesion.query(Categoria)
            .join(ProductoCategoria)
            .join(Producto)
            .join(Seccion)
            .filter(Seccion.nombre == nombre_seccion)
            .distinct()
            .order_by(func.random())
        )
        # Si se especifica un límite, lo aplicamos; en caso contrario, devolvemos todo
        return consulta.limit(limite).all() if limite else consulta.all()

    # Función auxiliar para recuperar URLs de imágenes aleatorias de una sección
    def imagenes_aleatorias(nombre_seccion, limite=8):
        # Consultamos únicamente la columna de URL de imagen y aleatorizamos los resultados
        filas = (
            sesion.query(ImagenColor.imagen_url)
            .join(Producto)
            .join(Seccion)
            .filter(Seccion.nombre == nombre_seccion)
            .order_by(func.random())
            .limit(limite)
            .all()
        )
        # Desempaquetamos las tuplas para devolver solo las URL en una lista
        return [url for (url,) in filas]

    # Obtenemos las categorías completas para hombre y mujer (sin límite)
    categorias_hombre = categorias_aleatorias('hombre', limite=None)
    categorias_mujer = categorias_aleatorias('mujer', limite=None)

    # Obtenemos un subconjunto aleatorio de categorías para destacar en la interfaz
    categorias_hombre_aleatorias = categorias_aleatorias('hombre')
    categorias_mujer_aleatorias = categorias_aleatorias('mujer')

    # Recogemos un conjunto de imágenes aleatorias para cada sección
    imagenes_hombre_aleatorias = imagenes_aleatorias('hombre')
    imagenes_mujer_aleatorias = imagenes_aleatorias('mujer')

    # Cerramos la sesión tras completar las consultas
    sesion.close()

    # Devolvemos un diccionario con toda la información necesaria
    return {
        'categorias': categorias,
        'categorias_hombre': categorias_hombre,
        'categorias_mujer': categorias_mujer,
        'categorias_hombre_aleatorias': categorias_hombre_aleatorias,
        'categorias_mujer_aleatorias': categorias_mujer_aleatorias,
        'imagenes_hombre_aleatorias': imagenes_hombre_aleatorias,
        'imagenes_mujer_aleatorias': imagenes_mujer_aleatorias,
    }
