# CHAT-AI
A fast, lightweight AI chat application built with Streamlit (frontend) and FastAPI (backend), powered by OpenRouter language models.

## Features
* Real-time chat interface using Streamlit
* FastAPI backend for handling AI requests
* Supports OpenRouter models (LLaMA, Mistral, GPT, etc.)
* Chat history stored in session state
* Optimized request handling with retries and timeouts
* Modular and easy-to-extend architecture

## Project Structure

```
.
├── app_ui.py        # Streamlit frontend
├── main.py          # FastAPI backend
├── .env             # API keys (not included in repo)
├── requirements.txt
└── README.md
```

## Installation
### 1. Clone the repository
```
git clone https://github.com/pbpallavi23/CHAT-AI
cd CHAT-AI
```
### 2. Create a virtual environment
```
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```
### 3. Install dependencies
```
pip install -r requirements.txt
```
## Environment Variables
Put your API key in the .env file

## Running the Application
### Start Backend (FastAPI)
First terminal : 
```
uvicorn main:app --reload
```
Second terminal : 
```
streamlit run app_ui.py
```

## How It Works

1. The user sends a message via the Streamlit interface
2. The message is sent to the FastAPI backend (`/api/chat`)
3. The backend forwards the request to an OpenRouter model
4. The AI response is returned and displayed in the UI
