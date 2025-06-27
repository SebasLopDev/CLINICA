import pymysql

def obtener_conexion():
    try:
        conexion = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='clinica1'
        )
        print("Conexión exitosa a la base de datos")
        return conexion
    except pymysql.MySQLError as e:
        print("Error al conectar:", e)
        return None