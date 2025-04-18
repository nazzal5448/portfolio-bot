from langchain_groq.chat_models import ChatGroq
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_core.prompts import ChatPromptTemplate
import os
import dotenv

# ===============================
# CONFIGURATION
# ===============================

dotenv.load_dotenv(".env")
GROQ_API_KEY = os.environ["GROQ_API_KEY"]

# ===============================
# Embedding Model
# ===============================

embedding_model = HuggingFaceEmbeddings(
    model_name="intfloat/e5-small-v2",
    encode_kwargs={"normalize_embeddings": True}
)

# ===============================
# Load Vector DB (FAISS)
# ===============================

vectorstore = FAISS.load_local(
    "faiss_index",
    embedding_model,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"fetch_k": 2, "k": 2}
)

# ===============================
# LLM via Groq (Fastest available)
# ===============================

llm = ChatGroq(
    model="meta-llama/llama-4-maverick-17b-128e-instruct",
    api_key=GROQ_API_KEY
)

# ===============================
# Prompt Template
# ===============================

prompt_template = ChatPromptTemplate.from_messages([
    ("system", """
You are Xel, Nazzal Kausar's AI assistant. Your job is to help people learn about Nazzal's expertise.
Be friendly and professional. Base your answers only on this context: {context}.  if the context is not 
available, answer it generically but do not get too off-topic.
"""),
    ("user", "hi"),
    ("ai", "Hi, I am Xel, Nazzal Kausar's AI Assistant. How may I help you?")
    ("user", "ok"),
    ("ai", "Great! is there anything else I can help you with?"),
    ("user", "Hi, who are you?"),
    ("ai", "Hi, I am Xel, Nazzal Kausar's AI Assistant. How may I help you?"),
    ("user", "{question}")
])

# ===============================
# RAG Chain
# ===============================

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    return_source_documents=False,
    chain_type_kwargs={"prompt": prompt_template}
)

output_parser = StrOutputParser()
