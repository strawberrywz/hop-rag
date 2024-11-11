from fastapi import APIRouter, Query, WebSocket, Request, Form
from fastapi.responses import HTMLResponse
from app.core.chat_model import ChatModel
from fastapi.templating import Jinja2Templates

router = APIRouter()
chat_model = ChatModel() 
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def chat(
    request: Request,
    question: str = Query(None, description="Type your question here", max_length=256),
):
    context = {"request": request, "question": question, "answer": None}
    
    if question:
        try:
            response = chat_model.generate_response(question)
            context["answer"] = response
        except Exception as e:
            context["error"] = str(e)
    
    return templates.TemplateResponse("chat.html", context)

@router.post("/", response_class=HTMLResponse)
async def chat_submit(
    request: Request,
    question: str = Form(...)
):
    try:
        response = chat_model.generate_response(question)
        context = {
            "request": request,
            "question": question,
            "answer": response
        }
    except Exception as e:
        context = {
            "request": request,
            "question": question,
            "error": str(e)
        }
    
    return templates.TemplateResponse("chat.html", context)

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            user_input = await websocket.receive_text()
            response = chat_model.generate_response(user_input)
            await websocket.send_json({
                "user": user_input,
                "bot": response
            })
    except Exception as e:
        await websocket.send_json({
            "error": str(e)
        })