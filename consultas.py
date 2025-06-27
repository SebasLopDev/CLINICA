# consultas.py
import pymysql
from bd import obtener_conexion


 
def insertar_usuario_y_paciente(nombre, apellido, dni, fecha_nacimiento, sexo, telefono, direccion, email, contrasena, id_rol):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Si es PACIENTE (id_rol == 1), insertar en tabla Paciente
            id_paciente = None
            id_medico = None

            if id_rol == "1":
                sql_paciente = """
                    INSERT INTO Paciente (nombre, apellido, dni, fecha_nacimiento, sexo, telefono, direccion, email)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql_paciente, (nombre, apellido, dni, fecha_nacimiento, sexo, telefono, direccion, email))
                id_paciente = cursor.lastrowid

            elif id_rol == "2":
                sql_medico = """
                    INSERT INTO Medico (nombre, apellido, email, estado)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql_medico, (nombre, apellido, email, 'activo'))
                id_medico = cursor.lastrowid

            # Insertar en Usuario_Sistema
            sql_usuario = """
                INSERT INTO Usuario_Sistema (nombre_user, contrasena_user, email_user, id_rol, id_paciente, id_medico)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_usuario, (nombre, contrasena, email, id_rol, id_paciente, id_medico))

        conexion.commit()
    finally:
        conexion.close()
   
'''def insertar_paciente(nombre, apellido, dni, fecha_nacimiento, sexo, telefono, direccion, email):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sql = """
        INSERT INTO Paciente (
            nombre, apellido, dni, fecha_nacimiento,
            sexo, telefono, direccion, email
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    valores = (nombre, apellido, dni, fecha_nacimiento, sexo, telefono, direccion, email)

    try:
        cursor.execute(sql, valores)
        conexion.commit()
        print("Paciente insertado correctamente.")
    except pymysql.MySQLError as e:
        print("Error al insertar paciente:", e)
    finally:
        cursor.close()
        conexion.close()'''
    
