from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from chatbot import chat_with_argus

app = FastAPI(
    title="A.R.G.U.S",
    version="1.0.0"
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Request model
class ChatRequest(BaseModel):
    message: str


# Home page
@app.get("/")
async def home():
    return FileResponse("templates/index.html")


# Chat endpoint
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        reply = await chat_with_argus(
            user_message=request.message,
            history=[]
        )

        return {
            "success": True,
            "reply": reply
        }

    except Exception as e:
        print(f"[ERROR] {e}")

        return {
            "success": False,
            "reply": "Sorry, something went wrong while contacting Argus."
        }


# Health check
@app.get("/health")
async def health():
    return {
        "status": "online",
        "message": "Argus is running!"
    }


# Run locally
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )