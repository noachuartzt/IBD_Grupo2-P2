## CONSULTAS SIMPLES

1. ***Articles***: listado ordenado de artículos en los que un autor específico ha participado.



````sql
LOAD CSV WITH HEADERS FROM 'https://github.com/noachuartzt/IBD_Grupo2-P2/blob/main/parser/csv/2ca14fe14f0bd2f1363f3b735e788d12c3f9f332.csv' AS row

MATCH (authors:User {id:row.authors}) 
MATCH (paperId:User {id:row.paperId})
MATCH (year:User {id:row.year})

MERGE (paperId)-[:PUBLISHED_IN]->(year)
MERGE (paperId)-[:WRITTEN_BY]->(authors)

````