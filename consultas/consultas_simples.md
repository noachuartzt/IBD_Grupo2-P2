## CONSULTAS SIMPLES

1. ***Articles***: listado ordenado de artículos en los que un autor específico ha participado.

**Neo4j**

````sql
// Cargamos los datos del CSV
LOAD CSV WITH HEADERS FROM 'https://github.com/noachuartzt/IBD_Grupo2-P2/raw/main/parser/csv/2ca14fe14f0bd2f1363f3b735e788d12c3f9f332.csv' AS row

// Crear nodo Paper
MERGE (p:Paper {id: row.paperId})
SET p.title = row.title
SET p.abstract = row.abstract

// Crear nodo Year
MERGE (y:Year {year: row.year})

// Crear relación PUBLISHED_IN
MERGE (p)-[:PUBLISHED_IN {publicationDate: row.publicationDate}]->(y)

// Crear nodo Author
WITH row.authors AS json_authors
WITH apoc.json.parse(json_authors) AS authors
UNWIND authors AS a

MERGE (a:Author {name: trim(author.name)})

// Crear relación WRITTEN_BY
MERGE (p)-[:WRITTEN_BY {name: trim(author)}]->(a)

// Consulta
MATCH (p:Paper)-[:WRITTEN_BY]->(a:Author {name: '<author_name>'})
RETURN p.title, ORDER BY (p.year) ASC
````

````