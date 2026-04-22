#importing app, error responses, definition and validation of inputs
#importing ai, os for communication with python, loading .env

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging

#loading .env
load_dotenv()
logging.basicConfig(level=logging.INFO)

#API handling
app = FastAPI()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OpenRouter API key was not found. Check .env file")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

#model request
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]


#route for sending msg to chatgpt
@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        messages = request.messages

        #filters empty requests
        if not messages:
            raise HTTPException(status_code=400, detail="Messages cannot be empty")

        logging.info("Chat request received")

        last_error = None

        # reduced retries (prevents artificial delay)
        for attempt in range(2):
            try:
                response = client.chat.completions.create(
                    model="meta-llama/llama-3.1-8b-instruct",

                    messages=[
                        # system prompt (controls behaviour)
                        {"role": "system", "content": "You are a helpful, concise AI assistant."},

                        # conversation history from frontend
                        *[m.model_dump() for m in messages]
                    ],

                    timeout=20
                )

                message = response.choices[0].message.content

                return {"response": message}

            except Exception as e:
                last_error = e
                logging.warning(f"Attempt {attempt+1} failed: {e}")

                # small fixed delay instead of exponential (removes UI lag spikes)
                import time
                time.sleep(1)

        raise HTTPException(status_code=500, detail=str(last_error))

    except HTTPException as e:
        raise e

    except Exception as e:
        logging.error("Error : %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")