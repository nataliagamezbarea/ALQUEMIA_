from flask import render_template, request  # Importamos cosas de Flask: para mostrar HTML y leer lo que el usuario escribe
from sqlalchemy.orm import joinedload  # Esto sirve para traer relaciones de la base de datos (aunque aquí ni lo usamos jaja)
from backend.base_de_datos import db, obtener_tabla  # Aquí traemos la base de datos y una función para conseguir las tablas
from math import ceil  # Esto es para redondear hacia arriba, súper útil para calcular las páginas

def busqueda():
    # Obtenemos lo que el usuario escribió en el buscador, si no puso nada, queda vacío
    busqueda = request.args.get('busqueda', '')

    # Si no escribieron nada en el buscador...
    if not busqueda:
        # Mostramos la página de búsqueda sin resultados (solo el input vacío y ya)
        return render_template('busqueda.html', busqueda=busqueda)
    
    # Sacamos en qué página estamos, si no hay, asumimos que es la 1
    pagina_actual = request.args.get('pagina', 1, type=int)
    productos_por_pagina = 42  # 42 productos por página 

    # Traemos nuestras tablas de la base de datos (productos, secciones, etc.)
    Producto = obtener_tabla('productos')
    Seccion = obtener_tabla('secciones')
    Categoria = obtener_tabla('categorias')
    ProductoCategoria = obtener_tabla('productos_categorias')

    # Hacemos una consulta que une las tablas y busca productos que contengan el texto buscado
    query = db.session.query(Producto).join(Seccion).join(ProductoCategoria).join(Categoria)
    query = query.filter(Producto.nombre.ilike(f"%{busqueda}%"))  # Buscamos sin importar mayúsculas o minúsculas

    # Ahora ordenamos los productos por ID y los dividimos por páginas
    productos_paginados = query.order_by(Producto.id_producto).paginate(page=pagina_actual, per_page=productos_por_pagina)

    # Calculamos cuántas páginas en total hay con los resultados (redondeando hacia arriba obvio)
    total_paginas = ceil(query.count() / productos_por_pagina)

    # Finalmente mostramos la página con los resultados que tocan en esa página
    return render_template('busqueda.html', productos=productos_paginados.items, pagina_actual=pagina_actual,total_paginas=total_paginas,busqueda=busqueda)
