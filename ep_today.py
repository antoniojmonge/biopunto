from flask import Blueprint, jsonify
from connection import conectar_biometrico
from mysql.connector import Error
from datetime import date

ep_today = Blueprint("ep_today", __name__)

#---MODULO DE HOY----#
@ep_today.route('/api/asistencia_hoy')
def asistencia_hoy():
    conn  = conectar_biometrico()
    if not conn:
        return jsonify({"error": "No se pudo conectar al biométrico"}), 500
    
    usuarios = conn.get_users()
    user_dict = {user.user_id: user.name for user in usuarios}
    asistencias = conn.get_attendance()
    hoy = date.today()
    registros_hoy = []

    conn.disconnect()
    for att in asistencias:
        if att.timestamp.date() == hoy:
            nombre = user_dict.get(att.user_id, "Desconocido")
            registros_hoy.append({
                "user_id":att.user_id,
                "nombre": nombre,
                "fecha":att.timestamp.strftime("%d %b %Y %I:%M %p"),    
                "estado":att.status
            })
    return jsonify({"registros": registros_hoy})


