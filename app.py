from flask import Flask, render_template, request, redirect, url_for, flash, session
import consultas
import pymysql.err # Importante para capturar errores específicos


app = Flask(__name__)
app.secret_key = "clave_segura"

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/registro', methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        dni = request.form["dni"]
        fecha_nacimiento = request.form["fecha_nacimiento"]
        sexo = request.form["sexo"]
        telefono = request.form["telefono"]
        direccion = request.form["direccion"]
        email = request.form["email"]
        contrasena = request.form["contrasena"]
        id_rol = request.form["id_rol"]

        try:
            # Función que guarda el usuario y el paciente
            consultas.insertar_usuario_y_paciente(
                nombre, apellido, dni, fecha_nacimiento, sexo,
                telefono, direccion, email, contrasena, id_rol
            )
            flash("Usuario registrado con éxito.", "success")
            return redirect(url_for('registrar'))

        except pymysql.err.IntegrityError as e:
            # Si el error es por clave foránea inválida o email duplicado
            if "foreign key constraint" in str(e).lower():
                flash("Rol inválido. Por favor selecciona un rol correcto.", "danger")
            elif "duplicate" in str(e).lower():
                flash("El correo o DNI ya está registrado.", "warning")
            else:
                flash("Ocurrió un error inesperado. Intenta nuevamente.", "danger")
    
    return render_template("registro.html")




@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_paciente', methods=["GET", "POST"])
def login_paciente():
    if request.method == "POST":
        dni = request.form["dni"]
        contrasena = request.form["contrasena"]

        usuario = consultas.obtener_usuario_paciente_por_dni(dni)

        if usuario and usuario["contrasena_user"] == contrasena:
            session["usuario_id"] = usuario["paciente_id"]
            session["nombre"] = usuario["nombre"]
            session["rol"] = "paciente"
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for('pagina_paciente'))
        else:
            flash("DNI o contraseña incorrectos", "danger")

    return render_template("login_paciente.html")



@app.route('/login_medico', methods=["GET", "POST"])
def login_medico():
    if request.method == "POST":
        email = request.form["email"]
        contrasena = request.form["contrasena"]

        usuario = consultas.obtener_usuario_medico_por_email(email)

        if usuario and usuario["contrasena_user"] == contrasena:  # O usa check_password_hash si está encriptada
            session["usuario_id"] = usuario["medico_id"]
            session["nombre"] = usuario["nombre"]
            session["rol"] = "medico"
            flash("Inicio de sesión exitoso " , "success")
            return redirect(url_for('pagina_medico'))
        else:
            flash("Email o contraseña incorrectos", "danger")

    return render_template("login_medico.html")


@app.route('/pagina_paciente')
def pagina_paciente():
    if 'usuario_id' in session and session.get('rol') == 'paciente':
        return render_template('pagina_paciente.html', nombre=session['nombre'])
    else:
        flash("Acceso denegado. Solo para pacientes.", "danger")
        return redirect(url_for('login_paciente'))

@app.route('/pagina_medico')
def pagina_medico():
    if 'usuario_id' in session and session.get('rol') == 'medico':
        return render_template('pagina_medico.html', nombre=session['nombre'])
    else:
        flash("Acceso denegado. Solo para médicos.", "danger")
        return redirect(url_for('login_medico'))

@app.route('/logout')
def logout():
    session.clear()
    flash("Has cerrado sesión correctamente", "info")
    return redirect(url_for('login'))



if __name__ == '__main__':
    print("Iniciando Flask en http://localhost:5000")
    app.run(debug=True)

'''@app.route('/registro', methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        dni = request.form["dni"]
        fecha_nacimiento = request.form["fecha_nacimiento"]
        sexo = request.form["sexo"]
        telefono = request.form["telefono"]
        direccion = request.form["direccion"]
        email = request.form["email"]
        contrasena = request.form["contrasena"]
        id_rol = request.form["id_rol"]  # Rol seleccionado (1, 2, 3)

        consultas.insertar_usuario_y_paciente(nombre, apellido, dni, fecha_nacimiento, sexo, telefono, direccion, email, contrasena, id_rol)
        return redirect("/bienvenida")
    
    return render_template("registro.html")'''
'''@app.route('/guardar_paciente', methods=['POST'])
def guardar_paciente():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    dni = request.form['dni']
    fecha_nacimiento = request.form['fecha_nacimiento']  # formato: 'YYYY-MM-DD'
    sexo = request.form['sexo']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    email = request.form['email']

    consultas.insertar_paciente(nombre, apellido, dni, fecha_nacimiento, sexo, telefono, direccion, email)

    return redirect(url_for('home'))'''