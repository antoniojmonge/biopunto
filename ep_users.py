from flask import Blueprint, request, jsonify
from connection import conectar_biometrico, obtener_conexion_mysql
from mysql.connector import Error
import os 
import csv
from datetime import date
from io import StringIO

endpoint_user = Blueprint("endpoint_user", __name__)
#--------------------------GESTION DE MANIPULACION DE DATOS CON MYSQL -----------------------------#

@endpoint_user.route('/api/lista_usuarios')
def lista_usuarios():
    conn = obtener_conexion_mysql()
    if not conn:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                u.dni,
                u.nombre,
                a.area AS area_nombre,
                a.id AS area_id,
                p.privilegio AS privilegio_nombre,
                p.id AS privilegio_id,
                e.estado AS estado_nombre,
                e.id AS estado_id,
                c.id as company_id,
                u.fecha_registro
            FROM usuarios u
            LEFT JOIN area a ON u.area_id = a.id
            LEFT JOIN privilegio p ON u.privilegio_id = p.id
            LEFT JOIN estado e ON u.estado_id = e.id
            LEFT JOIN company c on u.company_id = c.id
        """)
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"usuarios": usuarios})
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 500
    
#Listar dinamicamente la lista de compañias.
@endpoint_user.route('/api/lista_companies')
def lista_companies():
    conn = obtener_conexion_mysql()
    if not conn:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                id,
                name_company
            FROM company 
        """)
        companies = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"companies": companies})
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 500
    
@endpoint_user.route('/api/lista_area')
def lista_area():
    conn = obtener_conexion_mysql()
    if not conn:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select id, area as area_name from area")
        area = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"area": area})
    except Exception as e:
        conn.close()
        return  jsonify({"error": str(e)}),500

# Actualizar usuario mysql
@endpoint_user.route('/api/actualizar_usuario', methods=['POST'])
def actualizar_usuario():
    data = request.get_json()
    print(f"Payload recibido en backend: {data}")  # 👈 AQUI
    try:
        dni = str(data.get("dni")).strip()  # O usa "dni" si prefieres, según tu fetch
        nombre = str(data.get("nombre")).strip()
        grupo = int(data.get("grupo", 1))          # Mapea a area_id
        privilegio = int(data.get("privilegio", 1))
        estado = int(data.get("estado", 1))
        company = int(data.get("company",1))

        print(f"Valores: dni={dni}, nombre={nombre}, grupo={grupo}, privilegio={privilegio}, estado={estado}, company={company}")  # 👈 Y AQUI

        conn_mysql = obtener_conexion_mysql()
        if not conn_mysql:
            return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

        cursor = conn_mysql.cursor()
        sql = """
            UPDATE usuarios
            SET nombre = %s,
                area_id = %s,
                privilegio_id = %s,
                estado_id = %s,
                company_id = %s
            WHERE dni = %s
        """
        cursor.execute(sql, (nombre, grupo, privilegio, estado, company, dni))
        conn_mysql.commit()
        cursor.close()
        conn_mysql.close()

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@endpoint_user.route('/eliminar_usuario/<int:uid>', methods=["DELETE"])
def eliminar_usuario(uid):
    try:
        conn = conectar_biometrico()
        if not conn:
            return jsonify({"mensaje": "Error al conectar con el biométrico"}), 400

        users = conn.get_users()
        usuario_obj = next((u for u in users if str(u.user_id) == str(uid)), None)

        if not usuario_obj:
            return jsonify({"mensaje": f"⚠️ Usuario {uid} no existe"}), 404

        # Usamos el uid real (identificador interno del biométrico)
        conn.delete_user(uid=usuario_obj.uid)

        conn.enable_device()
        conn.disconnect()

        return jsonify({"mensaje": f"Usuario {uid} eliminado correctamente"})

    except Exception as e:
        return jsonify({'mensaje': f"❌ Error al eliminar el usuario: {str(e)}"}), 500



