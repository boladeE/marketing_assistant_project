from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
from copywriter import generate_marketing_copy
from brand_style import BrandStyleManager
from config import settings
from fastapi.templating import Jinja2Templates
from fastapi import Request


class CopyRequest(BaseModel):
    prompt: str

app = FastAPI(title="Marketing Assistant AI")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize templates
templates = Jinja2Templates(directory="backend/templates")

# Initialize brand style manager

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/generate-copy")
def create_marketing_copy(request: Request):
    print(f"Received request: {request}")
    # print(f"Received prompt: {request.prompt}")
    generated_copy = "Something"
    # print(f"Generated copy: {generated_copy}")

    return templates.TemplateResponse("index.html", {"request": request, "generated_copy": generated_copy})
    # try:
    #     # Generate the marketing copy using the simplified function
    #     generated_copy = generate_marketing_copy(request.prompt)
    #     print(f"Generated copy: {generated_copy}")
    #     return {
    #         "status": "success",
    #         "data": {
    #             "generated_copy": generated_copy
    #         }
    #     }
    # except Exception as e:
    #     print(f"Error generating copy: {str(e)}")
    #     raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True) 