# Integração dos Módulos

Nesta seção, vamos integrar os três componentes principais da Nina IA (STT, LLM e TTS) para criar um sistema completo e funcional. Vamos criar os arquivos necessários para a orquestração dos componentes, gerenciamento de personalidade, gerenciamento de sessão e interface principal.

## Estrutura de Diretórios

Antes de começar, vamos verificar se a estrutura de diretórios está correta:

```cmd
cd C:\NinaIA
dir nina_ia
```

Você deve ver os seguintes diretórios:
- `stt` - Sistema de reconhecimento de voz
- `llm` - Sistema de processamento de linguagem natural
- `tts` - Sistema de síntese de voz
- `core` - Componentes principais do sistema
- `data` - Dados e configurações
- `interface` - Interface do usuário

Se algum diretório estiver faltando, crie-o:

```cmd
mkdir -p nina_ia\core nina_ia\data nina_ia\interface
mkdir -p nina_ia\data\profiles nina_ia\data\memory nina_ia\data\config nina_ia\data\temp
```

## Criação do Perfil Padrão

Vamos criar um perfil padrão para a Nina IA:

1. Crie o arquivo `C:\NinaIA\nina_ia\data\profiles\default_profile.json` com o seguinte conteúdo:

```json
{
  "name": "Nina",
  "description": "Assistente de inteligência artificial local",
  "personality": {
    "formality_level": 50,
    "humor_level": 50,
    "technicality_level": 50,
    "response_speed": "médio",
    "verbosity": "médio"
  },
  "voice": {
    "model": "tts_models/pt/cv/vits",
    "speed": 1.0,
    "pitch": 0.0
  },
  "language": {
    "primary": "pt",
    "secondary": "en"
  },
  "preferences": {
    "greeting": "Olá, eu sou a Nina, sua assistente de inteligência artificial. Como posso ajudar você hoje?",
    "farewell": "Até logo! Foi um prazer ajudar.",
    "error_message": "Desculpe, ocorreu um erro. Poderia tentar novamente?"
  }
}
```

## Criação do Gerenciador de Personalidade

Vamos criar o gerenciador de personalidade, que será responsável por carregar e gerenciar os perfis da Nina IA:

1. Crie o arquivo `C:\NinaIA\nina_ia\core\personality_manager.py` com o seguinte conteúdo:

```python
import os
import json
import logging
import copy

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("personality_manager")

class PersonalityManager:
    def __init__(self, profiles_dir=None):
        """
        Inicializa o gerenciador de personalidade.
        
        Args:
            profiles_dir: Diretório onde os perfis estão armazenados
        """
        if profiles_dir is None:
            profiles_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "data",
                "profiles"
            )
        
        self.profiles_dir = profiles_dir
        self.profiles = {}
        self.active_profile = None
        
        # Carregar perfis
        self._load_profiles()
        
        # Ativar perfil padrão
        self.activate_profile("default")
    
    def _load_profiles(self):
        """Carrega todos os perfis disponíveis."""
        if not os.path.exists(self.profiles_dir):
            logger.warning(f"Diretório de perfis não encontrado: {self.profiles_dir}")
            os.makedirs(self.profiles_dir, exist_ok=True)
            self._create_default_profile()
            return
        
        # Listar arquivos de perfil
        profile_files = [f for f in os.listdir(self.profiles_dir) if f.endswith('.json')]
        
        if not profile_files:
            logger.warning("Nenhum perfil encontrado. Criando perfil padrão.")
            self._create_default_profile()
            return
        
        # Carregar cada perfil
        for profile_file in profile_files:
            profile_path = os.path.join(self.profiles_dir, profile_file)
            profile_name = os.path.splitext(profile_file)[0]
            
            try:
                with open(profile_path, 'r', encoding='utf-8') as f:
                    profile_data = json.load(f)
                
                self.profiles[profile_name] = profile_data
                logger.info(f"Perfil carregado: {profile_name}")
            except Exception as e:
                logger.error(f"Erro ao carregar perfil {profile_name}: {str(e)}")
        
        # Verificar se o perfil padrão existe
        if "default" not in self.profiles:
            logger.warning("Perfil padrão não encontrado. Criando perfil padrão.")
            self._create_default_profile()
    
    def _create_default_profile(self):
        """Cria o perfil padrão."""
        default_profile = {
            "name": "Nina",
            "description": "Assistente de inteligência artificial local",
            "personality": {
                "formality_level": 50,
                "humor_level": 50,
                "technicality_level": 50,
                "response_speed": "médio",
                "verbosity": "médio"
            },
            "voice": {
                "model": "tts_models/pt/cv/vits",
                "speed": 1.0,
                "pitch": 0.0
            },
            "language": {
                "primary": "pt",
                "secondary": "en"
            },
            "preferences": {
                "greeting": "Olá, eu sou a Nina, sua assistente de inteligência artificial. Como posso ajudar você hoje?",
                "farewell": "Até logo! Foi um prazer ajudar.",
                "error_message": "Desculpe, ocorreu um erro. Poderia tentar novamente?"
            }
        }
        
        # Salvar perfil padrão
        self.profiles["default"] = default_profile
        self.save_profile("default")
    
    def get_profile(self, profile_name):
        """
        Obtém um perfil pelo nome.
        
        Args:
            profile_name: Nome do perfil
            
        Returns:
            Dicionário com os dados do perfil ou None se não encontrado
        """
        return self.profiles.get(profile_name)
    
    def get_active_profile(self):
        """
        Obtém o perfil ativo.
        
        Returns:
            Dicionário com os dados do perfil ativo
        """
        return self.active_profile
    
    def activate_profile(self, profile_name):
        """
        Ativa um perfil.
        
        Args:
            profile_name: Nome do perfil a ser ativado
            
        Returns:
            True se o perfil foi ativado com sucesso, False caso contrário
        """
        if profile_name not in self.profiles:
            logger.error(f"Perfil não encontrado: {profile_name}")
            return False
        
        # Fazer uma cópia do perfil para evitar modificações acidentais
        self.active_profile = copy.deepcopy(self.profiles[profile_name])
        logger.info(f"Perfil ativado: {profile_name}")
        
        return True
    
    def create_profile(self, profile_name, profile_data):
        """
        Cria um novo perfil.
        
        Args:
            profile_name: Nome do perfil
            profile_data: Dicionário com os dados do perfil
            
        Returns:
            True se o perfil foi criado com sucesso, False caso contrário
        """
        if profile_name in self.profiles:
            logger.warning(f"Perfil já existe: {profile_name}")
            return False
        
        # Adicionar perfil
        self.profiles[profile_name] = profile_data
        
        # Salvar perfil
        success = self.save_profile(profile_name)
        
        if success:
            logger.info(f"Perfil criado: {profile_name}")
        
        return success
    
    def update_profile(self, profile_name, profile_data):
        """
        Atualiza um perfil existente.
        
        Args:
            profile_name: Nome do perfil
            profile_data: Dicionário com os dados do perfil
            
        Returns:
            True se o perfil foi atualizado com sucesso, False caso contrário
        """
        if profile_name not in self.profiles:
            logger.error(f"Perfil não encontrado: {profile_name}")
            return False
        
        # Atualizar perfil
        self.profiles[profile_name] = profile_data
        
        # Salvar perfil
        success = self.save_profile(profile_name)
        
        if success:
            logger.info(f"Perfil atualizado: {profile_name}")
            
            # Se o perfil ativo foi atualizado, reativá-lo
            if self.active_profile and self.active_profile.get("name") == profile_name:
                self.activate_profile(profile_name)
        
        return success
    
    def delete_profile(self, profile_name):
        """
        Exclui um perfil.
        
        Args:
            profile_name: Nome do perfil
            
        Returns:
            True se o perfil foi excluído com sucesso, False caso contrário
        """
        if profile_name not in self.profiles:
            logger.error(f"Perfil não encontrado: {profile_name}")
            return False
        
        if profile_name == "default":
            logger.error("Não é possível excluir o perfil padrão")
            return False
        
        # Excluir arquivo de perfil
        profile_path = os.path.join(self.profiles_dir, f"{profile_name}.json")
        
        try:
            if os.path.exists(profile_path):
                os.remove(profile_path)
            
            # Remover do dicionário de perfis
            del self.profiles[profile_name]
            
            logger.info(f"Perfil excluído: {profile_name}")
            
            # Se o perfil ativo foi excluído, ativar o perfil padrão
            if self.active_profile and self.active_profile.get("name") == profile_name:
                self.activate_profile("default")
            
            return True
        except Exception as e:
            logger.error(f"Erro ao excluir perfil {profile_name}: {str(e)}")
            return False
    
    def save_profile(self, profile_name):
        """
        Salva um perfil em disco.
        
        Args:
            profile_name: Nome do perfil
            
        Returns:
            True se o perfil foi salvo com sucesso, False caso contrário
        """
        if profile_name not in self.profiles:
            logger.error(f"Perfil não encontrado: {profile_name}")
            return False
        
        # Criar diretório se não existir
        os.makedirs(self.profiles_dir, exist_ok=True)
        
        # Salvar perfil
        profile_path = os.path.join(self.profiles_dir, f"{profile_name}.json")
        
        try:
            with open(profile_path, 'w', encoding='utf-8') as f:
                json.dump(self.profiles[profile_name], f, indent=2, ensure_ascii=False)
            
            logger.info(f"Perfil salvo: {profile_name}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar perfil {profile_name}: {str(e)}")
            return False
    
    def list_profiles(self):
        """
        Lista todos os perfis disponíveis.
        
        Returns:
            Lista de nomes de perfis
        """
        return list(self.profiles.keys())

# Função para teste
def test_personality_manager():
    print("Testando gerenciador de personalidade...")
    
    # Inicializar gerenciador
    manager = PersonalityManager()
    
    # Listar perfis
    profiles = manager.list_profiles()
    print(f"\nPerfis disponíveis: {', '.join(profiles)}")
    
    # Obter perfil ativo
    active_profile = manager.get_active_profile()
    print(f"\nPerfil ativo: {active_profile['name']}")
    print(f"Nível de formalidade: {active_profile['personality']['formality_level']}")
    print(f"Nível de humor: {active_profile['personality']['humor_level']}")
    print(f"Nível de tecnicidade: {active_profile['personality']['technicality_level']}")
    
    # Criar novo perfil
    new_profile = copy.deepcopy(manager.get_profile("default"))
    new_profile["name"] = "Teste"
    new_profile["description"] = "Perfil de teste"
    new_profile["personality"]["formality_level"] = 80
    new_profile["personality"]["humor_level"] = 30
    
    success = manager.create_profile("teste", new_profile)
    print(f"\nCriação de perfil de teste: {'Sucesso' if success else 'Falha'}")
    
    # Ativar novo perfil
    manager.activate_profile("teste")
    active_profile = manager.get_active_profile()
    print(f"\nNovo perfil ativo: {active_profile['name']}")
    print(f"Nível de formalidade: {active_profile['personality']['formality_level']}")
    print(f"Nível de humor: {active_profile['personality']['humor_level']}")
    
    # Excluir perfil de teste
    success = manager.delete_profile("teste")
    print(f"\nExclusão de perfil de teste: {'Sucesso' if success else 'Falha'}")
    
    # Verificar perfil ativo após exclusão
    active_profile = manager.get_active_profile()
    print(f"\nPerfil ativo após exclusão: {active_profile['name']}")
    
    print("\nTeste concluído.")

if __name__ == "__main__":
    test_personality_manager()
```

## Criação do Gerenciador de Sessão

Vamos criar o gerenciador de sessão, que será responsável por manter o contexto da conversa:

1. Crie o arquivo `C:\NinaIA\nina_ia\core\session_manager.py` com o seguinte conteúdo:

```python
import os
import json
import logging
import time
import uuid
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("session_manager")

class SessionManager:
    def __init__(self, sessions_dir=None):
        """
        Inicializa o gerenciador de sessão.
        
        Args:
            sessions_dir: Diretório onde as sessões são armazenadas
        """
        if sessions_dir is None:
            sessions_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "data",
                "sessions"
            )
        
        self.sessions_dir = sessions_dir
        os.makedirs(self.sessions_dir, exist_ok=True)
        
        self.active_session = None
        self.session_id = None
    
    def create_session(self):
        """
        Cria uma nova sessão.
        
        Returns:
            ID da sessão criada
        """
        # Gerar ID único para a sessão
        session_id = str(uuid.uuid4())
        
        # Criar estrutura da sessão
        session = {
            "id": session_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "interactions": []
        }
        
        # Salvar sessão
        self._save_session(session_id, session)
        
        # Ativar sessão
        self.active_session = session
        self.session_id = session_id
        
        logger.info(f"Nova sessão criada: {session_id}")
        
        return session_id
    
    def load_session(self, session_id):
        """
        Carrega uma sessão existente.
        
        Args:
            session_id: ID da sessão a ser carregada
            
        Returns:
            True se a sessão foi carregada com sucesso, False caso contrário
        """
        session_path = os.path.join(self.sessions_dir, f"{session_id}.json")
        
        if not os.path.exists(session_path):
            logger.error(f"Sessão não encontrada: {session_id}")
            return False
        
        try:
            with open(session_path, 'r', encoding='utf-8') as f:
                session = json.load(f)
            
            self.active_session = session
            self.session_id = session_id
            
            logger.info(f"Sessão carregada: {session_id}")
            
            return True
        except Exception as e:
            logger.error(f"Erro ao carregar sessão {session_id}: {str(e)}")
            return False
    
    def add_interaction(self, user_input, assistant_response, metadata=None):
        """
 
(Content truncated due to size limit. Use line ranges to read in chunks)