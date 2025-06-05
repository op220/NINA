from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any, Optional
from utils.memory_client import MemoryClient

router = APIRouter()
memory_client = MemoryClient()

@router.get("/statistics", response_model=Dict[str, Any])
async def get_statistics():
    """
    Retorna estatísticas gerais do sistema de memória.
    """
    try:
        statistics = memory_client.get_statistics()
        return statistics
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter estatísticas: {str(e)}"
        )

@router.get("/statistics/users", response_model=Dict[str, Any])
async def get_user_statistics(
    limit: int = Query(10, description="Número máximo de usuários a incluir nas estatísticas")
):
    """
    Retorna estatísticas específicas de usuários.
    """
    try:
        statistics = memory_client.get_statistics()
        
        # Extrair estatísticas de usuários
        user_stats = {
            "user_count": statistics.get("user_count", 0),
            "top_users": statistics.get("top_users", [])[:limit],
            "average_interactions_per_user": statistics.get("interaction_count", 0) / max(1, statistics.get("user_count", 1))
        }
        
        return user_stats
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter estatísticas de usuários: {str(e)}"
        )

@router.get("/statistics/channels", response_model=Dict[str, Any])
async def get_channel_statistics(
    limit: int = Query(10, description="Número máximo de canais a incluir nas estatísticas")
):
    """
    Retorna estatísticas específicas de canais.
    """
    try:
        statistics = memory_client.get_statistics()
        
        # Extrair estatísticas de canais
        channel_stats = {
            "channel_count": statistics.get("channel_count", 0),
            "top_channels": statistics.get("top_channels", [])[:limit],
            "average_interactions_per_channel": statistics.get("interaction_count", 0) / max(1, statistics.get("channel_count", 1))
        }
        
        return channel_stats
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter estatísticas de canais: {str(e)}"
        )

@router.get("/statistics/topics", response_model=Dict[str, Any])
async def get_topic_statistics(
    limit: int = Query(10, description="Número máximo de tópicos a incluir nas estatísticas")
):
    """
    Retorna estatísticas específicas de tópicos.
    """
    try:
        statistics = memory_client.get_statistics()
        
        # Extrair estatísticas de tópicos
        topic_stats = {
            "top_topics": statistics.get("top_topics", [])[:limit]
        }
        
        return topic_stats
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter estatísticas de tópicos: {str(e)}"
        )

@router.get("/statistics/activity", response_model=Dict[str, Any])
async def get_activity_statistics(
    days: int = Query(7, description="Número de dias para incluir nas estatísticas de atividade")
):
    """
    Retorna estatísticas de atividade ao longo do tempo.
    """
    try:
        activity_stats = memory_client.get_activity_statistics(days=days)
        return activity_stats
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter estatísticas de atividade: {str(e)}"
        )
