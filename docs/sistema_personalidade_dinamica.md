# Sistema de Personalidade Dinâmica

## Arquitetura do Sistema

### Componentes Principais
1. **Gerenciador de Personalidade**: Mantém e atualiza o arquivo persona.json
2. **Adaptador de Personalidade**: Aplica mudanças baseadas nos insights de conversas
3. **Controlador de Evolução**: Gerencia a velocidade e limites das mudanças
4. **Armazenamento de Perfis**: Mantém diferentes perfis por canal ou grupo
5. **Integrador de Contexto**: Incorpora a personalidade no contexto do LLM

### Fluxo de Dados
1. Insights são recebidos do sistema de análise de padrões
2. Controlador de evolução avalia quais mudanças são permitidas
3. Adaptador de personalidade aplica as mudanças ao perfil atual
4. Gerenciador de personalidade atualiza o arquivo persona.json
5. Integrador de contexto incorpora a personalidade nas interações da IA

## Implementação

### Estrutura do Arquivo persona.json
```json
{
  "version": "1.0",
  "last_updated": "2025-04-24T17:35:00.000Z",
  "global": {
    "name": "Nina",
    "base_personality": {
      "tone": "neutro",
      "formality_level": 50,
      "humor_level": 30,
      "empathy_level": 70,
      "technicality_level": 50
    },
    "evolution_settings": {
      "max_change_per_session": 5,
      "min_interactions_for_change": 10,
      "restricted_traits": [],
      "locked_traits": []
    }
  },
  "channels": {},
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
    "last_interaction": null,
    "evolution_log": []
  }
}
```

### Gerenciador de Personalidade
```python
import os
import json
import logging
from datetime import datetime
import copy
from typing import Dict, List, Any, Optional, Union

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("personality_manager.log")
    ]
)
logger = logging.getLogger("PersonalityManager")

class PersonalityManager:
    def __init__(self, persona_file_path: str = "./data/persona/persona.json"):
        """
        Inicializa o gerenciador de personalidade.
        
        Args:
            persona_file_path: Caminho para o arquivo persona.json
        """
        self.persona_file_path = persona_file_path
        self.persona_dir = os.path.dirname(persona_file_path)
        
        # Garantir que o diretório exista
        os.makedirs(self.persona_dir, exist_ok=True)
        
        # Carregar ou criar arquivo de personalidade
        self.persona = self._load_or_create_persona()
        
        logger.info(f"Gerenciador de personalidade inicializado. Arquivo: {persona_file_path}")
    
    def _load_or_create_persona(self) -> Dict[str, Any]:
        """
        Carrega o arquivo de personalidade ou cria um novo se não existir.
        
        Returns:
            Dicionário com dados de personalidade
        """
        try:
            if os.path.exists(self.persona_file_path):
                with open(self.persona_file_path, 'r', encoding='utf-8') as f:
                    persona = json.load(f)
                logger.info(f"Arquivo de personalidade carregado: {self.persona_file_path}")
                return persona
            else:
                # Criar arquivo padrão
                persona = self._create_default_persona()
                self._save_persona(persona)
                logger.info(f"Arquivo de personalidade padrão criado: {self.persona_file_path}")
                return persona
        except Exception as e:
            logger.error(f"Erro ao carregar arquivo de personalidade: {e}")
            persona = self._create_default_persona()
            self._save_persona(persona)
            logger.info(f"Arquivo de personalidade padrão criado após erro: {self.persona_file_path}")
            return persona
    
    def _create_default_persona(self) -> Dict[str, Any]:
        """
        Cria uma personalidade padrão.
        
        Returns:
            Dicionário com personalidade padrão
        """
        return {
            "version": "1.0",
            "last_updated": datetime.now().isoformat(),
            "global": {
                "name": "Nina",
                "base_personality": {
                    "tone": "neutro",
                    "formality_level": 50,
                    "humor_level": 30,
                    "empathy_level": 70,
                    "technicality_level": 50
                },
                "evolution_settings": {
                    "max_change_per_session": 5,
                    "min_interactions_for_change": 10,
                    "restricted_traits": [],
                    "locked_traits": []
                }
            },
            "channels": {},
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
                "last_interaction": None,
                "evolution_log": []
            }
        }
    
    def _save_persona(self, persona: Dict[str, Any] = None) -> bool:
        """
        Salva o arquivo de personalidade.
        
        Args:
            persona: Dicionário com dados de personalidade (opcional)
            
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        try:
            # Usar persona fornecida ou a atual
            data = persona if persona is not None else self.persona
            
            # Atualizar timestamp
            data["last_updated"] = datetime.now().isoformat()
            
            # Salvar arquivo
            with open(self.persona_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Arquivo de personalidade salvo: {self.persona_file_path}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar arquivo de personalidade: {e}")
            return False
    
    def get_persona(self) -> Dict[str, Any]:
        """
        Obtém a personalidade atual.
        
        Returns:
            Dicionário com dados de personalidade
        """
        return copy.deepcopy(self.persona)
    
    def get_channel_persona(self, guild_id: str, channel_id: str) -> Dict[str, Any]:
        """
        Obtém a personalidade específica para um canal.
        
        Args:
            guild_id: ID do servidor
            channel_id: ID do canal
            
        Returns:
            Dicionário com dados de personalidade do canal
        """
        channel_key = f"{guild_id}_{channel_id}"
        
        # Verificar se existe personalidade para este canal
        if "channels" in self.persona and channel_key in self.persona["channels"]:
            # Combinar personalidade global com a do canal
            persona = copy.deepcopy(self.persona)
            
            # Sobrescrever com dados específicos do canal
            channel_data = persona["channels"][channel_key]
            
            # Mesclar personalidade base
            if "base_personality" in channel_data:
                for key, value in channel_data["base_personality"].items():
                    persona["global"]["base_personality"][key] = value
            
            # Mesclar vocabulário
            if "vocabulary" in channel_data:
                for key, value in channel_data["vocabulary"].items():
                    persona["vocabulary"][key] = value
            
            # Mesclar tópicos
            if "topics" in channel_data:
                for key, value in channel_data["topics"].items():
                    persona["topics"][key] = value
            
            return persona
        else:
            # Retornar personalidade global
            return copy.deepcopy(self.persona)
    
    def update_base_personality(self, updates: Dict[str, Any], channel_key: str = None) -> bool:
        """
        Atualiza a personalidade base.
        
        Args:
            updates: Dicionário com atualizações
            channel_key: Chave do canal (opcional)
            
        Returns:
            True se atualizou com sucesso, False caso contrário
        """
        try:
            if channel_key:
                # Atualizar personalidade do canal
                if "channels" not in self.persona:
                    self.persona["channels"] = {}
                
                if channel_key not in self.persona["channels"]:
                    self.persona["channels"][channel_key] = {
                        "base_personality": {},
                        "vocabulary": {
                            "frequent_words": [],
                            "expressions": [],
                            "custom_vocabulary": []
                        },
                        "topics": {
                            "favorite_topics": [],
                            "knowledge_areas": []
                        }
                    }
                
                # Atualizar personalidade base do canal
                if "base_personality" not in self.persona["channels"][channel_key]:
                    self.persona["channels"][channel_key]["base_personality"] = {}
                
                for key, value in updates.items():
                    self.persona["channels"][channel_key]["base_personality"][key] = value
            else:
                # Atualizar personalidade global
                for key, value in updates.items():
                    self.persona["global"]["base_personality"][key] = value
            
            # Registrar atualização no log de evolução
            self._log_evolution("base_personality", updates, channel_key)
            
            # Salvar alterações
            return self._save_persona()
        except Exception as e:
            logger.error(f"Erro ao atualizar personalidade base: {e}")
            return False
    
    def update_vocabulary(self, frequent_words: List[Dict[str, Any]] = None, 
                         expressions: List[Dict[str, Any]] = None,
                         custom_vocabulary: List[str] = None,
                         channel_key: str = None) -> bool:
        """
        Atualiza o vocabulário.
        
        Args:
            frequent_words: Lista de palavras frequentes
            expressions: Lista de expressões
            custom_vocabulary: Lista de vocabulário personalizado
            channel_key: Chave do canal (opcional)
            
        Returns:
            True se atualizou com sucesso, False caso contrário
        """
        try:
            target = self.persona
            
            if channel_key:
                # Atualizar vocabulário do canal
                if "channels" not in self.persona:
                    self.persona["channels"] = {}
                
                if channel_key not in self.persona["channels"]:
                    self.persona["channels"][channel_key] = {
                        "base_personality": {},
                        "vocabulary": {
                            "frequent_words": [],
                            "expressions": [],
                            "custom_vocabulary": []
                        },
                        "topics": {
                            "favorite_topics": [],
                            "knowledge_areas": []
                        }
                    }
                
                if "vocabulary" not in self.persona["channels"][channel_key]:
                    self.persona["channels"][channel_key]["vocabulary"] = {
                        "frequent_words": [],
                        "expressions": [],
                        "custom_vocabulary": []
                    }
                
                target = self.persona["channels"][channel_key]
            
            # Atualizar palavras frequentes
            if frequent_words is not None:
                target["vocabulary"]["frequent_words"] = frequent_words
            
            # Atualizar expressões
            if expressions is not None:
                target["vocabulary"]["expressions"] = expressions
            
            # Atualizar vocabulário personalizado
            if custom_vocabulary is not None:
                target["vocabulary"]["custom_vocabulary"] = custom_vocabulary
            
            # Registrar atualização no log de evolução
            updates = {}
            if frequent_words is not None:
                updates["frequent_words"] = len(frequent_words)
            if expressions is not None:
                updates["expressions"] = len(expressions)
            if custom_vocabulary is not None:
                updates["custom_vocabulary"] = len(custom_vocabulary)
            
            self._log_evolution("vocabulary", updates, channel_key)
            
            # Salvar alterações
            return self._save_persona()
        except Exception as e:
            logger.error(f"Erro ao atualizar vocabulário: {e}")
            return False
    
    def update_topics(self, favorite_topics: List[Dict[str, Any]] = None,
                     knowledge_areas: List[Dict[str, Any]] = None,
                     channel_key: str = None) -> bool:
        """
        Atualiza os tópicos.
        
        Args:
            favorite_topics: Lista de tópicos favoritos
            knowledge_areas: Lista de áreas de conhecimento
            channel_key: Chave do canal (opcional)
            
        Returns:
            True se atualizou com sucesso, False caso contrário
        """
        try:
            target = self.persona
            
            if channel_key:
                # Atualizar tópicos do canal
                if "channels" not in self.persona:
                    self.persona["channels"] = {}
                
                if channel_key not in self.persona["channels"]:
                    self.persona["channels"][channel_key] = {
                        "base_personality": {},
                        "vocabulary": {
                            "frequent_words": [],
                            "expressions": [],
                            "custom_vocabulary": []
                        },
                        "topics": {
                            "favorite_topics": [],
                            "knowledge_areas": []
                        }
                    }
                
                if "topics" not in self.persona["channels"][channel_key]:
                    self.persona["channels"][channel_key]["topics"] = {
                        "favorite_topics": [],
                        "knowledge_areas": []
                    }
                
                target = self.persona["channels"][channel_key]
            
            # Atualizar tópicos favoritos
            if favorite_topics is not None:
                target["topics"]["favorite_topics"] = favorite_topics
            
            # Atualizar áreas de conhecimento
            if knowledge_areas is not None:
                target["topics"]["knowledge_areas"] = knowledge_areas
            
            # Registrar atualização no log de evolução
            updates = {}
            if favorite_topics is not None:
                updates["favorite_topics"] = len(favorite_topics)
            if knowledge_areas is not None:
                updates["knowledge_areas"] = len(knowledge_areas)
            
            self._log_evolution("topics", updates, channel_key)
            
            # Salvar alterações
            return self._save_persona()
        except Exception as e:
       
(Content truncated due to size limit. Use line ranges to read in chunks)