from flask import Flask, render_template, request, redirect, url_for, flash, session
import consultas


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/registrar', methods=["GET", "POST"])
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
    
    return render_template("registro.html")


@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_paciente')
def login_paciente():
    return render_template('login_paciente.html')

@app.route('/login_medico')
def login_medico():
    return render_template('login_medico.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

if __name__ == '__main__':
    print("Iniciando Flask en http://localhost:5000")
    app.run(debug=True)

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