from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat, tenants, users

app = FastAPI(
    title="Chat Agents API",
    description="API para plataforma de chat multi-agente",
    version="1.0.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix='/chat')
app.include_router(tenants.router, prefix='/tenants')
app.include_router(users.router, prefix='/users')

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "chat-agents-api"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000) 