import sys
import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple

# Adicionar o diretório raiz ao path para importar outros módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.memory_manager import MemoryManager
from core.personality_manager import PersonalityManager


class NinaMemoryIntegrator:
    """
    Classe responsável por integrar o sistema de memória de longo prazo com a Nina IA existente.
    Serve como ponte entre o sistema de memória e o orquestrador principal da Nina.
    """
    
    def __init__(self, memory_db_path: str, profiles_dir: str):
        """
        Inicializa o integrador de memória.
        
        Args:
            memory_db_path: Caminho para o banco de dados SQLite de memória
            profiles_dir: Diretório onde os perfis de personalidade são armazenados
        """
        self.memory_manager = MemoryManager(db_path=memory_db_path)
        self.personality_manager = PersonalityManager(profiles_dir=profiles_dir)
        self.current_user_id = None
        self.current_channel_id = None
        
    def set_context(self, user_id: str, channel_id: str) -> None:
        """
        Define o contexto atual para interação (usuário e canal).
        
        Args:
            user_id: ID do usuário atual
            channel_id: ID do canal atual
        """
        self.current_user_id = user_id
        self.current_channel_id = channel_id
        
    def process_input(self, text: str, user_id: str, channel_id: str, 
                     timestamp: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Processa uma entrada de texto, armazena na memória e extrai informações relevantes.
        
        Args:
            text: Texto da mensagem
            user_id: ID do usuário que enviou a mensagem
            channel_id: ID do canal onde a mensagem foi enviada
            timestamp: Timestamp da mensagem (opcional, usa o atual se não fornecido)
            
        Returns:
            Dicionário com informações extraídas e metadados da mensagem
        """
        if timestamp is None:
            timestamp = datetime.now()
            
        # Definir contexto atual
        self.set_context(user_id, channel_id)
        
        # Armazenar a mensagem na memória
        interaction_id = self.memory_manager.store_interaction(
            user_id=user_id,
            channel_id=channel_id,
            content=text,
            timestamp=timestamp
        )
        
        # Analisar a mensagem para extrair informações
        analysis = self.memory_manager.analyze_interaction(text)
        
        # Atualizar perfil do usuário com base na análise
        self.memory_manager.update_user_profile(
            user_id=user_id,
            topics=analysis.get('topics', []),
            emotions=analysis.get('emotions', []),
            expressions=analysis.get('expressions', [])
        )
        
        # Atualizar perfil do canal com base na análise
        self.memory_manager.update_channel_profile(
            channel_id=channel_id,
            topics=analysis.get('topics', []),
            tone=analysis.get('tone', 'neutral')
        )
        
        # Retornar informações processadas
        return {
            'interaction_id': interaction_id,
            'analysis': analysis,
            'user_profile': self.memory_manager.get_user_profile(user_id),
            'channel_profile': self.memory_manager.get_channel_profile(channel_id)
        }
        
    def get_context_for_response(self, user_id: str, channel_id: str, 
                               max_interactions: int = 10) -> Dict[str, Any]:
        """
        Obtém o contexto necessário para gerar uma resposta personalizada.
        
        Args:
            user_id: ID do usuário para quem responder
            channel_id: ID do canal onde responder
            max_interactions: Número máximo de interações anteriores a incluir
            
        Returns:
            Dicionário com contexto para resposta
        """
        # Definir contexto atual
        self.set_context(user_id, channel_id)
        
        # Obter perfil do usuário
        user_profile = self.memory_manager.get_user_profile(user_id)
        
        # Obter perfil do canal
        channel_profile = self.memory_manager.get_channel_profile(channel_id)
        
        # Obter personalidade adaptada para o canal
        personality = self.personality_manager.get_channel_personality(channel_id)
        
        # Obter interações recentes no canal
        recent_interactions = self.memory_manager.get_recent_interactions(
            channel_id=channel_id,
            limit=max_interactions
        )
        
        # Construir contexto para resposta
        context = {
            'user_profile': user_profile,
            'channel_profile': channel_profile,
            'personality': personality,
            'recent_interactions': recent_interactions,
            'timestamp': datetime.now().isoformat()
        }
        
        return context
        
    def adapt_personality(self, channel_id: str) -> Dict[str, Any]:
        """
        Adapta a personalidade da Nina com base no histórico do canal.
        
        Args:
            channel_id: ID do canal para adaptar a personalidade
            
        Returns:
            Personalidade adaptada
        """
        # Obter perfil do canal
        channel_profile = self.memory_manager.get_channel_profile(channel_id)
        
        # Obter personalidade base
        base_personality = self.personality_manager.get_default_personality()
        
        # Adaptar personalidade com base no perfil do canal
        adapted_personality = self.personality_manager.adapt_personality(
            base_personality=base_personality,
            channel_profile=channel_profile
        )
        
        # Salvar personalidade adaptada para o canal
        self.personality_manager.save_channel_personality(
            channel_id=channel_id,
            personality=adapted_personality
        )
        
        return adapted_personality
        
    def update_after_response(self, response_text: str, user_id: str, 
                            channel_id: str) -> None:
        """
        Atualiza a memória após uma resposta da Nina.
        
        Args:
            response_text: Texto da resposta da Nina
            user_id: ID do usuário para quem respondeu
            channel_id: ID do canal onde respondeu
        """
        # Armazenar a resposta na memória
        self.memory_manager.store_interaction(
            user_id='nina',  # ID especial para a própria Nina
            channel_id=channel_id,
            content=response_text,
            timestamp=datetime.now(),
            is_nina_response=True,
            target_user_id=user_id
        )
        
    def get_user_memories(self, user_id: str) -> Dict[str, Any]:
        """
        Obtém todas as memórias relacionadas a um usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Dicionário com todas as memórias do usuário
        """
        return {
            'profile': self.memory_manager.get_user_profile(user_id),
            'interactions': self.memory_manager.get_user_interactions(user_id),
            'topics': self.memory_manager.get_user_topics(user_id),
            'emotions': self.memory_manager.get_user_emotions(user_id),
            'expressions': self.memory_manager.get_user_expressions(user_id)
        }
        
    def get_channel_memories(self, channel_id: str) -> Dict[str, Any]:
        """
        Obtém todas as memórias relacionadas a um canal.
        
        Args:
            channel_id: ID do canal
            
        Returns:
            Dicionário com todas as memórias do canal
        """
        return {
            'profile': self.memory_manager.get_channel_profile(channel_id),
            'interactions': self.memory_manager.get_channel_interactions(channel_id),
            'topics': self.memory_manager.get_channel_topics(channel_id),
            'users': self.memory_manager.get_channel_users(channel_id),
            'personality': self.personality_manager.get_channel_personality(channel_id)
        }
        
    def clear_user_memory(self, user_id: str) -> bool:
        """
        Limpa todas as memórias de um usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            True se bem-sucedido, False caso contrário
        """
        try:
            self.memory_manager.clear_user_memory(user_id)
            return True
        except Exception as e:
            print(f"Erro ao limpar memória do usuário: {e}")
            return False
            
    def clear_channel_memory(self, channel_id: str) -> bool:
        """
        Limpa todas as memórias de um canal.
        
        Args:
            channel_id: ID do canal
            
        Returns:
            True se bem-sucedido, False caso contrário
        """
        try:
            self.memory_manager.clear_channel_memory(channel_id)
            return True
        except Exception as e:
            print(f"Erro ao limpar memória do canal: {e}")
            return False
            
    def backup_memory(self, backup_dir: str) -> str:
        """
        Cria um backup do sistema de memória.
        
        Args:
            backup_dir: Diretório onde salvar o backup
            
        Returns:
            Caminho para o arquivo de backup
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"memory_backup_{timestamp}.db")
        
        try:
            self.memory_manager.create_backup(backup_file)
            return backup_file
        except Exception as e:
            print(f"Erro ao criar backup: {e}")
            return ""
            
    def restore_memory(self, backup_file: str) -> bool:
        """
        Restaura o sistema de memória a partir de um backup.
        
        Args:
            backup_file: Caminho para o arquivo de backup
            
        Returns:
            True se bem-sucedido, False caso contrário
        """
        try:
            self.memory_manager.restore_from_backup(backup_file)
            return True
        except Exception as e:
            print(f"Erro ao restaurar backup: {e}")
            return False
