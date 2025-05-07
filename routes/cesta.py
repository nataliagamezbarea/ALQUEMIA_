from flask import request, redirect, url_for, session
from backend.base_de_datos import db, obtener_tabla

def añadir_producto_cesta():
    user_id = session.get("user")
    if not user_id:
        session['message'] = 'Debes iniciar sesión para añadir productos a la cesta.'
        session['message_type'] = 'error'
        return redirect(url_for('login'))

    id_producto = request.form.get('id_producto')
    id_color = request.form.get('id_color_radio')  # ← CORREGIDO aquí
    id_talla = request.form.get('id_talla')

    if not id_producto or not id_color or not id_talla:
        session['message'] = 'Faltan datos para añadir el producto.'
        session['message_type'] = 'error'
        return redirect(request.referrer or url_for('home'))

    # Obtener la tabla ProductoVariante utilizando obtener_tabla
    ProductoVariante = obtener_tabla('producto_variante')

    variante = db.session.query(ProductoVariante).filter_by(
        id_producto=id_producto,
        id_color=id_color,
        id_talla=id_talla
    ).first()

    if not variante:
        session['message'] = 'No se encontró la variante seleccionada.'
        session['message_type'] = 'error'
        return redirect(request.referrer or url_for('home'))

    # Buscar o crear la cesta del usuario
    Cesta = obtener_tabla('cesta')
    cesta = db.session.query(Cesta).filter_by(id_usuario=user_id).first()
    if not cesta:
        cesta = Cesta(id_usuario=user_id)
        db.session.add(cesta)
        db.session.commit()

    # Buscar si el producto ya está en la cesta
    CestaProducto = obtener_tabla('cesta_producto')
    producto_cesta = db.session.query(CestaProducto).filter_by(
        id_cesta=cesta.id_cesta,
        id_variantes=variante.id_variantes
    ).first()

    if producto_cesta:
        producto_cesta.cantidad += 1
    else:
        nuevo_producto_cesta = CestaProducto(
            id_cesta=cesta.id_cesta,
            id_variantes=variante.id_variantes,
            cantidad=1
        )
        db.session.add(nuevo_producto_cesta)

    db.session.commit()

    session['message'] = 'Producto añadido a tu cesta.'
    session['message_type'] = 'success'
    return redirect(request.referrer or url_for('home'))


def eliminar_producto_cesta(id_variantes):
    user_id = session.get("user")
    if not user_id:
        session['message'] = 'Debes iniciar sesión para modificar tu cesta.'
        session['message_type'] = 'error'
        return redirect(url_for('login'))

    # Obtener las tablas necesarias
    Cesta = obtener_tabla('cesta')
    CestaProducto = obtener_tabla('cesta_producto')

    cesta = db.session.query(Cesta).filter_by(id_usuario=user_id).first()
    if not cesta:
        session['message'] = 'No tienes una cesta activa.'
        session['message_type'] = 'error'
        return redirect(request.referrer or url_for('home'))

    producto_cesta = db.session.query(CestaProducto).filter_by(
        id_cesta=cesta.id_cesta,
        id_variantes=id_variantes
    ).first()

    if producto_cesta:
        db.session.delete(producto_cesta)
        db.session.commit()

    session['message'] = 'Producto eliminado de tu cesta.'
    session['message_type'] = 'success'
    return redirect(request.referrer or url_for('home'))


def actualizar_cantidad_producto(id_variantes):
    user_id = session.get("user")
    if not user_id:
        session['message'] = 'Debes iniciar sesión para modificar tu cesta.'
        session['message_type'] = 'error'
        return redirect(url_for('login'))

    nueva_cantidad = int(request.form.get('cantidad', 1))

    # Obtener las tablas necesarias
    Cesta = obtener_tabla('cesta')
    CestaProducto = obtener_tabla('cesta_producto')

    cesta = db.session.query(Cesta).filter_by(id_usuario=user_id).first()
    if not cesta:
        session['message'] = 'No tienes una cesta activa.'
        session['message_type'] = 'error'
        return redirect(request.referrer or url_for('home'))

    producto_cesta = db.session.query(CestaProducto).filter_by(
        id_cesta=cesta.id_cesta,
        id_variantes=id_variantes
    ).first()

    if producto_cesta:
        if nueva_cantidad >= 1:
            producto_cesta.cantidad = nueva_cantidad
            db.session.commit()
        else:
            # Si la cantidad es menor que 1, elimina el producto
            db.session.delete(producto_cesta)
            db.session.commit()

    session['message'] = 'Cantidad actualizada correctamente.'
    session['message_type'] = 'success'
    return redirect(request.referrer or url_for('home'))
