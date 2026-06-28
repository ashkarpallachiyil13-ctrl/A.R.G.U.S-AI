from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from chatbot import stream_chat_with_argus

app = FastAPI(
    title="A.R.G.U.S",
    version="1.0.0"
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


class ChatRequest(BaseModel):
    message: str


@app.get("/")
async def home():
    return FileResponse("templates/index.html")


@app.post("/chat")
async def chat(request: ChatRequest):

    try:

        return StreamingResponse(
            stream_chat_with_argus(
                user_message=request.message,
                history=[]
            ),
            media_type="text/plain"
        )

    except Exception as e:

        print(f"[ERROR] {e}")

        return {
            "success": False,
            "reply": "Sorry, something went wrong while contacting Argus."
        }


@app.get("/health")
async def health():
    return {
        "status": "online",
        "message": "Argus is running!"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )