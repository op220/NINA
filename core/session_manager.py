"""
Módulo para gerenciamento de sessões de conversa.
Parte do projeto Nina IA para gerenciamento de contexto de conversas.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime

from memory.memory_manager import MemoryManager


# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SessionManager:
    """
    Gerenciador de sessões de conversa.
    """
    
    def __init__(self, memory_dir: str = None):
        """
        Inicializa o gerenciador de sessões.
        
        Args:
            memory_dir: Diretório para armazenar dados de memória (None = usar padrão)
        """
        self.memory_manager = MemoryManager(memory_dir)
        self.active_sessions = {}
        
        logger.info("Gerenciador de sessões inicializado")
    
    def create_session(self, session_name: Optional[str] = None) -> str:
        """
        Cria uma nova sessão de conversa.
        
        Args:
            session_name: Nome da sessão (opcional)
            
        Returns:
            ID da sessão criada
        """
        session_id = self.memory_manager.generate_session_id()
        
        # Armazenar metadados da sessão
        metadata = {
            "name": session_name or f"Sessão {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat()
        }
        
       #self.memory_manager.store_user_info(f"session:{session_id}", metadata)
        
        # Adicionar à lista de sessões ativas
        self.active_sessions[session_id] = metadata
        
        logger.info(f"Sessão criada: {session_id} ({metadata['name']})")
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtém informações de uma sessão.
        
        Args:
            session_id: ID da sessão
            
        Returns:
            Metadados da sessão ou None se não encontrada
        """
        # Verificar cache de sessões ativas
        if session_id in self.active_sessions:
            return self.active_sessions[session_id]
        
        # Buscar no armazenamento
        metadata = self.memory_manager.get_user_info(f"session:{session_id}")
        
        if metadata:
            # Adicionar ao cache
            self.active_sessions[session_id] = metadata
            return metadata
        
        return None
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """
        Lista todas as sessões.
        
        Returns:
            Lista de metadados de sessões
        """
        all_info = self.memory_manager.get_all_user_info()
        
        sessions = []
        for key, value in all_info.items():
            if key.startswith("session:"):
                session_id = key.split(":", 1)[1]
                sessions.append({
                    "id": session_id,
                    **value
                })
        
        # Ordenar por data de última atividade (mais recente primeiro)
        sessions.sort(key=lambda s: s.get("last_activity", ""), reverse=True)
        
        return sessions
    
    def update_session_activity(self, session_id: str) -> bool:
        """
        Atualiza o timestamp de última atividade de uma sessão.
        
        Args:
            session_id: ID da sessão
            
        Returns:
            True se a operação foi bem-sucedida
        """
        metadata = self.get_session(session_id)
        
        if not metadata:
            logger.error(f"Sessão não encontrada: {session_id}")
            return False
        
        # Atualizar timestamp
        metadata["last_activity"] = datetime.now().isoformat()
        
        # Atualizar no armazenamento
        result = self.memory_manager.store_user_info(f"session:{session_id}", metadata)
        
        # Atualizar no cache
        if result:
            self.active_sessions[session_id] = metadata
        
        return result
    
    def rename_session(self, session_id: str, new_name: str) -> bool:
        """
        Renomeia uma sessão.
        
        Args:
            session_id: ID da sessão
            new_name: Novo nome
            
        Returns:
            True se a operação foi bem-sucedida
        """
        metadata = self.get_session(session_id)
        
        if not metadata:
            logger.error(f"Sessão não encontrada: {session_id}")
            return False
        
        # Atualizar nome
        metadata["name"] = new_name
        
        # Atualizar no armazenamento
        result = self.memory_manager.store_user_info(f"session:{session_id}", metadata)
        
        # Atualizar no cache
        if result:
            self.active_sessions[session_id] = metadata
            logger.info(f"Sessão renomeada: {session_id} -> {new_name}")
        
        return result
    
    def delete_session(self, session_id: str) -> bool:
        """
        Exclui uma sessão e seu histórico de conversas.
        
        Args:
            session_id: ID da sessão
            
        Returns:
            True se a operação foi bem-sucedida
        """
        # Verificar se a sessão existe
        if not self.get_session(session_id):
            logger.error(f"Sessão não encontrada: {session_id}")
            return False
        
        # Limpar histórico de conversas
        self.memory_manager.clear_conversation_history(session_id)
        
        # Remover metadados da sessão
        result = self.memory_manager.delete_user_info(f"session:{session_id}")
        
        # Remover do cache
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
        
        if result:
            logger.info(f"Sessão excluída: {session_id}")
        
        return result
    
    def add_message(self, 
                    session_id: str,
                    role: str,
                    content: str,
                    metadata: Optional[Dict[str, Any]] = None) -> int:
        """
        Adiciona uma mensagem a uma sessão.
        
        Args:
            session_id: ID da sessão
            role: Papel do emissor ('user', 'assistant', 'system')
            content: Conteúdo da mensagem
            metadata: Metadados adicionais (opcional)
            
        Returns:
            ID da mensagem adicionada
        """
        # Verificar se a sessão existe
        if not self.get_session(session_id):
            logger.error(f"Sessão não encontrada: {session_id}")
            return -1
        
        # Atualizar timestamp de atividade
        self.update_session_activity(session_id)
        
        # Adicionar mensagem
        return self.memory_manager.add_conversation_message(
            session_id=session_id,
            role=role,
            content=content,
            metadata=metadata
        )
    
    def get_messages(self, 
                     session_id: str,
                     limit: Optional[int] = None,
                     roles: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Obtém mensagens de uma sessão.
        
        Args:
            session_id: ID da sessão
            limit: Número máximo de mensagens a retornar (None = sem limite)
            roles: Lista de papéis a filtrar (None = todos)
            
        Returns:
            Lista de mensagens
        """
        # Verificar se a sessão existe
        if not self.get_session(session_id):
            logger.error(f"Sessão não encontrada: {session_id}")
            return []
        
        return self.memory_manager.get_conversation_history(
            session_id=session_id,
            limit=limit,
            roles=roles
        )
    
    def get_messages_for_llm(self, 
                             session_id: str,
                             limit: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Obtém mensagens formatadas para envio ao LLM.
        
        Args:
            session_id: ID da sessão
            limit: Número máximo de mensagens a retornar (None = sem limite)
            
        Returns:
            Lista de mensagens no formato esperado pelo LLM
        """
        # Verificar se a sessão existe
        if not self.get_session(session_id):
            logger.error(f"Sessão não encontrada: {session_id}")
            return []
        
        return self.memory_manager.get_conversation_messages_for_llm(
            session_id=session_id,
            limit=limit
        )
    
    def clear_session_history(self, session_id: str) -> bool:
        """
        Limpa o histórico de mensagens de uma sessão.
        
        Args:
            session_id: ID da sessão
            
        Returns:
            True se a operação foi bem-sucedida
        """
        # Verificar se a sessão existe
        if not self.get_session(session_id):
            logger.error(f"Sessão não encontrada: {session_id}")
            return False
        
        return self.memory_manager.clear_conversation_history(session_id)
    
    def export_session(self, session_id: str, output_file: str) -> bool:
        """
        Exporta uma sessão para um arquivo JSON.
        
        Args:
            session_id: ID da sessão
            output_file: Caminho para o arquivo de saída
            
        Returns:
            True se a operação foi bem-sucedida
        """
        # Verificar se a sessão existe
        metadata = self.get_session(session_id)
        if not metadata:
            logger.error(f"Sessão não encontrada: {session_id}")
            return False
        
        try:
            # Obter histórico de mensagens
            messages = self.memory_manager.get_conversation_history(session_id)
            
            # Criar estrutura de exportação
            export_data = {
                "session_id": session_id,
                "metadata": metadata,
                "messages": messages
            }
            
            # Salvar em arquivo
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Sessão exportada: {session_id} -> {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao exportar sessão: {e}")
            return False
    
    def import_session(self, input_file: str, new_session_id: Optional[str] = None) -> Optional[str]:
        """
        Importa uma sessão de um arquivo JSON.
        
        Args:
            input_file: Caminho para o arquivo de entrada
            new_session_id: ID para a nova sessão (None = gerar novo)
            
        Returns:
            ID da sessão importada ou None se falhou
        """
        try:
            # Carregar arquivo
            with open(input_file, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            # Extrair dados
            metadata = import_data.get("metadata", {})
            messages = import_data.get("messages", [])
            
            # Gerar novo ID de sessão se não especificado
            session_id = new_session_id or self.memory_manager.generate_session_id()
            
            # Atualizar metadados
            metadata["imported_from"] = import_data.get("session_id")
            metadata["imported_at"] = datetime.now().isoformat()
            metadata["last_activity"] = datetime.now().isoformat()
            
            # Armazenar metadados
            self.memory_manager.store_user_info(f"session:{session_id}", metadata)
            
            # Adicionar ao cache
            self.active_sessions[session_id] = metadata
            
            # Importar mensagens
            for msg in messages:
                self.memory_manager.add_conversation_message(
                    session_id=session_id,
                    role=msg.get("role", "user"),
                    content=msg.get("content", ""),
                    metadata=msg.get("metadata")
                )
            
            logger.info(f"Sessão importada: {input_file} -> {session_id}")
            return session_id
            
        except Exception as e:
            logger.error(f"Erro ao importar sessão: {e}")
            return None


if __name__ == "__main__":
    # Exemplo de uso
    import tempfile
    
    # Criar diretório temporário para memória
    temp_dir = tempfile.mkdtemp()
    
    # Inicializar gerenciador de sessões
    session_manager = SessionManager(temp_dir)
    
    # Criar sessão
    session_id = session_manager.create_session("Conversa de teste")
    print(f"Sessão criada: {session_id}")
    
    # Adicionar mensagens
    session_manager.add_message(session_id, "system", "Você é um assistente útil chamado Nina.")
    session_manager.add_message(session_id, "user", "Olá, como você está?")
    session_manager.add_message(session_id, "assistant", "Olá! Estou bem, obrigada por perguntar. Como posso ajudar você hoje?")
    
    # Obter mensagens
    messages = session_manager.get_messages(session_id)
    print("\nMensagens da sessão:")
    for msg in messages:
        print(f"[{msg['role']}] {msg['content']}")
    
    # Listar sessões
    sessions = session_manager.list_sessions()
    print("\nSessões disponíveis:")
    for session in sessions:
        print(f"- {session['name']} (ID: {session['id']})")
    
    # Exportar sessão
    export_file = os.path.join(temp_dir, "sessao_exportada.json")
    session_manager.export_session(session_id, export_file)
    print(f"\nSessão exportada para: {export_file}")
