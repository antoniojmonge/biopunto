from zk import ZK
import mysql.connector
from mysql.connector import Error

#Conexión con el biometric
ip_biometrico = '192.168.12.49'
port= 4370
timeout = 120
password=123
def conectar_biometrico():
    try:
        zk = ZK(
            ip= ip_biometrico, 
            port=port,
            timeout=timeout,
            password=password,
            force_udp=True,
            ommit_ping=True)   
        print(f"✔️ Conexion exitosa con el biométrico")
        conn = zk.connect()            
        return conn
    except Exception as e:
        print (f"❌ Error al conectar con el biométrico: {e}")
        return None
conectar_biometrico()
    
#conexion con mysql
def obtener_conexion_mysql():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="control_biometrico"
        ) 
        if conexion.is_connected():
            print("✔️ Conexión exitosa a la base de datos")
            return conexion
        else:
            print("❌ Error al conectar con la bdd")
            return None
    except Error as e:
        print(f"❌ Error general al conectar: {e}")
        return None

