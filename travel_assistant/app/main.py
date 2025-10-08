from fastapi import FastAPI
from travel_assistant.app.error_handlers import register_error_handlers

app = FastAPI(title="Travel Assistant AI")

register_error_handlers(app)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
