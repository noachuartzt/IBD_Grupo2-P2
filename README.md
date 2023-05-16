# IBD_Grupo2-P2: *Infraestructura UPM para publicaciones científicas*

<i><small>**Alumnos:** Noa Chu, Che Cui, Carlota Medrano, Alejandro Pequeño<br>Última actualización: 2023-05-01</small></i></div>

Este repositorio contiene los archivos necesarios para crear una infraestructura basada en Docker que soporte la gestión enriquecida de publicaciones científicas en formato PDF para el archivo digital de la Universidad Politécnica de Madrid (UPM) que actualmente gestiona los trabajos fin de grado, fin de tesis y tesis doctorales de los alumnos de la Universidad pero se pide una nueva versión de la plataforma para poder gestionar también las publicaciones científicas de sus investigadores, lo cual es un desafío porque el volumen de datos que se ha de soportar es mucho mayor que con los TFGs, TFMs, y tesis. En cuanto a la parte de la gestión enriquecida, se quieren ofrecer datos estadísticos sobre los autores de las publicaciones, sus colaboraciones, las áreas de investigación, y además facilitar la exploración de su contenido y la búsqueda avanzada desde su propio portal web. La infraestructura se basa en **Apache Hadoop** como sistema de almacenamiento distribuido.

Todos los archivos han sido creados y modificados por los miembros del **Grupo 2** de la asignatura de IBD de ***Ciencia de Datos e Inteligencia Artificial de la Universidad Politécnica de Madrid*** (*UPM*): Noa Chu, Che Cui, Carlota Medrano, Alejandro Pequeño.
****

## Requisitos

Para la realización de la práctica serán necesarios los siguientes servicios:

- Tener instalado **GIT** en su máquina. Si no, puedes descargarlo desde [aquí](https://git-scm.com/downloads).
- Tener instalado **Docker** en su máquina. Si no, puedes descargarlo desde [aquí](https://www.docker.com/products/docker-desktop/).

***
## Dudas para el Profesor

1. Archivo `corpus.txt` y lista de DOIs con respecto a los doccumentos proporcionados

***

## Pasos

### 1. Clonado del repositorio de GitHub

**1.1** Dirígete al buscador de Windows y busca `cmd` o `powershell` para abrir la terminal de tu ordenador.

***NOTA***: si se realiza desde MAC OS teclee `cmd`+`espace` para buscar y abrir la terminal de tu ordenador.

**1.2** Una vez en la terminal, sitúate en la carpeta donde quieres clonar el repositorio, puedes hacerlo usando el siguiente comando: 

```
cd <path>
```

***NOTA***: Si su ruta tiene algún espacio o carácter especial, es necesario poner la ruta entre comillas dobles:

```
cd "<path>"
```

**1.3** Una vez en la carpeta deseada, ejecuta el siguiente comando para clonar el repositorio:

```
git clone "https://github.com/noachuartzt/IBD_Grupo2-P2"
```

Para este paso, se ha proporcionado el HTTPS del repositorio de GitHub. Esta URL se puede encontrar también en la página principal del [repositorio](https://github.com/noachuartzt/IBD_Grupo2-P2), en la parte superior derecha, pulsando en el botón verde "Code". En la ventana que se abre, selecciona la opción "HTTPS" y copia el link. También puedes obtenerlo en el archivo [Repository.md](Repository.md) del repositorio de GitHub.

***NOTA***: Pero también se podría realizar mediante una llave SSH. Para ello, siga el fichero [MAC_guide](MAC_guide.md)

**1.4** Una vez clonado el repositorio, accede a la carpeta clonada:

```
cd IBD_Grupo2-P2 
```

Esto se hace, pues, queremos ejecutar los archivos de la carpeta para la creación de la imagen a través del terminal.

### 2. Publications
### 3. Static Data
### 4. Dynamic Data

### 5. Simple Queries
#### 5.2 Texts
Este paso devuelve un listado ordenado de párrafos, junto con el título del artículo al que pertenecen, que contienen un término específico. La relevancia viene determinada por el tamaño del párrafo y la frecuencia del término, por lo cual, cuando un término aparece la misma cantidad de veces en dos textos, el texto de menor tamaño aparece primero con un score mayor.

Para realizar esta tarea, hemos utilizado el motor de búsqueda Elasticsearch por su eficiencia en cuanto al indexado. Primero, hay que conectar al contenedor "elasticsearch". Para ello, vamos a utilizar el cliente de Python para Elasicsearch. Accedemos al `texts.ipynb` que se encuentra en el directorio `4-simple_queries/`.

El archivo `texts.ipynb` nos propociona los códigos necesarios para acceder al cluster autogestionado de Elasticsearch via HTTP por el puerto 9200 del localhost. Una vez conectado, se puede indexar datos, solo en caso de que es la primera vez que levantas el contenedor o quieres añadir nuevos datos. Sin embargo, en caso contrario no es necesario ejercutarlo. A continuación, está la query necesaria para consultar por el término clave que quieras. Al ejecutar la celda te pedirá como input una palabra clave y como resultado te devolverá un dataframe ordenado por score(relevancia)  de los párrafos y el título del artículo.

Por último, en el caso de que quieras eliminar un índice, también es posible con la ejecución de la última celda del ipynb. Sin embargo, los índices borrados no son recuperables.

### 6. Complex Queries
