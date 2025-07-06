# consultas.py
import pymysql
from bd import obtener_conexion


 
def insertar_usuario_rol(nombre, apellido, dni, fecha_nacimiento, sexo, telefono, direccion, email, contrasena, id_rol):
    # Formatear nombre y apellido en InitCap
    nombre = nombre.strip().capitalize()
    apellido = apellido.strip().capitalize()

    # También puedes limpiar otros campos si quieres:
    email = email.strip().lower()

    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
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

            sql_usuario = """
                INSERT INTO Usuario_Sistema (nombre_user, contrasena_user, email_user, id_rol, id_paciente, id_medico)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_usuario, (nombre, contrasena, email, id_rol, id_paciente, id_medico))

        conexion.commit()
    finally:
        conexion.close()

        
        
def obtener_usuario_paciente_por_dni(dni):
    conexion = obtener_conexion()
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """ SELECT us.*, p.nombre, p.id_paciente AS paciente_id
                FROM Usuario_Sistema us
                JOIN Paciente p ON us.id_paciente = p.id_paciente
                WHERE p.dni = %s AND us.id_rol = 1 """

            cursor.execute(sql, (dni,))
            return cursor.fetchone()
    finally:
        conexion.close()
        
def obtener_usuario_medico_por_email(email):
    conexion = obtener_conexion()
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT us.*, m.nombre, m.id_medico AS medico_id
                FROM Usuario_Sistema us
                JOIN Medico m ON us.id_medico = m.id_medico
                WHERE us.email_user = %s AND us.id_rol = 2
            """
            cursor.execute(sql, (email,))
            return cursor.fetchone()
    finally:
        conexion.close()

def obtener_citas_por_paciente(paciente_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT c.*, m.nombre AS nombre_medico, s.nombre AS nombre_sala
                FROM Cita c
                JOIN Medico m ON c.id_medico = m.id_medico
                LEFT JOIN Sala s ON c.id_sala = s.id_sala
                WHERE c.id_paciente = %s
            """
            cursor.execute(sql, (paciente_id,))
            return cursor.fetchall()
    finally:
        conexion.close()
        
def insertar_cita(fecha, hora, motivo, id_medico, id_paciente, id_sala):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Cita (fecha, hora, motivo, id_medico, id_paciente, id_sala)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (fecha, hora, motivo, id_medico, id_paciente, id_sala))
            conexion.commit()
    finally:
        conexion.close()

def obtener_cita_por_id(id_cita):
    conexion = obtener_conexion()
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT c.*, me.id_especialidad
                FROM Cita c
                JOIN Medico_Especialidad me ON c.id_medico = me.id_medico
                WHERE c.id_cita = %s
            """
            cursor.execute(sql, (id_cita,))
            return cursor.fetchone()
    finally:
        conexion.close()

'''def obtener_cita_por_id(id_cita):
    conexion = obtener_conexion()
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM Cita WHERE id_cita = %s"
            cursor.execute(sql, (id_cita,))
            return cursor.fetchone()
    finally:
        conexion.close()'''


def actualizar_cita(id_cita, fecha, hora, motivo, id_medico, id_sala=None):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = """
                UPDATE Cita
                SET fecha = %s, hora = %s, motivo = %s, id_medico = %s, id_sala = %s
                WHERE id_cita = %s
            """
            cursor.execute(sql, (fecha, hora, motivo, id_medico, id_sala, id_cita))
        conexion.commit()
    finally:
        conexion.close()


def eliminar_cita(id_cita):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "DELETE FROM Cita WHERE id_cita = %s"
            cursor.execute(sql, (id_cita,))
        conexion.commit()
    finally:
        conexion.close()

def obtener_medicos_activos():
    conexion = obtener_conexion()
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM Medico WHERE estado = 'activo'"
            cursor.execute(sql)
            return cursor.fetchall()
    finally:
        conexion.close()

def obtener_salas_disponibles():
    conexion = obtener_conexion()
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM Sala WHERE estado = 'disponible'"
            cursor.execute(sql)
            return cursor.fetchall()
    finally:
        conexion.close()
        
        
 #otras funciones
def obtener_especialidades():
    conexion = obtener_conexion()
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM Especialidad")
            return cursor.fetchall()
    finally:
        conexion.close()

def obtener_medicos_por_especialidad(id_especialidad):
    conexion = obtener_conexion()
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT m.id_medico, m.nombre, m.apellido
                FROM Medico m
                JOIN Medico_Especialidad me ON m.id_medico = me.id_medico
                WHERE me.id_especialidad = %s
            """, (id_especialidad,))
            return cursor.fetchall()
    finally:
        conexion.close()

def obtener_turnos_medico(id_medico):
    conexion = obtener_conexion()
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT dia_semana, hora_inicio, hora_fin
                FROM Turno_Medico
                WHERE id_medico = %s
            """, (id_medico,))
            return cursor.fetchall()
    finally:
        conexion.close()

def obtener_precio_por_especialidad(id_especialidad):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT precio_consulta FROM Especialidad WHERE id_especialidad = %s
            """, (id_especialidad,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
    finally:
        conexion.close()
        
def obtener_sala_disponible_para_medico(id_medico, fecha, hora):
    conexion = obtener_conexion()
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT s.id_sala
                FROM Sala s
                WHERE s.estado = 'disponible'
                AND NOT EXISTS (
                    SELECT 1 FROM Cita c
                    WHERE c.id_sala = s.id_sala AND c.fecha = %s AND c.hora = %s
                )
                LIMIT 1
            """, (fecha, hora))
            resultado = cursor.fetchone()
            return resultado["id_sala"] if resultado else None
    finally:
        conexion.close()
        
def listar_doctores():
    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT nombre, apellido, email FROM Medico WHERE estado='activo'")
            rows = cursor.fetchall()
            cols = [col[0] for col in cursor.description]
        return [dict(zip(cols, row)) for row in rows]
    finally:
        conn.close()    
        
def obtener_especialidades_con_descripcion():
    conexion = obtener_conexion()
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT id_especialidad, nombre_espclidad, descripcion_espclidad FROM especialidad order by nombre_espclidad")
            return cursor.fetchall()
    finally:
        conexion.close()

'''def obtener_doctores_por_especialidad(id_especialidad):
    conexion = obtener_conexion()
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT m.id_medico, m.nombre, m.apellido, m.email, e.nombre_espclidad
                FROM Medico m
                JOIN Medico_Especialidad me ON m.id_medico = me.id_medico
                JOIN Especialidad e ON me.id_especialidad = e.id_especialidad
                WHERE me.id_especialidad = %s
            """
            cursor.execute(sql, (id_especialidad,))
            return cursor.fetchall()
    finally:
        conexion.close()'''        
            
   
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
    
