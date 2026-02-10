import io
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from .services.endee_client import EndeeClient
from endee import Precision
from .core.parser import ResumeParser
from .core.embedder import OnlineEmbedder
from typing import List
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette import status
import re
import io


load_dotenv()

# 2. Get the token from the environment
HF_TOKEN = os.getenv("HF_TOKEN")



embedder = OnlineEmbedder(token=HF_TOKEN)

app = FastAPI(title="Resume Screening AI - Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Your React app's address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
parser = ResumeParser()

db_client = EndeeClient()

# This runs the moment 'uvicorn' starts the app
@app.on_event("startup")
async def startup_event():
    
    db_client.initialize_collection()

@app.get("/")
def read_root():
    return {"status": "Backend is running"}

# multiple files upload and process

@app.post("/upload-batch")
async def upload_batch(files: List[UploadFile] = File(...)):
    report = []
    
    for file in files:
        try:
            # 1. Read and Parse
            content = await file.read()
            # Wrap in BytesIO to ensure it's a stream
            pdf_stream = io.BytesIO(content)
            
            raw_text = parser.extract_raw_text(pdf_stream)
            structured_data = parser.segment_resume(raw_text)
            
            # --- Extract Contextual Data ---
            cities = ["Bengaluru", "Bangalore", "Pune", "Mumbai", "Hyderabad", "Delhi", "Chennai"]
            detected_city = "Not Specified"
            # Lowercase search for better matching
            search_text = raw_text.lower()
            for city in cities:
                if city.lower() in search_text:
                    detected_city = city
                    break
            
            exp_match = re.search(r"(\d+)\+?\s*(years?|yrs?)", raw_text, re.IGNORECASE)
            exp_years = exp_match.group(0) if exp_match else "Not Specified"

            # 2. Vectorize
            text_to_embed = (
                f"Candidate Skills: {structured_data['skills']}. "
                f"Location: {detected_city}. "
                f"Experience: {exp_years}."
            )
            vector = embedder.generate_vector(text_to_embed)
            
            # 3. Store in Endee
            success = db_client.insert_resume(
                filename=file.filename,
                vector=vector,
                metadata={
                    "filename": file.filename, 
                    "skills": structured_data["skills"],
                    "experience_text": structured_data["experience"],
                    "detected_location": detected_city,
                    "years_of_experience": exp_years
                }
            )

            if success:
                report.append({"file": file.filename, "status": "Success"})
            else:
                # If DB fails, we still want to continue to the next file
                report.append({"file": file.filename, "status": "Database Error"})
        
        except Exception as e:
            print(f"Error processing {file.filename}: {e}")
            report.append({"file": file.filename, "status": f"Error: {str(e)}"})
            
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "summary": report, 
            "total_processed": len(report)
        }
    )
@app.get("/search")
async def search_resumes(query: str, top_k: int = 5):
    # 1. Generate vector from user search string
    query_vector = embedder.generate_vector(query)
    
    # 2. Get results from SDK
    results = db_client.search_resumes(query_vector, top_k=top_k)
    
   
    formatted_results = []
    for item in results:
        formatted_results.append({
            "id": item['id'],               
            "score": item['similarity'],   
            "metadata": item.get('meta'),  
            "vector_returned": "True" if 'vector' in item else "False"
        })
        
    return {"results": formatted_results}

#To reset the DB


@app.delete("/reset")
async def reset_database():
    try:
      
        db_client.client.delete_index("resumes")
       
     
        db_client.client.create_index(
            name="resumes",
            dimension=384,
            space_type="cosine",
            precision=Precision.INT8D 
        ) 
        
      
        db_client.initialize_collection()
        
        return {"status": "success", "message": "Index cleared and recreated"}
    except Exception as e:
        print(f"Reset Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

#Db vector count
@app.get("/stats")
async def get_stats():
    try:
        # Re-fetch the index reference to clear any local cache
        db_client.index = db_client.client.get_index(name=db_client.index_name)
        info = db_client.index.describe()

        # print(f"DEBUG: Live Count from DB: {info.get('count')}")
        
        return {
            "total_documents": info.get("count", 0),
            "dimension": info.get("dimension", 384),
            "status": "connected"
        }
    except Exception as e:
        # If the index doesn't exist yet, we return 0 rather than failing
        print(f"Stats error: {e}")
        return {
            "total_documents": 0, 
            "status": "initializing",
            "error": str(e)
        }
### Testing apis:-

@app.get("/test-connection")
def test_connection():
    is_alive = db_client.check_health()
    if is_alive:
        return {
            "database_connection": "Success",
            "message": "Connected to Endee Engine on port 8080"
        }
    return {
        "database_connection": "Failed",
        "message": "Cannot reach the Docker engine. Is 'docker compose up' running?"
    }

@app.post("/parse")
async def parse_resume(file: UploadFile = File(...)):
    # Read the file into memory
    content = await file.read()
    pdf_stream = io.BytesIO(content)
    
    # Extract and Segment
    raw_text = parser.extract_raw_text(pdf_stream)
    structured_data = parser.segment_resume(raw_text)
    
    return {
        "filename": file.filename,
        "segments": {
            "skills_preview": structured_data["skills"][:200],
            "experience_preview": structured_data["experience"][:200]
        },
        "full_text_length": len(raw_text)
    }

# Processing and embedding endpoint

@app.post("/process-and-embed")
async def process_and_embed(file: UploadFile = File(...)):
    # 1. Parse
    content = await file.read()
    raw_text = parser.extract_raw_text(io.BytesIO(content))
    structured_data = parser.segment_resume(raw_text)
    
 
 
    text_to_embed = structured_data["skills"] if structured_data["skills"] else raw_text[:500]
    vector = embedder.generate_vector(text_to_embed)
    
    return {
        "filename": file.filename,
        "vector_dimensions": len(vector),
        "vector_sample": vector[:5], 
        "status": "Ready for Endee Database"
    }


