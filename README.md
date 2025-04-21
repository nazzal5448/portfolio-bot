# 🤖 Portfolio Bot – AI Assistant for Nazzal Kausar

**Xel** (aka Portfolio Bot) is an AI-powered assistant that helps visitors learn about Nazzal Kausar and his services.  
Built with LangChain, Groq LLMs, Hugging Face Embeddings, and FastAPI, this chatbot supports secure conversations with memory and document-based knowledge retrieval.

---

## 🚀 Features

- 🔐 **Token-secured API** using Bearer authentication
- 🧠 **Conversational Memory** via LangChain's buffer memory
- 📚 **RAG (Retrieval-Augmented Generation)** from uploaded PDF
- ⚡ **Groq LLM** integration for ultra-fast inference (`mixtral` / `llama-4`)
- 💾 FAISS vector store for fast semantic retrieval
- ☁️ Ready for deployment on Render / Railway

---

## 🛠️ Tech Stack

- 🧱 **LangChain** (chat chains, memory, retrieval)
- 🧠 **Groq** LLMs via `langchain-groq`
- 💬 **Hugging Face** embeddings (`e5-small-v2`)
- 🧠 **FAISS** for vector indexing
- ⚡ **FastAPI** backend

---

## 📁 Project Structure

```
portfolio-bot/
├── data/                    # PDF documents
├── faiss_index/             # FAISS vector store (optional)
├── main.py                  # FastAPI app
├── langchain_setup.py       # LLM, embedding, retriever, memory setup
├── .env                     # API keys
├── requirements.txt         # All dependencies
└── README.md
```

---

## 🧪 Local Setup

> ⚡ Requires Python 3.11+ (use `uv`, `venv`, or `poetry`)

### 1. Clone & install dependencies
```bash
git clone https://github.com/nazzal5448/portfolio-bot.git
cd portfolio-bot

# Option 1: Using uv (recommended)
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 2. Setup `.env`

```env
GROQ_API_KEY=your_groq_key_here
CHATBOT_API_KEY=nazzal_secret_token
```

### 3. Run the API
```bash
uv run uvicorn main:app --reload
```

Then open:
```
http://localhost:8000/docs
```

---

## 🔒 Authentication

All requests must include the `Authorization` header:
```
Authorization: Bearer nazzal_secret_token
```

---

## ☁️ Deploying to Render (Python)

1. Create a new **Web Service** on [Render.com](https://render.com)
2. Set your Python version to `3.11`
3. Set build command:
   ```bash
   uv pip install -r requirements.txt
   ```
4. Set start command:
   ```bash
   uv run uvicorn main:app --host 0.0.0.0 --port 10000
   ```
5. Add environment variables in Render's dashboard:
   - `GROQ_API_KEY`
   - `CHATBOT_API_KEY`

---

## 📬 API Example (cURL)

```bash
curl -X POST http://localhost:8000/chat \
-H "Authorization: Bearer nazzal_secret_token" \
-H "Content-Type: application/json" \
-d '{"query": "Tell me about Nazzal\'s services."}'
```

---

## 📌 Future Features

- 💾 Multi-user memory via Redis
- 🔁 Async background task queues
- 🧠 Skill-based tool calling (RAG + n8n)

---

## 🧑‍💻 About Nazzal

This project is built by [Nazzal Kausar](https://nazzalkausar.com), an aspiring AI Engineer focused on RAG systems, GenAI apps, and workflow automation.

---

## 📃 License

MIT – feel free to fork, reuse, and improve!
```
