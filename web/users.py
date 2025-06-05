from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Dict, Any, Optional
from utils.memory_client import MemoryClient

router = APIRouter()
memory_client = MemoryClient()

@router.get("/users", response_model=List[Dict[str, Any]])
async def get_users(
    limit: int = Query(20, description="Número máximo de usuários a retornar"),
    offset: int = Query(0, description="Número de usuários a pular")
):
    """
    Retorna a lista de usuários registrados no sistema de memória.
    """
    try:
        users = memory_client.get_users(limit=limit, offset=offset)
        return users
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter usuários: {str(e)}"
        )

@router.get("/users/{user_id}", response_model=Dict[str, Any])
async def get_user(
    user_id: str = Path(..., description="ID do usuário")
):
    """
    Retorna os detalhes de um usuário específico.
    """
    try:
        user = memory_client.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"Usuário com ID {user_id} não encontrado"
            )
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter usuário: {str(e)}"
        )

@router.put("/users/{user_id}", response_model=Dict[str, Any])
async def update_user(
    user_id: str = Path(..., description="ID do usuário"),
    data: Dict[str, Any] = None
):
    """
    Atualiza as informações de um usuário específico.
    """
    try:
        success = memory_client.update_user(user_id, data)
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Usuário com ID {user_id} não encontrado ou não foi possível atualizar"
            )
        return {"status": "success", "message": f"Usuário {user_id} atualizado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao atualizar usuário: {str(e)}"
        )

@router.delete("/users/{user_id}/memory", response_model=Dict[str, Any])
async def delete_user_memory(
    user_id: str = Path(..., description="ID do usuário")
):
    """
    Remove todas as memórias associadas a um usuário.
    """
    try:
        success = memory_client.delete_user_memory(user_id)
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Usuário com ID {user_id} não encontrado ou não foi possível remover memórias"
            )
        return {"status": "success", "message": f"Memórias do usuário {user_id} removidas com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao remover memórias do usuário: {str(e)}"
        )

@router.get("/users/{user_id}/interactions", response_model=List[Dict[str, Any]])
async def get_user_interactions(
    user_id: str = Path(..., description="ID do usuário"),
    limit: int = Query(20, description="Número máximo de interações a retornar")
):
    """
    Retorna as interações de um usuário específico.
    """
    try:
        interactions = memory_client.get_user_interactions(user_id, limit=limit)
        return interactions
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter interações do usuário: {str(e)}"
        )

@router.get("/users/{user_id}/topics", response_model=List[Dict[str, Any]])
async def get_user_topics(
    user_id: str = Path(..., description="ID do usuário")
):
    """
    Retorna os tópicos de interesse de um usuário específico.
    """
    try:
        user = memory_client.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"Usuário com ID {user_id} não encontrado"
            )
        return user.get("topics", [])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter tópicos do usuário: {str(e)}"
        )

@router.get("/users/{user_id}/expressions", response_model=List[Dict[str, Any]])
async def get_user_expressions(
    user_id: str = Path(..., description="ID do usuário")
):
    """
    Retorna as expressões frequentes de um usuário específico.
    """
    try:
        user = memory_client.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"Usuário com ID {user_id} não encontrado"
            )
        metadata = user.get("metadata", {})
        return metadata.get("frequent_expressions", [])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter expressões do usuário: {str(e)}"
        )

@router.get("/search/users", response_model=List[Dict[str, Any]])
async def search_users(
    query: str = Query(..., description="Termo de busca"),
    limit: int = Query(20, description="Número máximo de resultados")
):
    """
    Busca usuários por nome.
    """
    try:
        results = memory_client.search(query, search_type="users", limit=limit)
        return results.get("users", [])
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar usuários: {str(e)}"
        )
