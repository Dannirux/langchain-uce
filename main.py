from fastapi import FastAPI, UploadFile, File, HTTPException
from uce_langchain.lang_script import process_doc, create_db_from_document
from typing import Union
from pydantic import BaseModel
import shutil
import tempfile

app = FastAPI()

db = None

class DocumentData(BaseModel):
    path: str

class DocumentAnswer(BaseModel):
    answer: str

@app.post("/chat/create")
async def create_db_endpoint(doc: UploadFile = File(...)):
    global db
    try:
        with tempfile.NamedTemporaryFile(delete=False, prefix="test", suffix=".pdf") as temp_file:
            shutil.copyfileobj(doc.file, temp_file)
            temp_file_path = temp_file.name
        db = create_db_from_document(temp_file_path)
        return {"db": "Creada con éxito"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/answer")
def process_question_endpoint(item: DocumentAnswer):
    if db is None:
        return {"error": "Base de datos no creada"}
    respuesta = process_doc(question=item.answer, db=db)
    return {"reply": respuesta}
