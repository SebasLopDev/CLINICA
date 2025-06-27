CREATE TABLE Sala (
    id_sala INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    tipo VARCHAR(50),
    estado ENUM('disponible','ocupado','no_disponible') NOT NULL
);

CREATE TABLE Historial_Medico (
    id_historial_medico INT PRIMARY KEY AUTO_INCREMENT,
    antecedentes_historial VARCHAR(100),
    alergias_historial VARCHAR(100),
    enfermedades_cronicas VARCHAR(100)
);

CREATE TABLE Paciente (
    id_paciente INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    dni VARCHAR(15) UNIQUE NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    sexo CHAR(1) NOT NULL CHECK (sexo IN ('M', 'F')),
    telefono VARCHAR(20),
    direccion VARCHAR(200),
    email VARCHAR(100) UNIQUE NOT NULL,
    id_historial_medico INT UNIQUE,
    CONSTRAINT fk_paciente_historial FOREIGN KEY(id_historial_medico) REFERENCES Historial_Medico(id_historial_medico)
);

CREATE TABLE Medico (
    id_medico INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    estado ENUM('activo', 'inactivo') NOT NULL
);

CREATE TABLE Cita (
    id_cita INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATE NOT NULL,
    hora VARCHAR(10) NOT NULL,
    estado ENUM('disponible','ocupado','no_disponible') NOT NULL,
    motivo VARCHAR(255) NOT NULL,
    id_medico INT NOT NULL,
    id_paciente INT NOT NULL,
    id_sala INT, 
    FOREIGN KEY (id_medico) REFERENCES Medico(id_medico),
    FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente),
    FOREIGN KEY (id_sala) REFERENCES Sala(id_sala)
    
);

CREATE TABLE Examen_Medico (
    id_examen INT PRIMARY KEY AUTO_INCREMENT,
    tipo_exmen ENUM('SANGRE','RAYOSX','ECOGRAFIA','ORINA') NOT NULL,
    fecha_exmen DATE NOT NULL,
    resultado_exmen VARCHAR(180) NOT NULL,
    id_cita INT NOT NULL,
    FOREIGN KEY (id_cita) REFERENCES Cita(id_cita)
);

CREATE TABLE Medicamento (
    id_medicamento INT PRIMARY KEY AUTO_INCREMENT,
    nombre_medcmnto VARCHAR(100) NOT NULL,
    presentacion ENUM('CAPSULA','JARABE','INYECTABLE','MASTICABLE'),
    descrip_medcmnto VARCHAR(200)
);

CREATE TABLE Receta (
    id_receta INT PRIMARY KEY AUTO_INCREMENT,
    indicaciones_receta VARCHAR(255) NOT NULL,
    id_cita INT NOT NULL,
    FOREIGN KEY (id_cita) REFERENCES Cita(id_cita)
);

CREATE TABLE Receta_Medicamento (
    id_receta_medicamento INT PRIMARY KEY AUTO_INCREMENT,
    indicaciones_medcmnto VARCHAR(255),
    id_medicamento INT NOT NULL,
    id_receta INT NOT NULL,
    FOREIGN KEY (id_medicamento) REFERENCES Medicamento(id_medicamento),
    FOREIGN KEY (id_receta) REFERENCES Receta(id_receta)
);

CREATE TABLE Enfermedad (
    id_enfermedad INT PRIMARY KEY AUTO_INCREMENT,
    nombre_enfrmdad VARCHAR(100) NOT NULL,
    descrip_enfrmdad VARCHAR(255)
);

CREATE TABLE Diagnostico (
    id_diagnostico INT PRIMARY KEY AUTO_INCREMENT,
    descripcion_dgnstico VARCHAR(255),
    id_enfermedad INT NOT NULL,
    id_cita INT NOT NULL,
    FOREIGN KEY (id_enfermedad) REFERENCES Enfermedad(id_enfermedad),
    FOREIGN KEY (id_cita) REFERENCES Cita(id_cita)
);

CREATE TABLE Tratamiento (
    id_tratamiento INT PRIMARY KEY AUTO_INCREMENT,
    descrip_trtmnto VARCHAR(255),
    duracion_trtmnto INT,
    id_diagnostico INT NOT NULL,
    FOREIGN KEY (id_diagnostico) REFERENCES Diagnostico(id_diagnostico)
);

CREATE TABLE Especialidad (
    id_especialidad INT PRIMARY KEY AUTO_INCREMENT,
    nombre_espclidad VARCHAR(100) NOT NULL,
    descripcion_espclidad VARCHAR(200)
);

CREATE TABLE Rol (
    id_rol INT PRIMARY KEY AUTO_INCREMENT,
    nombre_rol ENUM('PACIENTE','MEDICO','ADMIN') NOT NULL
);

CREATE TABLE Usuario_Sistema (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre_user VARCHAR(50) NOT NULL,
    contrasena_user VARCHAR(100),
    email_user VARCHAR(100) UNIQUE,
    id_rol INT NOT NULL,
    id_paciente INT ,
    id_medico INT,    
    FOREIGN KEY (id_rol) REFERENCES Rol(id_rol),
    FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente),
    FOREIGN KEY (id_medico) REFERENCES Medico(id_medico)

);

CREATE TABLE Factura (
    id_factura INT PRIMARY KEY AUTO_INCREMENT,
    monto_total DECIMAL(10,2) NOT NULL,
    estado ENUM('CANCELADO', 'PAGADO', 'PENDIENTE'),
    metodo_facturacion VARCHAR(100),
    id_usuario INT NOT NULL,
    id_paciente INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuario_Sistema(id_usuario),
    FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente)
);

CREATE TABLE Pago (
    id_pago INT PRIMARY KEY AUTO_INCREMENT,
    monto DECIMAL(10,2) NOT NULL,
    metodo_pago ENUM('EFECTIVO','TARJETA') NOT NULL,
    fecha_pago DATE NOT NULL,
    id_cita INT NOT NULL,
    FOREIGN KEY (id_cita) REFERENCES Cita(id_cita)
);

CREATE TABLE Turno_Medico (
    id_turno INT PRIMARY KEY AUTO_INCREMENT,
    dia_semana VARCHAR(20) NOT NULL,
    hora_inicio VARCHAR(10) NOT NULL,
    hora_fin VARCHAR(10) NOT NULL,
    id_medico INT NOT NULL,
    FOREIGN KEY (id_medico) REFERENCES Medico(id_medico)
);

