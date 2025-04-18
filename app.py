from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from langchain_setup import qa_chain, output_parser
import os
import dotenv
import uvicorn

app = FastAPI()
dotenv.load_dotenv()

API_KEY = os.environ["API_KEY"]

class QueryInput(BaseModel):
    query: str

@app.get("/")
def home():
    return {"message":"The chatbot is running!"}


@app.post("/chat")
async def chat(input: QueryInput, authorization: str = Header(None)):
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    query = input.query
    result = qa_chain.invoke(query)
    parsed_output = output_parser.invoke(result.get("result"))

    return {
        "response": parsed_output,
        "raw": result
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000)) 
    uvicorn.run(app, host="0.0.0.0", port=port)
