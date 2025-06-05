from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile
from typing import List, Dict, Any, Optional
from utils.memory_client import MemoryClient
import os

router = APIRouter()
memory_client = MemoryClient()

@router.get("/settings", response_model=Dict[str, Any])
async def get_settings():
    """
    Retorna as configurações atuais do sistema de memória.
    """
    try:
        settings = memory_client.get_settings()
        return settings
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter configurações: {str(e)}"
        )

@router.put("/settings", response_model=Dict[str, Any])
async def update_settings(
    settings: Dict[str, Any]
):
    """
    Atualiza as configurações do sistema de memória.
    """
    try:
        success = memory_client.update_settings(settings)
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Não foi possível atualizar as configurações"
            )
        return {"status": "success", "message": "Configurações atualizadas com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao atualizar configurações: {str(e)}"
        )

@router.post("/settings/backup", response_model=Dict[str, Any])
async def create_backup(
    backup_name: str = Query(None, description="Nome personalizado para o backup (opcional)")
):
    """
    Cria um backup do sistema de memória.
    """
    try:
        # Gerar nome do backup se não fornecido
        if not backup_name:
            from datetime import datetime
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Adicionar extensão .db se não presente
        if not backup_name.endswith(".db"):
            backup_name += ".db"
        
        # Definir caminho do backup
        backup_dir = os.path.join(os.getcwd(), "backups")
        os.makedirs(backup_dir, exist_ok=True)
        backup_path = os.path.join(backup_dir, backup_name)
        
        # Criar backup
        success = memory_client.backup(backup_path)
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Não foi possível criar o backup"
            )
        
        return {
            "status": "success", 
            "message": "Backup criado com sucesso",
            "backup_path": backup_path,
            "backup_name": backup_name
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar backup: {str(e)}"
        )

@router.post("/settings/restore", response_model=Dict[str, Any])
async def restore_backup(
    backup_file: UploadFile = File(..., description="Arquivo de backup para restaurar")
):
    """
    Restaura o sistema de memória a partir de um backup.
    """
    try:
        # Salvar arquivo de backup temporariamente
        temp_backup_path = os.path.join(os.getcwd(), "temp_backup.db")
        with open(temp_backup_path, "wb") as buffer:
            buffer.write(await backup_file.read())
        
        # Restaurar a partir do backup
        success = memory_client.restore(temp_backup_path)
        
        # Remover arquivo temporário
        os.remove(temp_backup_path)
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Não foi possível restaurar o backup"
            )
        
        return {"status": "success", "message": "Sistema restaurado com sucesso a partir do backup"}
    except HTTPException:
        raise
    except Exception as e:
        # Tentar remover arquivo temporário em caso de erro
        try:
            if os.path.exists(temp_backup_path):
                os.remove(temp_backup_path)
        except:
            pass
        
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao restaurar backup: {str(e)}"
        )

@router.get("/settings/backups", response_model=List[Dict[str, Any]])
async def list_backups():
    """
    Lista todos os backups disponíveis.
    """
    try:
        backup_dir = os.path.join(os.getcwd(), "backups")
        os.makedirs(backup_dir, exist_ok=True)
        
        backups = []
        for filename in os.listdir(backup_dir):
            if filename.endswith(".db"):
                file_path = os.path.join(backup_dir, filename)
                file_stats = os.stat(file_path)
                
                backups.append({
                    "name": filename,
                    "path": file_path,
                    "size": file_stats.st_size,
                    "created_at": file_stats.st_ctime
                })
        
        # Ordenar por data de criação (mais recente primeiro)
        backups.sort(key=lambda x: x["created_at"], reverse=True)
        
        return backups
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar backups: {str(e)}"
        )

@router.get("/settings/plugins", response_model=List[Dict[str, Any]])
async def get_plugins():
    """
    Retorna a lista de plugins disponíveis e seus status.
    """
    try:
        plugins = memory_client.get_plugins()
        return plugins
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter plugins: {str(e)}"
        )

@router.put("/settings/plugins/{plugin_id}", response_model=Dict[str, Any])
async def update_plugin_status(
    plugin_id: str,
    status: bool
):
    """
    Ativa ou desativa um plugin específico.
    """
    try:
        success = memory_client.update_plugin_status(plugin_id, status)
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Plugin com ID {plugin_id} não encontrado ou não foi possível atualizar"
            )
        return {"status": "success", "message": f"Status do plugin {plugin_id} atualizado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao atualizar status do plugin: {str(e)}"
        )
