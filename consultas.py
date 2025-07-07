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
        
        
        
def obtener_diagnosticos_por_medico(id_medico):
    conexion = obtener_conexion()
    with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("""
            SELECT d.id_diagnostico, d.descripcion_dgnstico,
                   e.nombre_enfrmdad,
                   p.nombre AS nombre_paciente, p.apellido AS apellido_paciente,
                   c.fecha
            FROM Diagnostico d
            JOIN Enfermedad e ON d.id_enfermedad = e.id_enfermedad
            JOIN Cita c ON d.id_cita = c.id_cita
            JOIN Paciente p ON c.id_paciente = p.id_paciente
            WHERE c.id_medico = %s
            ORDER BY c.fecha DESC
        """, (id_medico,))
        return cursor.fetchall()
    
def insertar_diagnostico(descripcion, id_enfermedad, id_cita):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Diagnostico (descripcion_dgnstico, id_enfermedad, id_cita)
            VALUES (%s, %s, %s)
        """, (descripcion, id_enfermedad, id_cita))
        conexion.commit()

def obtener_enfermedades():
    conexion = obtener_conexion()
    with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT id_enfermedad, nombre_enfrmdad FROM Enfermedad")
        return cursor.fetchall()

def obtener_citas_medico(id_medico):
    conexion = obtener_conexion()
    with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("""
            SELECT c.id_cita, c.fecha, c.hora, p.nombre, p.apellido
            FROM Cita c
            JOIN Paciente p ON c.id_paciente = p.id_paciente
            WHERE c.id_medico = %s
            ORDER BY c.fecha DESC
        """, (id_medico,))
        return cursor.fetchall()

   
def insertar_receta(indicaciones, id_cita):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Receta (indicaciones_receta, id_cita)
            VALUES (%s, %s)
        """, (indicaciones, id_cita))
        conexion.commit()

def obtener_receta_por_cita(id_cita):
    conexion = obtener_conexion()
    with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM Receta WHERE id_cita = %s", (id_cita,))
        return cursor.fetchone()
    

def obtener_diagnostico_por_id(id_diagnostico):
    conexion = obtener_conexion()
    with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("""
            SELECT * FROM Diagnostico WHERE id_diagnostico = %s
        """, (id_diagnostico,))
        return cursor.fetchone()

def actualizar_diagnostico(id_diagnostico, descripcion, id_enfermedad):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            UPDATE Diagnostico
            SET descripcion_dgnstico = %s, id_enfermedad = %s
            WHERE id_diagnostico = %s
        """, (descripcion, id_enfermedad, id_diagnostico))
        conexion.commit()
        
def eliminar_diagnostico(id_diagnostico):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Diagnostico WHERE id_diagnostico = %s", (id_diagnostico,))
        conexion.commit()
        
def obtener_receta_por_diagnostico(id_diagnostico):
    conexion = obtener_conexion()
    with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
        # Obtenemos la cita asociada al diagnóstico
        cursor.execute("""
            SELECT r.* FROM Diagnostico d
            JOIN Cita c ON d.id_cita = c.id_cita
            JOIN Receta r ON r.id_cita = c.id_cita
            WHERE d.id_diagnostico = %s
        """, (id_diagnostico,))
        return cursor.fetchone()

def obtener_medicamentos_por_receta(id_receta):
    conexion = obtener_conexion()
    with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("""
            SELECT rm.*, m.nombre_medcmnto, m.presentacion
            FROM Receta_Medicamento rm
            JOIN Medicamento m ON rm.id_medicamento = m.id_medicamento
            WHERE rm.id_receta = %s
        """, (id_receta,))
        return cursor.fetchall()
    
def obtener_medicamentos_disponibles():
    conexion = obtener_conexion()
    with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM Medicamento")
        return cursor.fetchall()

def insertar_receta_medicamento(id_receta, id_medicamento, indicaciones):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Receta_Medicamento (id_receta, id_medicamento, indicaciones_medcmnto)
            VALUES (%s, %s, %s)
        """, (id_receta, id_medicamento, indicaciones))
    conexion.commit()
    
def obtener_medicamento_por_id(id_medicamento):
    conexion = obtener_conexion()
    with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM Medicamento WHERE id_medicamento = %s", (id_medicamento,))
        return cursor.fetchone()

def actualizar_medicamento(id_medicamento, nombre, presentacion, descripcion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            UPDATE Medicamento
            SET nombre_medcmnto = %s, presentacion = %s, descrip_medcmnto = %s
            WHERE id_medicamento = %s
        """, (nombre, presentacion, descripcion, id_medicamento))
        conexion.commit()

def eliminar_medicamento(id_medicamento):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Medicamento WHERE id_medicamento = %s", (id_medicamento,))
        conexion.commit()

def obtener_receta_por_id(id_receta):
    conexion = obtener_conexion()
    with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM Receta WHERE id_receta = %s", (id_receta,))
        return cursor.fetchone()

def actualizar_receta(id_receta, indicaciones):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            UPDATE Receta SET indicaciones_receta = %s
            WHERE id_receta = %s
        """, (indicaciones, id_receta))
        conexion.commit()

def eliminar_receta(id_receta):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Receta WHERE id_receta = %s", (id_receta,))
        conexion.commit()
    
    
def eliminar_relaciones_medicamento(id_medicamento):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Receta_Medicamento WHERE id_medicamento = %s", (id_medicamento,))
    conexion.commit()
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
    
