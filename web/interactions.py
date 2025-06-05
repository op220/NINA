from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Dict, Any, Optional
from utils.memory_client import MemoryClient

router = APIRouter()
memory_client = MemoryClient()

@router.get("/interactions", response_model=List[Dict[str, Any]])
async def get_interactions(
    limit: int = Query(20, description="Número máximo de interações a retornar"),
    offset: int = Query(0, description="Número de interações a pular")
):
    """
    Retorna a lista de interações recentes no sistema de memória.
    """
    try:
        interactions = memory_client.get_interactions(limit=limit, offset=offset)
        return interactions
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter interações: {str(e)}"
        )

@router.get("/interactions/{interaction_id}", response_model=Dict[str, Any])
async def get_interaction(
    interaction_id: int = Path(..., description="ID da interação")
):
    """
    Retorna os detalhes de uma interação específica.
    """
    try:
        interaction = memory_client.get_interaction(interaction_id)
        if not interaction:
            raise HTTPException(
                status_code=404,
                detail=f"Interação com ID {interaction_id} não encontrada"
            )
        return interaction
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter interação: {str(e)}"
        )

@router.delete("/interactions/{interaction_id}", response_model=Dict[str, Any])
async def delete_interaction(
    interaction_id: int = Path(..., description="ID da interação")
):
    """
    Remove uma interação específica.
    """
    try:
        success = memory_client.delete_interaction(interaction_id)
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Interação com ID {interaction_id} não encontrada ou não foi possível remover"
            )
        return {"status": "success", "message": f"Interação {interaction_id} removida com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao remover interação: {str(e)}"
        )

@router.get("/search/interactions", response_model=List[Dict[str, Any]])
async def search_interactions(
    query: str = Query(..., description="Termo de busca"),
    limit: int = Query(20, description="Número máximo de resultados")
):
    """
    Busca interações por conteúdo.
    """
    try:
        results = memory_client.search_interactions(query, limit=limit)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar interações: {str(e)}"
        )
