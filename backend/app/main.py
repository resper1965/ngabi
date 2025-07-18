from fastapi import FastAPI
from app.routers import chat, tenants, users

app = FastAPI()

app.include_router(chat.router, prefix='/chat')
app.include_router(tenants.router, prefix='/tenants')
app.include_router(users.router, prefix='/users')

if __name__ == '___main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000) 