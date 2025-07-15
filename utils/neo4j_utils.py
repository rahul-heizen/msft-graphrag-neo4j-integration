from neo4j import GraphDatabase
from config.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

class Neo4jConnection:
    def __init__(self):
        self._driver = None

    def connect(self):
        if not self._driver:
            self._driver = GraphDatabase.driver(
                NEO4J_URI,
                auth=(NEO4J_USER, NEO4J_PASSWORD)
            )
        return self._driver

    def close(self):
        if self._driver:
            self._driver.close()
            self._driver = None

    def verify_connectivity(self):
        try:
            with self.connect().session() as session:
                result = session.run("RETURN 1")
                return result.single()[0] == 1
        except Exception as e:
            print(f"Failed to connect to Neo4j: {str(e)}")
            return False

    def create_medical_document(self, title, content, embeddings):
        query = """
        CREATE (d:Document {title: $title})
        WITH d
        UNWIND $chunks AS chunk
        CREATE (c:Chunk {
            content: chunk.content,
            embedding: chunk.embedding
        })
        CREATE (d)-[:CONTAINS]->(c)
        """
        with self.connect().session() as session:
            session.run(query, title=title, chunks=content)

    def search_similar_chunks(self, query_embedding, similarity_threshold=0.7, limit=5):
        from config.config import MEDICAL_KNOWLEDGE_QUERY
        
        with self.connect().session() as session:
            result = session.run(
                MEDICAL_KNOWLEDGE_QUERY,
                similarity_threshold=similarity_threshold,
                limit=limit
            )
            return [record for record in result]

neo4j_connection = Neo4jConnection() 