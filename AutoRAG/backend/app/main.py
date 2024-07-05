from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.rag import RAGSystem
from app.models import get_model
from app.fine_tuning import fine_tune_model
from app.quantization import quantize_model
import logging
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os
import shutil

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Set up authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dummy user database (replace with a real database in production)
users_db = {
    "testuser": {
        "username": "testuser",
        "hashed_password": "fakehashed_password"
    }
}

class User(BaseModel):
    username: str

class Query(BaseModel):
    text: str
    model_name: str

class FineTuneRequest(BaseModel):
    model_name: str
    data_path: str

class RAGSetupRequest(BaseModel):
    model: str
    dataset_path: str

def fake_hash_password(password: str):
    return "fakehashed_" + password

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)

def fake_decode_token(token):
    return User(username=token)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = User(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}

@app.post("/query")
@limiter.limit("5/minute")
async def query_model(query: Query, current_user: User = Depends(get_current_user)):
    try:
        model = get_model(query.model_name)
        rag_system = RAGSystem(model)
        response = rag_system.query(query.text)
        logger.info(f"Successfully queried model {query.model_name}")
        return {"response": response}
    except Exception as e:
        logger.error(f"Error querying model: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error querying model: {str(e)}")

@app.post("/fine-tune")
@limiter.limit("1/hour")
async def fine_tune(request: FineTuneRequest, current_user: User = Depends(get_current_user)):
    try:
        fine_tuned_model = fine_tune_model(request.model_name, request.data_path)
        logger.info(f"Successfully fine-tuned model {request.model_name}")
        return {"message": "Fine-tuning completed", "model": fine_tuned_model}
    except Exception as e:
        logger.error(f"Error fine-tuning model: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fine-tuning model: {str(e)}")

@app.post("/quantize")
@limiter.limit("1/hour")
async def quantize(model_name: str, current_user: User = Depends(get_current_user)):
    try:
        quantized_model = quantize_model(model_name)
        logger.info(f"Successfully quantized model {model_name}")
        return {"message": "Quantization completed", "model": quantized_model}
    except Exception as e:
        logger.error(f"Error quantizing model: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error quantizing model: {str(e)}")

@app.post("/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):
    try:
        file_location = f"data/uploads/{file.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
        logger.info(f"Successfully uploaded dataset: {file.filename}")
        return {"success": True, "dataset_path": file_location}
    except Exception as e:
        logger.error(f"Error uploading dataset: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error uploading dataset: {str(e)}")

@app.post("/setup-rag")
async def setup_rag(request: RAGSetupRequest):
    try:
        model = get_model(request.model)
        rag_system = RAGSystem(model)
        rag_system.load_documents(request.dataset_path)
        logger.info(f"Successfully set up RAG system with model {request.model} and dataset {request.dataset_path}")
        return {"success": True}
    except Exception as e:
        logger.error(f"Error setting up RAG system: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error setting up RAG system: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)