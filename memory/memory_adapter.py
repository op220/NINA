import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("nina_memory_adapter")

class NinaMemoryAdapter:
    """
    Adaptador para integrar o sistema de memória com o orquestrador principal da Nina IA.
    Esta classe é responsável por adaptar as chamadas do orquestrador para o sistema de memória.
    """
    
    def __init__(self, memory_integrator=None, config_path=None):
        """
        Inicializa o adaptador de memória.
        
        Args:
            memory_integrator: Instância do NinaMemoryIntegrator (opcional)
            config_path: Caminho para o arquivo de configuração (opcional)
        """
        self.config = self._load_config(config_path)
        
        # Se não foi fornecido um integrador, criar um novo
        if memory_integrator is None:
            try:
                from core.memory_integrator import NinaMemoryIntegrator
                
                memory_db_path = self.config.get('memory_db_path', 'memory.db')
                profiles_dir = self.config.get('profiles_dir', 'data/profiles')
                
                self.memory_integrator = NinaMemoryIntegrator(
                    memory_db_path=memory_db_path,
                    profiles_dir=profiles_dir
                )
                logger.info(f"Inicializado NinaMemoryIntegrator com DB: {memory_db_path}")
            except ImportError as e:
                logger.error(f"Erro ao importar NinaMemoryIntegrator: {e}")
                self.memory_integrator = None
        else:
            self.memory_integrator = memory_integrator
            
        self.enabled = self.config.get('enabled', True)
        
    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Carrega a configuração do adaptador.
        
        Args:
            config_path: Caminho para o arquivo de configuração
            
        Returns:
            Dicionário com configurações
        """
        default_config = {
            'enabled': True,
            'memory_db_path': 'memory.db',
            'profiles_dir': 'data/profiles',
            'max_context_interactions': 10,
            'backup_dir': 'backups',
            'auto_backup': True,
            'auto_backup_interval': 24  # horas
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    # Mesclar configurações padrão com as do usuário
                    config = {**default_config, **user_config}
                    logger.info(f"Configuração carregada de {config_path}")
                    return config
            except Exception as e:
                logger.error(f"Erro ao carregar configuração: {e}")
                return default_config
        else:
            logger.info("Usando configuração padrão")
            return default_config
            
    def is_enabled(self) -> bool:
        """
        Verifica se o sistema de memória está habilitado.
        
        Returns:
            True se o sistema estiver habilitado, False caso contrário
        """
        return self.enabled and self.memory_integrator is not None
        
    def process_input(self, text: str, user_id: str, channel_id: str, 
                     metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Processa uma entrada de texto e armazena na memória.
        
        Args:
            text: Texto da mensagem
            user_id: ID do usuário que enviou a mensagem
            channel_id: ID do canal onde a mensagem foi enviada
            metadata: Metadados adicionais (opcional)
            
        Returns:
            Dicionário com informações processadas ou vazio se desabilitado
        """
        if not self.is_enabled():
            logger.warning("Sistema de memória desabilitado, ignorando entrada")
            return {}
            
        try:
            timestamp = None
            if metadata and 'timestamp' in metadata:
                if isinstance(metadata['timestamp'], str):
                    timestamp = datetime.fromisoformat(metadata['timestamp'])
                elif isinstance(metadata['timestamp'], datetime):
                    timestamp = metadata['timestamp']
                    
            result = self.memory_integrator.process_input(
                text=text,
                user_id=user_id,
                channel_id=channel_id,
                timestamp=timestamp
            )
            
            logger.info(f"Processada entrada do usuário {user_id} no canal {channel_id}")
            return result
        except Exception as e:
            logger.error(f"Erro ao processar entrada: {e}")
            return {}
            
    def enrich_context(self, context: Dict[str, Any], user_id: str, 
                      channel_id: str) -> Dict[str, Any]:
        """
        Enriquece o contexto da conversa com informações da memória.
        
        Args:
            context: Contexto atual da conversa
            user_id: ID do usuário
            channel_id: ID do canal
            
        Returns:
            Contexto enriquecido com informações da memória
        """
        if not self.is_enabled():
            logger.warning("Sistema de memória desabilitado, retornando contexto original")
            return context
            
        try:
            max_interactions = self.config.get('max_context_interactions', 10)
            
            memory_context = self.memory_integrator.get_context_for_response(
                user_id=user_id,
                channel_id=channel_id,
                max_interactions=max_interactions
            )
            
            # Mesclar contexto original com informações da memória
            enriched_context = {**context, 'memory': memory_context}
            
            # Adicionar informações de personalidade ao contexto principal
            if 'personality' in memory_context:
                enriched_context['personality'] = memory_context['personality']
                
            logger.info(f"Contexto enriquecido para usuário {user_id} no canal {channel_id}")
            return enriched_context
        except Exception as e:
            logger.error(f"Erro ao enriquecer contexto: {e}")
            return context
            
    def update_after_response(self, response_text: str, user_id: str, 
                            channel_id: str) -> None:
        """
        Atualiza a memória após uma resposta da Nina.
        
        Args:
            response_text: Texto da resposta da Nina
            user_id: ID do usuário para quem respondeu
            channel_id: ID do canal onde respondeu
        """
        if not self.is_enabled():
            logger.warning("Sistema de memória desabilitado, ignorando atualização")
            return
            
        try:
            self.memory_integrator.update_after_response(
                response_text=response_text,
                user_id=user_id,
                channel_id=channel_id
            )
            
            logger.info(f"Memória atualizada após resposta para usuário {user_id}")
        except Exception as e:
            logger.error(f"Erro ao atualizar memória após resposta: {e}")
            
    def adapt_personality(self, channel_id: str) -> Dict[str, Any]:
        """
        Adapta a personalidade da Nina com base no histórico do canal.
        
        Args:
            channel_id: ID do canal
            
        Returns:
            Personalidade adaptada ou vazio se desabilitado
        """
        if not self.is_enabled():
            logger.warning("Sistema de memória desabilitado, ignorando adaptação de personalidade")
            return {}
            
        try:
            personality = self.memory_integrator.adapt_personality(channel_id)
            logger.info(f"Personalidade adaptada para o canal {channel_id}")
            return personality
        except Exception as e:
            logger.error(f"Erro ao adaptar personalidade: {e}")
            return {}
            
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Obtém o perfil de um usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Perfil do usuário ou vazio se desabilitado
        """
        if not self.is_enabled():
            logger.warning("Sistema de memória desabilitado, ignorando obtenção de perfil")
            return {}
            
        try:
            return self.memory_integrator.memory_manager.get_user_profile(user_id)
        except Exception as e:
            logger.error(f"Erro ao obter perfil do usuário: {e}")
            return {}
            
    def get_channel_profile(self, channel_id: str) -> Dict[str, Any]:
        """
        Obtém o perfil de um canal.
        
        Args:
            channel_id: ID do canal
            
        Returns:
            Perfil do canal ou vazio se desabilitado
        """
        if not self.is_enabled():
            logger.warning("Sistema de memória desabilitado, ignorando obtenção de perfil")
            return {}
            
        try:
            return self.memory_integrator.memory_manager.get_channel_profile(channel_id)
        except Exception as e:
            logger.error(f"Erro ao obter perfil do canal: {e}")
            return {}
            
    def create_backup(self) -> str:
        """
        Cria um backup do sistema de memória.
        
        Returns:
            Caminho para o arquivo de backup ou string vazia se falhar
        """
        if not self.is_enabled():
            logger.warning("Sistema de memória desabilitado, ignorando backup")
            return ""
            
        try:
            backup_dir = self.config.get('backup_dir', 'backups')
            
            # Garantir que o diretório de backup existe
            os.makedirs(backup_dir, exist_ok=True)
            
            backup_file = self.memory_integrator.backup_memory(backup_dir)
            logger.info(f"Backup criado em {backup_file}")
            return backup_file
        except Exception as e:
            logger.error(f"Erro ao criar backup: {e}")
            return ""
