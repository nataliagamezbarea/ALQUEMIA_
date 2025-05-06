from flask import redirect, render_template, session, url_for
from datetime import datetime, timedelta
from backend.base_de_datos import db, obtener_tabla  # Importamos las funciones necesarias

def compras():
    # Verifico si el usuario está logueado. Si no, lo redirijo al login.
    user_id = session.get("user")
    if not user_id:
        return redirect(url_for("login"))

    # Obtengo todas las tablas necesarias de la base de datos
    Pedido = obtener_tabla('pedidos')  # Tabla de los pedidos realizados
    PedidoProducto = obtener_tabla('pedidos_productos')  # Relación entre pedidos y productos
    ProductoVariante = obtener_tabla('productos_variantes')  # Información de variantes como talla y color
    Producto = obtener_tabla('productos')  # Información básica del producto
    Color = obtener_tabla('colores')  # Colores disponibles de productos
    Talla = obtener_tabla('tallas')  # Tallas disponibles de productos

    # Realizo la consulta de todos los pedidos del usuario con las tablas necesarias unidas
    pedidos = db.session.query(
        Pedido, PedidoProducto, ProductoVariante, Producto, Color, Talla
    ).join(PedidoProducto, Pedido.id_pedido == PedidoProducto.id_pedido
    ).join(ProductoVariante, PedidoProducto.id_variantes == ProductoVariante.id_variantes
    ).join(Producto, ProductoVariante.id_producto == Producto.id_producto
    ).join(Color, ProductoVariante.id_color == Color.id_color
    ).join(Talla, ProductoVariante.id_talla == Talla.id_talla
    ).filter(Pedido.id_usuario == user_id).all()  # Filtro para obtener solo los pedidos del usuario logueado

    # Preparo los datos de los pedidos y calculo las fechas de entrega
    pedidos_info = []
    for pedido, pedido_producto, producto_variante, producto, color, talla in pedidos:
        fecha_pedido = pedido.fecha  # Obtengo la fecha de pedido

        # Calculo las fechas de entrega
        fecha_entrega_min = fecha_pedido + timedelta(days=3)
        fecha_entrega_max = fecha_pedido + timedelta(days=5)

        # Calculo los días restantes para la entrega
        dias_restantes = (fecha_entrega_max - datetime.now().date()).days

        # Añado la información de los productos al pedido
        productos = {
            'producto': producto.nombre,
            'color': color.color,
            'talla': talla.talla,
            'cantidad': pedido_producto.cantidad,
            'total_producto': pedido_producto.total_producto
        }

        # Guardo toda la información relevante para la plantilla
        pedidos_info.append({
            'pedido_id': pedido.id_pedido,
            'fecha_pedido': fecha_pedido,
            'fecha_entrega_min': fecha_entrega_min,
            'fecha_entrega_max': fecha_entrega_max,
            'dias_restantes': dias_restantes,
            'productos': productos
        })

    # Renderizo la plantilla con los pedidos y la información calculada
    return render_template('user/compras.html', pedidos=pedidos_info)
