from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

app = FastAPI(title="NeuralMix Engine")

print("Loading AI Model (all-MiniLM-L6-v2)...")
# Load model (optimized for cpu)
model = SentenceTransformer('all-MiniLM-L6-v2') 

print("Initializing Vector Database...")
# Persistent storage in the 'db' folder
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="songs")

class ScrobbleData(BaseModel):
    id: str # Lyrion Track ID (url or int)
    artist: str
    title: str
    album: str = ""
    genre: str = ""

@app.get("/status")
def status():
    return {
        "status": "online",
        "model": "all-MiniLM-L6-v2 (Loaded)",
        "db_count": collection.count()
    }

@app.post("/vectorize")
def vectorize_track(track: ScrobbleData):
    # create rich text representation
    text = f"{track.title} by {track.artist}. Genre: {track.genre}. Album: {track.album}"
    
    # Generate Embedding
    embedding = model.encode(text).tolist()
    
    # Store in Chroma
    collection.upsert(
        documents=[text],
        embeddings=[embedding],
        metadatas=[{"artist": track.artist, "title": track.title, "genre": track.genre}],
        ids=[track.id]
    )
    
    return {"message": "Vectorized", "id": track.id}

@app.post("/similar")
def find_similar(track: ScrobbleData, limit: int = 10):
    text = f"{track.title} by {track.artist}. Genre: {track.genre}"
    embedding = model.encode(text).tolist()
    
    results = collection.query(
        query_embeddings=[embedding],
        n_results=limit
    )
    
    # Flatten results
    hits = []
    if results['ids']:
        for i, id in enumerate(results['ids'][0]):
            hits.append({
                "id": id,
                "score": results['distances'][0][i] if results['distances'] else 0,
                "metadata": results['metadatas'][0][i] if results['metadatas'] else {}
            })
            
    return {"hits": hits}

if __name__ == "__main__":
    port = int(os.getenv("NEURALMIX_PORT", 8090))
    print(f"Starting NeuralMix Brain on port {port} (HOST: 0.0.0.0)...")
    uvicorn.run(app, host="0.0.0.0", port=port)
