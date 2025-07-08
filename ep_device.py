from flask import Blueprint, jsonify
from connection import conectar_biometrico, ip_biometrico, port, timeout, password
from zk import ZK

endpoint_device = Blueprint("endpoint_device", __name__)

@endpoint_device.route('/data_device')
def data_device():
    try:
        conn = conectar_biometrico()
        if not conn:
            return  jsonify({"Error": "No se pudo conectar al biométrico"})
        name = conn.get_device_name()
        firmware = conn.get_firmware_version()
        serie = conn.get_serialnumber()        
        return jsonify({    
            "name": name,
            "firmware": firmware,
            "serie": serie,
            "ip_biometrico": ip_biometrico,
            "port": port,
            "timeout": timeout,
            "password": password
        })
    except Exception as e:        
        return jsonify ({"Error": str(e)})
    finally:
        if conn:    
            conn.disconnect()

        
