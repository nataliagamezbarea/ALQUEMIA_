from flask import render_template, request, get_flashed_messages
from sqlalchemy import func
from backend.base_de_datos import db, obtener_tabla

def catalogo():
    # Obtener tablas necesarias desde la base de datos
    Producto = obtener_tabla('productos')
    Categoria = obtener_tabla('categorias')
    ProductoCategoria = obtener_tabla('productos_categorias')
    Seccion = obtener_tabla('secciones')
    ImagenColor = obtener_tabla('productos_imagenes_colores')

    # Función para obtener imágenes por producto en una sección
    def obtener_imagenes(seccion_nombre):
        return (
            db.session.query(ImagenColor)
            .join(Producto)
            .join(Seccion)
            .filter(Seccion.nombre == seccion_nombre)
            .all()
        )

    # Recuperar categorías y productos

    # Obtener sección y categoría desde parámetros de la URL
    nombre_seccion = request.args.get('seccion', 'hombre')
    nombre_categoria = request.args.get('categoria', None)

    consulta_productos = db.session.query(Producto).join(ProductoCategoria).join(Categoria).join(Seccion)
    if nombre_seccion:
        consulta_productos = consulta_productos.filter(Seccion.nombre == nombre_seccion)
    if nombre_categoria:
        consulta_productos = consulta_productos.filter(Categoria.nombre == nombre_categoria)

    pagina_actual = request.args.get('pagina', 1, type=int)
    productos_por_pagina = 12
    productos_paginados = consulta_productos.paginate(page=pagina_actual, per_page=productos_por_pagina, error_out=False)

    # Obtener imágenes y asociarlas a productos
    imagenes = obtener_imagenes(nombre_seccion)

    # Enriquecer productos con sus imágenes
    for producto in productos_paginados.items:
        producto.imagenes = [img for img in imagenes if img.id_producto == producto.id_producto]

    # Renderizar plantilla con los datos
    return render_template(
        'tienda/catalogo.html',
        productos=productos_paginados.items,  # Productos actuales de la página
        pagina_actual=pagina_actual,
        total_paginas=productos_paginados.pages,  # Total de páginas calculado por paginate
    )


# Vista para mostrar el detalle de un producto
def producto_detalle(id_producto):
    Producto = obtener_tabla('productos')
    ImagenColor = obtener_tabla('productos_imagenes_colores')
    Variante = obtener_tabla('productos_variantes')
    Color = obtener_tabla('colores')

    # Obtener el producto por su ID
    producto = db.session.query(Producto).get(id_producto)

    if not producto:
        return "Producto no encontrado", 404

    # Obtener las imágenes asociadas al producto
    imagenes_por_color = {}
    imagenes = db.session.query(ImagenColor).filter(ImagenColor.id_producto == id_producto).all()
    for imagen in imagenes:
        if imagen.id_color not in imagenes_por_color:
            imagenes_por_color[imagen.id_color] = []
        imagenes_por_color[imagen.id_color].append(imagen.imagen_url)

    # Obtener variantes del producto (por ejemplo, colores y tallas)
    variantes = db.session.query(Variante).filter(Variante.id_producto == id_producto).all()

    # Obtener productos recomendados (puedes personalizar esta parte)
    productos_recomendados = db.session.query(Producto).limit(4).all()

    return render_template(
        'user/producto_detalle.html',
        producto=producto,
        imagenes_por_color=imagenes_por_color,
        productos_recomendados=productos_recomendados,
        id_variante=None  # Este valor podría venir de alguna lógica adicional (por ejemplo, por el color o talla)
    )
