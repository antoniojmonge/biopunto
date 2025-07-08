from flask import Blueprint, send_file, after_this_request, Response
from connection import conectar_biometrico, obtener_conexion_mysql
from tempfile import NamedTemporaryFile
from mysql.connector import Error
import os 
import csv
from datetime import date
from io import StringIO

endpoint_reports = Blueprint("endpoint_reports", __name__)

@endpoint_reports.route('/descargar_reporte_usuarios')
def descargar_reporte_usuarios():
    conn = obtener_conexion_mysql()
    if not conn:
        return "Error de conexión", 500

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                u.id,
                u.dni,
                u.nombre,                
                a.area AS area,
                p.privilegio AS privilegio,
                e.estado AS estado,
                c.name_company as company,
                u.fecha_registro
            FROM 
                usuarios u
            JOIN 
                area a ON u.area_id = a.id
            JOIN 
                privilegio p ON u.privilegio_id = p.id
            JOIN 
                estado e ON u.estado_id = e.id
            JOIN 
                company c ON u.company_id = c.id
        """)
        usuarios = cursor.fetchall()
    except Exception as e:
        return f"Error al consultar la base de datos: {e}", 500
    finally:
        cursor.close()
        conn.close()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "DNI", "Nombre", "Área", "Privilegio", "Estado", "Empresa", "Fecha Registro"])
    for user in usuarios:
        writer.writerow(user)

    output.seek(0)

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=reporte_usuarios.csv"}
    )

@endpoint_reports.route('/descargar_reporte_asistencia_diaria')
def descargar_reporte_asistencia_diaria():
    conn = conectar_biometrico()
    if not conn:
        return "No se estableció conexion", 500
    
    usuarios = conn.get_users()
    user_dic = {user.user_id: user.name for user in usuarios}
    asistencias = conn.get_attendance()
    hoy = date.today()
    registros_hoy = []

    conn.disconnect()

    for att in asistencias:
        if att.timestamp.date() == hoy:
            nombre = user_dic.get(att.user_id, "Desconocido")
            registros_hoy.append((att.user_id, nombre, att.timestamp, att.status))

    tmp = NamedTemporaryFile(mode="w", delete=False, suffix=".csv", newline='', encoding="utf-8")
    filepath = tmp.name

    writer = csv.writer(tmp)
    writer.writerow(["ID Usuario","Nombre","Fecha y hora", "Estado"])
    for user in registros_hoy:
        writer.writerow(user)
    tmp.close()

    # ✅ Marcar para borrar luego
    @after_this_request
    def borrar_archivo(response):
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"Error eliminando archivo temporal: {e}")
        return response

    return send_file(filepath,
                     as_attachment=True,
                     download_name="reporte_asistencia_diaria.csv",
                     mimetype="text/csv")

@endpoint_reports.route('/descargar_reporte_asistencia_historica')
def descargar_reporte_asistencia_historica():
    conn = conectar_biometrico()
    if not conn:
        return "Error de conexion con el biometrico", 500
    usuarios = conn.get_users()
    user_dict = {user.user_id: user.name for user in usuarios}
    asistencias = conn.get_attendance()
    conn.disconnect()

    tmp = NamedTemporaryFile(mode="w", delete=False, suffix=".csv", newline="", encoding="utf-8")
    filepath = tmp.name

    writer = csv.writer(tmp)
    writer.writerow(["Id usuario", "Nombre", "Fecha y hora", "Estado"])
    for att in asistencias:
        nombre = user_dict.get(att.user_id, "Desconocido")
        writer.writerow([att.user_id, nombre, att.timestamp, att.status])
    tmp.close()
        
    # ✅ Marcar para borrar luego
    @after_this_request
    def borrar_archivo(response):
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"Error eliminando archivo temporal: {e}")
        return response

    return send_file(filepath,
                     as_attachment=True,
                     download_name="reporte_asistencia_historica.csv",
                     mimetype="text/csv")
