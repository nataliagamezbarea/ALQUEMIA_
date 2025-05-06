from flask import session, jsonify  # Importamos cosas de Flask para manejar sesiones (usuarios) y responder con JSON
from backend.base_de_datos import db, obtener_tabla  # Nuestra base de datos y una función mágica para traer tablas

def obtener_cesta():
    # Primero vemos si el usuario ha iniciado sesión (si no, ni modo, no puede ver su cesta )
    user_id = session.get("user")
    if not user_id:
        return jsonify({"error": "Debes iniciar sesión para ver tu cesta."}), 401  # Mensaje de error y código 401 (no autorizado)

    # Traemos todas las tablas que vamos a usar (esto es como nuestro inventario de info)
    Cesta = obtener_tabla("cestas")
    CestaProducto = obtener_tabla("cestas_productos")
    ProductoVariante = obtener_tabla("productos_variantes")
    ProductoImagen = obtener_tabla("productos_imagenes_colores")
    Producto = obtener_tabla("productos")

    # Buscamos la cesta del usuario en la base de datos
    cesta = db.session.execute(db.select(Cesta).where(Cesta.id_usuario == user_id)).all()
    
    # Si no tiene cesta aún (aw), devolvemos una vacía
    if not cesta:
        return {"productos_cesta": [], "numero_productos": 0, "total": 0.0}

    # Ahora buscamos todos los productos que están en esa cesta
    productos = db.session.execute(
        db.select(CestaProducto).where(CestaProducto.id_cesta == cesta[0].id_cesta)
    ).all()

    productos_cesta = []  # Aquí vamos a guardar lo que el usuario tiene en su cesta
    total = 0.0  # Y esto es para ir sumando el precio total 

    for producto in productos:
        # Buscamos la variante del producto (como talla, color, etc.)
        variante = db.session.get(ProductoVariante, producto.id_variantes)
        if not variante:
            continue  # Si no hay variante, seguimos con el siguiente

        # Ahora conseguimos el producto base (para nombre, precio, etc.)
        producto = db.session.get(Producto, variante.id_producto)

        # Y buscamos la imagen que corresponde al color de esa variante 
        imagen = db.session.execute(
            db.select(ProductoImagen).where(
                ProductoImagen.id_producto == variante.id_producto,
                ProductoImagen.id_color == variante.id_color
            )
        ).all()
        
        imagen_url = imagen[0].imagen_url if imagen else None  # Si hay imagen, la tomamos, si no, queda en None

        # Guardamos toda la info del producto en la lista para mostrarla después en el carrito
        productos_cesta.append({
            "id": producto.id,
            "cantidad": producto.cantidad,
            "imagen_url": imagen_url,
            "nombre": producto.nombre,
            "precio": float(producto.precio)
        })

        # Sumamos el precio total según cuántos haya
        total += float(producto.precio) * producto.cantidad

    # Al final devolvemos toda la info: los productos, cuántos hay, y cuánto cuesta todo
    return {
        "productos_cesta": productos_cesta,
        "numero_productos": sum(producto['cantidad'] for producto in productos_cesta),
        "total": round(total, 2)  # Redondeamos a 2 decimales porque obvio, somos ordenadas ✨
    }
