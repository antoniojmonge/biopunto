from flask import Blueprint, jsonify
from connection import conectar_biometrico, obtener_conexion_mysql
from mysql.connector import Error
from datetime import date

endpoint_dashboard = Blueprint("endpoint_dashboard",__name__)

def user_exists(conn, uid):
    try:
        users = conn.get_users()
        for user in users:
            # Convertimos ambos a string para asegurar coincidencia
            if str(user.user_id) == str(uid):
                return True
        return False
    except Exception as e:
        print(f"Error comprobando existencia de usuario: {e}")
        return False

def existe_usuario_en_mysql(user_id):
    conn = obtener_conexion_mysql()
    cursor = conn.cursor() 
    cursor.execute("Select 1 from usuarios where dni = %s", (user_id,))
    existe = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return existe

def insertar_usuario_mysql(dni, nombre):
    conn = obtener_conexion_mysql()
    cursor = conn.cursor()
    sql = "insert into usuarios (dni, nombre, area_id, privilegio_id, estado_id) values (%s,%s,%s,%s,%s)"
    cursor.execute(sql, (dni,nombre,1,1,1))
    conn.commit()
    cursor.close()
    conn.close()

@endpoint_dashboard.route('/api/sincronizar_usuarios_a_mysql', methods=['GET'])
def sincronizar_usuarios_a_mysql():
    conn = conectar_biometrico()
    if not conn:
        return jsonify({"error": "No se pudo conectar al biométrico"}), 500
    
    try:
        nuevos = 0
        for user in conn.get_users():
            dni = user.user_id
            nombre = user.name.strip()

            if not existe_usuario_en_mysql(dni):
                insertar_usuario_mysql(dni,nombre)
                nuevos += 1
                
        conn.disconnect()
        return jsonify({"mensaje": f"{nuevos} usuarios nuevos sincronizados desde el biométrico."})

    except Exception as e:
        conn.disconnect()
        return jsonify({"error": str(e)}),500
    
@endpoint_dashboard.route('/total_usuarios')
def total_usuarios():
    conn = obtener_conexion_mysql()
    if not conn:
        return "Error en la conexion", 500
    try:
        cursor = conn.cursor()
        cursor.execute("select count(*) from usuarios")
        total = cursor.fetchone()[0]
    except Exception as e:
        return f"Error al consultar la base de datos: {e}", 500
    finally:
        cursor.close()
        conn.close()
    return jsonify(total=total)

@endpoint_dashboard.route('/api/datos_biometrico', methods=["GET"])
def datos_biometrico():
    try:
        conn = conectar_biometrico()
        if not conn:
            return jsonify({"error": "No se pudo conectar al biometrico"})                
        asistencias =  obtener_asistencias(conn)
        asistencias_de_hoy = asistencias_hoy(conn)
        conn.disconnect()

        return jsonify({            
            "asistencias": asistencias,
            "asistencias_hoy": asistencias_de_hoy
        })
    except Exception as e:
        return jsonify({"error": str(e)}),500
 
def obtener_asistencias(conn):
    try:
        asistencias = conn.get_attendance()
        return len(asistencias)
    except Exception as e:
        print(f"Error al obtener las asistencias: {e}")
        return None
    
def asistencias_hoy(conn):
    try:
        asistencias = conn.get_attendance()
        hoy = date.today()
        asistencias_de_hoy = [a for a in asistencias if a.timestamp.date() == hoy]
        return len(asistencias_de_hoy)
    except Exception as e:
        print(f"Error al obtener las asistencias de hoy: {e}")
        return None
    

