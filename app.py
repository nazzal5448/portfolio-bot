from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from langchain_setup import qa_chain, output_parser
from fastapi.middleware.cors import CORSMiddleware
import os
import dotenv
import uvicorn
import asyncio

app = FastAPI()
dotenv.load_dotenv()

API_KEY = os.environ["API_KEY"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://nazzalkausar.com"],  
    allow_credentials=True,
    allow_methods=["GET", "POST"],               
    allow_headers=["*"],
    max_age=3600
)


class QueryInput(BaseModel):
    query: str

@app.get("/")
def home():
    return {"message":"The chatbot is running!"}

@app.get("/ping")
def ping():
    return {"message":"The site is up and running!"}

@app.post("/chat")
async def chat(input: QueryInput, authorization: str = Header(None)):
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    query = input.query
    result = await asyncio.to_thread(qa_chain.invoke, query)
    parsed_output = await asyncio.to_thread(output_parser.invoke, result.get("result"))


    return {
        "response": parsed_output
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000)) 
    uvicorn.run(app, host="0.0.0.0", port=port)
