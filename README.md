<center>
<h1> Infraestructura UPM para publicaciones científicas </h1>
<h2> IBD_Grupo2-P2</h2>
</center>
<i><small>**Alumnos:** Noa Chu, Che Cui, Carlota Medrano, Alejandro Pequeño<br>Última actualización: 2023-05-01</small></i></div>

Este repositorio contiene los archivos necesarios para crear una infraestructura basada en Docker que soporte la gestión enriquecida de publicaciones científicas en formato PDF para el archivo digital de la Universidad Politécnica de Madrid (UPM) que actualmente gestiona los trabajos fin de grado, fin de tesis y tesis doctorales de los alumnos de la Universidad pero se pide una nueva versión de la plataforma para poder gestionar también las publicaciones científicas de sus investigadores, lo cual es un desafío porque el volumen de datos que se ha de soportar es mucho mayor que con los TFGs, TFMs, y tesis. En cuanto a la parte de la gestión enriquecida, se quieren ofrecer datos estadísticos sobre los autores de las publicaciones, sus colaboraciones, las áreas de investigación, y además facilitar la exploración de su contenido y la búsqueda avanzada desde su propio portal web.

El siguiente repositorio está dividido en 5 apartados (*carpetas*):
- **(1-publications)**: contiene los archivos necesarios para la conversión de los documentos PDF a `json` a partir de una lista de DOIs.
- **2-static_data**: contiene los archivos necesarios para la generación de dos archivos `csv` que contienen información estática sobre los documentos.
- **3-dynamic_data**: contiene los archivos necesarios para la generación de un archivo `csv` que contienen el número de aparicion de un término en concreto.
- **4-simple_queries**: contiene los archivos necesarios para realizar consultas de listado mediante **Neo4j** y **Elasticsearch**.
- **5-advanced_queries**: contiene los archivos necesarios para realizar consultas avanzadas mediante **Neo4j** y **Spark**.
- **docker**: contiene los archivos necesarios para la creación de la infraestructura basada en **Docker**.

Todos los archivos han sido creados y modificados por los miembros del **Grupo 2** de la asignatura de IBD de ***Ciencia de Datos e Inteligencia Artificial de la Universidad Politécnica de Madrid*** (*UPM*): Noa Chu, Che Cui, Carlota Medrano, Alejandro Pequeño.
****

<h2> Requisitos</h2>

Para la realización de la práctica serán necesarios los siguientes servicios:

- Tener instalado **GIT** en su máquina. Si no, puedes descargarlo desde [aquí](https://git-scm.com/downloads).
- Tener instalado **Docker** en su máquina. Si no, puedes descargarlo desde [aquí](https://www.docker.com/products/docker-desktop/).

***

<h2> Pasos </h2>

## 0. Clonado del repositorio de GitHub

**0.1** Dirígete al buscador de Windows y busca `cmd` o `powershell` para abrir la terminal de tu ordenador.

***NOTA***: si se realiza desde MAC OS teclee `cmd`+`espace` para buscar y abrir la terminal de tu ordenador.

**0.2** Una vez en la terminal, sitúate en la carpeta donde quieres clonar el repositorio, puedes hacerlo usando el siguiente comando: 

```
cd <path>
```

***NOTA***: Si su ruta tiene algún espacio o carácter especial, es necesario poner la ruta entre comillas dobles:

```
cd "<path>"
```

**0.3** Una vez en la carpeta deseada, ejecuta el siguiente comando para clonar el repositorio:

```
git clone "https://github.com/noachuartzt/IBD_Grupo2-P2"
```

Para este paso, se ha proporcionado el HTTPS del repositorio de GitHub. Esta URL se puede encontrar también en la página principal del [repositorio](https://github.com/noachuartzt/IBD_Grupo2-P2), en la parte superior derecha, pulsando en el botón verde "Code". En la ventana que se abre, selecciona la opción "HTTPS" y copia el link. También puedes obtenerlo en el archivo [Repository.md](Repository.md) del repositorio de GitHub.

***NOTA***: Pero también se podría realizar mediante una llave SSH. Para ello, siga el fichero [MAC_guide](MAC_guide.md)

**0.4** Una vez clonado el repositorio, accede a la carpeta clonada:

```
cd IBD_Grupo2-P2 
```

Esto se hace, pues, queremos ejecutar los archivos de la carpeta para la creación de la imagen a través del terminal.

## 1. Publications

En este apartado disponemos de **2 carpetas y 3 ficheros**:
- [json](/json): carpeta que contiene por cada DOI existente en [Semantic Web Scholar API](https://api.semanticscholar.org/), un archivo `json` con la meta-información del documento.
- [csv](/csv): careta que contiene un archivo `csv` con la meta-información de los documentos parseada y estructurada a partir de los archivos `json`.
- [corpus.txt](/corpus.txt): fichero que contiene una lista de DOIs de los documentos que se quieren parsear.
- [parse.py](/parse.py): fichero que contiene las funciones necesarias para parsear los archivos `json` y generar el archivo `csv`.
- [test.ipynb](/test.ipynb): fichero que contiene el código necesario para ejecutar el (parse.py)[/parse.py] y generar los archivos previamente mencionados.

### Instrucciones

1. Dirígete a la carpeta `1-publications` del repositorio clonado y abre el **jupyter-notebook** `test.ipynb` (*no hace falta hacerlo desde la terminal*):
2. Una vez abierto, **vscode** o culalquier otro editor de texto, ejecuta todas las celdas del notebook.

***NOTA 1***: Dicho fichero, importa de [parse.py](/parse.py) las funciones necesarias `doi_to_json` y `json_to_csv` para parsear la lista de DOIs a los archivos `json` y generar el archivo `csv` respectivamente. No obstante, antes de generar dichos archivos, comprueba si las carpetas [json](/json) y [csv](/csv) existen, si no es así, las crea. Una vez comprobado, ejecuta las funciones mencionadas anteriormente.

***NOTA 2***: El archivo generado en [csv/output](/csv/output.csv) es el que se utilizará en el siguiente apartado, [2-static_data](/2-static_data).


## 2. Static Data

En este apartado, disponemos de 2 ficheros `csv`:
- [authors.csv](/2-static_data/authors.csv): fichero que contiene el número de publicaciones por autor. (*author, puublications*)
- [documents.csv](/2-static_data/documents.csv): fichero que contiene la meta-información de los documentos. (*file_name, title, num_pages, creation_date, modification_date*)

Los archivos mencionados anteriormente, se han generado mediante el [parse.py](1-publications/parse.py) del apartado anterior, en la función `json_to_csv`.


## 3. Dynamic Data

En este apartado se pretende generar: 

- **Keywords.csv**: contiene el número de apariciones de un término concreto (e.g. ‘virus’), o cualquiera de sus sinónimos en inglés (e.g. ‘infection’, ‘microbe’..), en el corpus
    -Columnas: ‘word’ y ‘frequency’

Para ello, hemos creado un MapReduce. Es un único programa guardado con dos distintas extensiones:
- [keywordsCounter.ipynb](/3-dynamic_data/keywordsCounter.ipynb): se trata de un notebook de **jupyter** que contiene el código necesario para generar un archivo `csv` con la frecuencia de las palabras indicadas como keywords (input) de los documentos.

Se ha decidido utilizar la tecnología map reduce en spark por los siguinetes motivos:

- **Tipo de conteo**: a diferencia de otras tecnologías, map reduce permite realizar un conteo de palabras de forma eficiente. Además de contar palabaras duplicadas en mismo documento, contrario a lo que sucede con otras tecnologías como elastic search.
- **Escalabilidad**: Spark es una tecnología escalable, que permite procesar grandes volúmenes de datos de forma eficiente, como sucede con el caso de nuestro corpus.
- **Facilidad de uso**: Spark es una tecnología que permite procesar grandes volúmenes de datos de forma eficiente. Y sin necesidad de usar java, como en el caso de Hadoop.
- **Velocidad**: Spark es una tecnología que permite procesar grandes volúmenes de datos de forma eficiente. Que quizás en el caso de unso papers científicos no es tan necesaria. Pero que en el caso de un corpus de papers a nivel internacional, sí que puede ser necesario.


## 4. Simple Queries

En este apartado, disponemos de 2 ficheros:
- [articles_queries.md](/4-simple_queries/articles_queries.md): contiene la query necesaria para listar ordenadamente los artículos en los que un autor específico ha participado.
- [texts.ipynb](/4-simple_queries/texts.ipynb): contiene el código necesario para listar ordenadamente los párrafos por el tamaño del párrafo y la frecuencia del término.

### Articles

Para realizar esta tarea, hemos utilizado la interfaz de línea de comandos de Neo4j. Para ello, vamos a utilizar el cliente de Python para Neo4j.

### Texts

Este paso devuelve un listado ordenado de párrafos, junto con el título del artículo al que pertenecen, que contienen un término específico. La relevancia viene determinada por el tamaño del párrafo y la frecuencia del término, por lo cual, cuando un término aparece la misma cantidad de veces en dos textos, el texto de menor tamaño aparece primero con un score mayor.

Para realizar esta tarea, hemos utilizado el motor de búsqueda Elasticsearch por su eficiencia en cuanto al indexado. Primero, hay que conectar al contenedor "elasticsearch". Para ello, vamos a utilizar el cliente de Python para Elasicsearch. Accedemos al `texts.ipynb` que se encuentra en el directorio `4-simple_queries/`.

El archivo `texts.ipynb` nos propociona los códigos necesarios para acceder al cluster autogestionado de Elasticsearch via HTTP por el puerto 9200 del localhost. Una vez conectado, se puede indexar datos, solo en caso de que es la primera vez que levantas el contenedor o quieres añadir nuevos datos. Sin embargo, en caso contrario no es necesario ejercutarlo. A continuación, está la query necesaria para consultar por el término clave que quieras. Al ejecutar la celda te pedirá como input una palabra clave y como resultado te devolverá un dataframe ordenado por score(relevancia)  de los párrafos y el título del artículo.

Por último, en el caso de que quieras eliminar un índice, también es posible con la ejecución de la última celda del ipynb.  

***NOTA***: los índices borrados no son recuperables.

## 5. Complex Queries

### Docker

Hay dos ficheros disponibles en este directorio:

- [ibd_g2_mac](/ibd_g2_mac): Este fichero contiene las instrucciones para instalar Docker en un sistema operativo Mac.
- [ibd_g2_ubuntu](/ibd_g2_windows): Este fichero contiene las instrucciones para instalar Docker en un sistema operativo Windows.

Ambos ficheros contienen un archivo llamado `docker-compose.yml`, el cual proporciona las instrucciones para configurar los contenedores necesarios para ejecutar la práctica. Sin embargo, hay que tener en cuenta que uno de ellos está diseñado para la arquitectura **arm** (*Mac*), mientras que el otro está diseñado para la arquitectura **amd** (*Windows*).

***IMPORTANTE***: Asegúrate de utilizar el fichero correspondiente a tu arquitectura al levantar el contenedor. Si utilizas el fichero incorrecto, es posible que los contenedores tengan un rendimiento deficiente o incluso que no funcionen correctamente.