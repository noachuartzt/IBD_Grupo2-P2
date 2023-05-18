### ***Articles***
Listado ordenado de artículos en los que un autor específico ha participado.
- La relevancia viene determinada por el número de autores (_menor número de autores, mayor relevancia del autor concreto_)

Creación de nodos y relaciones:
````sql
// Cargamos los datos del CSV
LOAD CSV WITH HEADERS FROM 'https://github.com/noachuartzt/IBD_Grupo2-P2/raw/main/1-publications/csv/output.csv' AS row

// Crear nodo Paper
MERGE (p:Paper {id: row.paperId, title: row.title})
SET p.publicationDate = CASE WHEN row.publicationDate IS NOT NULL THEN row.publicationDate ELSE "Unknown" END
SET p.abstract = CASE WHEN row.abstract IS NOT NULL THEN row.abstract ELSE "Unknown" END

// Crear nodo Author
WITH row, split(row.authorId, ',') AS ids, split(row.authorName, ',') AS names, p
UNWIND range(0, size(ids)-1) AS i

MERGE (a:Author {id: ids[i]})
SET a.name = names[i]

// Crear relación WRITTEN_BY
MERGE (p)-[:WRITTEN_BY {authorId: row.authorId}]->(a)
````

Consultas:

````sql
// Consulta 1
MATCH (p:Paper)-[:WRITTEN_BY]->(:Author {name: '<author_name>'})
MATCH (p)-[:WRITTEN_BY]->(a:Author)
RETURN p.title AS Title, COUNT(a) AS numAuthors
ORDER BY numAuthors ASC
````
````sql
// Otra Opción
MATCH (a:Author {name: '<author_name>'})<-[:WRITTEN_BY]-(p:Paper)-[:WRITTEN_BY]->(b:Author) WHERE a <> b
RETURN p.title as Title, COUNT (b) + 1 as numAuthors
ORDER BY numAuthors ASC
````
