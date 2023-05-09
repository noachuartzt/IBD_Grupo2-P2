## CONSULTAS SIMPLES

1. ***Articles***: listado ordenado de artículos en los que un autor específico ha participado.

**Neo4j**

````sql
-- Cargamos los datos del CSV
LOAD CSV WITH HEADERS FROM 'https://github.com/noachuartzt/IBD_Grupo2-P2/blob/main/parser/csv/2ca14fe14f0bd2f1363f3b735e788d12c3f9f332.csv' AS row

-- Creamos los nodos necesarios
MATCH (authors:User {id:row.authors}) 
MATCH (paper:User {id:row.paperId})
MATCH (year:User {id:row.year})

-- Definimos las propiedades
SET paper.title = row.title
SET paper.abstract = row.abstract

-- Creamos las relaciones
MERGE (paper)-[:PUBLISHED_IN {publicationDate: row.publicationDate}]->(year)

UNWIND split(row.authors, ';') AS author                -- Separamos los autores
MERGE (paper)-[:WRITTEN_BY {name: trim(author)}]->(author)


-- Consulta
MATCH (p:User)-[:WRITTEN_BY]->(a:User {name:'<author_name>'})
RETURN p.title AS title, p.year AS year
ORDER BY p.year ASC

````