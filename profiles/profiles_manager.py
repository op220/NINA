"""
Módulo para gerenciamento de perfis de personalidade da IA.
Parte do projeto Nina IA para configuração de múltiplos perfis.
"""

import os
import json
import logging
import shutil
from typing import Dict, Any, Optional, List, Union
from datetime import datetime

from .personality_manager import PersonalityManager

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProfilesManager:
    """
    Gerenciador de múltiplos perfis de personalidade.
    """
    
    def __init__(self, profiles_dir: str = None):
        """
        Inicializa o gerenciador de perfis.
        
        Args:
            profiles_dir: Diretório para armazenar perfis (None = usar padrão)
        """
        self.profiles_dir = profiles_dir or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data", "profiles"
        )
        self.active_profile = None
        
        # Criar diretório de perfis se não existir
        os.makedirs(self.profiles_dir, exist_ok=True)
        
        # Inicializar gerenciador de personalidade com perfil padrão
        default_profile_path = os.path.join(self.profiles_dir, "default_profile.json")
        self.personality_manager = PersonalityManager(default_profile_path)
        
        # Verificar se existe pelo menos um perfil
        if not os.listdir(self.profiles_dir):
            logger.info("Nenhum perfil encontrado, criando perfil padrão")
            self.personality_manager.create_default_profile()
            self.personality_manager.save_profile()
        
        self.active_profile = "default_profile"
    
    def list_profiles(self) -> List[str]:
        """
        Lista os perfis disponíveis.
        
        Returns:
            Lista de nomes de perfis
        """
        profiles = []
        
        for file in os.listdir(self.profiles_dir):
            if file.endswith(".json"):
                profile_name = os.path.splitext(file)[0]
                profiles.append(profile_name)
        
        return profiles
    
    def get_active_profile_name(self) -> str:
        """
        Obtém o nome do perfil ativo.
        
        Returns:
            Nome do perfil ativo
        """
        return self.active_profile
    
    def get_active_profile(self) -> Dict[str, Any]:
        """
        Obtém o perfil ativo.
        
        Returns:
            Dicionário com o perfil ativo
        """
        return self.personality_manager.get_profile()
    
    def load_profile(self, profile_name: str) -> bool:
        """
        Carrega um perfil pelo nome.
        
        Args:
            profile_name: Nome do perfil
            
        Returns:
            True se o perfil foi carregado com sucesso
        """
        profile_path = os.path.join(self.profiles_dir, f"{profile_name}.json")
        
        if not os.path.exists(profile_path):
            logger.error(f"Perfil não encontrado: {profile_name}")
            return False
        
        # Carregar perfil
        self.personality_manager = PersonalityManager(profile_path)
        self.active_profile = profile_name
        
        logger.info(f"Perfil carregado: {profile_name}")
        return True
    
    def create_profile(self, profile_name: str, base_profile: Optional[str] = None) -> bool:
        """
        Cria um novo perfil.
        
        Args:
            profile_name: Nome do novo perfil
            base_profile: Nome do perfil base (None = usar perfil ativo)
            
        Returns:
            True se o perfil foi criado com sucesso
        """
        # Verificar se o perfil já existe
        new_profile_path = os.path.join(self.profiles_dir, f"{profile_name}.json")
        if os.path.exists(new_profile_path):
            logger.error(f"Perfil já existe: {profile_name}")
            return False
        
        # Se base_profile for especificado, carregar esse perfil primeiro
        if base_profile:
            base_profile_path = os.path.join(self.profiles_dir, f"{base_profile}.json")
            if not os.path.exists(base_profile_path):
                logger.error(f"Perfil base não encontrado: {base_profile}")
                return False
            
            # Copiar perfil base
            shutil.copy(base_profile_path, new_profile_path)
            
            # Carregar o novo perfil
            self.personality_manager = PersonalityManager(new_profile_path)
            self.active_profile = profile_name
            
            # Atualizar nome e timestamps
            profile = self.personality_manager.get_profile()
            profile["name"] = profile_name
            profile["created_at"] = datetime.now().isoformat()
            profile["updated_at"] = datetime.now().isoformat()
            self.personality_manager.save_profile()
            
        else:
            # Usar perfil ativo como base
            current_profile = self.personality_manager.get_profile()
            
            # Criar novo perfil baseado no atual
            with open(new_profile_path, 'w', encoding='utf-8') as f:
                new_profile = current_profile.copy()
                new_profile["name"] = profile_name
                new_profile["created_at"] = datetime.now().isoformat()
                new_profile["updated_at"] = datetime.now().isoformat()
                json.dump(new_profile, f, ensure_ascii=False, indent=2)
            
            # Carregar o novo perfil
            self.personality_manager = PersonalityManager(new_profile_path)
            self.active_profile = profile_name
        
        logger.info(f"Perfil criado: {profile_name}")
        return True
    
    def delete_profile(self, profile_name: str) -> bool:
        """
        Exclui um perfil.
        
        Args:
            profile_name: Nome do perfil a ser excluído
            
        Returns:
            True se o perfil foi excluído com sucesso
        """
        # Não permitir excluir o perfil ativo
        if profile_name == self.active_profile:
            logger.error("Não é possível excluir o perfil ativo")
            return False
        
        profile_path = os.path.join(self.profiles_dir, f"{profile_name}.json")
        
        if not os.path.exists(profile_path):
            logger.error(f"Perfil não encontrado: {profile_name}")
            return False
        
        # Excluir perfil
        os.remove(profile_path)
        
        logger.info(f"Perfil excluído: {profile_name}")
        return True
    
    def rename_profile(self, old_name: str, new_name: str) -> bool:
        """
        Renomeia um perfil.
        
        Args:
            old_name: Nome atual do perfil
            new_name: Novo nome do perfil
            
        Returns:
            True se o perfil foi renomeado com sucesso
        """
        old_path = os.path.join(self.profiles_dir, f"{old_name}.json")
        new_path = os.path.join(self.profiles_dir, f"{new_name}.json")
        
        if not os.path.exists(old_path):
            logger.error(f"Perfil não encontrado: {old_name}")
            return False
        
        if os.path.exists(new_path):
            logger.error(f"Já existe um perfil com o nome: {new_name}")
            return False
        
        # Renomear arquivo
        os.rename(old_path, new_path)
        
        # Se for o perfil ativo, atualizar referência
        if old_name == self.active_profile:
            self.active_profile = new_name
            self.personality_manager = PersonalityManager(new_path)
            
            # Atualizar nome no perfil
            profile = self.personality_manager.get_profile()
            profile["name"] = new_name
            self.personality_manager.save_profile()
        
        logger.info(f"Perfil renomeado: {old_name} -> {new_name}")
        return True
    
    def get_personality_manager(self) -> PersonalityManager:
        """
        Obtém o gerenciador de personalidade atual.
        
        Returns:
            Gerenciador de personalidade
        """
        return self.personality_manager
    
    def build_system_prompt(self) -> str:
        """
        Constrói o prompt de sistema com base na personalidade ativa.
        
        Returns:
            Prompt de sistema formatado
        """
        return self.personality_manager.build_system_prompt()


if __name__ == "__main__":
    # Exemplo de uso
    import tempfile
    
    # Criar diretório temporário para perfis
    temp_dir = tempfile.mkdtemp()
    
    # Inicializar gerenciador de perfis
    manager = ProfilesManager(temp_dir)
    
    # Criar perfis
    manager.create_profile("amigavel")
    manager.create_profile("formal")
    
    # Listar perfis
    print("Perfis disponíveis:")
    for profile in manager.list_profiles():
        print(f"  - {profile}")
    
    # Carregar perfil
    manager.load_profile("amigavel")
    
    # Modificar perfil
    personality_manager = manager.get_personality_manager()
    personality_manager.set_speech_style("amigável")
    personality_manager.set_mood("alegre")
    
    # Exibir prompt de sistema
    print("\nPrompt de sistema (amigável):")
    print(manager.build_system_prompt())
    
    # Carregar outro perfil
    manager.load_profile("formal")
    
    # Modificar perfil
    personality_manager = manager.get_personality_manager()
    personality_manager.set_speech_style("formal")
    personality_manager.set_mood("sério")
    
    # Exibir prompt de sistema
    print("\nPrompt de sistema (formal):")
    print(manager.build_system_prompt())
