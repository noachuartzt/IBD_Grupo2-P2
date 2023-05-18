<center>
<h1> Infraestructura UPM para publicaciones científicas </h1>
<h2> IBD_Grupo2-P2</h2>
</center>
<i><small><b>Alumnos</b>: Noa Chu, Che Cui, Carlota Medrano, Alejandro Pequeño<br><b>Última actualización</b>: 2023-05-01</small></i></div>
<p></p>

Este repositorio contiene los archivos necesarios para crear una infraestructura basada en Docker que soporte la gestión enriquecida de publicaciones científicas en formato PDF para el archivo digital de la Universidad Politécnica de Madrid (_UPM_) que actualmente gestiona los trabajos fin de grado, fin de tesis y tesis doctorales de los alumnos de la Universidad pero se pide una nueva versión de la plataforma para poder gestionar también las publicaciones científicas de sus investigadores, lo cual es un desafío porque el volumen de datos que se ha de soportar es mucho mayor que con los TFGs, TFMs, y tesis. En cuanto a la parte de la gestión enriquecida, se quieren ofrecer datos estadísticos sobre los autores de las publicaciones, sus colaboraciones, las áreas de investigación, y además facilitar la exploración de su contenido y la búsqueda avanzada desde su propio portal web.

El siguiente repositorio está dividido en 5 apartados (*carpetas*):
- **[1-publications](1-publications)**: contiene los archivos necesarios para la conversión de los documentos PDF a `json` a partir de una lista de DOIs.
- **[2-static_data](2-static_data)**: contiene los archivos necesarios para la generación de dos archivos `csv` que contienen información estática sobre los documentos.
- **[3-dynamic_data](3-dynamic_data)**: contiene los archivos necesarios para la generación de un archivo `csv` que contienen el número de aparicion de un término en concreto.
- **[4-simple_queries](4-simple_queries)**: contiene los archivos necesarios para realizar consultas de listado mediante **Neo4j** y **Elasticsearch**.
- **[5-advanced_queries](5-advanced_queries)**: contiene los archivos necesarios para realizar consultas avanzadas mediante **Neo4j** y **Spark**.
- **[docker](docker)**: contiene los archivos necesarios para la creación de la infraestructura basada en **Docker**.

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
- **[json](1-publications/json)**: carpeta que contiene por cada DOI existente en [Semantic Web Scholar API](https://api.semanticscholar.org/), un archivo `json` con la meta-información del documento.
- **[csv](1-publications/csv)**: carpeta que contiene un archivo `csv` con la meta-información de los documentos parseada y estructurada a partir de los archivos `json`.
- **[corpus.txt](/corpus.txt)**: fichero que contiene una lista de DOIs de los documentos que se quieren parsear.
- **[parse.py](/parse.py)**: fichero que contiene las funciones necesarias para parsear los archivos `json` y generar el archivo `csv`.
- **[test.ipynb](/test.ipynb)**: fichero que contiene el código necesario para ejecutar el [/parser.py](1-publications/parser.py) y generar los archivos previamente mencionados.

### 1.1.Instrucciones

1. Dirígete a la carpeta [1-publications](1-publications) del repositorio clonado y abre el [jupyter-notebook](test.ipynb) (*no hace falta hacerlo desde la terminal*):
   
2. Una vez abierto, abre **vscode** o culalquier otro editor de texto, ejecuta todas las celdas del notebook. 

***NOTA 1***: Dicho fichero, importa de [/parser.py](1-publications/parser.py) las funciones necesarias `doi_to_json` y `json_to_csv` para parsear la lista de DOIs a los archivos `json` y generar el archivo `csv` respectivamente. No obstante, antes de generar dichos archivos, comprueba si las carpetas [json](1-publications/json) y [csv](1-publications/csv) existen, si no es así, las crea. Una vez comprobado, ejecuta las funciones mencionadas anteriormente.

**IMPORTANTE**: El archivo generado en [csv/output](/csv/output.csv) es el que se utilizará en el siguiente apartado, [2-static_data](/2-static_data). Por tanto, **realiza un *commit* al repositorio git**, ya que la consulta **Neo4j** extrae el `csv` generado de **GitHub**. Para ello, abre una terminal y ejecuta los siguientes comandos:

```bash
git add .
git commit -m "Files Created"
git push origin head
```


## 2. Static Data

En este apartado se pretende generar **2 ficheros** `csv`:

- **authors.csv**: contiene el número de publicaciones por autor. (Columnas: *author, puublications*)
- **documents.csv**: contiene la meta-información de los documentos. (Columnas: *file_name, title, num_pages, creation_date, modification_date*)

Los archivos mencionados anteriormente, se han generado mediante el [parser.py](1-publications/parser.py) del apartado anterior, en la función `json_to_csv`.

Dado que los datos a generar son datos estáticos, es decir, no cambian con el tiempo, y no se espera un alto volumen de datos, hemos decidido utilizar la tecnología **pandas** para la generación de los archivos `csv`.


## 3. Dynamic Data

En este apartado se pretende generar: 

- **Keywords.csv**: contiene el número de apariciones de un término concreto (e.g. ‘virus’), o cualquiera de sus sinónimos en inglés (e.g. ‘infection’, ‘microbe’..), en el corpus
    -Columnas: ‘word’ y ‘frequency’

Para ello, hemos creado un **MapReduce**. Es un único programa guardado con dos distintas extensiones:
- [keywordsCounter.ipynb](/3-dynamic_data/keywordsCounter.ipynb): se trata de un notebook de **jupyter** que contiene el código necesario para generar un archivo `csv` con la frecuencia de las palabras indicadas como keywords (input) de los documentos.

Se ha decidido utilizar la tecnología **map reduce en spark** por los siguinetes motivos:

- **Tipo de conteo**: a diferencia de otras tecnologías, *map reduce* permite realizar un conteo de palabras de forma eficiente, gracias a su procesamiento distribuido. Además de contar palabaras duplicadas en mismo documento, contrario a lo que sucede con otras tecnologías como *Elastic Search*.
- **Escalabilidad**: Spark es una tecnología escalable, que permite procesar grandes volúmenes de datos de forma eficiente, como sucede con el caso de nuestro corpus.
- **Facilidad de uso**: Spark es una tecnología que permite procesar grandes volúmenes de datos de forma eficiente. Y sin necesidad de usar java, como en el caso de *Hadoop*.
- **Velocidad**: Spark es una tecnología que permite procesar grandes volúmenes de datos de forma eficiente. Que quizás en el caso de unos papers científicos no es tan necesaria. Pero que en el caso de un corpus de papers a nivel internacional, sí que puede ser necesario.


## 4. Simple Queries

En este apartado, disponemos de **3 ficheros**:
- [articles_queries.md](/4-simple_queries/articles_queries.md): contiene la query necesaria para listar ordenadamente los artículos en los que un autor específico ha participado.
- - [articles.ipynb](/4-simple_queries/articles.ipynb): contiene el código necesario para listar ordenadamente los artículos en los que un autor específico ha participado.
- [texts.ipynb](/4-simple_queries/texts.ipynb): contiene el código necesario para listar ordenadamente los párrafos por el tamaño del párrafo y la frecuencia del término.

### 4.1.Articles

Este paso devuelve una lista ordenada de artículos en los que un autor específico ha participado. La relevancia viene determinada por el número de autores qu han participado en los artículos en los que el autor específico ha participado.

Para realizar esta tarea, se puede utilizar tanto la línea de comandoa de **Neo4j** como la interfaz web.  En nuestro caso, vamos a utilizar el cliente de Python para **Neo4j**.  

Teniendo en mente las consultas de **"4.1 Articles"** y **"5.1 Collaborators"**, pensamos que la mejor solución tanto para el volumen de datos como para una mayor eficiencia, es la de utilizar una base de datos de grafos, ya que involucran la relación entre autores y la relevancia de su participación en los artículos. Por ello, hemos decidido utilizar **Neo4j**.

El archivo [articles_queries.md](/4-simple_queries/articles_queries.md) nos proporciona los códigos necesarios para realizar la consulta en la línea de comandos de **Neo4j**, no obstante, en el archivo [articles.ipynb](/4-simple_queries/articles.ipynb) se encuentra el código necesario para realizar la consulta en el cliente de Python para **Neo4j**. Dicho archivo, se conecta al contenedor "**Neo4j**" via HTTP por el puerto 7687 del localhost. Una vez conectado, se importan los datos del archivo [csv/output.csv](/csv/output.csv) y se crea la estructura de la base de datos. Finalmente, se realiza la consulta y se muestra el resultado.

### 4.2.Texts

Este paso devuelve un listado ordenado de párrafos, junto con el título del artículo al que pertenecen, que contienen un término específico. La relevancia viene determinada por el tamaño del párrafo y la frecuencia del término, por lo cual, cuando un término aparece la misma cantidad de veces en dos textos, el texto de menor tamaño aparece primero con un ***score*** mayor.

Para realizar esta tarea, hemos utilizado el motor de búsqueda Elasticsearch por su eficiencia en cuanto al indexado. Elasticsearch utiliza índice invertido, que consiste en indexar el contenido de los documentos en palabras y números. Además muestra la localización de esas palabras o números, facilitando así la búsqueda en documentos completos.

Primero, hay que conectar al contenedor "**Elastic Search**". Para ello, vamos a utilizar el cliente de Python para **Elastic Search**, que se encuentra en el archivo [texts.ipynb](/4-simple_queries/texts.ipynb).

El archivo `texts.ipynb` nos propociona los códigos necesarios para acceder al cluster autogestionado de Elasticsearch via HTTP por el puerto 9200 del localhost. Una vez conectado, se puede indexar datos, solo en caso de que es la primera vez que levantas el contenedor o quieres añadir nuevos datos. Sin embargo, en caso contrario no es necesario ejercutarlo. A continuación, está la query necesaria para consultar por el término clave que quieras. Al ejecutar la celda te pedirá como input una palabra clave y como resultado te devolverá un dataframe ordenado por ***score*** (*relevancia*) de los párrafos y el título del artículo.

Por último, en el caso de que quieras eliminar un índice, también es posible con la ejecución de la última celda del ipynb.  

***NOTA***: los índices borrados no son recuperables.

## 5. Complex Queries

En este apartado, disponemos de **4 ficheros**:
- [collaborators_queries.md](/5-complex_queries/collaborators_queries.md): contiene la query necesaria para listar ordenadamente los colaboradores de un autor específico.
- [collaborators.ipynb](/5-complex_queries/collaborators.ipynb): contiene el código necesario para listar ordenadamente los colaboradores de un autor específico.
- [wordLengthCounter.ipynb](5-complex_queries/wordLengthCounter.ipynb): contiene el código necesario para listar ordenadamente el número de palabras de longitud n.
- [wordLengthCounter.py](5-complex_queries/wordLengthCounter.py): contiene el mismo código que el anterior, pero en formato `.py`.

### 5.1.Collaborators

De nuevo acudimos a **Neo4j** para realizar estas consultas ya que al tratarse de una base de datos de grafos es más eficiente para la búqueda de ***coloaboradores***. Ya que en este tipo de bases de edatos, las relaciones importan tanto o más que los datos en sí.

De igual forma que en el apartado anterior, el archivo [collaborators.ipynb](/5-complex_queries/collaborators.ipynb) nos proporciona los códigos necesarios para realizar la consulta en el cliente de Python para **Neo4j**. 

### 5.2.Words

De nuevo utilizamos la tecnología **Map Reduce en Spark** para realizar esta tarea. En este caso, se utiliza para obtener el número de palabras de longitud $n$. El notebook [wordLengthCounter.ipynb](5-complex_queries/wordLengthCounter.ipynb) devuelve una tupla con la longitud $n$ seleccionada y el número de palabras de esa longitud que hay en el corpus.

## 6. Docker

Hay dos ficheros disponibles en este directorio:

- [ibd_g2_mac](/ibd_g2_mac): Este fichero contiene las instrucciones para instalar Docker en un sistema operativo Mac.
- [ibd_g2_ubuntu](/ibd_g2_windows): Este fichero contiene las instrucciones para instalar Docker en un sistema operativo Windows.

Ambos ficheros contienen un archivo llamado `docker-compose.yml`, el cual proporciona las instrucciones para configurar los contenedores necesarios para ejecutar la práctica. Sin embargo, hay que tener en cuenta que uno de ellos está diseñado para la arquitectura **arm** (*Mac*), mientras que el otro está diseñado para la arquitectura **amd** (*Windows*).

***IMPORTANTE***: Asegúrate de utilizar el fichero correspondiente a tu arquitectura al levantar el contenedor. Si utilizas el fichero incorrecto, es posible que los contenedores tengan un rendimiento deficiente o incluso que no funcionen correctamente.
