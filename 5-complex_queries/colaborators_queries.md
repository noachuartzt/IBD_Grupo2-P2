## CONSULTAS COMPLEJAS

2. ***Collaborators***: listado ordenado de autores relacionados con un autor específico.
- La relación entre autores viene determinada por su colaboración directa en un artículo o indirecta a través de autores comunes.

**Neo4j**

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
MATCH (a:Author {name: "Y. Filali"})<-[:WRITTEN_BY]-(p:Paper)-[:WRITTEN_BY]->(b:Author) WHERE a <> b
WITH b, COUNT(p) AS Collaborations
ORDER BY Collaborations DESC
RETURN b.name AS Name, Collaborations 
````
