# Sistema de Personalidade por Canal para Discord

## Visão Geral

O sistema de personalidade por canal permite que a Nina IA adapte seu comportamento de forma diferente em diferentes canais do Discord. Isso possibilita que a IA desenvolva "personas" distintas com base nas interações específicas de cada canal, tornando suas respostas mais contextualizadas e apropriadas para diferentes comunidades e tópicos de discussão.

## Arquitetura do Sistema

### Componentes Principais

1. **Gerenciador de Perfis de Canal**: Mantém perfis de personalidade separados para cada canal
2. **Seletor de Contexto**: Seleciona o perfil apropriado com base no canal atual
3. **Armazenamento de Perfis**: Sistema de persistência para perfis de canal
4. **Adaptador de Canal**: Ajusta o comportamento da IA com base no perfil do canal
5. **Integração com Discord**: Identifica canais e gerencia contextos de conversas

### Fluxo de Dados

1. Uma mensagem é recebida de um canal específico do Discord
2. O sistema identifica o canal e carrega o perfil de personalidade correspondente
3. O contexto de personalidade é aplicado ao processamento da mensagem
4. A resposta é gerada considerando as características específicas do canal
5. As interações são analisadas para continuar evoluindo o perfil do canal

## Implementação

### Gerenciador de Perfis de Canal

```python
import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Union

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("channel_profile_manager.log")
    ]
)
logger = logging.getLogger("ChannelProfileManager")

class ChannelProfileManager:
    """
    Gerenciador de perfis de personalidade por canal.
    """
    
    def __init__(self, profiles_dir: str = "./data/profiles/channels", 
                personality_manager=None):
        """
        Inicializa o gerenciador de perfis de canal.
        
        Args:
            profiles_dir: Diretório para armazenar perfis de canal
            personality_manager: Instância do gerenciador de personalidade principal
        """
        self.profiles_dir = profiles_dir
        self.personality_manager = personality_manager
        self.active_profiles = {}  # guild_id_channel_id -> profile
        
        # Garantir que o diretório exista
        os.makedirs(profiles_dir, exist_ok=True)
        
        logger.info(f"Gerenciador de perfis de canal inicializado. Diretório: {profiles_dir}")
    
    def set_personality_manager(self, personality_manager) -> None:
        """
        Define o gerenciador de personalidade principal.
        
        Args:
            personality_manager: Instância do gerenciador de personalidade
        """
        self.personality_manager = personality_manager
        logger.info("Gerenciador de personalidade definido")
    
    def get_profile_path(self, guild_id: str, channel_id: str) -> str:
        """
        Obtém o caminho para o arquivo de perfil de um canal.
        
        Args:
            guild_id: ID do servidor
            channel_id: ID do canal
            
        Returns:
            Caminho para o arquivo de perfil
        """
        return os.path.join(self.profiles_dir, f"{guild_id}_{channel_id}.json")
    
    def load_profile(self, guild_id: str, channel_id: str) -> Dict[str, Any]:
        """
        Carrega o perfil de um canal.
        
        Args:
            guild_id: ID do servidor
            channel_id: ID do canal
            
        Returns:
            Dicionário com perfil do canal
        """
        try:
            channel_key = f"{guild_id}_{channel_id}"
            
            # Verificar se o perfil já está carregado
            if channel_key in self.active_profiles:
                return self.active_profiles[channel_key]
            
            # Caminho do arquivo
            profile_path = self.get_profile_path(guild_id, channel_id)
            
            # Verificar se o arquivo existe
            if os.path.exists(profile_path):
                # Carregar perfil
                with open(profile_path, 'r', encoding='utf-8') as f:
                    profile = json.load(f)
                
                # Armazenar no cache
                self.active_profiles[channel_key] = profile
                
                logger.info(f"Perfil carregado para o canal {channel_key}")
                return profile
            else:
                # Criar perfil padrão
                profile = self._create_default_profile(guild_id, channel_id)
                
                # Salvar perfil
                self.save_profile(guild_id, channel_id, profile)
                
                logger.info(f"Perfil padrão criado para o canal {channel_key}")
                return profile
        except Exception as e:
            logger.error(f"Erro ao carregar perfil para o canal {guild_id}_{channel_id}: {e}")
            return self._create_default_profile(guild_id, channel_id)
    
    def _create_default_profile(self, guild_id: str, channel_id: str) -> Dict[str, Any]:
        """
        Cria um perfil padrão para um canal.
        
        Args:
            guild_id: ID do servidor
            channel_id: ID do canal
            
        Returns:
            Dicionário com perfil padrão
        """
        try:
            # Obter personalidade global como base
            if self.personality_manager:
                global_persona = self.personality_manager.get_persona()
                
                # Criar cópia da personalidade global
                profile = {
                    "guild_id": guild_id,
                    "channel_id": channel_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                    "base_personality": global_persona["global"]["base_personality"].copy(),
                    "vocabulary": {
                        "frequent_words": [],
                        "expressions": [],
                        "custom_vocabulary": []
                    },
                    "topics": {
                        "favorite_topics": [],
                        "knowledge_areas": []
                    },
                    "interaction_history": {
                        "total_interactions": 0,
                        "last_interaction": None
                    },
                    "channel_info": {
                        "name": "",
                        "description": "",
                        "category": "",
                        "is_nsfw": False
                    }
                }
                
                return profile
            else:
                # Criar perfil padrão básico
                return {
                    "guild_id": guild_id,
                    "channel_id": channel_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                    "base_personality": {
                        "tone": "neutro",
                        "formality_level": 50,
                        "humor_level": 30,
                        "empathy_level": 70,
                        "technicality_level": 50
                    },
                    "vocabulary": {
                        "frequent_words": [],
                        "expressions": [],
                        "custom_vocabulary": []
                    },
                    "topics": {
                        "favorite_topics": [],
                        "knowledge_areas": []
                    },
                    "interaction_history": {
                        "total_interactions": 0,
                        "last_interaction": None
                    },
                    "channel_info": {
                        "name": "",
                        "description": "",
                        "category": "",
                        "is_nsfw": False
                    }
                }
        except Exception as e:
            logger.error(f"Erro ao criar perfil padrão para o canal {guild_id}_{channel_id}: {e}")
            return {
                "guild_id": guild_id,
                "channel_id": channel_id,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "base_personality": {
                    "tone": "neutro",
                    "formality_level": 50,
                    "humor_level": 30,
                    "empathy_level": 70,
                    "technicality_level": 50
                },
                "vocabulary": {
                    "frequent_words": [],
                    "expressions": [],
                    "custom_vocabulary": []
                },
                "topics": {
                    "favorite_topics": [],
                    "knowledge_areas": []
                },
                "interaction_history": {
                    "total_interactions": 0,
                    "last_interaction": None
                },
                "channel_info": {
                    "name": "",
                    "description": "",
                    "category": "",
                    "is_nsfw": False
                }
            }
    
    def save_profile(self, guild_id: str, channel_id: str, profile: Dict[str, Any] = None) -> bool:
        """
        Salva o perfil de um canal.
        
        Args:
            guild_id: ID do servidor
            channel_id: ID do canal
            profile: Dicionário com perfil (opcional)
            
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        try:
            channel_key = f"{guild_id}_{channel_id}"
            
            # Usar perfil fornecido ou obter do cache
            if profile is None:
                if channel_key in self.active_profiles:
                    profile = self.active_profiles[channel_key]
                else:
                    logger.error(f"Perfil não encontrado para o canal {channel_key}")
                    return False
            
            # Atualizar timestamp
            profile["updated_at"] = datetime.now().isoformat()
            
            # Caminho do arquivo
            profile_path = self.get_profile_path(guild_id, channel_id)
            
            # Salvar perfil
            with open(profile_path, 'w', encoding='utf-8') as f:
                json.dump(profile, f, ensure_ascii=False, indent=2)
            
            # Atualizar cache
            self.active_profiles[channel_key] = profile
            
            logger.info(f"Perfil salvo para o canal {channel_key}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar perfil para o canal {guild_id}_{channel_id}: {e}")
            return False
    
    def update_profile(self, guild_id: str, channel_id: str, updates: Dict[str, Any]) -> bool:
        """
        Atualiza o perfil de um canal.
        
        Args:
            guild_id: ID do servidor
            channel_id: ID do canal
            updates: Dicionário com atualizações
            
        Returns:
            True se atualizou com sucesso, False caso contrário
        """
        try:
            # Carregar perfil
            profile = self.load_profile(guild_id, channel_id)
            
            # Aplicar atualizações
            for key, value in updates.items():
                if key in profile:
                    if isinstance(value, dict) and isinstance(profile[key], dict):
                        # Mesclar dicionários
                        profile[key].update(value)
                    else:
                        # Substituir valor
                        profile[key] = value
            
            # Salvar perfil
            return self.save_profile(guild_id, channel_id, profile)
        except Exception as e:
            logger.error(f"Erro ao atualizar perfil para o canal {guild_id}_{channel_id}: {e}")
            return False
    
    def update_base_personality(self, guild_id: str, channel_id: str, 
                               personality_updates: Dict[str, Any]) -> bool:
        """
        Atualiza a personalidade base de um canal.
        
        Args:
            guild_id: ID do servidor
            channel_id: ID do canal
            personality_updates: Dicionário com atualizações de personalidade
            
        Returns:
            True se atualizou com sucesso, False caso contrário
        """
        try:
            # Carregar perfil
            profile = self.load_profile(guild_id, channel_id)
            
            # Aplicar atualizações
            for key, value in personality_updates.items():
                profile["base_personality"][key] = value
            
            # Incrementar contador de interações
            profile["interaction_history"]["total_interactions"] += 1
            profile["interaction_history"]["last_interaction"] = datetime.now().isoformat()
            
            # Salvar perfil
            return self.save_profile(guild_id, channel_id, profile)
        except Exception as e:
            logger.error(f"Erro ao atualizar personalidade base para o canal {guild_id}_{channel_id}: {e}")
            return False
    
    def update_vocabulary(self, guild_id: str, channel_id: str, 
                         frequent_words: List[Dict[str, Any]] = None,
                         expressions: List[Dict[str, Any]] = None,
                         custom_vocabulary: List[str] = None) -> bool:
        """
        Atualiza o vocabulário de um canal.
        
        Args:
            guild_id: ID do servidor
            channel_id: ID do canal
            frequent_words: Lista de palavras frequentes
            expressions: Lista de expressões
            custom_vocabulary: Lista de vocabulário personalizado
            
        Returns:
            True se atualizou com sucesso, False caso contrário
        """
        try:
            # Carregar perfil
            profile = self.load_profile(guild_id, channel_id)
            
            # Atualizar palavras frequentes
            if frequent_words is not None:
                profile["vocabulary"]["frequent_words"] = frequent_words
            
            # Atualizar expressões
            if expressions is not None:
                profile["vocabulary"]["expressions"] = expressions
            
            # Atualizar vocabulário personalizado
            if custom_vocabulary is not None:
                profile["vocabulary"]["custom_vocabulary"] = custom_vocabulary
            
            # Incrementar contador de interações
            profile["interaction_history"]["total_interactions"] += 1
            profile["interaction_history"]["last_interaction"] = datetime.now().isoformat()
            
            # Salvar perfil
            return self.save_profile(guild_id, channel_id, profile)
        except Exception as e:
            logger.error(f"Erro ao atualizar vocabulário para o canal {guild_id}_{channel_id}: {e}")
            return False
    
    def update_topics(self, guild_id: str, channel_id: str,
                     favorite_topics: List[Dict[str, Any]] = None,
                     knowledge_areas: List[Dict[str, Any]] = None) -> bool:
        """
        Atualiza os tópicos de um canal.
        
        Args:
            guild_id: ID do servidor
            channel_id: ID do canal
            favorite_topics: Lista de tópicos favoritos
            knowledge_areas: Lista de áreas de conhecimento
            
        Returns:
            True se atualizou com sucesso, False caso contrário
        """
        try:
            # Carregar perfil
            profile = self.load_profile(guild_id, channel_id)
            
(Content truncated due to size limit. Use line ranges to read in chunks)