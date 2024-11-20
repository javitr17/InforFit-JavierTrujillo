document.addEventListener("DOMContentLoaded", function() {
    const planSections = document.querySelectorAll('.registroPlanSeccion');
    const botonConfirmar = document.querySelector('.registroBoton a');

    // Deshabilitamos el botón al cargar la página
    botonConfirmar.setAttribute("disabled", true);

    planSections.forEach(plan => {
        plan.addEventListener('click', function() {
            // Limpiar el borde de todos los elementos `.registroPlan`
            document.querySelectorAll('.registroPlan').forEach(elemento => {
                elemento.style.border = "none";  // Elimina el borde
            });
            //recuperación del html del nombre del contrato
            let contrato = plan.querySelector('.registroPlanTitulo').textContent;
            contrato = contrato.charAt(0).toUpperCase() + contrato.slice(1).toLowerCase();

            //deducimos el valor de duracion y el precio en funcion del nombre del contrato
            if (contrato=='Anual'){
                duracion='12 meses'
                renovacion='tras 12 meses indefinidamente'
                precio='24.99€'

            }
            if(contrato=='Mensual'){
                duracion='1 mes'
                renovacion='tras 1 mes indefinidamente'
                precio='38.99€'

            }
            if(contrato=='Semestral'){
                duracion='6 meses'
                renovacion='tras 6 meses indefinidamente'
                precio='32.99€'


            }

            //introducimos en el html el valor de contrato
            document.querySelectorAll('.registroTexto')[0].textContent= 'Contrato';
            document.querySelectorAll('.registroValor')[0].textContent = contrato;



            //introducimos en el html el valor de duracion y estilos
            document.querySelectorAll('.registroTexto')[1].textContent= 'Duración:';
            const duracionContrato=document.querySelectorAll('.registroValor')[1]
            duracionContrato.textContent = duracion;
            const duracionContratoAñadirEstilos=duracionContrato.closest('.registroPlanDetalle')


            //introducimos en el html el precio de inscripción
            document.querySelectorAll('.registroTexto')[2].textContent= 'Cuota de inscripción:';
            document.querySelectorAll('.registroValor')[2].textContent = '15.00€';

             //introducimos en el html el plazo de cancelación
            document.querySelectorAll('.registroTexto')[3].textContent= 'Renovación:';
            document.querySelectorAll('.registroValor')[3].textContent = renovacion;

            //introducimos en el html el plazo de cancelación
            document.querySelectorAll('.registroTexto')[4].textContent= 'Recisión:';
            document.querySelectorAll('.registroValor')[4].textContent = '14 días antes del fin del contrato';
            //introducimos en el html el precio del cotrato
            document.querySelector('.registroCuotaMensualTexto').textContent= 'CUOTA MENSUAL';
            document.querySelector('.registroCuotMensualValor').textContent = precio;

            //cambiar el color de fondo del botón
            document.querySelector('.registroBoton a').style.cssText='background-color: #FFCC00;';
            document.querySelector('.registroSeccionDer1').style.height='42%'

            //poner borde de seccion seleccionada en amarillo
            const ponerBordeAmarillo = plan.closest('.registroPlan');
            ponerBordeAmarillo.style.border = "5px solid #FFCC00";
            //habilitamos el contenedor
            document.querySelector('.registroPlanDetalles').style.display='block'
            //añadimos un parametro a la url del boton para pasar el contenedor que se selecciona a
            //la vista del siguiente template
            document.querySelector('.registroBoton a').href = '/InForFit/signUpDatos?contrato=' + encodeURIComponent(contrato);
            console.log(document.querySelector('.registroBoton a'))

            // Habilitamos el botón de confirmación cuando se selecciona un plan
            botonConfirmar.removeAttribute("disabled");




        });
    });
});
