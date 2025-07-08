from flask import Blueprint, jsonify, request
from connection import obtener_conexion_mysql
from mysql.connector import Error
from datetime import date

endpoint_enterprise = Blueprint("endpoint_enterprise", __name__)

@endpoint_enterprise.route('/show_data')
def show_data():
    conn = obtener_conexion_mysql()
    if not conn:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                id, 
                name_enterprise,
                document,
                ubigeo,
                link,
                security_pass                               
            FROM 
                enterprise
        """)
        data_enterprise = cursor.fetchall()
        return jsonify({"data_enterprise": data_enterprise})
    except Exception as e:
        return jsonify({"Error": str(e)}),500
    finally:
        cursor.close()
        conn.close()

@endpoint_enterprise.route('/update_enterprise', methods= ['POST'])
def update_enterprise():
    conn = obtener_conexion_mysql()
    if not conn:
        return jsonify({"Sin conexion a la bdd"}),500
    
    try:
        data = request.json
        print("payload recibido: ", data)
        cursor = conn.cursor()
        sql = """
            UPDATE enterprise
            set name_enterprise=%s, link=%s, document=%s, ubigeo=%s
            where id=%s
        """
        cursor.execute(sql, (data['name_enterprise'], data['link'], data['document'], data['ubigeo'], data['id']))
        conn.commit()
        return jsonify({"mensaje":"Empresa actualziada correctamente"})
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

#----------------------------CLAVE DE SEGURIDAD--------------------#
@endpoint_enterprise.route('/update_password', methods = ['POST'])
def update_password():
    conn = obtener_conexion_mysql()
    if not conn:
        return jsonify({"Error al conectar a la bdd"}),500
    try:
        data = request.json
        print("Contraseña recibida", data)
        cursor = conn.cursor()
        sql = """
            UPDATE enterprise set security_pass = %s where id =%s
        """
        cursor.execute(sql,(data['security_pass'], data['id']))
        conn.commit()
        return jsonify({"Contraseña actualizada correctamente"})
    except Exception as e:        
        return jsonify({"Error": str(e)}),500
    finally:
        cursor.close()
        conn.close()

#----------------------------EMPRESAS--------------------#
@endpoint_enterprise.route('/show_company', methods=["POST"])       
def show_company():
    conn = obtener_conexion_mysql()
    if not conn:
        return jsonify({"Error al conectar con la bdd"}),500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
                SELECT 
                    id,
                    name_company,
                    document_company,
                    location
                FROM
                    company
        """)
        data_company = cursor.fetchall()
        return jsonify({"data_company":data_company})
    except Exception as e:
        return jsonify({"Error": str(e)}),500
    finally:
        cursor.close()
        conn.close()

@endpoint_enterprise.route('/create_company', methods=["POST"])
def create_company():
    conn = obtener_conexion_mysql()
    if not conn:
        return jsonify({"Error al conectar a la bdd"}),500
    cursor = None
    try:
        data = request.json
        name_company = data.get('name_company')
        document_company = data.get('document_company')
        location = data.get('location')

        if not name_company or not document_company or not location:
            return jsonify({"Error": "Todos los campos son obligatorios"}),400
        cursor = conn.cursor()
        sql = """
            insert into company (name_company, document_company, location) values (%s, %s, %s)
        """
        cursor.execute(sql,(name_company, document_company, location))
        conn.commit()
        return jsonify({"mensaje" :"Empresa creada con éxito "})
    except Exception as e:
        return jsonify({"Error": str(e)}),500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@endpoint_enterprise.route('/update_company', methods=["POST"])
def update_company():
    conn = obtener_conexion_mysql()
    if not conn:
        return jsonify({"Error al conectar a la bdd"}),500
    try:
        data = request.json
        cursor = conn.cursor()
        sql = """
            UPDATE company 
            set name_company=%s, document_company=%s, location=%s 
            where id=%s        
        """
        cursor.execute(sql,(
            data['name_company'],
            data['document_company'],
            data['location'],
            data['id']
        ))
        conn.commit()
        return jsonify({"mensaje":"Empresa actualizada correctamente"})
    except Exception as e:
        return  jsonify({"error": str(e)}),500
    finally:
        conn.close()
        cursor.close()

@endpoint_enterprise.route('/delete_company', methods=["POST"])
def delete_company():
    conn = obtener_conexion_mysql()
    if not conn:
        return jsonify({"Error al conectar a la bdd"}),500
    cursor = None
    try:
        data = request.json
        company_id = data.get("id")
        if not company_id:
            return jsonify({"Error":"ID de empresa requerido"}),400
        cursor = conn.cursor()
        sql = "delete from company where id = %s"
        cursor.execute(sql, (company_id,))
        conn.commit()

        return jsonify({"mensaje":"empresa bien eliminada xddd"})
    except Exception as e:
        return jsonify({"Error": str(e)}),500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

#----------------------------AREA--------------------#
@endpoint_enterprise.route('/update_area', methods = ["POST"])
def update_area():
    conn = obtener_conexion_mysql()
    if not conn:
        return jsonify({"Error al conectar con la bdd"}),500
    try:
        data = request.json
        cursor = conn.cursor()
        sql = """
            update area 
                set area = %s
            where id =%s
        """
        cursor.execute(sql, (
            data['area'],
            data['id']
        ))
        conn.commit()
        return jsonify({"Area editada"})
    except Exception as e:
        return jsonify({"error:":str(e)}),500
    finally:
        if conn: conn.close()
        if cursor: cursor.close()
    
@endpoint_enterprise.route('/create_area', methods = ["POST"])
def create_area():
    conn = obtener_conexion_mysql()
    if not conn:
        return jsonify({"Error al conectar con la bdd"}),500
    cursor = None
    try:
        data = request.json
        name_area = data.get("area")
        if not name_area:
            return jsonify({"error":"Digitar un área nueva"}),400    
        cursor = conn.cursor()
        sql = "insert into area (area) values (%s)"
        cursor.execute(sql, (name_area,))
        conn.commit()
        return jsonify({"Area creada correctamente"})
    except Exception as e:
        return jsonify({"Error": str(e)}),500
    finally:
        if conn: conn.close()
        if cursor: cursor.close()

@endpoint_enterprise.route('/show_area',  methods=["POST"])
def show_area():
    conn  = obtener_conexion_mysql()
    if not conn:
        return jsonify({"Error al conectar con la bdd"}),500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
                select 
                    id,
                    area
                from area                       
        """)
        data_area = cursor.fetchall()
        return jsonify({"data_area":data_area})
    except Exception as e:
        return jsonify({"error": str(e)}),500
    finally:
        if conn: conn.close()
        if cursor: cursor.close()

@endpoint_enterprise.route('/delete_area', methods=["POST"])
def delete_area():
    conn = obtener_conexion_mysql()
    if not conn:
        return jsonify({"Error al conectar con la bdd"}),500
    cursor = None
    try:
        data = request.json
        area_id = data.get("id")
        if not area_id:
            return jsonify({"Error":"Id del area requerido"}),400
        cursor = conn.cursor()
        sql = "delete from area where id = %s"
        cursor.execute(sql, (area_id,))
        conn.commit()
        return jsonify({"mensaje":"area correctamente eliminada"})
    except Exception as e:
        return jsonify({"error": str(e)}),500
    finally:
        if conn: conn.close()
        if cursor: cursor.close()
    

#----------------------------Planilla--------------------#
@endpoint_enterprise.route('/show_payment', methods = ["POST"])
def show_payment():
    conn = obtener_conexion_mysql()
    if not conn:
        return jsonify({"No hay conexión con la bdd"}),500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
                select
                    id,
                    description,
                    salary,
                    discount_afp
                from
                    payment                    
        """)
        data_payment = cursor.fetchall()
        return jsonify({"data_payment": data_payment})
    except Exception as e:
        return jsonify({"error": str(e)}),500
    finally:
        if conn: conn.close()
        if cursor: cursor.close()

@endpoint_enterprise.route('/create_payment', methods = ["POST"])
def create_payment():
    conn = obtener_conexion_mysql()
    if not conn:
        return jsonify ({"Sin conexion con la bdd"}), 500
    try:
        data = request.json
        description = data.get("description")
        salary = data.get("salary")
        discount_afp = data.get("discount_afp")
        if not description or not salary or not discount_afp:
            return jsonify({"error":"Digitar un nuevo salario"}),400        
        cursor = conn.cursor()
        sql = "insert into payment(description, salary, discount_afp) values (%s, %s, %s)"
        cursor.execute(sql, (description, salary, discount_afp))
        conn.commit()
        return jsonify({"mensaje":"planilla creada"})
    except Exception as e:
        return jsonify({"error": str(e)}),500
    finally:
        if conn: conn.close()
        if cursor: cursor.close()

@endpoint_enterprise.route('/update_payment', methods = ["POST"])
def update_payment():
    conn = obtener_conexion_mysql()
    if not conn:
        return jsonify({"sin conexion con bdd"}),500     
    try:
        data = request.json
        cursor = conn.cursor()
        sql = """
            UPDATE payment
            set description =%s, salary = %s, discount_afp = %s
            where id = %s
        """
        cursor.execute(sql,(
            data['description'],
            data['salary'],
            data['discount_afp'],
            data['id']
        ))
        conn.commit()
        return jsonify({"mensaje":"planilla actualizada"})
    except Exception as e:
        return jsonify({"error": str(e)}),500
    finally:
        if conn: conn.close()
        if cursor: cursor.close()

@endpoint_enterprise.route('/delete_payment', methods = ["POST"])
def delete_payment():
    conn = obtener_conexion_mysql()
    if not conn:
        return jsonify({"Sin conexion bdd"}),500
    try:
        data = request.json
        payment_id = data.get('id')
        if not payment_id:
            return jsonify({"error":"Se necesita el id"}),400
        cursor = conn.cursor()
        sql = "delete from payment where id=%s"
        cursor.execute(sql, (payment_id,))
        conn.commit()       
        return jsonify({"mensaje":"Eliminado"})
    except Exception as e:
        return jsonify ({"error" :str(e)}),500
    finally:
        if conn: conn.close()
        if cursor: cursor.close()

    
