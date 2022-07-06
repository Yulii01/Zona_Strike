# Zona_Strike
Proyecto de tesis para la obtención de licenciado en Ciencias de la Computacion

Aplicación de métodos de procesamientos de imágenes para la detección de un objeto en movimiento a alta velocidad.

Introducción:
Con el desarrollo de la tecnología y la automatización de las tareas,es cada vez mayor ver como se va haciendo uso de esta en casi todas las ramas de la sociedad. El mundo deportivo es una de las esfera donde el uso de aplicaciones  y softwares se va haciendo mayor, tratando de aplicar mas estrictamente las reglas. La propuesta de este trabajo es la detección de la trayectoria de la bola de baseball después de ser lanzada por el pitcher. El objetivo viene complementado con la creacion de la llamada zona de strike de cada bateador para finalmente determinar si el lanzamiento cae en zona 
reglamentaria. Se trabaja con un video de un lanzamiento realizado en la serie nacional recién terminada. El proceso del trabajo muestra algunos procesamientos realizados a los frame para lograr tener una detección mas acercada y real .

Desarrollo:
	Un video no es mas que una serie de frame consecutivos, y sobre estas imágenes se realizan los procesos de mejora. El primer procedimiento utilizado fue la aplicación de métodos de sustracción de fondos .
	La sustracción de fondo es una técnica ampliamente utilizada para detectar objetos en movimiento a partir de cámaras estáticas. El proceso de sustracción es también denominada extracción de primer plano o de objetos en movimiento (foreground extraction), y consiste en una serie de m´etodos que permiten distinguir entre zonas de fondo o estaticas (background), y zonas dinamicas que se corresponden con el primer plano (foreground). Durante el proceso investigativo se probaron varios métodos como el algoritmo Sigma-Delta,Frame Difference, Vibe y Mixture Of Gaussian. Para el desarrollo se utilizo el el MOG, implementado en la biblioteca de open-cv de python. El resultado es una reducción importante de los valores significativos de la imagen para minimizar el proceso de detección centrándose solo en los objetos resaltados los cuales son los potenciales objetos en movimiento.













Como se puede apreciar la imagen cambia los pixeles resaltando solo aquellos de importancia par la investigacion.
