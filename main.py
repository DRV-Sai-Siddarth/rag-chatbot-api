import os
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from graph_utils import get_graph_context
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq

load_dotenv()

app = FastAPI()

# API Model
class Query(BaseModel):
    question: str

# LLM & Prompt
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="mixtral-8x7b-32768"  # Or llama3-8b
)

template = """
You are a helpful assistant answering questions using the JNTUH knowledge graph.
Use the following graph data to respond clearly and concisely.

Context: {context}

Question: {question}

Answer:
"""

prompt = PromptTemplate.from_template(template)
chain = LLMChain(llm=llm, prompt=prompt)

@app.post("/ask")
def ask_question(q: Query, x_api_key: str = Header(...)):
    if x_api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Unauthorized")
    context = get_graph_context(q.question)
    response = chain.invoke({"context": context, "question": q.question})
    return {"response": response["text"]}
