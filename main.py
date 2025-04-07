from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from query_engine import query_engine 


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class Query(BaseModel):
    question: str

@app.post("/chat-assistant")
async def chat_assistant(query: Query):

    response = query_engine(query.question)

    return {"response": response}