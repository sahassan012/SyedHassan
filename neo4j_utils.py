from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
user = "neo4j"
password = "test_root"

driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False, database="academicworld")

def get_top_10_keywords_by_university(university):
    query = """
                MATCH (f:FACULTY)-[:AFFILIATION_WITH]->(i:INSTITUTE),
                        (f)-[:INTERESTED_IN]->(k:KEYWORD)
                WHERE i.name = $university_name
                WITH k, count(k) as keyword_count
                ORDER BY keyword_count DESC
                LIMIT 10
                RETURN k.name as Keyword, keyword_count as Count
            """

    with driver.session() as session:
        result = session.run(query, university_name=university)
        top_keywords = [record for record in result]

    return top_keywords