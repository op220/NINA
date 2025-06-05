# Adaptação de Plugins com Base na Personalidade Aprendida

## Visão Geral

A adaptação de plugins é um componente essencial do sistema Nina IA que permite que os diferentes módulos e funcionalidades se ajustem dinamicamente com base na personalidade aprendida. Este documento descreve a implementação do sistema de adaptação de plugins, que permite que a IA modifique seu comportamento em diferentes contextos e interações.

## Arquitetura do Sistema

### Componentes Principais

1. **Gerenciador de Plugins**: Responsável por carregar, registrar e gerenciar plugins
2. **Adaptador de Plugins**: Ajusta o comportamento dos plugins com base na personalidade
3. **Contexto de Personalidade**: Fornece informações sobre a personalidade atual
4. **Interface de Plugin**: Define a interface padrão para todos os plugins adaptáveis

### Fluxo de Dados

1. O sistema de personalidade dinâmica atualiza o perfil da IA
2. O gerenciador de plugins notifica os plugins registrados sobre a mudança
3. Cada plugin adapta seu comportamento com base no novo perfil
4. O adaptador de plugins aplica transformações adicionais quando necessário

## Implementação

### Interface de Plugin Adaptável

```python
import os
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("adaptable_plugin.log")
    ]
)
logger = logging.getLogger("AdaptablePlugin")

class AdaptablePlugin(ABC):
    """
    Interface base para plugins adaptáveis.
    """
    
    def __init__(self, plugin_id: str, plugin_name: str):
        """
        Inicializa o plugin adaptável.
        
        Args:
            plugin_id: Identificador único do plugin
            plugin_name: Nome amigável do plugin
        """
        self.plugin_id = plugin_id
        self.plugin_name = plugin_name
        self.personality_context = {}
        self.enabled = True
        
        logger.info(f"Plugin adaptável inicializado: {plugin_name} ({plugin_id})")
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> bool:
        """
        Inicializa o plugin com configurações específicas.
        
        Args:
            config: Dicionário com configurações
            
        Returns:
            True se inicializado com sucesso, False caso contrário
        """
        pass
    
    @abstractmethod
    def process(self, input_data: Any) -> Any:
        """
        Processa dados de entrada.
        
        Args:
            input_data: Dados de entrada
            
        Returns:
            Dados processados
        """
        pass
    
    def update_personality_context(self, context: Dict[str, Any]) -> None:
        """
        Atualiza o contexto de personalidade.
        
        Args:
            context: Dicionário com contexto de personalidade
        """
        try:
            # Armazenar contexto anterior para comparação
            previous_context = self.personality_context.copy() if self.personality_context else {}
            
            # Atualizar contexto
            self.personality_context = context
            
            # Notificar sobre a atualização
            self.on_personality_updated(previous_context, context)
            
            logger.info(f"Contexto de personalidade atualizado para o plugin: {self.plugin_name}")
        except Exception as e:
            logger.error(f"Erro ao atualizar contexto de personalidade para o plugin {self.plugin_name}: {e}")
    
    def on_personality_updated(self, previous_context: Dict[str, Any], 
                              new_context: Dict[str, Any]) -> None:
        """
        Método chamado quando o contexto de personalidade é atualizado.
        
        Args:
            previous_context: Contexto anterior
            new_context: Novo contexto
        """
        try:
            # Implementação padrão (pode ser sobrescrita por subclasses)
            logger.info(f"Personalidade atualizada para o plugin: {self.plugin_name}")
            
            # Verificar mudanças significativas
            if previous_context and new_context:
                changes = []
                
                # Verificar mudanças na personalidade base
                if "personality" in previous_context and "personality" in new_context:
                    prev_personality = previous_context["personality"]
                    new_personality = new_context["personality"]
                    
                    for key in new_personality:
                        if key in prev_personality:
                            if isinstance(new_personality[key], (int, float)) and isinstance(prev_personality[key], (int, float)):
                                # Para valores numéricos, verificar diferença significativa
                                diff = abs(new_personality[key] - prev_personality[key])
                                if diff > 10:  # Diferença de 10% ou mais
                                    changes.append(f"{key}: {prev_personality[key]} -> {new_personality[key]}")
                            elif new_personality[key] != prev_personality[key]:
                                changes.append(f"{key}: {prev_personality[key]} -> {new_personality[key]}")
                
                if changes:
                    logger.info(f"Mudanças significativas para o plugin {self.plugin_name}: {', '.join(changes)}")
        except Exception as e:
            logger.error(f"Erro ao processar atualização de personalidade para o plugin {self.plugin_name}: {e}")
    
    def enable(self) -> None:
        """
        Habilita o plugin.
        """
        self.enabled = True
        logger.info(f"Plugin habilitado: {self.plugin_name}")
    
    def disable(self) -> None:
        """
        Desabilita o plugin.
        """
        self.enabled = False
        logger.info(f"Plugin desabilitado: {self.plugin_name}")
    
    def is_enabled(self) -> bool:
        """
        Verifica se o plugin está habilitado.
        
        Returns:
            True se habilitado, False caso contrário
        """
        return self.enabled
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Obtém metadados do plugin.
        
        Returns:
            Dicionário com metadados
        """
        return {
            "id": self.plugin_id,
            "name": self.plugin_name,
            "enabled": self.enabled,
            "has_personality_context": bool(self.personality_context)
        }
```

### Gerenciador de Plugins

```python
import os
import json
import logging
import importlib
import inspect
from typing import Dict, List, Any, Optional, Union, Type

# Importar interface de plugin
from adaptable_plugin import AdaptablePlugin

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("plugin_manager.log")
    ]
)
logger = logging.getLogger("PluginManager")

class PluginManager:
    """
    Gerenciador de plugins adaptáveis.
    """
    
    def __init__(self, plugins_dir: str = "./plugins", config_path: str = "./config/plugins.json"):
        """
        Inicializa o gerenciador de plugins.
        
        Args:
            plugins_dir: Diretório de plugins
            config_path: Caminho para o arquivo de configuração
        """
        self.plugins_dir = plugins_dir
        self.config_path = config_path
        self.plugins = {}  # id -> instância
        self.plugin_classes = {}  # id -> classe
        
        # Garantir que os diretórios existam
        os.makedirs(plugins_dir, exist_ok=True)
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        # Carregar configuração
        self.config = self._load_config()
        
        logger.info(f"Gerenciador de plugins inicializado. Diretório: {plugins_dir}")
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Carrega o arquivo de configuração.
        
        Returns:
            Dicionário com configurações
        """
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Configuração padrão
                config = {
                    "enabled_plugins": [],
                    "plugin_configs": {}
                }
                
                # Salvar configuração padrão
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                
                return config
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {e}")
            return {
                "enabled_plugins": [],
                "plugin_configs": {}
            }
    
    def _save_config(self) -> bool:
        """
        Salva o arquivo de configuração.
        
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        try:
            # Atualizar lista de plugins habilitados
            self.config["enabled_plugins"] = [
                plugin_id for plugin_id, plugin in self.plugins.items() if plugin.is_enabled()
            ]
            
            # Salvar configuração
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Configuração salva: {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar configuração: {e}")
            return False
    
    def discover_plugins(self) -> List[str]:
        """
        Descobre plugins disponíveis.
        
        Returns:
            Lista com IDs de plugins descobertos
        """
        try:
            discovered_plugins = []
            
            # Verificar se o diretório existe
            if not os.path.exists(self.plugins_dir):
                logger.warning(f"Diretório de plugins não existe: {self.plugins_dir}")
                return discovered_plugins
            
            # Adicionar diretório ao path
            import sys
            if self.plugins_dir not in sys.path:
                sys.path.append(self.plugins_dir)
            
            # Procurar arquivos Python
            for filename in os.listdir(self.plugins_dir):
                if filename.endswith(".py") and not filename.startswith("__"):
                    module_name = filename[:-3]  # Remover .py
                    
                    try:
                        # Importar módulo
                        module = importlib.import_module(module_name)
                        
                        # Procurar classes que herdam de AdaptablePlugin
                        for name, obj in inspect.getmembers(module):
                            if (inspect.isclass(obj) and 
                                issubclass(obj, AdaptablePlugin) and 
                                obj != AdaptablePlugin):
                                
                                # Criar instância temporária para obter ID
                                try:
                                    instance = obj("temp_id", "Temporary Instance")
                                    plugin_id = instance.plugin_id
                                    
                                    # Armazenar classe
                                    self.plugin_classes[plugin_id] = obj
                                    
                                    # Adicionar à lista de descobertos
                                    discovered_plugins.append(plugin_id)
                                    
                                    logger.info(f"Plugin descoberto: {plugin_id} ({name})")
                                except Exception as e:
                                    logger.error(f"Erro ao instanciar plugin {name}: {e}")
                    except Exception as e:
                        logger.error(f"Erro ao importar módulo {module_name}: {e}")
            
            return discovered_plugins
        except Exception as e:
            logger.error(f"Erro ao descobrir plugins: {e}")
            return []
    
    def load_plugin(self, plugin_id: str) -> bool:
        """
        Carrega um plugin.
        
        Args:
            plugin_id: ID do plugin
            
        Returns:
            True se carregou com sucesso, False caso contrário
        """
        try:
            # Verificar se o plugin já está carregado
            if plugin_id in self.plugins:
                logger.info(f"Plugin já carregado: {plugin_id}")
                return True
            
            # Verificar se a classe está disponível
            if plugin_id not in self.plugin_classes:
                # Tentar descobrir plugins
                self.discover_plugins()
                
                if plugin_id not in self.plugin_classes:
                    logger.error(f"Plugin não encontrado: {plugin_id}")
                    return False
            
            # Obter classe
            plugin_class = self.plugin_classes[plugin_id]
            
            # Criar instância
            plugin = plugin_class(plugin_id, plugin_class.__name__)
            
            # Obter configuração
            plugin_config = self.config["plugin_configs"].get(plugin_id, {})
            
            # Inicializar plugin
            if not plugin.initialize(plugin_config):
                logger.error(f"Falha ao inicializar plugin: {plugin_id}")
                return False
            
            # Verificar se o plugin deve estar habilitado
            if plugin_id in self.config["enabled_plugins"]:
                plugin.enable()
            else:
                plugin.disable()
            
            # Armazenar instância
            self.plugins[plugin_id] = plugin
            
            logger.info(f"Plugin carregado: {plugin_id}")
            return True
        except Exception as e:
            logger.error(f"Erro ao carregar plugin {plugin_id}: {e}")
            return False
    
    def load_all_plugins(self) -> int:
        """
        Carrega todos os plugins disponíveis.
        
        Returns:
            Número de plugins carregados com sucesso
        """
        try:
            # Descobrir plugins
            plugin_ids = self.discover_plugins()
            
            # Carregar cada plugin
            success_count = 0
            for plugin_id in plugin_ids:
                if self.load_plugin(plugin_id):
                    success_count += 1
            
            logger.info(f"{success_count}/{len(plugin_ids)} plugins carregados com sucesso")
            return success_count
        except Exception as e:
            logger.error(f"Erro ao carregar todos os plugins: {e}")
            return 0
    
    def unload_plugin(self, plugin_id: str) -> bool:
        """
        Descarrega um plugin.
        
        Args:
            plugin_id: ID do plugin
            
        Returns:
            True se descarregou com sucesso, False caso contrário
        """
        try:
            # Verificar se o plugin está carregado
            if plugin_id not in self.plugins:
                logger.info(f"Plugin não está carregado: {plugin_id}")
                return True
            
            # Remover instância
            del self.plugins[plugin_id]
            
            logger.info(f"Plugin descarregado: {plugin_id}")
            return True
        except Exception as e:
            logger.error(f"Erro ao descarregar plugin {plugin_id}: {e}")
  
(Content truncated due to size limit. Use line ranges to read in chunks)