from fastapi import FastAPI, File, Form, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import io
from pypdf import PdfReader

from wrapper import main

app = FastAPI()
security = HTTPBasic()


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = 'askPDF'
    correct_password = 'this_is_fun'
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )


# Request schema
class PromptSchema(BaseModel):
    string_value: str


# Response schema
class ModelResponse(BaseModel):
    extracted_text: Optional[str]


def is_valid_pdf(pdf_bytes: bytes) -> bool:
    try:
        with io.BytesIO(pdf_bytes) as pdf_stream:
            pdf_reader = PdfReader(pdf_stream)
            return len(pdf_reader.pages) > 0
    except Exception:
        return False


def get_pdf_bytes(file_path: str) -> bytes:
    """Read a PDF file from the given path and return its contents as bytes."""
    with open(file_path, 'rb') as file:
        pdf_bytes = file.read()
    return pdf_bytes


@app.post("/api", response_model=ModelResponse)
async def process_pdf(
        file: bytes = File(...),  # PDF file bytes
        user_prompt: str = Form(...),  # Additional string
        credentials: HTTPBasicCredentials = Depends(authenticate)
):
    try:
        # Read the PDF file bytes

        pdf_stream = io.BytesIO(file)
        if not is_valid_pdf(file):
            raise HTTPException(status_code=400, detail="Invalid PDF file")
        # get completion
        extracted_text = main(pdf_stream, user_prompt)

        # Return the response
        return ModelResponse(extracted_text=extracted_text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
