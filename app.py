from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from chatbot import stream_chat_with_argus

app = FastAPI(
    title="A.R.G.U.S",
    version="1.0.0"
)

# ==========================
# Static Files
# ==========================

app.mount("/static", StaticFiles(directory="static"), name="static")


# ==========================
# Request Model
# ==========================

class ChatRequest(BaseModel):
    message: str


# ==========================
# Home
# ==========================

@app.get("/")
async def home():
    return FileResponse("templates/index.html")


# ==========================
# Chat Endpoint (Streaming)
# ==========================

@app.post("/chat")
async def chat(request: ChatRequest):

    try:

        return StreamingResponse(
            stream_chat_with_argus(
                user_message=request.message,
                history=[]
            ),
            media_type="text/plain; charset=utf-8",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no"
            }
        )

    except Exception as e:

        print(f"[ERROR] {e}")

        return StreamingResponse(
            iter([
                "Sorry, something went wrong while contacting Argus."
            ]),
            media_type="text/plain; charset=utf-8"
        )


# ==========================
# Health Check
# ==========================

@app.get("/health")
async def health():
    return {
        "status": "online",
        "message": "Argus is running!"
    }


# ==========================
# Local Development
# ==========================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )