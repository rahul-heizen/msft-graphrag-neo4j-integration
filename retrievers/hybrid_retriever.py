from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from config.config import EMBEDDING_MODEL
from utils.neo4j_utils import neo4j_connection

class GraphRetriever:
    def __init__(self):
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)

    def _get_embeddings(self, text: str) -> List[float]:
        return self.embedding_model.encode(text).tolist()

    def add_document(self, title: str, content: str):
        # Split content into chunks (implement your chunking logic here)
        chunks = self._chunk_content(content)
        embeddings = [self._get_embeddings(chunk) for chunk in chunks]
        chunk_data = [
            {"content": chunk, "embedding": embedding}
            for chunk, embedding in zip(chunks, embeddings)
        ]
        neo4j_connection.create_medical_document(title, chunk_data, embeddings)

    def _chunk_content(self, content: str, chunk_size: int = 1000) -> List[str]:
        words = content.split()
        chunks = []
        current_chunk = []
        current_size = 0
        for word in words:
            if current_size + len(word) + 1 > chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_size = len(word)
            else:
                current_chunk.append(word)
                current_size += len(word) + 1
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        return chunks

    def retrieve(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        query_embedding = self._get_embeddings(query)
        global_results = neo4j_connection.search_similar_chunks(
            query_embedding=query_embedding,
            limit=k
        )
        combined_results = []
        seen_chunks = set()
        for record in global_results:
            if record['chunk'] not in seen_chunks:
                combined_results.append({
                    'chunk': record['chunk'],
                    'source': record['source'],
                    'retriever': 'graph'
                })
                seen_chunks.add(record['chunk'])
        return combined_results[:k] 