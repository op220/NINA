"""
Módulo para gerenciamento de perfil e personalidade da IA.
Parte do projeto Nina IA para personalização do comportamento.
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List, Union
from datetime import datetime

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PersonalityManager:
    """
    Gerenciador de perfil e personalidade da IA.
    """
    
    def __init__(self, profile_path: str = None):
        """
        Inicializa o gerenciador de personalidade.
        
        Args:
            profile_path: Caminho para o arquivo de perfil (None = usar padrão)
        """
        self.profile_path = profile_path or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data", "profiles", "default_profile.json"
        )
        self.profile = {}
        
        # Criar diretório de perfis se não existir
        os.makedirs(os.path.dirname(self.profile_path), exist_ok=True)
        
        # Carregar ou criar perfil
        if os.path.exists(self.profile_path):
            self.load_profile()
        else:
            self.create_default_profile()
            self.save_profile()
    
    def create_default_profile(self) -> None:
        """
        Cria um perfil padrão.
        """
        self.profile = {
            "name": "Nina",
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "personality": {
                "speech_style": "amigável",  # amigável, formal, casual, técnico
                "mood": "neutro",  # alegre, sério, neutro, reflexivo
                "preferences": ["tecnologia", "música", "filmes"],
                "description": "Assistente de IA amigável e prestativa"
            },
            "voice": {
                "model": "tts_models/pt/cv/vits",
                "speaker": None,
                "language": "pt",
                "speed": 1.0,
                "pitch": 1.0
            },
            "llm": {
                "model": "mistral",
                "temperature": 0.7,
                "max_tokens": 500
            },
            "stt": {
                "model": "base",
                "language": "pt"
            },
            "interface": {
                "theme": "dark",
                "wake_word": "Nina",
                "response_format": "voice_and_text"
            }
        }
        
        logger.info("Perfil padrão criado")
    
    def load_profile(self) -> bool:
        """
        Carrega o perfil do arquivo.
        
        Returns:
            True se o perfil foi carregado com sucesso
        """
        try:
            with open(self.profile_path, 'r', encoding='utf-8') as f:
                self.profile = json.load(f)
            
            logger.info(f"Perfil carregado: {self.profile.get('name', 'Sem nome')}")
            return True
        except Exception as e:
            logger.error(f"Erro ao carregar perfil: {e}")
            self.create_default_profile()
            return False
    
    def save_profile(self) -> bool:
        """
        Salva o perfil no arquivo.
        
        Returns:
            True se o perfil foi salvo com sucesso
        """
        try:
            # Atualizar timestamp
            self.profile["updated_at"] = datetime.now().isoformat()
            
            with open(self.profile_path, 'w', encoding='utf-8') as f:
                json.dump(self.profile, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Perfil salvo: {self.profile_path}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar perfil: {e}")
            return False
    
    def get_profile(self) -> Dict[str, Any]:
        """
        Obtém o perfil completo.
        
        Returns:
            Dicionário com o perfil
        """
        return self.profile
    
    def get_personality(self) -> Dict[str, Any]:
        """
        Obtém a personalidade.
        
        Returns:
            Dicionário com a personalidade
        """
        return self.profile.get("personality", {})
    
    def get_voice_settings(self) -> Dict[str, Any]:
        """
        Obtém as configurações de voz.
        
        Returns:
            Dicionário com as configurações de voz
        """
        return self.profile.get("voice", {})
    
    def get_llm_settings(self) -> Dict[str, Any]:
        """
        Obtém as configurações do LLM.
        
        Returns:
            Dicionário com as configurações do LLM
        """
        return self.profile.get("llm", {})
    
    def get_stt_settings(self) -> Dict[str, Any]:
        """
        Obtém as configurações do STT.
        
        Returns:
            Dicionário com as configurações do STT
        """
        return self.profile.get("stt", {})
    
    def get_interface_settings(self) -> Dict[str, Any]:
        """
        Obtém as configurações da interface.
        
        Returns:
            Dicionário com as configurações da interface
        """
        return self.profile.get("interface", {})
    
    def update_personality(self, personality: Dict[str, Any]) -> bool:
        """
        Atualiza a personalidade.
        
        Args:
            personality: Dicionário com a nova personalidade
            
        Returns:
            True se a personalidade foi atualizada com sucesso
        """
        try:
            self.profile["personality"] = personality
            return self.save_profile()
        except Exception as e:
            logger.error(f"Erro ao atualizar personalidade: {e}")
            return False
    
    def update_voice_settings(self, voice_settings: Dict[str, Any]) -> bool:
        """
        Atualiza as configurações de voz.
        
        Args:
            voice_settings: Dicionário com as novas configurações de voz
            
        Returns:
            True se as configurações foram atualizadas com sucesso
        """
        try:
            self.profile["voice"] = voice_settings
            return self.save_profile()
        except Exception as e:
            logger.error(f"Erro ao atualizar configurações de voz: {e}")
            return False
    
    def update_llm_settings(self, llm_settings: Dict[str, Any]) -> bool:
        """
        Atualiza as configurações do LLM.
        
        Args:
            llm_settings: Dicionário com as novas configurações do LLM
            
        Returns:
            True se as configurações foram atualizadas com sucesso
        """
        try:
            self.profile["llm"] = llm_settings
            return self.save_profile()
        except Exception as e:
            logger.error(f"Erro ao atualizar configurações do LLM: {e}")
            return False
    
    def update_stt_settings(self, stt_settings: Dict[str, Any]) -> bool:
        """
        Atualiza as configurações do STT.
        
        Args:
            stt_settings: Dicionário com as novas configurações do STT
            
        Returns:
            True se as configurações foram atualizadas com sucesso
        """
        try:
            self.profile["stt"] = stt_settings
            return self.save_profile()
        except Exception as e:
            logger.error(f"Erro ao atualizar configurações do STT: {e}")
            return False
    
    def update_interface_settings(self, interface_settings: Dict[str, Any]) -> bool:
        """
        Atualiza as configurações da interface.
        
        Args:
            interface_settings: Dicionário com as novas configurações da interface
            
        Returns:
            True se as configurações foram atualizadas com sucesso
        """
        try:
            self.profile["interface"] = interface_settings
            return self.save_profile()
        except Exception as e:
            logger.error(f"Erro ao atualizar configurações da interface: {e}")
            return False
    
    def set_name(self, name: str) -> bool:
        """
        Define o nome da IA.
        
        Args:
            name: Novo nome
            
        Returns:
            True se o nome foi atualizado com sucesso
        """
        try:
            self.profile["name"] = name
            return self.save_profile()
        except Exception as e:
            logger.error(f"Erro ao definir nome: {e}")
            return False
    
    def set_mood(self, mood: str) -> bool:
        """
        Define o humor da IA.
        
        Args:
            mood: Novo humor (alegre, sério, neutro, reflexivo)
            
        Returns:
            True se o humor foi atualizado com sucesso
        """
        try:
            if "personality" not in self.profile:
                self.profile["personality"] = {}
            
            self.profile["personality"]["mood"] = mood
            return self.save_profile()
        except Exception as e:
            logger.error(f"Erro ao definir humor: {e}")
            return False
    
    def set_speech_style(self, style: str) -> bool:
        """
        Define o estilo de fala da IA.
        
        Args:
            style: Novo estilo (amigável, formal, casual, técnico)
            
        Returns:
            True se o estilo foi atualizado com sucesso
        """
        try:
            if "personality" not in self.profile:
                self.profile["personality"] = {}
            
            self.profile["personality"]["speech_style"] = style
            return self.save_profile()
        except Exception as e:
            logger.error(f"Erro ao definir estilo de fala: {e}")
            return False
    
    def add_preference(self, preference: str) -> bool:
        """
        Adiciona uma preferência à IA.
        
        Args:
            preference: Nova preferência
            
        Returns:
            True se a preferência foi adicionada com sucesso
        """
        try:
            if "personality" not in self.profile:
                self.profile["personality"] = {}
            
            if "preferences" not in self.profile["personality"]:
                self.profile["personality"]["preferences"] = []
            
            if preference not in self.profile["personality"]["preferences"]:
                self.profile["personality"]["preferences"].append(preference)
                return self.save_profile()
            
            return True
        except Exception as e:
            logger.error(f"Erro ao adicionar preferência: {e}")
            return False
    
    def remove_preference(self, preference: str) -> bool:
        """
        Remove uma preferência da IA.
        
        Args:
            preference: Preferência a ser removida
            
        Returns:
            True se a preferência foi removida com sucesso
        """
        try:
            if ("personality" in self.profile and 
                "preferences" in self.profile["personality"] and
                preference in self.profile["personality"]["preferences"]):
                
                self.profile["personality"]["preferences"].remove(preference)
                return self.save_profile()
            
            return True
        except Exception as e:
            logger.error(f"Erro ao remover preferência: {e}")
            return False
    
    def list_available_profiles(self) -> List[str]:
        """
        Lista os perfis disponíveis.
        
        Returns:
            Lista de nomes de perfis
        """
        try:
            profiles_dir = os.path.dirname(self.profile_path)
            profiles = []
            
            for file in os.listdir(profiles_dir):
                if file.endswith(".json"):
                    profile_name = os.path.splitext(file)[0]
                    profiles.append(profile_name)
            
            return profiles
        except Exception as e:
            logger.error(f"Erro ao listar perfis: {e}")
            return []
    
    def load_profile_by_name(self, profile_name: str) -> bool:
        """
        Carrega um perfil pelo nome.
        
        Args:
            profile_name: Nome do perfil
            
        Returns:
            True se o perfil foi carregado com sucesso
        """
        try:
            profiles_dir = os.path.dirname(self.profile_path)
            new_profile_path = os.path.join(profiles_dir, f"{profile_name}.json")
            
            if os.path.exists(new_profile_path):
                self.profile_path = new_profile_path
                return self.load_profile()
            else:
                logger.error(f"Perfil não encontrado: {profile_name}")
                return False
        except Exception as e:
            logger.error(f"Erro ao carregar perfil por nome: {e}")
            return False
    
    def save_profile_as(self, profile_name: str) -> bool:
        """
        Salva o perfil atual com um novo nome.
        
        Args:
            profile_name: Novo nome do perfil
            
        Returns:
            True se o perfil foi salvo com sucesso
        """
        try:
            profiles_dir = os.path.dirname(self.profile_path)
            new_profile_path = os.path.join(profiles_dir, f"{profile_name}.json")
            
            # Atualizar timestamp
            self.profile["updated_at"] = datetime.now().isoformat()
            
            with open(new_profile_path, 'w', encoding='utf-8') as f:
                json.dump(self.profile, f, ensure_ascii=False, indent=2)
            
            self.profile_path = new_profile_path
            logger.info(f"Perfil salvo como: {profile_name}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar perfil como: {e}")
            return False
    
    def build_system_prompt(self) -> str:
        """
        Constrói o prompt de sistema com base na personalidade.
        
        Returns:
            Prompt de sistema formatado
        """
        name = self.profile.get("name", "Nina")
        personality = self.get_personality()
        
        speech_style = personality.get("speech_style", "amigável")
        preferences = personality.get("preferences", [])
        mood = personality.get("mood", "neutro")
        description = personality.get("description", "Assistente de IA amigável e prestativa")
        
        # Construir descrição de preferências
        prefs_text = ""
        if preferences:
            prefs_text = "Você gosta de falar sobre " + ", ".join(preferences) + ". "
        
        # Construir descrição de estilo de fala
        style_text = ""
        if speech_style == "formal":
            style_text = "Você fala de maneira formal e educada. "
        elif speech_style == "casual":
            style_text = "Você fala de maneira casual e descontraída. "
        elif speech_style == "amigável":
            style_text = "Você fala de maneira amigável e calorosa. "
        elif speech_style == "técnico":
            style_text = "Você fala de maneira técnica e precisa. "
        
        # Construir descrição de humor
        mood_text = ""
        if mood == "alegre":
            mood_text = "Seu humor atual é alegre e otimista. "
        elif mood == "sério":
            mood_text = "Seu humor atual é sério e focado. "
        elif mood == "neutro":
            mood_text = "Seu humor atual é neutro e equilibrado. "
        elif mood == "reflexivo":
            mood_text = "Seu humor atual é reflexivo e contemplativo. "
        
        # Montar prompt completo
        system_prompt = (
            f"Você é {name}, uma assistente de inteligência artificial. " +
            f"{description}. " +
            f"{style_text}" +
            f"{mood_text}" +
            f"{prefs_text}" +
            "Você responde de forma clara e concisa, " +
            "evitando repetições e usando linguagem simples."
        )
        return system_prompt