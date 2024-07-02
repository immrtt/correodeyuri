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
