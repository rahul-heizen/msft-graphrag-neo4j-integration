import os
from typing import List, Optional
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from retrievers.hybrid_retriever import GraphRetriever
from utils.neo4j_utils import neo4j_connection
import openai
from config.config import OPENAI_API_KEY
import traceback

app = FastAPI(title="Medical Chatbot")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

retriever = GraphRetriever()

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]

@app.on_event("startup")
async def startup_event():
    # Verify Neo4j connection
    if not neo4j_connection.verify_connectivity():
        raise Exception("Failed to connect to Neo4j database")

@app.post("/upload")
async def upload_medical_document(
    file: UploadFile = File(...),
    title: Optional[str] = None
):
    try:
        content = await file.read()
        content_str = content.decode("utf-8")
        
        # Use filename as title if not provided
        doc_title = title or file.filename
        
        # Add document to Neo4j
        retriever.add_document(doc_title, content_str)
        
        return {"message": f"Successfully uploaded and processed document: {doc_title}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Retrieve relevant context
        results = retriever.retrieve(request.question)
        
        # Combine retrieved chunks into context
        context = "\n".join([f"Source ({r['source']}): {r['chunk']}" for r in results])
        
        # Prepare prompt for OpenAI
        prompt = f"""You are a medical chatbot. Use the following medical context to answer the question.
        If you cannot answer the question based on the context, say so.
        
        Context:
        {context}
        
        Question: {request.question}
        
        Answer:"""
        
        # Get response from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        # Extract sources
        sources = list(set(r['source'] for r in results))
        
        return ChatResponse(
            answer=response.choices[0].message.content,
            sources=sources
        )
    except Exception as e:
        print("Exception in /chat endpoint:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 