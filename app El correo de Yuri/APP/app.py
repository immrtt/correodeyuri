from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import psycopg2

app = Flask(__name__)

# Configura la conexión a la base de datos
cnx = psycopg2.connect(user="mayra", password="Riquelme1999", host="servidor-personal.postgres.database.azure.com", port=5432, database="postgres")

@app.route('/')
def index():
    return render_template('registro.prin.html')

@app.route('/add')
def agregar():
    return render_template('add.html')

@app.route('/admin_pag')
def admin_pag():
    return render_template('admin_pag.html')

# Mostrar todos los trabajadores
@app.route('/mostrar_trabajadores')
def mostrar_trabajadores():
    try:
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM empleado")
        results = cursor.fetchall()
        cursor.close()
        
        trabajadores_list = [
            {
                "id_empleado": row[0],
                "rut": row[1],
                "nombres": row[2],
                "apellidos": row[3],
                "sexo": row[4],
                "telefono": row[5],
                "fecha_nacimiento": row[6],
                "fecha_ingreso": row[7],
                "correo": row[8],
                "id_area": row[9],
                "id_departamento": row[10],
                "id_cargo": row[11]
            } for row in results]

        return jsonify(trabajadores_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/admin_registro', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pswd']
        if username == 'admin28' and password == 'Admin28*':
            return redirect(url_for('admin_pag'))
        else:
            return render_template('admin.registro.html', error='Usuario o contraseña incorrectos')
    return render_template('admin.registro.html')

def username_valid(username, password):
    cursor = cnx.cursor()
    cursor.execute("SELECT contrasena FROM usuario WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()

    if result:
        stored_password = result[0]
        if password == stored_password:
            return True
    return False


@app.route('/trab_login', methods=['GET', 'POST'])
def trab_login():
        username = request.form['uname']
        password = request.form['pswd']
        
        if username_valid(username, password):
            session['uname'] = username
            return redirect(url_for('mostrar_datos_trabajador'))
        else:
            return render_template('trab.registro.html', error='Usuario o contraseña incorrectos')
    


@app.route('/mostrar_datos_trabajador')
def mostrar_datos_trabajador():
    if 'trab28' in session:
        
        trabajador = mostrar_trabajador(session['trab28'])
        
        return render_template('datos_emp.html', trabajador=trabajador)
    else:
        return redirect(url_for('login'))


@app.route('/trab_pag')
def trab_pag():
    return render_template('datos_emp.html') 

@app.route('/trab_registro')
def trab_registro():
    return render_template('trab.registro.html')

@app.route('/search', methods=['GET', 'POST'])
def search_trab():
    if request.method == 'POST':
        rut = request.form['b-rut']
        try:
            cursor = cnx.cursor()
            cursor.execute("SELECT * FROM empleado WHERE rut = %s", (rut,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                return redirect(url_for('mostrar_trabajador', rut=rut))
            else:
                return jsonify({"message": "No se encontraron datos"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return render_template('search.html')

@app.route('/mostrar_trabajador/<string:rut>')
def mostrar_trabajador(rut):
    try:
        cursor = cnx.cursor()
        cursor.execute("""
            SELECT e.id_empleado, e.rut, e.nombres, e.apellidos, e.sexo, e.telefono, e.fecha_nacimiento,
                   e.fecha_ingreso, e.correo, a.nombre_area, d.nombre_departamento, c.nombre_cargo
            FROM empleado e
            INNER JOIN area a ON e.id_area = a.id_area
            INNER JOIN departamento d ON e.id_departamento = d.id_departamento
            INNER JOIN cargo c ON e.id_cargo = c.id_cargo
            WHERE e.rut = %s
        """, (rut,))

        result = cursor.fetchone()
        
        if result:
            # Obtener datos del empleado
            id_empleado = result[0]
            rut = result[1]
            nombres = result[2]
            apellidos = result[3]
            sexo = result[4]
            telefono = result[5]
            fecha_nacimiento = result[6]
            fecha_ingreso = result[7]
            correo = result[8]
            nombre_area = result[9]
            nombre_departamento = result[10]
            nombre_cargo = result[11]

            print(f"ID del empleado: {id_empleado}")
            # Consulta para obtener carga familiar
            cursor.execute("SELECT * FROM carga_familiar WHERE id_empleado = %s", (id_empleado,))
            carga_familiar_results = cursor.fetchall()
            print(f"Cargas familiares resultados: {carga_familiar_results}")
            cargas_familiares = []
            for carga in carga_familiar_results:
                carga_familiar = {
                    "id_carga": carga[0],
                    "nombres": carga[1],
                    "apellidos": carga[2],
                    "edad": carga[3],
                    "sexo": carga[4],
                    "parentesco": carga[5]
                }
                cargas_familiares.append(carga_familiar)
            # Consulta para obtener contacto de emergencia
            cursor.execute("SELECT * FROM contacto_emergencia WHERE id_empleado = %s", (id_empleado,))
            contacto_emergencia_results = cursor.fetchall()
            print(f"Contactos de emergencia resultados: {contacto_emergencia_results}")
            contactos_emergencia = []
            for contacto in contacto_emergencia_results:
                contacto_emergencia = {
                    "nombres": contacto[0],
                    "apellidos": contacto[1],
                    "parentesco": contacto[2],
                    "telefono": contacto[3]
                }
                contactos_emergencia.append(contacto_emergencia)

            cursor.close()

            # Construir el objeto trabajador con todos los datos obtenidos
            trabajador = {
                "id_empleado": id_empleado,
                "rut": rut,
                "nombres": nombres,
                "apellidos": apellidos,
                "sexo": sexo,
                "telefono": telefono,
                "fecha_nacimiento": fecha_nacimiento,
                "fecha_ingreso": fecha_ingreso,
                "correo": correo,
                "nombre_area": nombre_area,
                "nombre_departamento": nombre_departamento,
                "nombre_cargo": nombre_cargo,
                "cargas_familiares": cargas_familiares,
                "contactos_emergencia": contactos_emergencia
            }

            print("Trabajador:", trabajador)
            return render_template('datos_emp.html', trabajador=trabajador)
        else:
            return jsonify({"message": "No se encontraron datos"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

#MODIFICAR EMPLEADO
@app.route('/modificar/<string:rut>', methods=['GET'])
def modificar_empleado_form(rut):
    try:
        cursor = cnx.cursor()
        cursor.execute("""
            SELECT e.id_empleado, e.rut, e.nombres, e.apellidos, e.sexo, e.telefono, e.fecha_nacimiento,
                   e.fecha_ingreso, e.correo, a.nombre_area, d.nombre_departamento, c.nombre_cargo
            FROM empleado e
            INNER JOIN area a ON e.id_area = a.id_area
            INNER JOIN departamento d ON e.id_departamento = d.id_departamento
            INNER JOIN cargo c ON e.id_cargo = c.id_cargo
            WHERE e.rut = %s
        """, (rut,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            id_empleado = result[0]
            rut = result[1]
            nombres = result[2]
            apellidos = result[3]
            sexo = result[4]
            telefono = result[5]
            fecha_nacimiento = result[6]
            fecha_ingreso = result[7]
            correo = result[8]
            nombre_area = result[9]
            nombre_departamento = result[10]
            nombre_cargo = result[11]

            trabajador = {
                "id_empleado": id_empleado,
                "rut": rut,
                "nombres": nombres,
                "apellidos": apellidos,
                "sexo": sexo,
                "telefono": telefono,
                "fecha_nacimiento": fecha_nacimiento,
                "fecha_ingreso": fecha_ingreso,
                "correo": correo,
                "nombre_area": nombre_area,
                "nombre_departamento": nombre_departamento,
                "nombre_cargo": nombre_cargo
            }

            return render_template('update.html', trabajador=trabajador)
        else:
            return jsonify({"message": "No se encontraron datos"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/modificar/<string:rut>', methods=['POST'])
def modificar_empleado(rut):
    try:
        id_empleado = request.form['t-id']
        rut = request.form['t-rut']
        nombres = request.form['t-nombres']
        apellidos = request.form['t-apellidos']
        sexo = request.form['t-sexo']
        telefono = request.form['t-telefono']
        fecha_nacimiento = request.form['t-fechanacimiento']
        fecha_ingreso = request.form['t-fechaingreso']
        correo = request.form['t-correo']
        nombre_area = request.form['t-area']
        nombre_departamento = request.form['t-depto']
        nombre_cargo = request.form['t-cargo']

        cursor = cnx.cursor()
        cursor.execute("""
            UPDATE empleado 
            SET rut = %s, nombres = %s, apellidos = %s, sexo = %s, telefono = %s, fecha_nacimiento = %s, 
                fecha_ingreso = %s, correo = %s
            WHERE id_empleado = %s
        """, (rut, nombres, apellidos, sexo, telefono, fecha_nacimiento, fecha_ingreso, correo, id_empleado))

        # Actualizar el área, departamento y cargo en sus respectivas tablas
        cursor.execute("UPDATE area SET nombre_area = %s WHERE id_area = (SELECT id_area FROM empleado WHERE id_empleado = %s)", (nombre_area, id_empleado))
        cursor.execute("UPDATE departamento SET nombre_departamento = %s WHERE id_departamento = (SELECT id_departamento FROM empleado WHERE id_empleado = %s)", (nombre_departamento, id_empleado))
        cursor.execute("UPDATE cargo SET nombre_cargo = %s WHERE id_cargo = (SELECT id_cargo FROM empleado WHERE id_empleado = %s)", (nombre_cargo, id_empleado))

        cnx.commit()
        cursor.close()
        
        return render_template('search.html')
       
    except Exception as e:
        return jsonify({"error": str(e)}), 500





    # eliminar empleado
@app.route('/eliminar_empleado/<string:rut>', methods=['DELETE'])
def eliminar_empleado(rut):
    try:
        cursor = cnx.cursor()
        
        # Obtener el id_empleado utilizando el rut
        cursor.execute("SELECT id_empleado FROM empleado WHERE rut = %s", (rut,))
        result = cursor.fetchone()
        
        if result:
            id_empleado = result[0]

            # Eliminar referencias en otras tablas
            cursor.execute("DELETE FROM carga_familiar WHERE id_empleado = %s", (id_empleado,))
            cursor.execute("DELETE FROM contacto_emergencia WHERE id_empleado = %s", (id_empleado,))

            # Eliminar el empleado
            cursor.execute("DELETE FROM empleado WHERE id_empleado = %s", (id_empleado,))
            
            # Confirmar los cambios
            cnx.commit()
            
            cursor.close()
            return jsonify({"message": "Empleado y sus referencias eliminados exitosamente"}), 200
        else:
            cursor.close()
            return jsonify({"message": "Empleado no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/add_trabajador', methods=['POST'])
def get_data():
    rut = request.form['t-rut']
    nombres = request.form['t-nombres']
    apellidos = request.form['t-apellidos']
    sexo = request.form['t-sexo']
    telefono = request.form['t-telefono']
    fecha_nacimiento = request.form['t-fechanacimiento']
    fecha_ingreso = request.form['t-fechaingreso']
    correo = request.form['t-correo']
    area = request.form['t-area']
    cargo = request.form['t-cargo']
    departamento = request.form['t-depto']

    #contacto_emergencia
    cnombres = request.form['c-nombres']
    capellidos = request.form['c-apellidos']
    cparentesco = request.form['c-parentesco']
    ctelefono = request.form['c-telefono']

    #cargas familiares
    canombres = request.form['ca-nombres']
    caapellidos = request.form['ca-apellidos']
    caparentesco = request.form['ca-parentesco']
    caedad = request.form['ca-edad']
    casexo = request.form['ca-sexo']

    try:
        cursor = cnx.cursor()

        # Verificar e insertar en la tabla area
        cursor.execute("SELECT 1 FROM area WHERE nombre_area = %s", (area,))
        if cursor.fetchone() is None:
            sql_area = "INSERT INTO area (nombre_area) VALUES (%s) RETURNING id_area"
            cursor.execute(sql_area, (area,))
            id_area = cursor.fetchone()[0]
        else:
            cursor.execute("SELECT id_area FROM area WHERE nombre_area = %s", (area,))
            id_area = cursor.fetchone()[0]

        # Verificar e insertar en la tabla departamento
        cursor.execute("SELECT 1 FROM departamento WHERE nombre_departamento = %s", (departamento,))
        if cursor.fetchone() is None:
            sql_departamento = "INSERT INTO departamento (nombre_departamento) VALUES (%s) RETURNING id_departamento"
            cursor.execute(sql_departamento, (departamento,))
            id_departamento = cursor.fetchone()[0]
        else:
            cursor.execute("SELECT id_departamento FROM departamento WHERE nombre_departamento = %s", (departamento,))
            id_departamento = cursor.fetchone()[0]

        # Verificar e insertar en la tabla cargo
        cursor.execute("SELECT 1 FROM cargo WHERE nombre_cargo = %s", (cargo,))
        if cursor.fetchone() is None:
            sql_cargo = "INSERT INTO cargo (nombre_cargo) VALUES (%s) RETURNING id_cargo"
            cursor.execute(sql_cargo, (cargo,))
            id_cargo = cursor.fetchone()[0]
        else:
            cursor.execute("SELECT id_cargo FROM cargo WHERE nombre_cargo = %s", (cargo,))
            id_cargo = cursor.fetchone()[0]

        # Insertar en la tabla empleado
        sql_empleado = """
        INSERT INTO empleado (rut, nombres, apellidos, sexo, telefono, fecha_nacimiento, fecha_ingreso, correo, id_area, id_departamento, id_cargo) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_empleado;
        """
        
        cursor.execute(sql_empleado, (rut, nombres, apellidos, sexo, telefono, fecha_nacimiento, fecha_ingreso, correo, id_area, id_departamento, id_cargo))
        id_empleado = cursor.fetchone()[0]
        # Después de insertar en la tabla empleado
    # Insertar en la tabla carga_familiar
        sql_carga_familiar = """
        INSERT INTO carga_familiar (nombres, apellidos, parentesco, edad, sexo, id_empleado)
        VALUES (%s, %s, %s, %s, %s, %s);
        """

        cursor.execute(sql_carga_familiar, (canombres, caapellidos, caparentesco, caedad, casexo, id_empleado))

        # Después de insertar en la tabla empleado
# Insertar en la tabla contacto_emergencia
        sql_contacto_emergencia = """
        INSERT INTO contacto_emergencia (nombres, apellidos, parentesco, telefono, id_empleado)
        VALUES (%s, %s, %s, %s, %s);
        """

        cursor.execute(sql_contacto_emergencia, (cnombres, capellidos, cparentesco, ctelefono, id_empleado))



        cnx.commit()
        cursor.close()

        return redirect(url_for('mostrar_trabajador', rut=rut))

    except Exception as e:
        cnx.rollback()
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
