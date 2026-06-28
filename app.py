from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from chatbot import chat_with_argus

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


class ChatRequest(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
async def home():
    with open("templates/index.html", "r", encoding="utf-8") as file:
        return file.read()


@app.post("/chat")
async def chat(request: ChatRequest):

    reply = await chat_with_argus(
        request.message,
        history=[]
    )

    return {
        "reply": reply
    }

@app.get("/health")
async def health():
    return {
        "status": "online",
        "message": "Argus is running!"
    }


# Import API routes later
# from routes.chat import router as chat_router
# app.include_router(chat_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )