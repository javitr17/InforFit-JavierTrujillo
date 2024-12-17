document.addEventListener("DOMContentLoaded", function () {
    const menu = document.querySelector('.indexMenu i');

    menu.addEventListener('click', function () {
        const body = document.querySelector('body');
        const hijosBody = body.children;
        const primerHijo = body.firstElementChild;
        const segundoHijo = primerHijo.nextElementSibling; // Selecciona el segundo hijo
        const botonInscripcion = document.querySelector('.cabeceraResponsive .navBoton');
        const contenedorMenu = document.querySelector('.indexMenu');
        const cabeceraResponsive = document.querySelector('.cabeceraResponsive');

        // Verificar si la clase bodyResponsive está presente
        if (body.classList.contains('bodyResponsive')) {
            // Si la clase .bodyResponsive está presente, quitarla
            body.classList.remove('bodyResponsive');

            // Restaurar todos los elementos a display:block
            Array.from(hijosBody).forEach(hijoBody => {
                hijoBody.style.display = ''; // Elimina el estilo en línea para que vuelva a los valores por defecto
            });
            if (botonInscripcion) {
                botonInscripcion.style.display = ''; // Mostrar el botón
            }

        } else {
            // Si la clase .bodyResponsive no está, agregarla
            body.classList.add('bodyResponsive');

            // Ocultar todos los elementos excepto el primero
            Array.from(hijosBody).forEach(hijoBody => {
                if (hijoBody !== primerHijo && hijoBody !== segundoHijo) {
                    hijoBody.style.display = 'none'; // Ocultar
                }
                segundoHijo.style.display = 'block';
            });
            // Ocultar el botón de inscripción
            if (botonInscripcion) {
                botonInscripcion.style.display = 'none'; // Ocultar el botón
            }
            contenedorMenu.style.gridColumn = '3/4';
        }
    });

    // Nueva funcionalidad para revertir los cambios si la resolución supera 1100px
    window.addEventListener('resize', function () {
        const body = document.querySelector('body');
        const hijosBody = body.children;
        const botonInscripcion = document.querySelector('.cabeceraResponsive .navBoton');
        const cabeceraResponsive = document.querySelector('.cabeceraResponsive');

        // Si el ancho de la pantalla supera los 1100px
        if (window.innerWidth > 1100) {
            // Eliminar la clase bodyResponsive
            body.classList.remove('bodyResponsive');

            // Restaurar todos los elementos a display:block
            Array.from(hijosBody).forEach(hijoBody => {
                hijoBody.style.display = ''; // Elimina el estilo en línea para que vuelva a los valores por defecto
            });

            // Mostrar el botón de inscripción
            if (botonInscripcion) {
                botonInscripcion.style.display = ''; // Mostrar el botón
            }

            // Restaurar los estilos de la cabeceraResponsive
        }
    });
});
