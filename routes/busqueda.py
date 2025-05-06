from flask import render_template, request  # Importamos para mostrar HTML y leer lo que el usuario escribe
from sqlalchemy.orm import joinedload  # No se usa en este caso, pero se importa si necesitamos cargar relaciones
from backend.base_de_datos import db, obtener_tabla  # Importamos la base de datos y la función para obtener las tablas
from math import ceil  # Para redondear hacia arriba y calcular las páginas de manera eficiente

def busqueda():
    # Obtenemos el texto que el usuario ha escrito en el buscador
    busqueda = request.args.get('busqueda', '')  # Si no hay nada escrito, será una cadena vacía

    # Si no se ha escrito nada, simplemente mostramos la página de búsqueda vacía
    if not busqueda:
        return render_template('busqueda.html', busqueda=busqueda)

    # Obtenemos el número de página actual (si no hay, asumimos que estamos en la página 1)
    pagina_actual = request.args.get('pagina', 1, type=int)
    productos_por_pagina = 42  # Establecemos que en cada página se mostrarán 42 productos

    # Traemos las tablas que necesitamos de la base de datos: productos, secciones, categorías, etc.
    Producto = obtener_tabla('productos')
    Seccion = obtener_tabla('secciones')
    Categoria = obtener_tabla('categorias')
    ProductoCategoria = obtener_tabla('productos_categorias')

    # Realizamos la consulta que une las tablas necesarias (productos, secciones, categorías)
    query = db.session.query(Producto).join(Seccion).join(ProductoCategoria).join(Categoria)
    
    # Filtramos los productos cuyo nombre contenga el texto de búsqueda, sin importar mayúsculas/minúsculas
    query = query.filter(Producto.nombre.ilike(f"%{busqueda}%"))

    # Paginamos los resultados, ordenando por ID del producto (esto es para que siempre aparezcan en el mismo orden)
    productos_paginados = query.order_by(Producto.id_producto).paginate(page=pagina_actual, per_page=productos_por_pagina)

    # Calculamos el número total de páginas basado en el número total de productos encontrados
    total_paginas = ceil(query.count() / productos_por_pagina)

    # Renderizamos la plantilla 'busqueda.html' y le pasamos los datos necesarios
    # Le pasamos los productos de la página actual, el número de la página actual, el total de páginas, y el texto de búsqueda
    return render_template(
        'busqueda.html', 
        productos=productos_paginados.items,  # Los productos que corresponden a la página actual
        pagina_actual=pagina_actual,          # Página actual en la que estamos
        total_paginas=total_paginas,          # Total de páginas para la paginación
        busqueda=busqueda                     # El término de búsqueda que el usuario introdujo
    )
