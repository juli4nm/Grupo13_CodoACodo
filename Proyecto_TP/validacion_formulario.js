// --------------------------------------------------------
// Se define una función llamada validarEnviar, que se 
// ejecuta cuando se presione "Enviar" en el formulario.
// --------------------------------------------------------
function validarEnviar() {
    // Validar el campo de nombre
    if (document.fvalida.nombre.value.length <= 3) {
        alert("Tiene que escribir su nombre");
        document.fvalida.nombre.focus();
        return;
    }
    // Validar el campo de Apellido
    if (document.fvalida.Apellido.value.length <= 2) {
        alert("Tiene que escribir su Apellido");
        document.fvalida.Apellido.focus();
        return;
    }

    // Validar DNI //

    let dni = document.fvalida.dni.value;

    dni = validarEntero(dni);
    document.fvalida.dni.value = dni;

    if (dni == "") {
        alert("Tiene que introducir un numero de 8 digitos.");
        document.fvalida.dni.focus();
        return;
    } else {
        if (dni < 1000000 > 99999999) {
            alert("El numero de DNI debe tener 8 digitos.");
            document.fvalida.dni.focus();
            return;
        }
    }

    // Validar la cantidad de huespedes. Debe ser un entero mayor que 1.
    let Hus = document.fvalida.Hus.value;

    Hus = validarEntero(Hus);


    if (Hus == "") {
        alert("Tiene que introducir un número entero.");
        document.fvalida.Hus.focus();
        return;
    } else {
        if (Hus < 1) {
            alert("Debe ser mayor de 1.");
            document.fvalida.Hus.focus();
            return;
        }
    }

    // Si todas las validaciones pasan, se envía el formulario.
    alert("Muchas gracias por enviar el formulario");
    document.fvalida.submit();
}


// --------------------------------------------------------
// validarEntero toma un valor como argumento. Esta función
// intenta convertir el valor a un número entero usando 
// parseInt. Si la conversión tiene éxito, devuelve el valor
// como número; de lo contrario, devuelve una cadena vacía.
// --------------------------------------------------------
function validarEntero(valor) {
    // Intentar convertir a entero.
    // Si era un entero no le afecta, si no lo era, lo intenta convertir.
    valor = parseInt(valor);

    // Comprobar si es un valor numérico
    if (isNaN(valor)) {
        // En caso de no ser un número, devuelve una cadena vacía
        return "";
    } else {
        // En caso de ser un número, devuelve el valor
        return valor;
    }
}