class Departamento{
    constructor(id, nombre){
        this._id = id;
        this._nombre = nombre;
    }

    get getId(){
        return this._id;
    }

    get getNombre(){
        return this._nombre;
    }

    setDepartamento(departamento){
        this._departamento = departamento;
    }
}

class Area{
    constructor(id, nombre){
        this._id = id;
        this._nombre = nombre;
    }

    get getId(){
        return this._id;
    }
    get getNombre(){
        return this._nombre;
    }

    setArea(area){
        this._area = area;
    }
}

class Cargafamiliar{
    constructor(rut, nombre, apellido,  
        sexo, fechanacimiento, parentesco){
        this._rut = rut;
        this._nombre = nombre;
        this._apellido = apellido;
        this._sexo = sexo;
        this._fechanacimiento = fechanacimiento;
        this._parentesco = parentesco;
    }
    
    get getRut(){
        return this._rut;
    }
    get getNombre(){
        return this._nombre;
    }
    get getApellido(){
        return this._apellido;
    }
    get getSexo(){
        return this._sexo;
    }
    get getFechanacimiento(){
        return this._fechanacimiento;
    }
    get getParentesco(){
        return this._parentesco;
    }
    setCargafamiliar(cargafamiliar){
        
    }
}


class Trabajador {
    constructor(id, rut, nombres, apellidos, sexo,
        direccion, cargo, area, departamento, telefono, correo, fechaingreso) {
        this.id = id
        this.rut = rut;
        this.nombres = nombres;
        this.apellidos = apellidos;
        this.sexo = sexo;
        this.direccion = direccion;
        this.cargo = cargo;
        this.area = area;
        this.departamento = departamento;
        this.telefono = telefono;
        this.correo = correo;
        this.fechaingreso = fechaingreso;
    }
}

let usuarios = [];
let contadorId = 1;

//AGREGAR TRABAJADOR >>>>>>>>>>>>
let addTrab = function () {
    let rt = document.getElementById("t-rut").value;
    let noms = document.getElementById("t-nombres").value;
    let aps = document.getElementById("t-apellidos").value;
    let sex = document.getElementById("t-sexo").value;
    let dire = document.getElementById("t-direccion").value;
    let crg = document.getElementById("t-cargo").value;
    let ar = document.getElementById("t-area").value;
    let dpto = document.getElementById("t-depto").value;
    let tel = parseFloat(document.getElementById("t-telefono").value);
    let crro = parseFloat(document.getElementById("t-correo").value);
    let fi = parseFloat(document.getElementById("t-fechaingreso").value);

    let t = new Trabajador(contadorId, rt, noms, aps, sex, ed, dire, crg, ar, dpto, tel, crro, fi);
    contadorId++;
    usuarios.push(t);

    fetch('/add_trabajador', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(t)
    })
        .then(response => response.json())
        .then(data => {
            console.log(`Respuesta del servidor: `, data);
        })
        .catch(err => {
            console.error(`Error: ${err}`);
        })

    alert("Agregado.");
    console.log(usuarios);
}



//ENCONTRAR TRABAJADOR >>>>>>>>>>>>>>>>
let findTrab = function () {
    let r = document.getElementById("b-rut").value;
    let p = usuarios.find(us => us.rut === r);
    if (p != undefined) {
        alert("Empleado encontrado");
        document.getElementById("r-id").innerHTML = "<b>ID: </b>" + contadorId + " ";
        document.getElementById("r-rut").innerHTML = "<b>Rut: </b>" + p.rut;
        document.getElementById("r-nombres").innerHTML = "<b>Nombres: </b>" + p.nombres + " " + p.apellidos;
        {/* document.getElementById("r-sexo").innerHTML = "<b>Sexo: </b>" + t.getSexo + " "; */ }
        document.getElementById("r-edad").innerHTML = "<b>Edad: </b>" + p.edad + " años";
        {/* document.getElementById("r-direccion").innerHTML = "<b>Dirección: </b>" + t.getDireccion + " "; */ }
        {/* document.getElementById("r-telefono").innerHTML = "<b>Telefono: </b>" + t.getTelefono + " "; */ }
        {/* document.getElementById("r-correo").innerHTML = "<b>Correo: </b>" + t.getCorreo + " "; */ }
        document.getElementById("r-cargo").innerHTML = "<b>Cargo: </b>" + p.cargo + " ";
        document.getElementById("r-departamento").innerHTML = "<b>Departamento: </b>" + p.departamento + " ";
        document.getElementById("r-area").innerHTML = "<b>Area: </b>" + p.area + " ";

    } else {
        alert("Persona no encontrada");
    }


}



//VALIDAR CONTRASEÑA >>>>>>>>>

document.getElementById("formulario").addEventListener("submit", function (event) {
    event.preventDefault(); // Evitar que el formulario se envíe automáticamente

    var contrasena = document.getElementById("contrasena").value;
    var resultado = validarContrasena(contrasena);

    var mensaje = document.getElementById("mensaje");
    if (resultado === true) {
        mensaje.textContent = "La contraseña es válida.";
        mensaje.style.color = "green";
    } else {
        mensaje.textContent = "La contraseña no es válida: " + resultado;
        mensaje.style.color = "red";
    }
});

function validarContrasena(contrasena) {
    // Definir las reglas de validación utilizando expresiones regulares
    var regexLongitud = /.{8,}/; // La contraseña debe tener al menos 8 caracteres
    var regexMayuscula = /[A-Z]/; // La contraseña debe contener al menos una letra mayúscula
    var regexMinuscula = /[a-z]/; // La contraseña debe contener al menos una letra minúscula
    var regexNumero = /\d/; // La contraseña debe contener al menos un número

    // Verificar si la contraseña cumple con todas las reglas
    if (!regexLongitud.test(contrasena)) {
        return "La contraseña debe tener al menos 8 caracteres.";
    }
    if (!regexMayuscula.test(contrasena)) {
        return "La contraseña debe contener al menos una letra mayúscula.";
    }
    if (!regexMinuscula.test(contrasena)) {
        return "La contraseña debe contener al menos una letra minúscula.";
    }
    if (!regexNumero.test(contrasena)) {
        return "La contraseña debe contener al menos un número.";
    }

    // Si la contraseña pasa todas las validaciones, devolver verdadero
    return true;
}

// agregar otra carga familiar
function agregarCargaFamiliar() {
    var cargaFamiliarOriginal = document.querySelector('.carga-familiar');
    var nuevaCargaFamiliar = cargaFamiliarOriginal.cloneNode(true);
    document.getElementById('cargas-familiares').appendChild(nuevaCargaFamiliar);
  }


  // eliminar empleado
  function eliminarEmpleado(rut) {
    if (confirm('¿Estás seguro de que deseas eliminar este empleado?')) {
        fetch(`/eliminar_empleado/${rut}`, {
            method: 'DELETE'
        }).then(response => {
            if (response.ok) {
                alert('Empleado eliminado exitosamente.');
                window.location.href = '/search';
            } else {
                alert('Error al eliminar el empleado.');
            }
        }).catch(error => {
            alert('Error al eliminar el empleado.');
            console.error('Error:', error);
        });
    }
}


