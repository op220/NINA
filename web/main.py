from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import sys

# Adicionar o diretório raiz ao path para importar módulos da Nina IA
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

# Importar routers
from routers import users, channels, interactions, statistics, settings

# Criar aplicação FastAPI
app = FastAPI(
    title="Nina IA - Interface Web",
    description="API para interface web do sistema de memória de longo prazo da Nina IA",
    version="1.0.0"
)

# Configurar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000", "http://127.0.0.1:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(channels.router, prefix="/api", tags=["channels"])
app.include_router(interactions.router, prefix="/api", tags=["interactions"])
app.include_router(statistics.router, prefix="/api", tags=["statistics"])
app.include_router(settings.router, prefix="/api", tags=["settings"])

# Rota raiz
@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Nina IA - Interface Web API",
        "docs": "/docs",
        "version": "1.0.0"
    }

# Montar arquivos estáticos para o frontend
app.mount("/", StaticFiles(directory="../frontend/public", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
