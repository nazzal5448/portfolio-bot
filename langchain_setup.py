from langchain_groq.chat_models import ChatGroq
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
# from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import os
import dotenv

# ===============================
# CONFIGURATION
# ===============================

dotenv.load_dotenv(".env")
GROQ_API_KEY = os.environ["GROQ_API_KEY"]
PDF_PATH = "data/data.pdf"

# ===============================
# Load the PDF document
# ===============================

# loader = PyPDFLoader(PDF_PATH)
# docs = loader.load()

# ===============================
# Split into chunks
# ===============================

# splitter = RecursiveCharacterTextSplitter(
#     chunk_size=1000,
#     chunk_overlap=50
# )
# chunks = splitter.split_documents(docs)

# ===============================
# Embed using Hugging Face
# ===============================

embedding_model = HuggingFaceEmbeddings(
    model_name="intfloat/e5-small-v2",
    encode_kwargs={"normalize_embeddings": True}
)

# ===============================
# Create Vector DB (FAISS)
# ===============================

# vectorstore = FAISS.from_documents(chunks, embedding_model)

# vectorstore.save_local("faiss_index")

vectorstore = FAISS.load_local("faiss_index", embedding_model, allow_dangerous_deserialization=True)

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"fetch_k": 3, "k":3})

# ===============================
# LLM via Groq
# ===============================

llm = ChatGroq(
    model="meta-llama/llama-4-maverick-17b-128e-instruct",
    api_key=GROQ_API_KEY
)

# ===============================
# Configuring Prompt Templates
# ===============================

prompt_template = ChatPromptTemplate(messages=[
("system", """
You are Xel, Nazzal Kausar's AI assistant. Your role is to help people know more about Nazzal.
Make sure to answer user's query precisely and try to connect with them emotionally. 
Your end goal should be to persuade people to hire nazzal for the service they need but do not
over persuade. 
Be friendly and professional.
Only answer from the context provided here : {context}
"""),
("user", "Hi, who are you?"),
("ai", "Hi, I am Xel, Nazzal Kausar's Ai Assistant. How may I help you?"),
("user", "{question}")])



# ===============================
# RAG Chain using LangChain
# ===============================


qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    return_source_documents=True,
    chain_type_kwargs={
        "prompt": prompt_template
    }
)



output_parser = StrOutputParser()

if __name__ == "__main__":
    output_parser = StrOutputParser()
    response = qa_chain.invoke("query: Hi, tell me about nazzal's services")
    print(output_parser.invoke(response.get("result")))
