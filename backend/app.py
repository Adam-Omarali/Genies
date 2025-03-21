from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import shutil
import ai
import logistics
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static directory
app.mount("/", StaticFiles(directory="../frontend/out", html=True), name="frontend")

app.mount("/api/static", StaticFiles(directory="static"), name="static")

@app.get("/api")
async def root():
    return {"message": "Hello World"}

@app.get("/api/books")
async def get_books():
    with open('books.json', 'r') as f:
        data = json.load(f)
    return data


@app.post("/api/upload-image")
async def upload_image(
    publisher: str = Form(...),
    original_price: float = Form(...),
    file: UploadFile = File(...)
):    
    try:
        # Create static directory if it doesn't exist
        os.makedirs("static", exist_ok=True)
        
        # Save the file to the static directory
        file_path = os.path.join("static", file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        book_entry = ai.process_book_return(file_path, original_price, publisher)
        
            
        return JSONResponse(content={"book": book_entry, "status": "success"})
    except Exception as e:
        return JSONResponse(content={"error": str(e), "status": "failed"})

@app.post("/api/routes")
async def get_routes(mode: str = Form(...), num_trucks: int = Form(...)):
    print(f"Generating routes for {mode} with {num_trucks} trucks")
    image_bytes = logistics.plot_routes_and_save(mode, num_trucks)
    return Response(
        content=image_bytes,
        media_type="image/png",
        headers={
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

@app.get("/api/delete")
async def delete_trajelon():
    try:
        # Read the current books
        with open('books.json', 'r') as f:
            books = json.load(f)
        
        # Find and remove Trajelon entry, saving the image filename
        trajelon_entry = None
        for index, book in enumerate(books['books']):
            if book.get('name', '').lower() == 'trajelon':
                trajelon_entry = book
                books['books'].pop(index)
                break
        
        if not trajelon_entry:
            return JSONResponse(content={"error": "Trajelon entry not found", "status": "failed"})
            
        # Save updated books.json
        with open('books.json', 'w') as f:
            json.dump(books, f, indent=4)
            
        # Delete the image file if it exists
        image_path = os.path.join("static", trajelon_entry.get('img', ''))
        if os.path.exists(image_path):
            os.remove(image_path)
            
        return JSONResponse(content={"message": "Trajelon entry and image deleted successfully", "status": "success"})
    except Exception as e:
        return JSONResponse(content={"error": str(e), "status": "failed"})

