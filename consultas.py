# consultas.py
import io
import pandas as pd
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
        
 #ADMIN
 
 # Obtener todos los pacientes (devolviendo lista de dicts)
def get_all_pacientes():
    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                  p.id_paciente,
                  p.nombre        AS nombre_paciente,
                  p.apellido      AS apellido_paciente,
                  p.dni,
                  p.fecha_nacimiento,
                  p.sexo,
                  p.telefono,
                  p.direccion,
                  p.email         AS email_paciente,
                  u.id_usuario,
                  u.nombre_user   AS nombre_usuario,
                  u.email_user    AS email_usuario
                FROM Paciente p
                LEFT JOIN Usuario_Sistema u
                  ON u.id_paciente = p.id_paciente
            """)
            rows = cursor.fetchall()
            cols = [col[0] for col in cursor.description]
        return [dict(zip(cols, row)) for row in rows]
    finally:
        conn.close()


# Actualizar paciente y usuario asociado
def update_paciente(id_paciente, nombre, apellido, dni,
                    fecha_nacimiento, sexo, telefono,
                    direccion, email):
    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            # 1) Actualiza Paciente
            cursor.execute(
                """
                UPDATE Paciente
                   SET nombre = %s,
                       apellido = %s,
                       dni = %s,
                       fecha_nacimiento = %s,
                       sexo = %s,
                       telefono = %s,
                       direccion = %s,
                       email = %s
                 WHERE id_paciente = %s
                """,
                (nombre, apellido, dni, fecha_nacimiento,
                 sexo, telefono, direccion, email,
                 id_paciente)
            )
            # 2) Actualiza Usuario_Sistema (solo nombre_user y email_user)
            cursor.execute(
                """
                UPDATE Usuario_Sistema
                   SET nombre_user = %s,
                       email_user  = %s
                 WHERE id_paciente = %s
                """,
                (nombre, email, id_paciente)
            )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print("Error al actualizar paciente y usuario:", e)
        return False
    finally:
        conn.close()
# Eliminar paciente y usuario asociado
def eliminar_paciente(id_paciente):
    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM Usuario_Sistema WHERE id_paciente = %s",
                (id_paciente,)
            )
            cursor.execute(
                "DELETE FROM Paciente WHERE id_paciente = %s",
                (id_paciente,)
            )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print("Error al eliminar paciente y usuario:", e)
        return False
    finally:
        conn.close()

def insertar_paciente_con_usuario(
    nombre, apellido, dni, fecha_nacimiento,
    sexo, telefono, direccion, email,
    nombre_user, contrasena_user,
    id_rol=1  # 1 = PACIENTE
):
    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            # Insertar Paciente
            cursor.execute(
                """
                INSERT INTO Paciente (
                  nombre, apellido, dni, fecha_nacimiento,
                  sexo, telefono, direccion, email
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (nombre, apellido, dni, fecha_nacimiento,
                 sexo, telefono, direccion, email)
            )
            id_paciente = cursor.lastrowid
            # Insertar Usuario_Sistema
            cursor.execute(
                """
                INSERT INTO Usuario_Sistema (
                  nombre_user, contrasena_user, email_user,
                  id_rol, id_paciente
                ) VALUES (%s, %s, %s, %s, %s)
                """,
                (nombre_user, contrasena_user, email, id_rol, id_paciente)
            )
        conn.commit()
        return id_paciente
    except Exception as e:
        conn.rollback()
        print("Error al insertar paciente+usuario:", e)
        return None
    finally:
        conn.close()
# Listar doctores y datos de usuario asociado
def get_all_doctores():
    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                  m.id_medico,
                  m.nombre        AS nombre_medico,
                  m.apellido      AS apellido_medico,
                  m.email         AS email_medico,
                  m.estado,
                  u.id_usuario,
                  u.nombre_user   AS nombre_usuario,
                  u.email_user    AS email_usuario
                FROM Medico m
                LEFT JOIN Usuario_Sistema u ON u.id_medico = m.id_medico
            """)
            rows = cursor.fetchall()
            cols = [col[0] for col in cursor.description]
        return [dict(zip(cols, row)) for row in rows]
    finally:
        conn.close()

# Insertar doctor + usuario en transacciÃ³n
def insertar_doctor_con_usuario(
    nombre, apellido, email, estado,
    nombre_user, contrasena_user,
    id_rol=2  # 2 = MEDICO
):
    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            # 1) Insertar en Medico
            cursor.execute(
                """
                INSERT INTO Medico (nombre, apellido, email, estado)
                VALUES (%s, %s, %s, %s)
                """,
                (nombre, apellido, email, estado)
            )
            id_medico = cursor.lastrowid
            # 2) Insertar en Usuario_Sistema
            cursor.execute(
                """
                INSERT INTO Usuario_Sistema (
                  nombre_user, contrasena_user, email_user,
                  id_rol, id_medico
                ) VALUES (%s, %s, %s, %s, %s)
                """,
                (nombre_user, contrasena_user, email, id_rol, id_medico)
            )
        conn.commit()
        return id_medico
    except Exception as e:
        conn.rollback()
        print("Error al insertar doctor+usuario:", e)
        return None
    finally:
        conn.close()

# Actualizar doctor + usuario asociado
def update_doctor(id_medico, nombre, apellido, email, estado):
    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            # Actualizar Medico
            cursor.execute(
                """
                UPDATE Medico
                   SET nombre   = %s,
                       apellido = %s,
                       email    = %s,
                       estado   = %s
                 WHERE id_medico = %s
                """,
                (nombre, apellido, email, estado, id_medico)
            )
            # Actualizar Usuario_Sistema
            cursor.execute(
                """
                UPDATE Usuario_Sistema
                   SET nombre_user = %s,
                       email_user  = %s
                 WHERE id_medico = %s
                """,
                (nombre, email, id_medico)
            )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print("Error al actualizar doctor y usuario:", e)
        return False
    finally:
        conn.close()

# Eliminar doctor + usuario asociado
def eliminar_doctor(id_medico):
    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM Usuario_Sistema WHERE id_medico = %s",
                (id_medico,)
            )
            cursor.execute(
                "DELETE FROM Medico WHERE id_medico = %s",
                (id_medico,)
            )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print("Error al eliminar doctor y usuario:", e)
        return False
    finally:
        conn.close()


#--------------
def get_pacientes_dataframe(desde=None, hasta=None, sexo=None, texto_busqueda=None):
    sql = """
      SELECT
        p.fecha_nacimiento         AS fecha_nacimiento,
        p.id_paciente,
        p.nombre,
        p.apellido,
        p.dni,
        p.sexo,
        p.email                   AS email_paciente,
        u.nombre_user             AS usuario_sistema
      FROM Paciente p
      LEFT JOIN Usuario_Sistema u ON u.id_paciente = p.id_paciente
      WHERE 1=1
    """
    params = []
    if desde:
        sql += " AND p.fecha_nacimiento >= %s"
        params.append(desde)
    if hasta:
        sql += " AND p.fecha_nacimiento <= %s"
        params.append(hasta)
    if sexo:
        sql += " AND p.sexo = %s"
        params.append(sexo)
    if texto_busqueda:
        sql += " AND (p.nombre LIKE %s OR p.apellido LIKE %s OR p.dni LIKE %s)"
        like = f"%{texto_busqueda}%"
        params.extend([like, like, like])

    conn = obtener_conexion()
    try:
        df = pd.read_sql(sql, conn, params=params)
    finally:
        conn.close()
    return df       
        

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
    
