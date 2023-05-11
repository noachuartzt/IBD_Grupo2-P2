## CONSULTAS COMPLEJAS

2. ***Collaborators***: listado ordenado de autores relacionados con un autor específico.
- La relación entre autores viene determinada por su colaboración directa en un artículo o indirecta a través de autores comunes.

**Neo4j**

````sql
// Cargamos los datos del CSV
LOAD CSV WITH HEADERS FROM 'https://github.com/noachuartzt/IBD_Grupo2-P2/raw/main/parser/csv/output.csv' AS row

// Crear nodo Paper y Authors
CREATE (:Paper {id: row.id, title: row.title}) WITH row, split(row.authors, ";") AS authors
UNWIND authors AS author_name

MERGE (a:Author {name: author_name})
CREATE (a)<-[:WRITTEN_BY]-(:Paper {id: row.id}) nDate IS NOT NULL THEN row.publicationDate ELSE "Unknown" END

// Consulta 1

````
