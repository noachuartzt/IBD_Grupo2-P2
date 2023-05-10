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

### 2. Configuraciñon de Elastic Search

*2.1* La imagen y sus respectivos contenedores ya se han creado con el docker compose inicial en el **Paso 1**

    ```
    version: '3'

    services:

    elasticsearch:
        image: docker.elastic.co/elasticsearch/elasticsearch:7.17.9
        container_name: elasticsearch
        environment:
        - discovery.type=single-node
        volumes:
        - ./data/:/usr/share/elasticsearch/data
        ports:
        - 9200:9200
        networks:
        - bdi_net

    logstash:
        image: docker.elastic.co/logstash/logstash:7.17.9
        container_name: logstash
        command: logstash -f /etc/logstash/conf.d/logstash.conf --config.reload.automatic
        environment:
        - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
        volumes:
        - ./data/:/usr/share/logstash/data/
        - ./logstash/conf.d/:/etc/logstash/conf.d/
        depends_on:
        - elasticsearch
        networks:
        - bdi_net

    networks:
    bdi_net:
        driver: bridge
    ```

*2.2* Editar el logstash.conf con los campos de los jsons

*2.3* La consulta para buscar los documentos que contienen una palabra clave en un campo específico es la siguiente:

    * Para buscar en todos los campos: 

        ``` 
        curl -X GET "localhost:9200/_search?q=<keyword>&pretty&df=<field>"
        ```

    * Para buscar en un campo específico: 

        ```
        GET <nombre_del_indice>/_search
        {
        "query": {
            "match": {
            "texts": "<término_específico>"
            }
        },
        "sort": [
            {
            "title.keyword": "asc"
            }
        ],
        "aggs": {
            "by_title": {
            "terms": {
                "field": "title.keyword"
            },
            "aggs": {
                "matching_paragraphs": {
                "top_hits": {
                    "sort": [
                    {
                        "_score": "desc"
                    }
                    ],
                    "size": 10,
                    "_source": {
                    "includes": [ "title", "paragraph" ]
                    }
                }
                }
            }
            }
        }
        }
        ```

### 3. Configuración de HDFS

*3.1* La imagen y sus respectivos contenedores ya se han creado con el docker compose inicial en el **Paso 1**

*3.3* Creamso el directorio src en /hadoop-deployment/yarn/jobs/

    ```
    mkdir src
    ```

*3.3* Añadimos el fichero wordsFile.txt, que contendrá las keywords que queremos contar, a /hadoop-deployment/yarn/jobs/src

*3.4* Compilamos el SpecialWordCount.java

    * Ejecutamos el nodo: 
    
        ```
        docker exec -t namenode /bin/bash
        ```

    * Compilamos el WordCOunt: 
        
        ```
        hadoop com.sun.tools.javac.Main SpecialWordCount.java
        ```

    * Para comprobar que todo ha salido correctamente: 
    
        ```
        ls -la
        ```

    * Construir lalibrería jar: 
    
        ```
        jar cf wc.jar SpecialWordCount*.class
        ```

    * Copiamos los ficheros de locala hdfs

        ```
        hdfs dfs -mkdir /keywords

        Hadoop fs -copyFromLocal wordsFile.txt /keywords/
        ```

    * Ejecutar la applicación mapReduce con el SpecialWordCount sobre wordsFile.txt: 
        
        ```
        hadoop jar wc.jar WordCount /keywords/wordsFile.txt /keywords/output
        ```

    * Vemos el resultado
    
        ```
        hadoop fs -cat /keywords/output/part-r-00000
        ```

