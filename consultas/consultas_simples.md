## CONSULTAS SIMPLES

1. ***Articles***: listado ordenado de artículos en los que un autor específico ha participado.
- La relevancia viene determinada por el número de autores (menor número de autores, mayor relevancia del autor concreto)

2. ***Collaborators***: listado ordenado de autores relacionados con un autor específico.
- La relación entre autores viene determinada por su colaboración directa en un artículo o indirecta a través de autores comunes

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
MATCH (p:Paper)-[:WRITTEN_BY]->(:Author {name: 'Y. Filali'}) WITH p
MATCH (p)-[:WRITTEN_BY]->(a:Author)
WITH p, count(a) AS numAuthors, a
ORDER BY numAuthors DESC
RETURN p.title, a.name

// Consulta 2
MATCH (a:Author {name: "Y. Filali"})<-[:WRITTEN_BY]-(p:Paper)-[:WRITTEN_BY]->(b:Author)
WHERE a <> b
WITH b, COUNT(p) AS collaborations
ORDER BY collaborations DESC
RETURN b.name, collaborations
````
