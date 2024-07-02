
CREATE TABLE ciudad(
    id_ciudad INT PRIMARY KEY,
    nombre_ciudad VARCHAR(30) NOT NULL
);
CREATE TABLE comuna(
    id_comuna INT PRIMARY KEY,
    nombre_comuna VARCHAR(30) NOT NULL,
    id_ciudad INT,
    Foreign Key (id_ciudad) REFERENCES ciudad(id_ciudad)
);
CREATE TABLE direccion(
    id_direccion INT PRIMARY KEY,
    numero INT NOT NULL,
    calle VARCHAR(30) NOT NULL,
    id_ciudad INT,
    id_comuna INT,
    Foreign Key (id_ciudad) REFERENCES ciudad(id_ciudad),
    Foreign Key (id_comuna) REFERENCES comuna(id_comuna)
);
CREATE TABLE usuario(
    id_usuario INT PRIMARY KEY,
    username VARCHAR(30) NOT NULL,
    contrasena VARCHAR(20)
);
CREATE TABLE administrador(
    id_admin INT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    id_usuario INT,
    Foreign Key (id_usuario) REFERENCES usuario(id_usuario)
);
CREATE TABLE cargo(
    id_cargo INT PRIMARY KEY,
    nombre_cargo VARCHAR(30) NOT NULL
);
CREATE TABLE departamento(
    id_departamento INT PRIMARY KEY,
    nombre_departamento VARCHAR(30) NOT NULL,
    id_cargo INT,
    Foreign Key (id_cargo) REFERENCES cargo(id_cargo)
);
CREATE TABLE area(
    id_area INT PRIMARY KEY,
    nombre_area VARCHAR(30) NOT NULL,
    id_departamento INT,
    Foreign Key (id_departamento) REFERENCES departamento(id_departamento)
);
CREATE TABLE empleado(
    id_empleado INT PRIMARY KEY,
    rut VARCHAR(11),
    nombres VARCHAR(30) NOT NULL,
    apellidos VARCHAR(30) NOT NULL,
    sexo VARCHAR(10) NOT NULL,
    telefono INT,
    fecha_ingreso date,
    fecha_nacimiento date,
    correo VARCHAR(30) NOT NULL,
    id_area INT,
    id_cargo INT,
    id_departamento INT,
    id_direccion INT,
    Foreign Key (id_area) REFERENCES area(id_area),
    Foreign Key (id_departamento) REFERENCES departamento(id_departamento),
    Foreign Key (id_cargo) REFERENCES cargo(id_cargo),
    Foreign Key (id_direccion) REFERENCES direccion(id_direccion)
);
CREATE TABLE contacto_emergencia(
    nombres VARCHAR(30) NOT NULL PRIMARY KEY,
    apellidos VARCHAR(30) NOT NULL,
    parentesco VARCHAR(20) NOT NULL,
    telefono int,
    id_empleado INT,
    Foreign Key (id_empleado) REFERENCES empleado(id_empleado)
);
CREATE TABLE carga_familiar(
    nombres VARCHAR(30) NOT NULL PRIMARY KEY,
    apellidos VARCHAR(30) NOT NULL,
    parentesco VARCHAR(20) NOT NULL,
    edad INT,
    sexo VARCHAR(10) NOT NULL,
    fecha_nacimiento date,
    id_empleado INT,
    Foreign Key (id_empleado) REFERENCES empleado(id_empleado)
);

CREATE SEQUENCE id_empleado;
CREATE SEQUENCE id_area;
CREATE SEQUENCE id_departamento;
CREATE SEQUENCE id_cargo;
CREATE SEQUENCE id_direccion;
CREATE SEQUENCE id_usuario;
CREATE SEQUENCE id_comuna;
CREATE SEQUENCE id_ciudad;
CREATE SEQUENCE id_admin;

ALTER TABLE area ADD CONSTRAINT unique_nombre_area UNIQUE (nombre_area);
ALTER TABLE departamento ADD CONSTRAINT unique_nombre_departamento UNIQUE (nombre_departamento);
ALTER TABLE cargo ADD CONSTRAINT unique_nombre_cargo UNIQUE (nombre_cargo);


INSERT INTO area (id_area, nombre_area) VALUES
(223,'Recursos Humanos'),
(224, 'Finanzas'),
(225, 'Tecnología'),
(226,'Marketing'),
(227, 'Ventas')
ON CONFLICT (nombre_area) DO NOTHING;

INSERT INTO departamento (id_departamento, nombre_departamento) VALUES
(112, 'Departamento A'),
(113, 'Departamento B'),
(114, 'Departamento C'),
(115, 'Departamento D'),
(116, 'Departamento E')
ON CONFLICT (nombre_departamento) DO NOTHING;

INSERT INTO cargo (id_cargo, nombre_cargo) VALUES
(332, 'Gerente'),
(333, 'Analista'),
(334, 'Desarrollador'),
(335, 'Contador'),
(336, 'Ejecutivo de ventas')
ON CONFLICT (nombre_cargo) DO NOTHING;