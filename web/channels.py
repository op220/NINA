from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Dict, Any, Optional
from utils.memory_client import MemoryClient

router = APIRouter()
memory_client = MemoryClient()

@router.get("/channels", response_model=List[Dict[str, Any]])
async def get_channels(
    limit: int = Query(20, description="Número máximo de canais a retornar"),
    offset: int = Query(0, description="Número de canais a pular")
):
    """
    Retorna a lista de canais registrados no sistema de memória.
    """
    try:
        channels = memory_client.get_channels(limit=limit, offset=offset)
        return channels
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter canais: {str(e)}"
        )

@router.get("/channels/{channel_id}", response_model=Dict[str, Any])
async def get_channel(
    channel_id: str = Path(..., description="ID do canal")
):
    """
    Retorna os detalhes de um canal específico.
    """
    try:
        channel = memory_client.get_channel(channel_id)
        if not channel:
            raise HTTPException(
                status_code=404,
                detail=f"Canal com ID {channel_id} não encontrado"
            )
        return channel
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter canal: {str(e)}"
        )

@router.put("/channels/{channel_id}", response_model=Dict[str, Any])
async def update_channel(
    channel_id: str = Path(..., description="ID do canal"),
    data: Dict[str, Any] = None
):
    """
    Atualiza as informações de um canal específico.
    """
    try:
        success = memory_client.update_channel(channel_id, data)
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Canal com ID {channel_id} não encontrado ou não foi possível atualizar"
            )
        return {"status": "success", "message": f"Canal {channel_id} atualizado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao atualizar canal: {str(e)}"
        )

@router.get("/channels/{channel_id}/interactions", response_model=List[Dict[str, Any]])
async def get_channel_interactions(
    channel_id: str = Path(..., description="ID do canal"),
    limit: int = Query(20, description="Número máximo de interações a retornar")
):
    """
    Retorna as interações em um canal específico.
    """
    try:
        interactions = memory_client.get_channel_interactions(channel_id, limit=limit)
        return interactions
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter interações do canal: {str(e)}"
        )

@router.get("/channels/{channel_id}/topics", response_model=List[Dict[str, Any]])
async def get_channel_topics(
    channel_id: str = Path(..., description="ID do canal")
):
    """
    Retorna os tópicos recorrentes em um canal específico.
    """
    try:
        channel = memory_client.get_channel(channel_id)
        if not channel:
            raise HTTPException(
                status_code=404,
                detail=f"Canal com ID {channel_id} não encontrado"
            )
        return channel.get("topics", [])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter tópicos do canal: {str(e)}"
        )

@router.get("/channels/{channel_id}/users", response_model=List[Dict[str, Any]])
async def get_channel_users(
    channel_id: str = Path(..., description="ID do canal")
):
    """
    Retorna os usuários ativos em um canal específico.
    """
    try:
        channel = memory_client.get_channel(channel_id)
        if not channel:
            raise HTTPException(
                status_code=404,
                detail=f"Canal com ID {channel_id} não encontrado"
            )
        return channel.get("active_users", [])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter usuários do canal: {str(e)}"
        )

@router.get("/channels/{channel_id}/personality", response_model=Dict[str, Any])
async def get_channel_personality(
    channel_id: str = Path(..., description="ID do canal")
):
    """
    Retorna a personalidade da Nina para um canal específico.
    """
    try:
        channel = memory_client.get_channel(channel_id)
        if not channel:
            raise HTTPException(
                status_code=404,
                detail=f"Canal com ID {channel_id} não encontrado"
            )
        metadata = channel.get("metadata", {})
        return metadata.get("nina_personality", {})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter personalidade do canal: {str(e)}"
        )

@router.put("/channels/{channel_id}/personality", response_model=Dict[str, Any])
async def update_channel_personality(
    channel_id: str = Path(..., description="ID do canal"),
    personality: Dict[str, Any] = None
):
    """
    Atualiza a personalidade da Nina para um canal específico.
    """
    try:
        success = memory_client.update_nina_personality(channel_id, personality)
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Canal com ID {channel_id} não encontrado ou não foi possível atualizar personalidade"
            )
        return {"status": "success", "message": f"Personalidade do canal {channel_id} atualizada com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao atualizar personalidade do canal: {str(e)}"
        )

@router.get("/search/channels", response_model=List[Dict[str, Any]])
async def search_channels(
    query: str = Query(..., description="Termo de busca"),
    limit: int = Query(20, description="Número máximo de resultados")
):
    """
    Busca canais por nome.
    """
    try:
        results = memory_client.search(query, search_type="channels", limit=limit)
        return results.get("channels", [])
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar canais: {str(e)}"
        )
