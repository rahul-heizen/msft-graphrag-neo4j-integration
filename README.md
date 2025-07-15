# Medical Chatbot with Microsoft GraphRAG and Neo4j

This project implements a medical chatbot using Microsoft's GraphRAG architecture integrated with Neo4j for enhanced retrieval and question answering capabilities. No vector database is used; all storage and retrieval is handled by Neo4j as a knowledge graph.

## Prerequisites

- Python 3.9+
- Neo4j Database (local or AuraDB)
- OpenAI API key
- Docker (optional, for containerization)

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd msft-graphrag-neo4j-integration
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file with the following variables:
```
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
OPENAI_API_KEY=your_openai_api_key
```

5. Start Neo4j:
- For local installation: Start your Neo4j server
- For AuraDB: Use the connection details provided by Neo4j AuraDB

6. Run the application:
```bash
python main.py
```

## Project Structure

- `main.py`: Entry point of the application
- `config/`: Configuration files and utilities
- `data/`: Sample medical documents and data processing scripts
- `retrievers/`: Implementation of Neo4j-based retriever
- `models/`: Neo4j data models and schemas
- `utils/`: Utility functions and helpers

## Architecture

This project implements the Microsoft GraphRAG architecture with the following components:

1. Document Processing Pipeline
2. Graph Retriever (Neo4j)
3. LLM Integration (OpenAI)
4. Query Processing and Response Generation

## License

MIT 