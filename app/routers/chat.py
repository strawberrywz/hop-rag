from fastapi import APIRouter, Query, WebSocket, Request, Form
from fastapi.responses import HTMLResponse
from app.core.chat_model import ChatModel
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
import json

router = APIRouter()
chat_model = ChatModel() 
templates = Jinja2Templates(directory="app/templates")

class Message(BaseModel):
    role: str
    content: str
    
    
class ChatRequest(BaseModel):
    messages: List[Message]
    

@router.post("/api/chat")
async def chat_api(request: ChatRequest):
  try:
    last_message = request.messages[-1]
    content = json.loads(last_message.content)
    user_input = content.get('input')
    response = chat_model.generate_response(user_input)
    return {"response": response}
  except Exception as e:
    return {"error": str(e)}

@router.get("/")
async def health(request: Request):
   return templates.TemplateResponse("health.html", {"request": request})
