from flask import Flask, render_template, request, redirect, url_for, flash, session
import consultas
import pymysql.err # Importante para capturar errores específicos
from datetime import datetime



app = Flask(__name__)
app.secret_key = "clave_segura"


'''@app.route('/')
def home():
    return render_template('index.html')'''
    
@app.route('/')
def home():
    doctores = consultas.listar_doctores()    
    return render_template('index.html',doctores=doctores)  


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
            consultas.insertar_usuario_rol(
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



#egdar 
@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html') 

@app.route('/mis_datos')
def mis_datos():
    return render_template('mis_datos.html')


@app.route('/especialidades')
def especialidades():
    lista_especialidades = consultas.obtener_especialidades_con_descripcion()
    return render_template('especialidades.html', especialidades=lista_especialidades)

@app.route('/staffmedicos')
def staff_medico():
    return render_template('staff_medico.html')

@app.route('/consultar_especialidades', methods=["GET", "POST"])
def consultar_especialidades():
    if 'usuario_id' not in session or session['rol'] != 'paciente':
        flash("No autorizado", "danger")
        return redirect(url_for('login_paciente'))

    especialidades = consultas.obtener_especialidades_con_descripcion()
    doctores = []
    especialidad_seleccionada = None

    if request.method == "POST":
        id_especialidad = request.form.get("id_especialidad")
        if id_especialidad:  # Solo si se seleccion� algo
            doctores = consultas.obtener_medicos_por_especialidad(id_especialidad)
            especialidad_seleccionada = int(id_especialidad)

    return render_template("consultar_especialidades.html",
                           especialidades=especialidades,
                           doctores=doctores,
                           especialidad_seleccionada=especialidad_seleccionada)
    
#finEdgar        

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


@app.route('/citas/nueva', methods=["GET", "POST"])
def nueva_cita():
    if 'usuario_id' not in session or session['rol'] != 'paciente':
        flash("No autorizado", "danger")
        return redirect(url_for('login_paciente'))

    paciente_id = session["usuario_id"]

    if request.method == "POST":
        fecha = request.form["fecha"]
        hora = request.form["hora"]
        motivo = request.form["motivo"]
        id_medico = request.form["id_medico"]
        #id_sala = request.form["id_sala"] or None
        id_sala = consultas.obtener_sala_disponible_para_medico(id_medico, fecha, hora)


        # Puedes agregar validación aquí si deseas asegurarte que la hora sea válida

        consultas.insertar_cita(fecha, hora, motivo, id_medico, paciente_id, id_sala)
        flash("Cita reservada con éxito", "success")
        return redirect(url_for('nueva_cita'))

    # Obtener todas las especialidades disponibles para mostrar en el formulario
    especialidades = consultas.obtener_especialidades()

    # También traemos las salas disponibles y las citas del paciente
    salas = consultas.obtener_salas_disponibles()
    citas = consultas.obtener_citas_por_paciente(paciente_id)

    return render_template(
        "citas/nueva_y_listado.html",
        citas=citas,
        salas=salas,
        especialidades=especialidades
    )

@app.route('/citas/<int:id>/editar', methods=["GET", "POST"])
def editar_cita(id):
    cita = consultas.obtener_cita_por_id(id)
    if not cita or cita["id_paciente"] != session.get("usuario_id"):
        flash("Acceso denegado", "danger")
        return redirect(url_for('nueva_cita'))

    if request.method == "POST":
        fecha = request.form["fecha"]
        hora = request.form["hora"]
        motivo = request.form["motivo"]
        id_medico = request.form["id_medico"]
        id_sala = request.form["id_sala"] or None
        consultas.actualizar_cita(id, fecha, hora, motivo, id_medico, id_sala)
        flash("Cita actualizada", "success")
        return redirect(url_for('nueva_cita'))

    # Obtener especialidad del médico actual
    medicos = consultas.obtener_medicos_por_especialidad(cita["id_especialidad"])
    salas = consultas.obtener_salas_disponibles()
    especialidades = consultas.obtener_especialidades()

    return render_template("citas/formulario_editar.html",
                           cita=cita,
                           medicos=medicos,
                           salas=salas,
                           especialidades=especialidades)

'''
@app.route('/citas/<int:id>/editar', methods=["GET", "POST"])
def editar_cita(id):
    cita = consultas.obtener_cita_por_id(id)
    if not cita or cita["id_paciente"] != session.get("usuario_id"):
        flash("Acceso denegado", "danger")
        return redirect(url_for('nueva_cita'))

    if request.method == "POST":
        fecha = request.form["fecha"]
        hora = request.form["hora"]
        motivo = request.form["motivo"]
        id_medico = request.form["id_medico"]
        id_sala = request.form["id_sala"] or None
        consultas.actualizar_cita(id, fecha, hora, motivo, id_medico, id_sala)
        flash("Cita actualizada", "success")
        return redirect(url_for('nueva_cita'))

    #medicos = consultas.obtener_medicos_activos()
    medicos = consultas.obtener_medicos_por_especialidad(cita["id_especialidad"])
    salas = consultas.obtener_salas_disponibles()
    return render_template("citas/formulario_editar.html",
                       cita=cita,
                       medicos=medicos,
                       salas=salas,
                       especialidades=especialidades)

'''

@app.route('/citas/<int:id>/eliminar')
def eliminar_cita(id):
    cita = consultas.obtener_cita_por_id(id)
    if not cita or cita["id_paciente"] != session.get("usuario_id"):
        flash("No autorizado", "danger")
        return redirect(url_for('nueva_cita'))

    consultas.eliminar_cita(id)
    flash("Cita eliminada", "info")
    return redirect(url_for('nueva_cita'))

@app.route('/api/medicos/<int:id_especialidad>')
def api_medicos(id_especialidad):
    medicos = consultas.obtener_medicos_por_especialidad(id_especialidad)
    return {"medicos": medicos}

@app.route('/api/turnos/<int:id_medico>')
def api_turnos(id_medico):
    turnos = consultas.obtener_turnos_medico(id_medico)
    return {"turnos": turnos}

@app.route('/api/precio_consulta/<int:id_especialidad>')
def api_precio_consulta(id_especialidad):
    precio = consultas.obtener_precio_por_especialidad(id_especialidad)
    return {"precio": precio}


@app.route('/diagnosticos')
def listar_diagnosticos():
    if session.get('rol') != 'medico':
        flash("Acceso denegado", "danger")
        return redirect(url_for('login_medico'))

    id_medico = session['usuario_id']
    lista = consultas.obtener_diagnosticos_por_medico(id_medico)
    return render_template("diagnosticos/lista.html", diagnosticos=lista)

@app.route('/diagnosticos/crear', methods=["GET", "POST"])
def crear_diagnostico():
    if 'usuario_id' not in session or session['rol'] != 'medico':
        flash("No autorizado", "danger")
        return redirect(url_for('login_medico'))

    id_medico = session['usuario_id']
    enfermedades = consultas.obtener_enfermedades()
    citas = consultas.obtener_citas_medico(id_medico)

    if request.method == "POST":
        descripcion = request.form["descripcion"]
        id_enfermedad = request.form["id_enfermedad"]
        id_cita = request.form["id_cita"]

        consultas.insertar_diagnostico(descripcion, id_enfermedad, id_cita)
        # Buscar el diagnóstico recién creado
        diagnosticos = consultas.obtener_diagnosticos_por_medico(id_medico)
        diagnostico_id = diagnosticos[0]["id_diagnostico"] if diagnosticos else None
        flash("Diagnóstico registrado correctamente", "success")
        return redirect(url_for('crear_receta', id_diagnostico=diagnostico_id))

    return render_template("diagnosticos/formulario_crear.html",
                           enfermedades=enfermedades,
                           citas=citas)

@app.route('/diagnosticos/<int:id>/editar', methods=["GET", "POST"])
def editar_diagnostico(id):
    if 'usuario_id' not in session or session['rol'] != 'medico':
        flash("No autorizado", "danger")
        return redirect(url_for('login_medico'))

    diagnostico = consultas.obtener_diagnostico_por_id(id)
    enfermedades = consultas.obtener_enfermedades()

    if request.method == "POST":
        nueva_descripcion = request.form["descripcion_dgnstico"]
        nueva_enfermedad = request.form["id_enfermedad"]
        consultas.actualizar_diagnostico(id, nueva_descripcion, nueva_enfermedad)
        flash("Diagnóstico actualizado", "success")
        return redirect(url_for('listar_diagnosticos'))

    return render_template("diagnosticos/formulario_editar_diagnostico.html",
                           diagnostico=diagnostico,
                           enfermedades=enfermedades)


@app.route('/diagnosticos/<int:id>/eliminar')
def eliminar_diagnostico(id):
    if 'usuario_id' not in session or session['rol'] != 'medico':
        flash("No autorizado", "danger")
        return redirect(url_for('login_medico'))

    consultas.eliminar_diagnostico(id)
    flash("Diagnóstico eliminado", "info")
    return redirect(url_for('listar_diagnosticos'))

@app.route('/diagnosticos/<int:id>/medicamentos')
def ver_medicamentos_diagnostico(id):
    if 'usuario_id' not in session or session['rol'] != 'medico':
        flash("Acceso no autorizado", "danger")
        return redirect(url_for('login_medico'))

    receta = consultas.obtener_receta_por_diagnostico(id)
    medicamentos = []
    if receta:
        medicamentos = consultas.obtener_medicamentos_por_receta(receta["id_receta"])

    return render_template("recetas/ver_medicamentos.html",
                           receta=receta,
                           medicamentos=medicamentos,
                           id_diagnostico=id)


@app.route('/diagnosticos/<int:id_diagnostico>/receta', methods=["GET", "POST"])
def crear_receta(id_diagnostico):
    if 'usuario_id' not in session or session['rol'] != 'medico':
        flash("Acceso no autorizado", "danger")
        return redirect(url_for('login_medico'))

    # Buscar la cita asociada al diagnóstico
    diagnostico = consultas.obtener_diagnostico_por_id(id_diagnostico)
    if not diagnostico:
        flash("Diagnóstico no encontrado", "danger")
        return redirect(url_for('listar_diagnosticos'))

    id_cita = diagnostico["id_cita"]

    if request.method == "POST":
        indicaciones = request.form["indicaciones_receta"]
        consultas.insertar_receta(indicaciones, id_cita)
        flash("Receta registrada con éxito", "success")
        return redirect(url_for('ver_medicamentos_diagnostico', id=id_diagnostico))

    return render_template("recetas/formulario_nuevo.html", id_diagnostico=id_diagnostico)


@app.route('/recetas/<int:id_receta>/medicamentos/nuevo', methods=["GET", "POST"])
def agregar_medicamento(id_receta):
    if 'usuario_id' not in session or session['rol'] != 'medico':
        flash("Acceso denegado", "danger")
        return redirect(url_for('login_medico'))

    medicamentos = consultas.obtener_medicamentos_disponibles()

    if request.method == "POST":
        id_medicamento = request.form["id_medicamento"]
        indicaciones = request.form["indicaciones_medcmnto"]

        consultas.insertar_receta_medicamento(id_receta, id_medicamento, indicaciones)
        flash("Medicamento agregado a la receta", "success")
        return redirect(request.referrer)

    return render_template("recetas/formulario_agregar_medicamento.html",
                           id_receta=id_receta,
                           medicamentos=medicamentos)
    
    
@app.route('/medicamentos/<int:id>/editar', methods=["GET", "POST"])
def editar_medicamento(id):
    if 'usuario_id' not in session or session['rol'] != 'medico':
        flash("Acceso denegado", "danger")
        return redirect(url_for('login_medico'))

    medicamento = consultas.obtener_medicamento_por_id(id)
    if request.method == "POST":
        nombre = request.form["nombre_medcmnto"]
        presentacion = request.form["presentacion"]
        descripcion = request.form["descrip_medcmnto"]

        consultas.actualizar_medicamento(id, nombre, presentacion, descripcion)
        flash("Medicamento actualizado correctamente", "success")
        return redirect(request.referrer)

    return render_template("medicamentos/formulario_editar.html", medicamento=medicamento)

'''@app.route('/medicamentos/<int:id>/eliminar')
def eliminar_medicamento(id):
    if 'usuario_id' not in session or session['rol'] != 'medico':
        flash("Acceso denegado", "danger")
        return redirect(url_for('login_medico'))

    consultas.eliminar_medicamento(id)
    flash("Medicamento eliminado", "info")
    return redirect(request.referrer)'''
    
@app.route('/medicamentos/<int:id>/eliminar')
def eliminar_medicamento(id):
    if 'usuario_id' not in session or session['rol'] != 'medico':
        flash("Acceso denegado", "danger")
        return redirect(url_for('login_medico'))

    try:
        consultas.eliminar_relaciones_medicamento(id)  # Primero elimina relaciones
        consultas.eliminar_medicamento(id)              # Luego elimina medicamento
        flash("Medicamento eliminado correctamente", "success")
    except Exception as e:
        flash(f"No se pudo eliminar el medicamento: {str(e)}", "danger")

    # Regresar a la receta actual
    id_diagnostico = request.args.get("id_diagnostico")
    return redirect(url_for('ver_medicamentos_diagnostico', id=id_diagnostico))
    

@app.route('/recetas/<int:id>/editar', methods=["GET", "POST"])
def editar_receta(id):
    if 'usuario_id' not in session or session['rol'] != 'medico':
        flash("Acceso denegado", "danger")
        return redirect(url_for('login_medico'))

    receta = consultas.obtener_receta_por_id(id)
    if request.method == "POST":
        indicaciones = request.form["indicaciones_receta"]
        consultas.actualizar_receta(id, indicaciones)
        flash("Receta actualizada correctamente", "success")
        return redirect(request.referrer)

    return render_template("recetas/formulario_editar.html", receta=receta)

@app.route('/recetas/<int:id>/eliminar')
def eliminar_receta(id):
    if 'usuario_id' not in session or session['rol'] != 'medico':
        flash("Acceso denegado", "danger")
        return redirect(url_for('login_medico'))

    consultas.eliminar_receta(id)
    flash("Receta eliminada", "info")
    return redirect(url_for('listar_diagnosticos'))
    

@app.route('/medicamentos')
def listar_medicamentos():
    if 'usuario_id' not in session or session['rol'] != 'medico':
        flash("Acceso denegado", "danger")
        return redirect(url_for('login_medico'))

    medicamentos = consultas.obtener_medicamentos_disponibles()
    return render_template("medicamentos/lista.html", medicamentos=medicamentos)

@app.route('/medicamentos/nuevo', methods=["GET", "POST"])
def crear_medicamento():
    if 'usuario_id' not in session or session['rol'] != 'medico':
        flash("Acceso denegado", "danger")
        return redirect(url_for('login_medico'))

    if request.method == "POST":
        nombre = request.form["nombre_medcmnto"]
        presentacion = request.form["presentacion"]
        descripcion = request.form["descrip_medcmnto"]
        consultas.insertar_medicamento(nombre, presentacion, descripcion)
        flash("Medicamento agregado", "success")
        return redirect(url_for('listar_medicamentos'))

    return render_template("medicamentos/formulario_nuevo.html")

@app.route('/recetas')
def listar_recetas():
    if 'usuario_id' not in session or session['rol'] != 'medico':
        flash("Acceso denegado", "danger")
        return redirect(url_for('login_medico'))

    recetas = consultas.obtener_recetas()  # Debes tener esta función en `consultas.py`
    return render_template("recetas/lista.html", recetas=recetas)



if __name__ == '__main__':
    print("Iniciando Flask en http://localhost:5000")
    app.run(debug=True)

