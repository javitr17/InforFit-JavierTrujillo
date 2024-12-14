# 📋 Descripción

El proyecto que he escogido consta de una aplicación web de una cadena de gimnasios llamada **InForFit**, surge en respuesta a la creciente demanda de digitalización en la industria del fitness, mostrándose como una plataforma intuitiva y con una estética algo diferente a lo que estamos acostumbrados en el sector.

Esta aplicación pretende **centralizar y automatizar las operaciones y tareas de recepcionistas u operarios del gimnasio**, ahorrando costos en gastos humanos y, sobre todo, en tiempo. Los usuarios podrán inscribirse en el gimnasio por sí mismos y gestionar todo lo referente a la suscripción y sus datos de forma sencilla.

Al registrarse en ella podrán disfrutar del acceso a las instalaciones del gimnasio por el tiempo que el plan de suscripción que hayan elegido les permita. Así como el acceso a las características para socios con las que cuenta la plataforma, entre ellas podemos diferenciar el acceso a información de interés, seguimiento del progreso a lo largo del tiempo o a la obtención de rutinas de entrenamiento, ya sea en casa o en el gimnasio, personalizada en función de ciertos parámetros como la duración del entrenamiento o el objetivo personal de ese usuario.

# ⚙️ Funcionamiento

## Página Principal

Al visitar la url de la aplicación web, nos topamos con la página principal de nuestro proyecto, en la cual podemos apreciar varios elementos como la barra de navegación en la parte superior, barra que se mantiene en varias páginas que veremos más adelante, en ella distinguimos el logo de la aplicación, enlaces a las distintas secciones de la plataforma, un botón que dirije al inicio de sesión/configuración del perfil y otro botón para el registro/cierre sesión. Se mostrará uno u otro en función de si el usuario está autenticado o no. 

Debajo de dicha barra de navegación podemos apreciar ciertos elementos visuales como fondos relacionados con el gimnasio, un panel con el detalle de un tipo de plan de suscripción al gimnasio o información sobre las ventajas de las funciones de la suscripción.

A continuación, si seguimos bajando en esta página principal, observamos otro panel horizontal, con imágenes de las distintas secciones de las que dispone la web, si se pulsan, al igual que en la barra de navegación, nos dirigen hacia ella.

Finalmente, en la parte inferior de la pantalla ubicamos el footer de la misma, el cual, al igual que la barra de navegación se mantiene en alguna de las páginas de nuestro proyecto (Ya que su implementación está realizada desde un template base del que extienden los demás templates). El contenido del mismo es meramente informativo y con un fin estético, a excepción de los logos de las redes sociales que si son pulsados si se abre una nueva ventana en el navegador, dirigiendo al usuario a dicha red social.

## Registro

El proceso de registro en la aplicación, viene dado por tres pantallas principales, en las que en cada una de ellas, manejamos los datos referentes al socio y a la suscripción que nos interesa almacenar. Estas tres pantallas tienen la misma estructura visual, que se conforma por el encabezado, que tendría una estética similar a la barra de navegación de la página principal pero eliminando los enlaces a las distintas secciones de la web y los botones y añadiendo el la parte derecha un indicador de la fase de registro en la que nos encontramos.

El desglose de dichas tres pantallas de registro es el siguiente:

### Registro > Plan

En la primera página del registro, dedicada a la selección del plan de suscripción, podremos ver un panel principal que nos permite escoger el plan de suscripción al gimnasio que más nos convenga, cuando hacemos clic en el plan deseado, observamos como aparecen los detalles de dicho plan en una sección secundaria ubicada en la derecha de la pantalla o abajo de del todo (la ubicación de la misma será en función de la resolución de pantalla del dispositivo con el que accedemos a la web).

Para continuar el proceso de registro debemos pulsar el botón de confirmar que aparecerá en el contenedor secundario.

### Registro > Datos Socio

En esta segunda página del proceso de registro, referente a los datos del socio que se necesitan saber para registrarlo, mantenemos la misma estructura de un contenedor principal y otro secundario. En el principal aparecen distintos formularios que el usuario debe rellenar sobre los datos personales, los datos domiciliarios y la contraseña con la que el usuario pretende acceder a la aplicación una vez esté registrado. Y en el secundario, se mantienen en todo momento los detalles del plan de suscripción seleccionado en la página anterior.

Para seguir avanzando en el registro se deberá hacer clic en el botón de continuar en la sección principal.

### Registro > Pago

Esta es la última página del registro, reservada al pago del usuario, en la acabamos con la misma estructura anterior. En el contenedor principal apreciamos un formulario con los detalles del pago. En cuanto al contenedor secundario, observamos que sigue conteniendo los datos del plan elegido y del total a pagar, y con un botón para realizar el pago, el cual está inicialmente deshabilitado, y solo se habilita cuando se introducen unos datos válidos en el formulario de los detalles del pago.

Para proceder con el pago de la inscripción y suscripción al gimnasio, se debe pulsar el botón para realizar el pago de la sección secundaria y la aplicación procesará el pago, mostrando un mensaje por pantalla en función del estado de la transacción realizada.

En el caso de que esta haya resultado exitosa, se muestran los datos de los cargos realizados y podremos volver a la página principal haciendo clic en un botón correspondiente.

En caso contrario, se muestra un mensaje de error en el pago y se da la posibilidad de volver a introducir los detalles del pago pulsando un botón dedicado para ello.





