import os
import sys
import json
import logging
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, Depends, Query, Body, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("nina_web_api")

# Adicionar o diretório raiz ao path para importar outros módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar o integrador de memória
try:
    from core.memory_integrator import NinaMemoryIntegrator
    from core.memory_adapter import NinaMemoryAdapter
except ImportError as e:
    logger.error(f"Erro ao importar módulos de memória: {e}")
    raise

# Modelos Pydantic para validação de dados
class UserProfile(BaseModel):
    user_id: str
    username: Optional[str] = None
    notes: Optional[str] = None
    first_seen: Optional[str] = None
    last_seen: Optional[str] = None
    interaction_count: Optional[int] = 0
    voice_time: Optional[int] = 0

class ChannelProfile(BaseModel):
    channel_id: str
    channel_name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = "texto"
    created_at: Optional[str] = None
    last_activity: Optional[str] = None
    message_count: Optional[int] = 0
    user_count: Optional[int] = 0

class Personality(BaseModel):
    formality_level: int = Field(50, ge=0, le=100)
    humor_level: int = Field(50, ge=0, le=100)
    technicality_level: int = Field(50, ge=0, le=100)
    response_speed: str = "médio"
    verbosity: str = "médio"

class LearningSettings(BaseModel):
    enabled: bool = True
    learning_rate: float = Field(0.5, ge=0.1, le=1.0)
    adaptation_speed: str = "médio"
    memory_weight: float = Field(0.7, ge=0.1, le=1.0)

class Interaction(BaseModel):
    id: str
    user_id: str
    channel_id: str
    content: str
    timestamp: str
    sentiment: Optional[str] = None
    is_nina_response: Optional[bool] = False
    target_user_id: Optional[str] = None

class Topic(BaseModel):
    name: str
    count: int
    percentage: float

class Emotion(BaseModel):
    name: str
    count: int
    percentage: float

class Expression(BaseModel):
    text: str
    count: int

class UserStats(BaseModel):
    topics: List[Topic] = []
    emotions: List[Emotion] = []
    expressions: List[Expression] = []

class ChannelStats(BaseModel):
    topics: List[Topic] = []
    active_users: List[Dict[str, Any]] = []

class SystemStats(BaseModel):
    user_count: int = 0
    channel_count: int = 0
    interaction_count: int = 0
    memory_size_mb: float = 0
    uptime_days: int = 0

class BackupInfo(BaseModel):
    path: str
    timestamp: str
    size_mb: float

class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

# Criar a aplicação FastAPI
app = FastAPI(
    title="Nina IA - API de Memória",
    description="API para gerenciar o sistema de memória de longo prazo da Nina IA",
    version="1.0.0"
)

# Configurar CORS para permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, limitar para a origem específica do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variáveis globais
memory_integrator = None
memory_adapter = None

# Função para inicializar o sistema de memória
def initialize_memory_system():
    global memory_integrator, memory_adapter
    
    try:
        # Carregar configuração
        config_path = os.environ.get("NINA_CONFIG_PATH", "config.json")
        
        # Inicializar o integrador de memória
        memory_db_path = os.environ.get("NINA_MEMORY_DB_PATH", "memory.db")
        profiles_dir = os.environ.get("NINA_PROFILES_DIR", "data/profiles")
        
        memory_integrator = NinaMemoryIntegrator(
            memory_db_path=memory_db_path,
            profiles_dir=profiles_dir
        )
        
        # Inicializar o adaptador de memória
        memory_adapter = NinaMemoryAdapter(
            memory_integrator=memory_integrator,
            config_path=config_path
        )
        
        logger.info("Sistema de memória inicializado com sucesso")
        return True
    except Exception as e:
        logger.error(f"Erro ao inicializar sistema de memória: {e}")
        return False

# Dependência para garantir que o sistema de memória está inicializado
def get_memory_system():
    if memory_integrator is None or memory_adapter is None:
        if not initialize_memory_system():
            raise HTTPException(status_code=500, detail="Sistema de memória não inicializado")
    return {"integrator": memory_integrator, "adapter": memory_adapter}

# Rotas da API

# Rota de status
@app.get("/api/status", response_model=ApiResponse)
def get_status(memory_system: Dict = Depends(get_memory_system)):
    return {
        "success": True,
        "message": "Sistema de memória operacional",
        "data": {
            "status": "online",
            "version": "1.0.0",
            "initialized": memory_system["integrator"] is not None
        }
    }

# Rotas para usuários
@app.get("/api/users", response_model=ApiResponse)
def get_users(
    memory_system: Dict = Depends(get_memory_system),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    try:
        users = memory_system["integrator"].memory_manager.get_all_users(limit=limit, offset=offset)
        return {
            "success": True,
            "message": f"Recuperados {len(users)} usuários",
            "data": users
        }
    except Exception as e:
        logger.error(f"Erro ao obter usuários: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/users/{user_id}", response_model=ApiResponse)
def get_user(
    user_id: str = Path(..., description="ID do usuário"),
    memory_system: Dict = Depends(get_memory_system)
):
    try:
        user = memory_system["integrator"].get_user_memories(user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"Usuário {user_id} não encontrado")
        
        return {
            "success": True,
            "message": f"Usuário {user_id} recuperado com sucesso",
            "data": user
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter usuário {user_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/users/{user_id}", response_model=ApiResponse)
def update_user(
    user_id: str = Path(..., description="ID do usuário"),
    user_data: UserProfile = Body(...),
    memory_system: Dict = Depends(get_memory_system)
):
    try:
        # Verificar se o usuário existe
        user = memory_system["integrator"].memory_manager.get_user_profile(user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"Usuário {user_id} não encontrado")
        
        # Atualizar perfil do usuário
        memory_system["integrator"].memory_manager.update_user_profile(
            user_id=user_id,
            **user_data.dict(exclude_unset=True, exclude={"user_id"})
        )
        
        return {
            "success": True,
            "message": f"Usuário {user_id} atualizado com sucesso",
            "data": memory_system["integrator"].memory_manager.get_user_profile(user_id)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar usuário {user_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/users/{user_id}/interactions", response_model=ApiResponse)
def delete_user_interactions(
    user_id: str = Path(..., description="ID do usuário"),
    interaction_ids: List[str] = Body(..., embed=True),
    memory_system: Dict = Depends(get_memory_system)
):
    try:
        # Verificar se o usuário existe
        user = memory_system["integrator"].memory_manager.get_user_profile(user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"Usuário {user_id} não encontrado")
        
        # Remover interações
        for interaction_id in interaction_ids:
            memory_system["integrator"].memory_manager.delete_interaction(interaction_id)
        
        return {
            "success": True,
            "message": f"Removidas {len(interaction_ids)} interações do usuário {user_id}",
            "data": None
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao remover interações do usuário {user_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/users/{user_id}", response_model=ApiResponse)
def clear_user_memory(
    user_id: str = Path(..., description="ID do usuário"),
    memory_system: Dict = Depends(get_memory_system)
):
    try:
        # Verificar se o usuário existe
        user = memory_system["integrator"].memory_manager.get_user_profile(user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"Usuário {user_id} não encontrado")
        
        # Limpar memória do usuário
        success = memory_system["integrator"].clear_user_memory(user_id)
        
        if success:
            return {
                "success": True,
                "message": f"Memória do usuário {user_id} limpa com sucesso",
                "data": None
            }
        else:
            raise HTTPException(status_code=500, detail=f"Falha ao limpar memória do usuário {user_id}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao limpar memória do usuário {user_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Rotas para canais
@app.get("/api/channels", response_model=ApiResponse)
def get_channels(
    memory_system: Dict = Depends(get_memory_system),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    try:
        channels = memory_system["integrator"].memory_manager.get_all_channels(limit=limit, offset=offset)
        return {
            "success": True,
            "message": f"Recuperados {len(channels)} canais",
            "data": channels
        }
    except Exception as e:
        logger.error(f"Erro ao obter canais: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/channels/{channel_id}", response_model=ApiResponse)
def get_channel(
    channel_id: str = Path(..., description="ID do canal"),
    memory_system: Dict = Depends(get_memory_system)
):
    try:
        channel = memory_system["integrator"].get_channel_memories(channel_id)
        if not channel:
            raise HTTPException(status_code=404, detail=f"Canal {channel_id} não encontrado")
        
        return {
            "success": True,
            "message": f"Canal {channel_id} recuperado com sucesso",
            "data": channel
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter canal {channel_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/channels/{channel_id}/personality", response_model=ApiResponse)
def update_channel_personality(
    channel_id: str = Path(..., description="ID do canal"),
    personality: Personality = Body(...),
    memory_system: Dict = Depends(get_memory_system)
):
    try:
        # Verificar se o canal existe
        channel = memory_system["integrator"].memory_manager.get_channel_profile(channel_id)
        if not channel:
            raise HTTPException(status_code=404, detail=f"Canal {channel_id} não encontrado")
        
        # Atualizar personalidade do canal
        memory_system["integrator"].personality_manager.save_channel_personality(
            channel_id=channel_id,
            personality=personality.dict()
        )
        
        return {
            "success": True,
            "message": f"Personalidade do canal {channel_id} atualizada com sucesso",
            "data": memory_system["integrator"].personality_manager.get_channel_personality(channel_id)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar personalidade do canal {channel_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/channels/{channel_id}/settings", response_model=ApiResponse)
def update_channel_settings(
    channel_id: str = Path(..., description="ID do canal"),
    settings: LearningSettings = Body(...),
    memory_system: Dict = Depends(get_memory_system)
):
    try:
        # Verificar se o canal existe
        channel = memory_system["integrator"].memory_manager.get_channel_profile(channel_id)
        if not channel:
            raise HTTPException(status_code=404, detail=f"Canal {channel_id} não encontrado")
        
        # Atualizar configurações do canal
        memory_system["integrator"].memory_manager.update_channel_settings(
            channel_id=channel_id,
            settings=settings.dict()
        )
        
        return {
            "success": True,
            "message": f"Configurações do canal {channel_id} atualizadas com sucesso",
            "data": memory_system["integrator"].memory_manager.get_channel_settings(channel_id)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar configurações do canal {channel_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/channels/{channel_id}", response_model=ApiResponse)
def clear_channel_memory(
    channel_id: str = Path(..., description="ID do canal"),
    memory_system: Dict = Depends(get_memory_system)
):
    try:
        # Verificar se o canal existe
        channel = memory_system["integrator"].memory_manager.get_channel_profile(channel_id)
        if not channel:
            raise HTTPException(status_code=404, detail=f"Canal {channel_id} não encontrado")
        
        # Limpar memória do canal
        success = memory_system["integrator"].clear_channel_memory(channel_id)
        
        if success:
            return {
                "success": True,
                "message": f"Memória do canal {channel_id} limpa com sucesso",
                "data": None
            }
        else:
            raise HTTPException(status_code=500, detail=f"Falha ao limpar memória do canal {channel_id}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao limpar memória do canal {channel_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Rotas para interações
@app.get("/api/interactions", response_model=ApiResponse)
def get_interactions(
    memory_system: Dict = Depends(get_memory_system),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    user_id: Optional[str] = Query(None),
    channel_id: Optional[str] = Query(None)
):
    try:
        # Filtrar por usuário e/ou canal se especificados
        if user_id and channel_id:
            interactions = memory_system["integrator"].memory_manager.get_user_channel_interactions(
                user_id=user_id,
                channel_id=channel_id,
                limit=limit,
                offset=offset
            )
        elif user_id:
            interactions = memory_system["integrator"].memory_manager.get_user_interactions(
                user_id=user_id,
                limit=limit,
                offset=offset
            )
        elif channel_id:
            interactions = memory_system["integrator"].memory_manager.get_channel_interactions(
                channel_id=channel_id,
                limit=limit,
                offset=offset
            )
        else:
            interactions = memory_system["integrator"].memory_manager.get_all_interactions(
                limit=limit,
                offset=offset
            )
    except Exception as e:
        logger.error(f"Erro ao recuperar interações: {e}")
        raise HTTPException(status_code=500, detail="Erro ao recuperar interações")
(Content truncated due to size limit. Use line ranges to read in chunks)