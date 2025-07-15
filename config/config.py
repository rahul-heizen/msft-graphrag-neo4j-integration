import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Neo4j Configuration
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model Configuration
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "gpt-4-turbo-preview"  # or any other OpenAI model

# Neo4j Cypher Queries
MEDICAL_KNOWLEDGE_QUERY = """
MATCH (d:Document)-[:CONTAINS]->(c:Chunk)
WHERE c.embedding_similarity >= $similarity_threshold
RETURN c.content as chunk, d.title as source, c.embedding_similarity as score
ORDER BY score DESC
LIMIT $limit
""" 