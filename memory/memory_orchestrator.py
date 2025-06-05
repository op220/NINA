import os
import sys
import json
import logging
from typing import Dict, List, Any, Optional

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("nina_orchestrator_extension")

class MemoryOrchestrator:
    """
    Extensão do orquestrador principal da Nina IA para integrar o sistema de memória.
    Esta classe estende o orquestrador existente com funcionalidades de memória de longo prazo.
    """
    
    def __init__(self, config_path=None):
        """
        Inicializa a extensão do orquestrador.
        
        Args:
            config_path: Caminho para o arquivo de configuração (opcional)
        """
        self.config = self._load_config(config_path)
        
        # Inicializar adaptador de memória
        try:
            from memory.memory_manager import MemoryManagerpter
            self.memory_adapter = NinaMemoryAdapter(config_path=config_path)
            logger.info("Adaptador de memória inicializado com sucesso")
        except ImportError as e:
            logger.error(f"Erro ao importar NinaMemoryAdapter: {e}")
            self.memory_adapter = None
            
        # Inicializar adaptador de personalidade
        try:
            from core.personality_manager import PersonalityManager
            profiles_dir = self.config.get('profiles_dir', 'data/profiles')
            self.personality_manager = PersonalityManager(profiles_dir=profiles_dir)
            logger.info(f"Gerenciador de personalidade inicializado com diretório: {profiles_dir}")
        except ImportError as e:
            logger.error(f"Erro ao importar PersonalityManager: {e}")
            self.personality_manager = None
            
    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Carrega a configuração da extensão.
        
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
            'auto_backup_interval': 24,  # horas
            'memory_weight': 0.7,  # peso das informações de memória no contexto
            'personality_adaptation_enabled': True
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
        Verifica se a extensão de memória está habilitada.
        
        Returns:
            True se a extensão estiver habilitada, False caso contrário
        """
        return self.config.get('enabled', True) and self.memory_adapter is not None
        
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa uma mensagem recebida, armazenando na memória e enriquecendo com contexto.
        
        Args:
            message: Dicionário com informações da mensagem
            
        Returns:
            Mensagem enriquecida com informações de memória
        """
        if not self.is_enabled():
            logger.warning("Extensão de memória desabilitada, retornando mensagem original")
            return message
            
        try:
            # Extrair informações da mensagem
            text = message.get('text', '')
            user_id = message.get('user_id', '')
            channel_id = message.get('channel_id', '')
            metadata = message.get('metadata', {})
            
            # Processar entrada e armazenar na memória
            memory_data = self.memory_adapter.process_input(
                text=text,
                user_id=user_id,
                channel_id=channel_id,
                metadata=metadata
            )
            
            # Adicionar informações de memória à mensagem
            enriched_message = {**message, 'memory_data': memory_data}
            
            logger.info(f"Mensagem processada e enriquecida com memória para usuário {user_id}")
            return enriched_message
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
            return message
            
    def enrich_context(self, context: Dict[str, Any], message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enriquece o contexto da conversa com informações da memória.
        
        Args:
            context: Contexto atual da conversa
            message: Mensagem processada
            
        Returns:
            Contexto enriquecido com informações da memória
        """
        if not self.is_enabled():
            logger.warning("Extensão de memória desabilitada, retornando contexto original")
            return context
            
        try:
            user_id = message.get('user_id', '')
            channel_id = message.get('channel_id', '')
            
            # Enriquecer contexto com informações da memória
            enriched_context = self.memory_adapter.enrich_context(
                context=context,
                user_id=user_id,
                channel_id=channel_id
            )
            
            logger.info(f"Contexto enriquecido para usuário {user_id} no canal {channel_id}")
            return enriched_context
        except Exception as e:
            logger.error(f"Erro ao enriquecer contexto: {e}")
            return context
            
    def adapt_personality_for_response(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapta a personalidade da Nina com base no contexto da conversa.
        
        Args:
            message: Mensagem processada
            
        Returns:
            Personalidade adaptada para o contexto atual
        """
        if not self.is_enabled() or not self.config.get('personality_adaptation_enabled', True):
            logger.warning("Adaptação de personalidade desabilitada")
            return {}
            
        try:
            channel_id = message.get('channel_id', '')
            
            # Adaptar personalidade com base no canal
            personality = self.memory_adapter.adapt_personality(channel_id)
            
            logger.info(f"Personalidade adaptada para o canal {channel_id}")
            return personality
        except Exception as e:
            logger.error(f"Erro ao adaptar personalidade: {e}")
            return {}
            
    def update_after_response(self, response: Dict[str, Any], message: Dict[str, Any]) -> None:
        """
        Atualiza a memória após uma resposta da Nina.
        
        Args:
            response: Resposta gerada pela Nina
            message: Mensagem original que gerou a resposta
        """
        if not self.is_enabled():
            logger.warning("Extensão de memória desabilitada, ignorando atualização")
            return
            
        try:
            response_text = response.get('text', '')
            user_id = message.get('user_id', '')
            channel_id = message.get('channel_id', '')
            
            # Atualizar memória com a resposta
            self.memory_adapter.update_after_response(
                response_text=response_text,
                user_id=user_id,
                channel_id=channel_id
            )
            
            logger.info(f"Memória atualizada após resposta para usuário {user_id}")
        except Exception as e:
            logger.error(f"Erro ao atualizar memória após resposta: {e}")
            
    def format_memory_for_llm(self, memory_data: Dict[str, Any]) -> str:
        """
        Formata os dados de memória para inclusão no prompt do LLM.
        
        Args:
            memory_data: Dados de memória
            
        Returns:
            String formatada com informações de memória para o LLM
        """
        try:
            if not memory_data:
                return ""
                
            # Formatar perfil do usuário
            user_profile = memory_data.get('user_profile', {})
            user_info = []
            
            if user_profile:
                user_info.append(f"Nome do usuário: {user_profile.get('username', 'Desconhecido')}")
                
                # Adicionar tópicos de interesse
                topics = user_profile.get('topics', {})
                if topics:
                    top_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)[:3]
                    topics_str = ", ".join([f"{topic}" for topic, _ in top_topics])
                    user_info.append(f"Tópicos de interesse: {topics_str}")
                    
                # Adicionar emoções predominantes
                emotions = user_profile.get('emotions', {})
                if emotions:
                    top_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:2]
                    emotions_str = ", ".join([f"{emotion}" for emotion, _ in top_emotions])
                    user_info.append(f"Emoções predominantes: {emotions_str}")
                    
                # Adicionar expressões frequentes
                expressions = user_profile.get('expressions', [])
                if expressions:
                    expressions_str = ", ".join([f'"{expr}"' for expr in expressions[:3]])
                    user_info.append(f"Expressões frequentes: {expressions_str}")
                    
            # Formatar perfil do canal
            channel_profile = memory_data.get('channel_profile', {})
            channel_info = []
            
            if channel_profile:
                channel_info.append(f"Canal: {channel_profile.get('channel_name', 'Desconhecido')}")
                
                # Adicionar tópicos do canal
                topics = channel_profile.get('topics', {})
                if topics:
                    top_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)[:3]
                    topics_str = ", ".join([f"{topic}" for topic, _ in top_topics])
                    channel_info.append(f"Tópicos do canal: {topics_str}")
                    
                # Adicionar tom do canal
                tone = channel_profile.get('tone', 'neutro')
                channel_info.append(f"Tom do canal: {tone}")
                
            # Formatar personalidade
            personality = memory_data.get('personality', {})
            personality_info = []
            
            if personality:
                formality = personality.get('formality_level', 50)
                if formality < 30:
                    personality_info.append("Estilo: informal")
                elif formality < 70:
                    personality_info.append("Estilo: neutro")
                else:
                    personality_info.append("Estilo: formal")
                    
                humor = personality.get('humor_level', 50)
                if humor > 70:
                    personality_info.append("Humor: presente")
                    
                technicality = personality.get('technicality_level', 50)
                if technicality < 30:
                    personality_info.append("Explicações: simples")
                elif technicality > 70:
                    personality_info.append("Explicações: técnicas")
                    
                verbosity = personality.get('verbosity', 'médio')
                if verbosity == 'conciso':
                    personality_info.append("Respostas: concisas")
                elif verbosity == 'detalhado':
                    personality_info.append("Respostas: detalhadas")
                
            # Combinar todas as informações
            memory_sections = []
            
            if user_info:
                memory_sections.append("Informações do Usuário:\n" + "\n".join([f"- {info}" for info in user_info]))
                
            if channel_info:
                memory_sections.append("Informações do Canal:\n" + "\n".join([f"- {info}" for info in channel_info]))
                
            if personality_info:
                memory_sections.append("Personalidade:\n" + "\n".join([f"- {info}" for info in personality_info]))
                
            # Adicionar interações recentes se disponíveis
            recent_interactions = memory_data.get('recent_interactions', [])
            if recent_interactions:
                interactions_str = []
                for i, interaction in enumerate(recent_interactions[-3:]):  # Últimas 3 interações
                    user = interaction.get('user_id', 'Desconhecido')
                    content = interaction.get('content', '')
                    interactions_str.append(f"{user}: {content}")
                
                if interactions_str:
                    memory_sections.append("Contexto Recente:\n" + "\n".join(interactions_str))
            
            return "\n\n".join(memory_sections)
        except Exception as e:
            logger.error(f"Erro ao formatar memória para LLM: {e}")
            return ""
            
    def create_backup(self) -> str:
        """
        Cria um backup do sistema de memória.
        
        Returns:
            Caminho para o arquivo de backup ou string vazia se falhar
        """
        if not self.is_enabled():
            logger.warning("Extensão de memória desabilitada, ignorando backup")
            return ""
            
        try:
            return self.memory_adapter.create_backup()
        except Exception as e:
            logger.error(f"Erro ao criar backup: {e}")
            return ""
