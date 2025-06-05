"""
Módulo de inicialização do sistema de memória de longo prazo da Nina IA.
Fornece funções para inicializar e acessar o sistema de memória.
"""

import os
import logging
from typing import Dict, Any, Optional

from .database import MemoryDatabase
from .memory_manager import MemoryManager
from .pattern_analyzer import PatternAnalyzer

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("memory_system.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("MemorySystem")

class MemorySystem:
    """
    Classe principal para o sistema de memória de longo prazo.
    Fornece uma interface unificada para todos os componentes do sistema.
    """
    
    def __init__(self, db_path: str = "memory.db", data_dir: str = "memory_data"):
        """
        Inicializa o sistema de memória.
        
        Args:
            db_path: Caminho para o arquivo do banco de dados SQLite
            data_dir: Diretório para armazenar os arquivos de dados
        """
        # Criar diretórios se não existirem
        os.makedirs(data_dir, exist_ok=True)
        
        # Inicializar componentes
        self.memory_manager = MemoryManager(db_path, data_dir)
        self.pattern_analyzer = PatternAnalyzer()
        
        logger.info(f"Sistema de memória inicializado: {db_path}, {data_dir}")
    
    def process_message(self, user_id: str, username: str, channel_id: str, 
                       guild_id: str, channel_name: str, channel_type: str, 
                       content: str) -> Dict[str, Any]:
        """
        Processa uma mensagem e atualiza o sistema de memória.
        
        Args:
            user_id: ID do usuário
            username: Nome do usuário
            channel_id: ID do canal
            guild_id: ID do servidor
            channel_name: Nome do canal
            channel_type: Tipo do canal
            content: Conteúdo da mensagem
            
        Returns:
            Dicionário com resultados do processamento
        """
        try:
            # Registrar usuário e canal
            self.memory_manager.register_user(user_id, username)
            self.memory_manager.register_channel(channel_id, guild_id, channel_name, channel_type)
            
            # Analisar mensagem
            analysis = self.pattern_analyzer.analyze_message(content)
            
            # Processar mensagem
            interaction_id = self.memory_manager.process_message(
                user_id=user_id,
                channel_id=channel_id,
                content=content,
                sentiment=analysis["sentiment"],
                topics=analysis["topics"]
            )
            
            # Registrar expressões detectadas
            for expression in analysis["expressions"]:
                self.memory_manager.add_user_expression(user_id, expression)
            
            return {
                "interaction_id": interaction_id,
                "analysis": analysis
            }
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
            return {
                "interaction_id": -1,
                "analysis": {},
                "error": str(e)
            }
    
    def process_voice_activity(self, user_id: str, username: str, channel_id: str, 
                              guild_id: str, channel_name: str, duration: int) -> bool:
        """
        Processa uma atividade de voz e atualiza o sistema de memória.
        
        Args:
            user_id: ID do usuário
            username: Nome do usuário
            channel_id: ID do canal
            guild_id: ID do servidor
            channel_name: Nome do canal
            duration: Duração da atividade em segundos
            
        Returns:
            True se a operação foi bem-sucedida, False caso contrário
        """
        try:
            # Registrar usuário e canal
            self.memory_manager.register_user(user_id, username)
            self.memory_manager.register_channel(channel_id, guild_id, channel_name, "voice")
            
            # Processar atividade de voz
            return self.memory_manager.process_voice_activity(user_id, channel_id, duration)
        except Exception as e:
            logger.error(f"Erro ao processar atividade de voz: {e}")
            return False
    
    def get_user_context(self, user_id: str) -> Dict[str, Any]:
        """
        Obtém o contexto de um usuário para uso pelo sistema Nina IA.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Dicionário com o contexto do usuário
        """
        return self.memory_manager.get_user_context(user_id)
    
    def get_channel_context(self, channel_id: str) -> Dict[str, Any]:
        """
        Obtém o contexto de um canal para uso pelo sistema Nina IA.
        
        Args:
            channel_id: ID do canal
            
        Returns:
            Dicionário com o contexto do canal
        """
        return self.memory_manager.get_channel_context(channel_id)
    
    def get_combined_context(self, user_id: str, channel_id: str) -> Dict[str, Any]:
        """
        Obtém um contexto combinado de usuário e canal para uso pelo sistema Nina IA.
        
        Args:
            user_id: ID do usuário
            channel_id: ID do canal
            
        Returns:
            Dicionário com o contexto combinado
        """
        user_context = self.get_user_context(user_id)
        channel_context = self.get_channel_context(channel_id)
        
        # Combinar contextos
        combined_context = {
            "user": user_context,
            "channel": channel_context
        }
        
        return combined_context
    
    def update_nina_personality(self, channel_id: str, personality: Dict[str, Any]) -> bool:
        """
        Atualiza a personalidade da Nina para um canal específico.
        
        Args:
            channel_id: ID do canal
            personality: Dicionário com configurações de personalidade
            
        Returns:
            True se a operação foi bem-sucedida, False caso contrário
        """
        return self.memory_manager.update_nina_personality(channel_id, personality)
    
    def suggest_nina_personality(self, channel_id: str) -> Dict[str, Any]:
        """
        Sugere configurações de personalidade para a Nina com base no padrão do canal.
        
        Args:
            channel_id: ID do canal
            
        Returns:
            Dicionário com configurações de personalidade sugeridas
        """
        try:
            # Obter mensagens recentes do canal
            channel_interactions = self.memory_manager.db.get_channel_interactions(channel_id, limit=100)
            
            if not channel_interactions:
                return {
                    "formality_level": 50,
                    "humor_level": 50,
                    "technicality_level": 50,
                    "response_speed": "médio",
                    "verbosity": "médio"
                }
            
            # Formatar mensagens para análise
            messages = []
            for interaction in channel_interactions:
                if "content_summary" in interaction and interaction["content_summary"]:
                    messages.append({
                        "user_id": interaction["user_id"],
                        "content": interaction["content_summary"]
                    })
            
            # Analisar padrão do canal
            channel_pattern = self.pattern_analyzer.analyze_channel_pattern(messages)
            
            # Sugerir personalidade
            return self.pattern_analyzer.suggest_nina_personality(channel_pattern)
        except Exception as e:
            logger.error(f"Erro ao sugerir personalidade da Nina: {e}")
            return {
                "formality_level": 50,
                "humor_level": 50,
                "technicality_level": 50,
                "response_speed": "médio",
                "verbosity": "médio"
            }
    
    def search(self, query: str, search_type: str = "all", limit: int = 20) -> Dict[str, Any]:
        """
        Realiza uma busca no sistema de memória.
        
        Args:
            query: Termo de busca
            search_type: Tipo de busca (all, users, channels, topics)
            limit: Número máximo de resultados por categoria
            
        Returns:
            Dicionário com resultados da busca
        """
        return self.memory_manager.search(query, search_type, limit)
    
    def delete_user_memory(self, user_id: str) -> bool:
        """
        Remove todas as memórias associadas a um usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            True se a operação foi bem-sucedida, False caso contrário
        """
        return self.memory_manager.delete_user_memory(user_id)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Obtém estatísticas gerais do sistema de memória.
        
        Returns:
            Dicionário com estatísticas
        """
        return self.memory_manager.get_statistics()
    
    def backup(self, backup_path: str) -> bool:
        """
        Cria um backup do sistema de memória.
        
        Args:
            backup_path: Caminho para o arquivo de backup
            
        Returns:
            True se a operação foi bem-sucedida, False caso contrário
        """
        return self.memory_manager.backup(backup_path)
    
    def restore(self, backup_path: str) -> bool:
        """
        Restaura o sistema de memória a partir de um backup.
        
        Args:
            backup_path: Caminho para o arquivo de backup
            
        Returns:
            True se a operação foi bem-sucedida, False caso contrário
        """
        return self.memory_manager.restore(backup_path)

# Instância global do sistema de memória
_memory_system = None

def init_memory_system(db_path: str = "memory.db", data_dir: str = "memory_data") -> MemorySystem:
    """
    Inicializa o sistema de memória global.
    
    Args:
        db_path: Caminho para o arquivo do banco de dados SQLite
        data_dir: Diretório para armazenar os arquivos de dados
        
    Returns:
        Instância do sistema de memória
    """
    global _memory_system
    if _memory_system is None:
        _memory_system = MemorySystem(db_path, data_dir)
    return _memory_system

def get_memory_system() -> Optional[MemorySystem]:
    """
    Obtém a instância global do sistema de memória.
    
    Returns:
        Instância do sistema de memória ou None se não inicializado
    """
    global _memory_system
    return _memory_system
