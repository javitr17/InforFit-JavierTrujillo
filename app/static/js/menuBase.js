document.addEventListener("DOMContentLoaded", function () {
    const menu = document.querySelector('.indexMenu i');

    menu.addEventListener('click', function () {
        const body = document.querySelector('body');
        const hijosBody = body.children;
        const primerHijo = body.firstElementChild;
        const segundoHijo = primerHijo.nextElementSibling; // Selecciona el segundo hijo
        const botonInscripcion = document.querySelector('.cabeceraResponsive .navBoton');
        const contenedorMenu=document.querySelector('.indexMenu');
        const cabeceraResponsive=document.querySelector('.cabeceraResponsive');

        // Verificar si la clase bodyResponsive está presente
        if (body.classList.contains('bodyResponsive')) {
            console.log('contiene bodyResponsive');

            // Si la clase .bodyResponsive está presente, quitarla
            body.classList.remove('bodyResponsive');

            // Restaurar todos los elementos a display:block
            Array.from(hijosBody).forEach(hijoBody => {
                console.log('Restaurando hijo:', hijoBody);
                hijoBody.style.display = ''; // Elimina el estilo en línea para que vuelva a los valores por defecto
            });
             if (botonInscripcion) {
                botonInscripcion.style.display = ''; // Mostrar el botón
            }

             cabeceraResponsive.style.gridTemplateColumns='2fr 6fr 2fr'


        } else {
            console.log('no contiene bodyResponsive');

            // Si la clase .bodyResponsive no está, agregarla
            body.classList.add('bodyResponsive');


            // Ocultar todos los elementos excepto el primero
            Array.from(hijosBody).forEach(hijoBody => {
                if (hijoBody !== primerHijo && hijoBody !== segundoHijo) {
                    hijoBody.style.display = 'none'; // Ocultar
                }
                segundoHijo.style.display='block';

            });
             // Ocultar el botón de inscripción
            if (botonInscripcion) {
                botonInscripcion.style.display = 'none'; // Ocultar el botón
            }
            contenedorMenu.style.gridColumn='3/4'
            cabeceraResponsive.style.gridTemplateColumns='7fr 1fr 2fr'



        }
    });
});
