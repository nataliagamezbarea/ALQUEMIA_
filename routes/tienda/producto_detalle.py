from flask import Flask, render_template, request
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from backend.base_de_datos import db, obtener_tabla

def producto_detalle(id_producto):
    # Obtener las clases reflejadas
    Producto = obtener_tabla('productos')
    Categoria = obtener_tabla('categorias')
    ProductoCategoria = obtener_tabla('productos_categorias')
    ImagenColor = obtener_tabla('productos_imagenes_colores')
    Variante = obtener_tabla('productos_variantes')
    Color = obtener_tabla('colores')
    Talla = obtener_tabla('tallas')

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

    # Obtener variantes del producto
    variantes = db.session.query(Variante).filter(Variante.id_producto == id_producto).all()

    # Obtener tallas disponibles
    tallas_disponibles = []
    for variante in variantes:
        if variante.tallas and variante.tallas not in tallas_disponibles:
            tallas_disponibles.append(variante.tallas)

    # Obtener categorías del producto
    categorias = (
        db.session.query(Categoria)
        .join(ProductoCategoria, ProductoCategoria.c.id_categoria == Categoria.id_categoria)
        .filter(ProductoCategoria.c.id_producto == id_producto)
        .all()
    )

    # Obtener productos recomendados basados en categorías
    productos_recomendados = (
        db.session.query(Producto)
        .join(ProductoCategoria, ProductoCategoria.c.id_producto == Producto.id_producto)
        .filter(ProductoCategoria.c.id_categoria.in_(
            [categoria.id_categoria for categoria in categorias]
        ))
        .filter(Producto.id_producto != id_producto)
        .distinct()
        .limit(4)
        .all()
    )

    # Obtener las primeras dos imágenes para cada producto recomendado
    imagenes_recomendadas = {}
    for prod in productos_recomendados:
        imagenes = (
            db.session.query(ImagenColor)
            .filter(ImagenColor.id_producto == prod.id_producto)
            .limit(2)  # Limitamos a las primeras dos imágenes
            .all()
        )
        # Asignamos las imágenes como URLs
        if imagenes:
            imagenes_recomendadas[prod.id_producto] = [imagen.imagen_url for imagen in imagenes]
        else:
            imagenes_recomendadas[prod.id_producto] = [None, None]  # Imágenes por defecto si no existen

    # Devolver la plantilla con los datos
    return render_template(
        'user/producto_detalle.html',
        producto=producto,
        imagenes_por_color=imagenes_por_color,
        productos_recomendados=productos_recomendados,
        imagenes_recomendadas=imagenes_recomendadas,
        variantes=variantes,
        categorias=categorias,
        tallas=tallas_disponibles
    )
