# Integração do Sistema de Personalidade por Canal com o Nina IA

## Visão Geral

Este documento descreve a integração do sistema de personalidade por canal com o sistema Nina IA existente. A integração permite que a Nina IA adapte seu comportamento de forma diferente em diferentes canais do Discord, mantendo a compatibilidade com todos os componentes existentes e garantindo um funcionamento harmonioso do sistema como um todo.

## Arquitetura da Integração

### Componentes Principais

1. **Módulo de Integração**: Conecta o sistema de personalidade por canal com o sistema Nina IA
2. **Adaptador de Orquestração**: Modifica o orquestrador principal para suportar contextos de canal
3. **Gerenciador de Sessão Aprimorado**: Estende o gerenciador de sessão para incluir informações de canal
4. **Ponte de Comunicação Discord**: Conecta o cliente Discord com o sistema Nina IA

### Fluxo de Dados

1. Uma mensagem é recebida do Discord através da ponte de comunicação
2. O gerenciador de sessão aprimorado identifica o canal e carrega o contexto apropriado
3. O adaptador de orquestração processa a mensagem usando o contexto do canal
4. A resposta é gerada e adaptada com base no perfil do canal
5. A resposta é enviada de volta ao Discord através da ponte de comunicação

## Implementação

### Módulo de Integração

```python
import os
import json
import logging
from typing import Dict, List, Any, Optional, Union

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("nina_integration.log")
    ]
)
logger = logging.getLogger("NinaIntegration")

class NinaIntegration:
    """
    Módulo de integração entre o sistema de personalidade por canal e o Nina IA.
    """
    
    def __init__(self, nina_system=None, personality_system=None):
        """
        Inicializa o módulo de integração.
        
        Args:
            nina_system: Instância do sistema Nina IA
            personality_system: Instância do sistema de personalidade
        """
        self.nina_system = nina_system
        self.personality_system = personality_system
        
        logger.info("Módulo de integração inicializado")
    
    def set_nina_system(self, nina_system) -> None:
        """
        Define o sistema Nina IA.
        
        Args:
            nina_system: Instância do sistema Nina IA
        """
        self.nina_system = nina_system
        logger.info("Sistema Nina IA definido")
    
    def set_personality_system(self, personality_system) -> None:
        """
        Define o sistema de personalidade.
        
        Args:
            personality_system: Instância do sistema de personalidade
        """
        self.personality_system = personality_system
        logger.info("Sistema de personalidade definido")
    
    def initialize(self) -> bool:
        """
        Inicializa a integração entre os sistemas.
        
        Returns:
            True se inicializado com sucesso, False caso contrário
        """
        try:
            # Verificar se os sistemas estão disponíveis
            if not self.nina_system:
                logger.error("Sistema Nina IA não disponível")
                return False
            
            if not self.personality_system:
                logger.error("Sistema de personalidade não disponível")
                return False
            
            # Conectar sistemas
            self._connect_systems()
            
            logger.info("Integração inicializada com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao inicializar integração: {e}")
            return False
    
    def _connect_systems(self) -> None:
        """
        Conecta os sistemas Nina IA e de personalidade.
        """
        try:
            # Verificar se o sistema Nina IA tem os componentes necessários
            if hasattr(self.nina_system, 'orchestrator'):
                # Conectar orquestrador com sistema de personalidade
                if hasattr(self.personality_system, 'channel_adapter'):
                    self.nina_system.orchestrator.set_channel_adapter(
                        self.personality_system.channel_adapter
                    )
                    logger.info("Orquestrador conectado com adaptador de canal")
            
            # Verificar se o sistema Nina IA tem gerenciador de sessão
            if hasattr(self.nina_system, 'session_manager'):
                # Conectar gerenciador de sessão com seletor de contexto
                if hasattr(self.personality_system, 'context_selector'):
                    self.nina_system.session_manager.set_context_selector(
                        self.personality_system.context_selector
                    )
                    logger.info("Gerenciador de sessão conectado com seletor de contexto")
            
            # Verificar se o sistema Nina IA tem processador LLM
            if hasattr(self.nina_system, 'llm_processor'):
                # Conectar processador LLM com sistema de personalidade
                self.nina_system.llm_processor.set_personality_system(
                    self.personality_system
                )
                logger.info("Processador LLM conectado com sistema de personalidade")
            
            logger.info("Sistemas conectados com sucesso")
        except Exception as e:
            logger.error(f"Erro ao conectar sistemas: {e}")
            raise
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa uma mensagem usando os sistemas integrados.
        
        Args:
            message: Dicionário com dados da mensagem
            
        Returns:
            Dicionário com resposta processada
        """
        try:
            # Extrair dados da mensagem
            guild_id = message.get("guild_id")
            channel_id = message.get("channel_id")
            user_id = message.get("user_id")
            content = message.get("content", "")
            
            # Verificar se os IDs estão presentes
            if not guild_id or not channel_id or not user_id:
                logger.error("IDs de guild, channel ou user ausentes na mensagem")
                return {
                    "success": False,
                    "error": "Dados incompletos na mensagem"
                }
            
            # Criar sessão para o usuário/canal
            session_id = f"{guild_id}_{channel_id}_{user_id}"
            
            # Processar mensagem com o sistema Nina IA
            response = self.nina_system.process_message(
                session_id=session_id,
                message=content,
                context={
                    "guild_id": guild_id,
                    "channel_id": channel_id,
                    "user_id": user_id
                }
            )
            
            return {
                "success": True,
                "response": response,
                "session_id": session_id
            }
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def update_channel_info(self, guild_id: str, channel_id: str, 
                           channel_info: Dict[str, Any]) -> bool:
        """
        Atualiza informações de um canal.
        
        Args:
            guild_id: ID do servidor
            channel_id: ID do canal
            channel_info: Dicionário com informações do canal
            
        Returns:
            True se atualizou com sucesso, False caso contrário
        """
        try:
            # Verificar se o sistema de personalidade tem adaptador de canal
            if hasattr(self.personality_system, 'channel_adapter'):
                # Processar informações do canal
                self.personality_system.channel_adapter.process_channel_info(
                    guild_id, channel_id, channel_info
                )
                
                logger.info(f"Informações do canal {guild_id}_{channel_id} atualizadas")
                return True
            else:
                logger.error("Adaptador de canal não disponível")
                return False
        except Exception as e:
            logger.error(f"Erro ao atualizar informações do canal {guild_id}_{channel_id}: {e}")
            return False
    
    def process_insights(self, guild_id: str, channel_id: str, 
                        insights: Dict[str, Any]) -> bool:
        """
        Processa insights de conversas para um canal.
        
        Args:
            guild_id: ID do servidor
            channel_id: ID do canal
            insights: Dicionário com insights de conversas
            
        Returns:
            True se processou com sucesso, False caso contrário
        """
        try:
            # Verificar se o sistema de personalidade tem método para processar insights
            if hasattr(self.personality_system, 'process_channel_insights'):
                # Processar insights
                self.personality_system.process_channel_insights(
                    guild_id, channel_id, insights
                )
                
                logger.info(f"Insights processados para o canal {guild_id}_{channel_id}")
                return True
            else:
                logger.error("Método para processar insights não disponível")
                return False
        except Exception as e:
            logger.error(f"Erro ao processar insights para o canal {guild_id}_{channel_id}: {e}")
            return False
```

### Adaptador de Orquestração

```python
import os
import json
import logging
from typing import Dict, List, Any, Optional, Union

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("orchestration_adapter.log")
    ]
)
logger = logging.getLogger("OrchestrationAdapter")

class OrchestrationAdapter:
    """
    Adaptador para o orquestrador principal do Nina IA.
    """
    
    def __init__(self, orchestrator=None, channel_adapter=None):
        """
        Inicializa o adaptador de orquestração.
        
        Args:
            orchestrator: Instância do orquestrador original
            channel_adapter: Instância do adaptador de canal
        """
        self.orchestrator = orchestrator
        self.channel_adapter = channel_adapter
        
        logger.info("Adaptador de orquestração inicializado")
    
    def set_orchestrator(self, orchestrator) -> None:
        """
        Define o orquestrador original.
        
        Args:
            orchestrator: Instância do orquestrador
        """
        self.orchestrator = orchestrator
        logger.info("Orquestrador definido")
    
    def set_channel_adapter(self, channel_adapter) -> None:
        """
        Define o adaptador de canal.
        
        Args:
            channel_adapter: Instância do adaptador de canal
        """
        self.channel_adapter = channel_adapter
        logger.info("Adaptador de canal definido")
    
    def process_message(self, session_id: str, message: str, 
                       context: Dict[str, Any] = None) -> str:
        """
        Processa uma mensagem usando o orquestrador e adaptador de canal.
        
        Args:
            session_id: ID da sessão
            message: Mensagem do usuário
            context: Contexto adicional (opcional)
            
        Returns:
            Resposta processada
        """
        try:
            # Verificar se o orquestrador está disponível
            if not self.orchestrator:
                logger.error("Orquestrador não disponível")
                return "Desculpe, ocorreu um erro ao processar sua mensagem."
            
            # Extrair IDs do contexto
            guild_id = None
            channel_id = None
            
            if context:
                guild_id = context.get("guild_id")
                channel_id = context.get("channel_id")
            
            # Processar mensagem com o orquestrador original
            response = self.orchestrator.process_message(session_id, message, context)
            
            # Adaptar resposta se o adaptador de canal estiver disponível
            if self.channel_adapter and guild_id and channel_id:
                response = self.channel_adapter.adapt_response(response, guild_id, channel_id)
            
            return response
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
            return "Desculpe, ocorreu um erro ao processar sua mensagem."
    
    def get_system_prompt(self, session_id: str, context: Dict[str, Any] = None) -> str:
        """
        Obtém o prompt de sistema para uma sessão.
        
        Args:
            session_id: ID da sessão
            context: Contexto adicional (opcional)
            
        Returns:
            String com prompt de sistema
        """
        try:
            # Extrair IDs do contexto
            guild_id = None
            channel_id = None
            
            if context:
                guild_id = context.get("guild_id")
                channel_id = context.get("channel_id")
            
            # Obter prompt de sistema do adaptador de canal se disponível
            if self.channel_adapter and guild_id and channel_id:
                return self.channel_adapter.get_system_prompt(guild_id, channel_id)
            
            # Caso contrário, usar o método original do orquestrador
            if self.orchestrator and hasattr(self.orchestrator, 'get_system_prompt'):
                return self.orchestrator.get_system_prompt(session_id, context)
            
            # Fallback para prompt padrão
            return "Você é Nina, uma assistente de IA amigável e prestativa."
        except Exception as e:
            logger.error(f"Erro ao obter prompt de sistema: {e}")
            return "Você é Nina, uma assistente de IA amigável e prestativa."
```

### Gerenciador de Sessão Aprimorado

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
        logging.FileHandler("enhanced_session_manager.log")
    ]
)
logger = logging.getLogger("EnhancedSessionManager")

class EnhancedSessionManager:
    """
    Gerenciador de sessão aprimorado com suporte a contextos de canal.
    """
    
    def __init__(self, session_manager=None, context_selector=None):
        """
        Inicializa o gerenciador de sessão aprimorado.
        
        Args:
            session_manager: Instância do gerenciador de sessão original
            context_selector: Instância do seletor de contexto
        """
        self.session_manager = session_manager
        self.context_selector = context_selector
        self.channel_sessions = {}  # session_id -> {guild_id, channel_id}
        
        logger.info("Gerenciador de sessão aprimorado inicializado")
    
    def set_session_manager(self, session_manager) -> None:
        """
        Define o gerenciador de sessão original.
        
        Args:
            session_manager: Instância do gerenciador de sessão
        """
        self.session_manager = session_manager
        logger.info("Gerenciador de sessão definido")
    
    def set_context_selector(self, context_selector) -> None:
        """
        Define o seletor de contexto.
        
        Args:
            context_selector: Instância do seletor de contexto
        """
        self.context_selector = context_selector
        logger.info("Seletor de contexto definido")
    
    def create_session(self, session_id: str, context: Dict[str, Any] = None) -> bool:
        """
        Cria uma nova sessão.
        
        Args:
            session_id: ID da sessão
            context: Contexto adicional (opcional)
            
        Returns:
            True se criou com sucesso, False caso contrário
        """
        try:
            # Verificar se o gerenciador de sessão original está disponível
            if not self.session_manager:
                logger.error("Gerenciador de sessão original não disponível")
                return False
            
            # Extrair IDs do contexto
            guild_id = None
            channel_id = None
            
            if context:
                guild_id = context.get("guild_id")
                channel_id = context.get("channel_id")
            
            # Criar sessão no gerenciador original
            result = self.session_manager.create_session(session_id, context)
            
            # Armazenar informações de canal se disponíveis
            if result and guild_id and channel_id:
                self.channel_sessions[session_id] = {
                    "guild_id": guild_id,
                    "channel_id": channel_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
            
            return result
        except Exception as e:
            logger.error(f"Erro ao criar sessão {session_id}: {e}")
            return False
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtém uma sessão.
        
        Args:
            session_id: ID da sessão
            
        Returns:
            Dicionário com dados da sessão ou None se não encontrada
        """
        try:
            # Verificar se o gerenciador de sessão original está disponível
            if not self.session_manager:
                logger.error("Gerenciador de sessão original não disponível")
                return None
            
            # Obter sessão do gerenciador original
            session = self.session_manager.get_session(session_id)
            
            # Adicionar informações de canal se disponíveis
            if session and session_id in self.channel_sessions:
                session["guild_id"] = self.channel_sessions[session_id]["guild_id"]
                session["channel_id"] = self.channel_sessions[session_id]["channel_id"]
            
            return session
        except Exception as e:
            logger.error(f"Erro ao obter sessão {session_id}: {e}")
            return None
    
    def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """
        Atualiza uma sessão.
        
        Args:
            session_id: ID da sessão
            updates: Dicionário com atualizações
            
        Returns:
            True se atualizou com sucesso, False caso contrário
        """
        try:
            # Verificar se o gerenciador de sessão original está disponível
            if not self.session_manager:
                logger.error("Gerenciador de sessão original não disponível")
                return False
            
            # Extrair IDs do contexto
            guild_id = updates.pop("guild_id", None)
            channel_id = updates.pop("channel_id", None)
            
            # Atualizar sessão no gerenciador original
            result = self.session_manager.update_session(session_id, updates)
            
            # Atualizar informações de canal se disponíveis
            if result and guild_id and channel_id:
                if session_id in self.channel_sessions:
                    self.channel_sessions[session_id]["guild_id"] = guild_id
                    self.channel_sessions[session_id]["channel_id"] = channel_id
                    self.channel_sessions[session_id]["updated_at"] = datetime.now().isoformat()
                else:
                    self.channel_sessions[session_id] = {
                        "guild_id": guild_id,
                        "channel_id": channel_id,
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat()
                    }
            
            return result
        except Exception as e:
            logger.error(f"Erro ao atualizar sessão {session_id}: {e}")
            return False
    
    def delete_session(self, session_id: str) -> bool:
        """
        Exclui uma sessão.
        
        Args:
            session_id: ID da sessão
            
        Returns:
            True se excluiu com sucesso, False caso contrário
        """
        try:
            # Verificar se o gerenciador de sessão original está disponível
            if not self.session_manager:
                logger.error("Gerenciador de sessão original não disponível")
                return False
            
            # Excluir sessão do gerenciador original
            result = self.session_manager.delete_session(session_id)
            
            # Remover informações de canal
            if result and session_id in self.channel_sessions:
                del self.channel_sessions[session_id]
            
            return result
        except Exception as e:
            logger.error(f"Erro ao excluir sessão {session_id}: {e}")
            return False
    
    def get_session_context(self, session_id: str) -> Dict[str, Any]:
        """
        Obtém o contexto de uma sessão.
        
        Args:
            session_id: ID da sessão
            
        Returns:
            Dicionário com contexto da sessão
        """
        try:
            # Verificar se o gerenciador de sessão original está disponível
            if not self.session_manager:
                logger.error("Gerenciador de sessão original não disponível")
                return {}
            
            # Obter contexto do gerenciador original
            context = self.session_manager.get_session_context(session_id)
            
            # Adicionar informações de canal se disponíveis
            if session_id in self.channel_sessions:
                guild_id = self.channel_sessions[session_id]["guild_id"]
                channel_id = self.channel_sessions[session_id]["channel_id"]
                
                context["guild_id"] = guild_id
                context["channel_id"] = channel_id
                
                # Adicionar contexto de personalidade se o seletor estiver disponível
                if self.context_selector:
                    personality_context = self.context_selector.select_context(guild_id, channel_id)
                    context["personality"] = personality_context
            
            return context
        except Exception as e:
            logger.error(f"Erro ao obter contexto da sessão {session_id}: {e}")
            return {}
    
    def add_message_to_history(self, session_id: str, role: str, content: str) -> bool:
        """
        Adiciona uma mensagem ao histórico da sessão.
        
        Args:
            session_id: ID da sessão
            role: Papel do remetente (user/assistant)
            content: Conteúdo da mensagem
            
        Returns:
            True se adicionou com sucesso, False caso contrário
        """
        try:
            # Verificar se o gerenciador de sessão original está disponível
            if not self.session_manager:
                logger.error("Gerenciador de sessão original não disponível")
                return False
            
            # Adicionar mensagem ao histórico no gerenciador original
            result = self.session_manager.add_message_to_history(session_id, role, content)
            
            # Atualizar timestamp se a sessão tiver informações de canal
            if result and session_id in self.channel_sessions:
                self.channel_sessions[session_id]["updated_at"] = datetime.now().isoformat()
            
            return result
        except Exception as e:
            logger.error(f"Erro ao adicionar mensagem ao histórico da sessão {session_id}: {e}")
            return False
    
    def get_message_history(self, session_id: str, max_messages: int = None) -> List[Dict[str, str]]:
        """
        Obtém o histórico de mensagens de uma sessão.
        
        Args:
            session_id: ID da sessão
            max_messages: Número máximo de mensagens (opcional)
            
        Returns:
            Lista com histórico de mensagens
        """
        try:
            # Verificar se o gerenciador de sessão original está disponível
            if not self.session_manager:
                logger.error("Gerenciador de sessão original não disponível")
                return []
            
            # Obter histórico do gerenciador original
            return self.session_manager.get_message_history(session_id, max_messages)
        except Exception as e:
            logger.error(f"Erro ao obter histórico de mensagens da sessão {session_id}: {e}")
            return []
    
    def get_channel_info(self, session_id: str) -> Optional[Dict[str, str]]:
        """
        Obtém informações de canal de uma sessão.
        
        Args:
            session_id: ID da sessão
            
        Returns:
            Dicionário com informações de canal ou None se não disponíveis
        """
        try:
            # Verificar se a sessão tem informações de canal
            if session_id in self.channel_sessions:
                return {
                    "guild_id": self.channel_sessions[session_id]["guild_id"],
                    "channel_id": self.channel_sessions[session_id]["channel_id"]
                }
            else:
                return None
        except Exception as e:
            logger.error(f"Erro ao obter informações de canal da sessão {session_id}: {e}")
            return None
```

### Ponte de Comunicação Discord

```python
import os
import json
import logging
import asyncio
import discord
from discord.ext import commands
from typing import Dict, List, Any, Optional, Union

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("discord_bridge.log")
    ]
)
logger = logging.getLogger("DiscordBridge")

class DiscordBridge:
    """
    Ponte de comunicação entre o Discord e o sistema Nina IA.
    """
    
    def __init__(self, nina_integration=None):
        """
        Inicializa a ponte de comunicação.
        
        Args:
            nina_integration: Instância do módulo de integração Nina
        """
        self.nina_integration = nina_integration
        self.bot = None
        self.active_channels = {}  # guild_id_channel_id -> last_activity_timestamp
        
        logger.info("Ponte de comunicação Discord inicializada")
    
    def set_nina_integration(self, nina_integration) -> None:
        """
        Define o módulo de integração Nina.
        
        Args:
            nina_integration: Instância do módulo de integração Nina
        """
        self.nina_integration = nina_integration
        logger.info("Módulo de integração Nina definido")
    
    def initialize_bot(self, token: str) -> None:
        """
        Inicializa o bot do Discord.
        
        Args:
            token: Token de autenticação do bot
        """
        try:
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True
            
            self.bot = commands.Bot(command_prefix="!", intents=intents)
            
            # Registrar eventos
            @self.bot.event
            async def on_ready():
                logger.info(f"Bot conectado como {self.bot.user}")
                
                # Inicializar canais
                await self._initialize_channels()
            
            @self.bot.event
            async def on_message(message):
                # Ignorar mensagens do próprio bot
                if message.author == self.bot.user:
                    return
                
                # Processar comandos
                await self.bot.process_commands(message)
                
                # Processar mensagem para Nina IA
                await self._process_message(message)
            
            @self.bot.event
            async def on_guild_channel_create(channel):
                # Inicializar novo canal
                await self._initialize_channel(channel)
            
            # Registrar comandos
            @self.bot.command(name="nina_help")
            async def nina_help(ctx):
                """Mostra informações de ajuda sobre a Nina IA."""
                embed = discord.Embed(
                    title="Ajuda da Nina IA",
                    description="Nina é uma assistente de IA que aprende com as conversas do Discord.",
                    color=discord.Color.blue()
                )
                
                embed.add_field(
                    name="Comandos Disponíveis",
                    value=(
                        "!nina_help - Mostra esta mensagem de ajuda\n"
                        "!nina_status - Verifica o status da Nina IA\n"
                        "!nina_reset - Reseta a personalidade do canal atual\n"
                        "!nina_personality - Mostra a personalidade atual do canal"
                    ),
                    inline=False
                )
                
                embed.add_field(
                    name="Como Usar",
                    value=(
                        "Basta mencionar @Nina ou usar o prefixo 'Nina, ' para interagir com a IA.\n"
                        "Exemplo: 'Nina, como está o tempo hoje?'"
                    ),
                    inline=False
                )
                
                await ctx.send(embed=embed)
            
            @self.bot.command(name="nina_status")
            async def nina_status(ctx):
                """Verifica o status da Nina IA."""
                if self.nina_integration:
                    await ctx.send("Nina IA está online e funcionando normalmente.")
                else:
                    await ctx.send("Nina IA está offline no momento.")
            
            @self.bot.command(name="nina_reset")
            async def nina_reset(ctx):
                """Reseta a personalidade do canal atual."""
                if not self.nina_integration:
                    await ctx.send("Nina IA está offline no momento.")
                    return
                
                guild_id = str(ctx.guild.id)
                channel_id = str(ctx.channel.id)
                
                # Atualizar informações do canal
                channel_info = {
                    "name": ctx.channel.name,
                    "description": ctx.channel.topic or "",
                    "category": ctx.channel.category.name if ctx.channel.category else "",
                    "is_nsfw": ctx.channel.is_nsfw()
                }
                
                # Resetar personalidade do canal
                if hasattr(self.nina_integration.personality_system, 'channel_adapter') and \
                   hasattr(self.nina_integration.personality_system.channel_adapter.context_selector, 'channel_profile_manager'):
                    
                    result = self.nina_integration.personality_system.channel_adapter.context_selector.channel_profile_manager.reset_profile(
                        guild_id, channel_id
                    )
                    
                    if result:
                        # Atualizar informações do canal após reset
                        self.nina_integration.update_channel_info(guild_id, channel_id, channel_info)
                        
                        await ctx.send("Personalidade do canal resetada para os valores padrão.")
                    else:
                        await ctx.send("Erro ao resetar personalidade do canal.")
                else:
                    await ctx.send("Sistema de personalidade por canal não está disponível.")
            
            @self.bot.command(name="nina_personality")
            async def nina_personality(ctx):
                """Mostra a personalidade atual do canal."""
                if not self.nina_integration:
                    await ctx.send("Nina IA está offline no momento.")
                    return
                
                guild_id = str(ctx.guild.id)
                channel_id = str(ctx.channel.id)
                
                # Obter perfil do canal
                if hasattr(self.nina_integration.personality_system, 'channel_adapter') and \
                   hasattr(self.nina_integration.personality_system.channel_adapter.context_selector, 'channel_profile_manager'):
                    
                    profile = self.nina_integration.personality_system.channel_adapter.context_selector.channel_profile_manager.load_profile(
                        guild_id, channel_id
                    )
                    
                    # Criar embed
                    embed = discord.Embed(
                        title=f"Personalidade da Nina no Canal #{ctx.channel.name}",
                        description="Características de personalidade aprendidas para este canal.",
                        color=discord.Color.blue()
                    )
                    
                    # Adicionar campos
                    personality = profile["base_personality"]
                    embed.add_field(
                        name="Tom",
                        value=personality.get("tone", "neutro"),
                        inline=True
                    )
                    embed.add_field(
                        name="Formalidade",
                        value=f"{personality.get('formality_level', 50)}/100",
                        inline=True
                    )
                    embed.add_field(
                        name="Humor",
                        value=f"{personality.get('humor_level', 30)}/100",
                        inline=True
                    )
                    embed.add_field(
                        name="Empatia",
                        value=f"{personality.get('empathy_level', 70)}/100",
                        inline=True
                    )
                    embed.add_field(
                        name="Tecnicidade",
                        value=f"{personality.get('technicality_level', 50)}/100",
                        inline=True
                    )
                    
                    # Adicionar tópicos favoritos
                    favorite_topics = profile["topics"]["favorite_topics"]
                    if favorite_topics:
                        topics_text = ""
                        for topic in favorite_topics[:5]:
                            if isinstance(topic, dict) and "topic" in topic:
                                topics_text += f"• {topic['topic']}\n"
                            elif isinstance(topic, str):
                                topics_text += f"• {topic}\n"
                        
                        if topics_text:
                            embed.add_field(
                                name="Tópicos Favoritos",
                                value=topics_text,
                                inline=False
                            )
                    
                    # Adicionar vocabulário personalizado
                    custom_vocab = profile["vocabulary"]["custom_vocabulary"]
                    if custom_vocab:
                        vocab_text = ", ".join(custom_vocab[:10])
                        
                        if vocab_text:
                            embed.add_field(
                                name="Vocabulário Personalizado",
                                value=vocab_text,
                                inline=False
                            )
                    
                    # Adicionar estatísticas
                    embed.add_field(
                        name="Interações",
                        value=profile["interaction_history"]["total_interactions"],
                        inline=True
                    )
                    
                    # Enviar embed
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Sistema de personalidade por canal não está disponível.")
            
            # Iniciar bot
            self.bot.run(token)
            
        except Exception as e:
            logger.error(f"Erro ao inicializar bot: {e}")
    
    async def _initialize_channels(self) -> None:
        """
        Inicializa todos os canais disponíveis.
        """
        try:
            for guild in self.bot.guilds:
                for channel in guild.text_channels:
                    await self._initialize_channel(channel)
            
            logger.info("Canais inicializados")
        except Exception as e:
            logger.error(f"Erro ao inicializar canais: {e}")
    
    async def _initialize_channel(self, channel) -> None:
        """
        Inicializa um canal.
        
        Args:
            channel: Objeto de canal do Discord
        """
        try:
            # Verificar se é um canal de texto
            if not isinstance(channel, discord.TextChannel):
                return
            
            # Verificar se o módulo de integração está disponível
            if not self.nina_integration:
                logger.warning("Módulo de integração Nina não disponível")
                return
            
            guild_id = str(channel.guild.id)
            channel_id = str(channel.id)
            
            # Obter informações do canal
            channel_info = {
                "name": channel.name,
                "description": channel.topic or "",
                "category": channel.category.name if channel.category else "",
                "is_nsfw": channel.is_nsfw()
            }
            
            # Atualizar informações do canal
            self.nina_integration.update_channel_info(guild_id, channel_id, channel_info)
            
            # Adicionar à lista de canais ativos
            self.active_channels[f"{guild_id}_{channel_id}"] = {
                "last_activity": discord.utils.utcnow().timestamp(),
                "name": channel.name,
                "guild_name": channel.guild.name
            }
            
            logger.info(f"Canal inicializado: {channel.guild.name} / #{channel.name}")
        except Exception as e:
            logger.error(f"Erro ao inicializar canal {channel.name}: {e}")
    
    async def _process_message(self, message) -> None:
        """
        Processa uma mensagem para Nina IA.
        
        Args:
            message: Objeto de mensagem do Discord
        """
        try:
            # Verificar se o módulo de integração está disponível
            if not self.nina_integration:
                logger.warning("Módulo de integração Nina não disponível")
                return
            
            # Verificar se a mensagem é para a Nina
            if not self._is_message_for_nina(message):
                return
            
            # Extrair conteúdo da mensagem
            content = self._extract_message_content(message)
            
            # Preparar dados da mensagem
            message_data = {
                "guild_id": str(message.guild.id),
                "channel_id": str(message.channel.id),
                "user_id": str(message.author.id),
                "username": message.author.name,
                "content": content,
                "timestamp": message.created_at.isoformat(),
                "attachments": [a.url for a in message.attachments],
                "mentions": [str(u.id) for u in message.mentions]
            }
            
            # Processar mensagem com o módulo de integração
            response_data = self.nina_integration.process_message(message_data)
            
            # Verificar se o processamento foi bem-sucedido
            if response_data["success"]:
                # Enviar resposta
                await message.channel.send(response_data["response"])
            else:
                # Enviar mensagem de erro
                await message.channel.send("Desculpe, ocorreu um erro ao processar sua mensagem.")
            
            logger.info(f"Mensagem processada: {message.guild.name} / #{message.channel.name}")
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
            
            # Tentar enviar mensagem de erro
            try:
                await message.channel.send("Desculpe, ocorreu um erro ao processar sua mensagem.")
            except:
                pass
    
    def _is_message_for_nina(self, message) -> bool:
        """
        Verifica se uma mensagem é direcionada à Nina.
        
        Args:
            message: Objeto de mensagem do Discord
            
        Returns:
            True se a mensagem for para a Nina, False caso contrário
        """
        try:
            # Verificar se o bot foi mencionado
            if self.bot.user in message.mentions:
                return True
            
            # Verificar se a mensagem começa com "Nina,"
            if message.content.lower().startswith("nina,"):
                return True
            
            return False
        except Exception as e:
            logger.error(f"Erro ao verificar se mensagem é para Nina: {e}")
            return False
    
    def _extract_message_content(self, message) -> str:
        """
        Extrai o conteúdo relevante de uma mensagem.
        
        Args:
            message: Objeto de mensagem do Discord
            
        Returns:
            Conteúdo da mensagem
        """
        try:
            content = message.content
            
            # Remover menção ao bot
            if self.bot.user in message.mentions:
                content = content.replace(f"<@{self.bot.user.id}>", "").strip()
                content = content.replace(f"<@!{self.bot.user.id}>", "").strip()
            
            # Remover prefixo "Nina,"
            if content.lower().startswith("nina,"):
                content = content[5:].strip()
            
            return content
        except Exception as e:
            logger.error(f"Erro ao extrair conteúdo da mensagem: {e}")
            return message.content
```

### Modificações no Processador LLM

```python
# Modificação na classe LLMProcessor

def set_personality_system(self, personality_system) -> None:
    """
    Define o sistema de personalidade.
    
    Args:
        personality_system: Instância do sistema de personalidade
    """
    self.personality_system = personality_system
    logger.info("Sistema de personalidade definido")

def process_message(self, session_id: str, message: str, context: Dict[str, Any] = None) -> str:
    """
    Processa uma mensagem usando o modelo de linguagem.
    
    Args:
        session_id: ID da sessão
        message: Mensagem do usuário
        context: Contexto adicional (opcional)
        
    Returns:
        Resposta do modelo
    """
    try:
        # Extrair IDs do contexto
        guild_id = None
        channel_id = None
        
        if context:
            guild_id = context.get("guild_id")
            channel_id = context.get("channel_id")
        
        # Obter histórico de mensagens
        message_history = self.session_manager.get_message_history(session_id)
        
        # Obter prompt de sistema
        system_prompt = self._get_system_prompt(session_id, guild_id, channel_id)
        
        # Preparar mensagens para o modelo
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Adicionar histórico de mensagens
        for msg in message_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Adicionar mensagem atual
        messages.append({"role": "user", "content": message})
        
        # Gerar resposta
        response = self.ollama_client.generate(
            model=self.model_name,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        
        # Extrair texto da resposta
        response_text = response["message"]["content"]
        
        # Adicionar mensagem do usuário ao histórico
        self.session_manager.add_message_to_history(session_id, "user", message)
        
        # Adicionar resposta ao histórico
        self.session_manager.add_message_to_history(session_id, "assistant", response_text)
        
        # Aplicar personalidade à resposta se o sistema de personalidade estiver disponível
        if hasattr(self, 'personality_system') and guild_id and channel_id:
            response_text = self.personality_system.apply_personality_to_message(
                response_text, guild_id, channel_id
            )
        
        return response_text
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}")
        return "Desculpe, ocorreu um erro ao processar sua mensagem."

def _get_system_prompt(self, session_id: str, guild_id: str = None, channel_id: str = None) -> str:
    """
    Obtém o prompt de sistema.
    
    Args:
        session_id: ID da sessão
        guild_id: ID do servidor (opcional)
        channel_id: ID do canal (opcional)
        
    Returns:
        String com prompt de sistema
    """
    try:
        # Verificar se o sistema de personalidade está disponível
        if hasattr(self, 'personality_system') and guild_id and channel_id:
            return self.personality_system.get_system_prompt(guild_id, channel_id)
        else:
            # Usar prompt padrão
            return (
                "Você é Nina, uma assistente de IA amigável e prestativa. "
                "Responda de forma clara, concisa e útil às perguntas do usuário."
            )
    except Exception as e:
        logger.error(f"Erro ao obter prompt de sistema: {e}")
        return "Você é Nina, uma assistente de IA amigável e prestativa."
```

### Modificações no Orquestrador Principal

```python
# Modificação na classe Orchestrator

def set_channel_adapter(self, channel_adapter) -> None:
    """
    Define o adaptador de canal.
    
    Args:
        channel_adapter: Instância do adaptador de canal
    """
    self.channel_adapter = channel_adapter
    logger.info("Adaptador de canal definido")

def process_message(self, session_id: str, message: str, context: Dict[str, Any] = None) -> str:
    """
    Processa uma mensagem de usuário.
    
    Args:
        session_id: ID da sessão
        message: Mensagem do usuário
        context: Contexto adicional (opcional)
        
    Returns:
        Resposta processada
    """
    try:
        # Verificar se a sessão existe
        if not self.session_manager.get_session(session_id):
            # Criar nova sessão
            self.session_manager.create_session(session_id, context)
        
        # Extrair IDs do contexto
        guild_id = None
        channel_id = None
        
        if context:
            guild_id = context.get("guild_id")
            channel_id = context.get("channel_id")
        
        # Processar mensagem com o processador LLM
        response = self.llm_processor.process_message(session_id, message, context)
        
        # Adaptar resposta se o adaptador de canal estiver disponível
        if hasattr(self, 'channel_adapter') and guild_id and channel_id:
            response = self.channel_adapter.adapt_response(response, guild_id, channel_id)
        
        # Sintetizar fala se necessário
        if self.tts_enabled:
            audio_file = self.tts_module.synthesize_speech(response)
            
            # Reproduzir áudio
            if audio_file:
                self.audio_playback.play_audio(audio_file)
        
        return response
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}")
        return "Desculpe, ocorreu um erro ao processar sua mensagem."

def get_system_prompt(self, session_id: str, context: Dict[str, Any] = None) -> str:
    """
    Obtém o prompt de sistema para uma sessão.
    
    Args:
        session_id: ID da sessão
        context: Contexto adicional (opcional)
        
    Returns:
        String com prompt de sistema
    """
    try:
        # Extrair IDs do contexto
        guild_id = None
        channel_id = None
        
        if context:
            guild_id = context.get("guild_id")
            channel_id = context.get("channel_id")
        
        # Obter prompt de sistema do adaptador de canal se disponível
        if hasattr(self, 'channel_adapter') and guild_id and channel_id:
            return self.channel_adapter.get_system_prompt(guild_id, channel_id)
        
        # Caso contrário, usar o método do processador LLM
        return self.llm_processor._get_system_prompt(session_id, guild_id, channel_id)
    except Exception as e:
        logger.error(f"Erro ao obter prompt de sistema: {e}")
        return "Você é Nina, uma assistente de IA amigável e prestativa."
```

## Inicialização do Sistema Integrado

```python
import os
import json
import logging
from typing import Dict, List, Any, Optional, Union

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("nina_system.log")
    ]
)
logger = logging.getLogger("NinaSystem")

def initialize_nina_system():
    """
    Inicializa o sistema Nina IA completo com suporte a personalidade por canal.
    
    Returns:
        Tupla com instâncias dos sistemas (nina_system, personality_system, nina_integration, discord_bridge)
    """
    try:
        # Importar classes
        from nina_ia.core.orchestrator import Orchestrator
        from nina_ia.core.session_manager import SessionManager
        from nina_ia.llm.llm_processor import LLMProcessor
        from nina_ia.llm.ollama_client import OllamaClient
        from nina_ia.stt.stt_module import STTModule
        from nina_ia.tts.tts_module import TTSModule
        from nina_ia.core.audio_playback import AudioPlayback
        
        from personality_system import PersonalitySystem
        from nina_integration import NinaIntegration
        from enhanced_session_manager import EnhancedSessionManager
        from orchestration_adapter import OrchestrationAdapter
        from discord_bridge import DiscordBridge
        
        # Inicializar componentes do Nina IA
        ollama_client = OllamaClient(host="localhost", port=11434)
        llm_processor = LLMProcessor(
            ollama_client=ollama_client,
            model_name="mistral"
        )
        session_manager = SessionManager()
        stt_module = STTModule()
        tts_module = TTSModule()
        audio_playback = AudioPlayback()
        
        # Inicializar orquestrador
        orchestrator = Orchestrator(
            llm_processor=llm_processor,
            session_manager=session_manager,
            stt_module=stt_module,
            tts_module=tts_module,
            audio_playback=audio_playback
        )
        
        # Inicializar sistema Nina IA
        nina_system = {
            "orchestrator": orchestrator,
            "llm_processor": llm_processor,
            "session_manager": session_manager,
            "stt_module": stt_module,
            "tts_module": tts_module,
            "audio_playback": audio_playback
        }
        
        # Inicializar sistema de personalidade
        personality_system = PersonalitySystem()
        
        # Inicializar módulo de integração
        nina_integration = NinaIntegration(
            nina_system=nina_system,
            personality_system=personality_system
        )
        
        # Inicializar integração
        nina_integration.initialize()
        
        # Inicializar ponte de comunicação Discord
        discord_bridge = DiscordBridge(
            nina_integration=nina_integration
        )
        
        logger.info("Sistema Nina IA inicializado com sucesso")
        
        return (nina_system, personality_system, nina_integration, discord_bridge)
    except Exception as e:
        logger.error(f"Erro ao inicializar sistema Nina IA: {e}")
        raise

def start_discord_bot(discord_bridge, token: str):
    """
    Inicia o bot do Discord.
    
    Args:
        discord_bridge: Instância da ponte de comunicação Discord
        token: Token de autenticação do bot
    """
    try:
        # Inicializar bot
        discord_bridge.initialize_bot(token)
    except Exception as e:
        logger.error(f"Erro ao iniciar bot do Discord: {e}")
        raise

# Exemplo de uso
if __name__ == "__main__":
    try:
        # Inicializar sistema
        nina_system, personality_system, nina_integration, discord_bridge = initialize_nina_system()
        
        # Carregar token do Discord
        with open("config/discord_token.json", "r") as f:
            config = json.load(f)
            token = config["token"]
        
        # Iniciar bot do Discord
        start_discord_bot(discord_bridge, token)
    except Exception as e:
        logger.error(f"Erro ao iniciar sistema: {e}")
```

## Configuração do Sistema

### Arquivo de Configuração Principal

```json
{
  "nina_system": {
    "llm": {
      "model_name": "mistral",
      "temperature": 0.7,
      "max_tokens": 1024,
      "ollama_host": "localhost",
      "ollama_port": 11434
    },
    "stt": {
      "model_type": "faster-whisper",
      "model_size": "medium",
      "use_gpu": true
    },
    "tts": {
      "model_name": "tts_models/pt/cv/vits",
      "use_gpu": true
    },
    "audio": {
      "sample_rate": 22050,
      "audio_device": "default"
    }
  },
  "personality_system": {
    "persona_file": "./data/persona/persona.json",
    "channel_profiles_dir": "./data/profiles/channels",
    "plugins_dir": "./plugins",
    "plugins_config": "./config/plugins.json",
    "evolution": {
      "max_change_per_session": 5,
      "min_interactions_for_change": 10,
      "restricted_traits": ["tone"],
      "locked_traits": []
    }
  },
  "discord": {
    "token_file": "./config/discord_token.json",
    "command_prefix": "!",
    "status_message": "Aprendendo com as conversas"
  }
}
```

### Arquivo de Token do Discord

```json
{
  "token": "SEU_TOKEN_DO_DISCORD_AQUI",
  "client_id": "SEU_CLIENT_ID_AQUI",
  "permissions": 3072
}
```

## Exemplo de Uso

```python
import os
import json
import logging
import asyncio
from typing import Dict, List, Any, Optional, Union

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("nina_example.log")
    ]
)
logger = logging.getLogger("NinaExample")

async def main():
    try:
        # Importar função de inicialização
        from nina_system import initialize_nina_system, start_discord_bot
        
        # Inicializar sistema
        nina_system, personality_system, nina_integration, discord_bridge = initialize_nina_system()
        
        # Carregar token do Discord
        with open("config/discord_token.json", "r") as f:
            config = json.load(f)
            token = config["token"]
        
        # Iniciar bot do Discord
        await start_discord_bot(discord_bridge, token)
    except Exception as e:
        logger.error(f"Erro ao executar exemplo: {e}")

# Executar exemplo
if __name__ == "__main__":
    asyncio.run(main())
```

## Testes de Integração

```python
import os
import json
import unittest
from unittest.mock import MagicMock, patch
from typing import Dict, List, Any, Optional, Union

class TestNinaIntegration(unittest.TestCase):
    """
    Testes de integração para o sistema Nina IA com personalidade por canal.
    """
    
    def setUp(self):
        """
        Configura o ambiente de teste.
        """
        # Criar mocks
        self.mock_nina_system = {
            "orchestrator": MagicMock(),
            "llm_processor": MagicMock(),
            "session_manager": MagicMock(),
            "stt_module": MagicMock(),
            "tts_module": MagicMock(),
            "audio_playback": MagicMock()
        }
        
        self.mock_personality_system = MagicMock()
        self.mock_personality_system.channel_adapter = MagicMock()
        self.mock_personality_system.context_selector = MagicMock()
        
        # Importar classes
        from nina_integration import NinaIntegration
        
        # Inicializar módulo de integração
        self.nina_integration = NinaIntegration(
            nina_system=self.mock_nina_system,
            personality_system=self.mock_personality_system
        )
        
        # Inicializar integração
        self.nina_integration.initialize()
    
    def test_process_message(self):
        """
        Testa o processamento de mensagem.
        """
        # Configurar mocks
        self.mock_nina_system["orchestrator"].process_message.return_value = "Resposta de teste"
        
        # Processar mensagem
        message = {
            "guild_id": "123456789",
            "channel_id": "987654321",
            "user_id": "111111111",
            "content": "Olá, Nina!"
        }
        
        result = self.nina_integration.process_message(message)
        
        # Verificar resultado
        self.assertTrue(result["success"])
        self.assertEqual(result["response"], "Resposta de teste")
        self.assertEqual(result["session_id"], "123456789_987654321_111111111")
        
        # Verificar chamadas
        self.mock_nina_system["orchestrator"].process_message.assert_called_once()
    
    def test_update_channel_info(self):
        """
        Testa a atualização de informações de canal.
        """
        # Configurar mocks
        self.mock_personality_system.channel_adapter.process_channel_info.return_value = None
        
        # Atualizar informações do canal
        guild_id = "123456789"
        channel_id = "987654321"
        channel_info = {
            "name": "test-channel",
            "description": "Canal de teste",
            "category": "Testes",
            "is_nsfw": False
        }
        
        result = self.nina_integration.update_channel_info(guild_id, channel_id, channel_info)
        
        # Verificar resultado
        self.assertTrue(result)
        
        # Verificar chamadas
        self.mock_personality_system.channel_adapter.process_channel_info.assert_called_once_with(
            guild_id, channel_id, channel_info
        )
    
    def test_process_insights(self):
        """
        Testa o processamento de insights.
        """
        # Configurar mocks
        self.mock_personality_system.process_channel_insights.return_value = None
        
        # Processar insights
        guild_id = "123456789"
        channel_id = "987654321"
        insights = {
            "speaker_insights": {
                "user1": {
                    "personality_traits": {
                        "formality": 0.5,
                        "humor": 0.3
                    }
                }
            }
        }
        
        result = self.nina_integration.process_insights(guild_id, channel_id, insights)
        
        # Verificar resultado
        self.assertTrue(result)
        
        # Verificar chamadas
        self.mock_personality_system.process_channel_insights.assert_called_once_with(
            guild_id, channel_id, insights
        )

class TestOrchestrationAdapter(unittest.TestCase):
    """
    Testes para o adaptador de orquestração.
    """
    
    def setUp(self):
        """
        Configura o ambiente de teste.
        """
        # Criar mocks
        self.mock_orchestrator = MagicMock()
        self.mock_channel_adapter = MagicMock()
        
        # Importar classes
        from orchestration_adapter import OrchestrationAdapter
        
        # Inicializar adaptador
        self.orchestration_adapter = OrchestrationAdapter(
            orchestrator=self.mock_orchestrator,
            channel_adapter=self.mock_channel_adapter
        )
    
    def test_process_message(self):
        """
        Testa o processamento de mensagem.
        """
        # Configurar mocks
        self.mock_orchestrator.process_message.return_value = "Resposta original"
        self.mock_channel_adapter.adapt_response.return_value = "Resposta adaptada"
        
        # Processar mensagem
        session_id = "123456789_987654321_111111111"
        message = "Olá, Nina!"
        context = {
            "guild_id": "123456789",
            "channel_id": "987654321"
        }
        
        result = self.orchestration_adapter.process_message(session_id, message, context)
        
        # Verificar resultado
        self.assertEqual(result, "Resposta adaptada")
        
        # Verificar chamadas
        self.mock_orchestrator.process_message.assert_called_once_with(session_id, message, context)
        self.mock_channel_adapter.adapt_response.assert_called_once_with(
            "Resposta original", "123456789", "987654321"
        )
    
    def test_get_system_prompt(self):
        """
        Testa a obtenção do prompt de sistema.
        """
        # Configurar mocks
        self.mock_channel_adapter.get_system_prompt.return_value = "Prompt de sistema personalizado"
        
        # Obter prompt de sistema
        session_id = "123456789_987654321_111111111"
        context = {
            "guild_id": "123456789",
            "channel_id": "987654321"
        }
        
        result = self.orchestration_adapter.get_system_prompt(session_id, context)
        
        # Verificar resultado
        self.assertEqual(result, "Prompt de sistema personalizado")
        
        # Verificar chamadas
        self.mock_channel_adapter.get_system_prompt.assert_called_once_with(
            "123456789", "987654321"
        )

class TestEnhancedSessionManager(unittest.TestCase):
    """
    Testes para o gerenciador de sessão aprimorado.
    """
    
    def setUp(self):
        """
        Configura o ambiente de teste.
        """
        # Criar mocks
        self.mock_session_manager = MagicMock()
        self.mock_context_selector = MagicMock()
        
        # Importar classes
        from enhanced_session_manager import EnhancedSessionManager
        
        # Inicializar gerenciador
        self.enhanced_session_manager = EnhancedSessionManager(
            session_manager=self.mock_session_manager,
            context_selector=self.mock_context_selector
        )
    
    def test_create_session(self):
        """
        Testa a criação de sessão.
        """
        # Configurar mocks
        self.mock_session_manager.create_session.return_value = True
        
        # Criar sessão
        session_id = "123456789_987654321_111111111"
        context = {
            "guild_id": "123456789",
            "channel_id": "987654321"
        }
        
        result = self.enhanced_session_manager.create_session(session_id, context)
        
        # Verificar resultado
        self.assertTrue(result)
        
        # Verificar chamadas
        self.mock_session_manager.create_session.assert_called_once_with(session_id, context)
        
        # Verificar armazenamento de informações de canal
        self.assertIn(session_id, self.enhanced_session_manager.channel_sessions)
        self.assertEqual(
            self.enhanced_session_manager.channel_sessions[session_id]["guild_id"],
            "123456789"
        )
        self.assertEqual(
            self.enhanced_session_manager.channel_sessions[session_id]["channel_id"],
            "987654321"
        )
    
    def test_get_session_context(self):
        """
        Testa a obtenção do contexto de sessão.
        """
        # Configurar mocks
        self.mock_session_manager.get_session_context.return_value = {
            "user_id": "111111111"
        }
        self.mock_context_selector.select_context.return_value = {
            "name": "Nina",
            "personality": {
                "tone": "neutro",
                "formality_level": 50
            }
        }
        
        # Configurar sessão
        session_id = "123456789_987654321_111111111"
        self.enhanced_session_manager.channel_sessions[session_id] = {
            "guild_id": "123456789",
            "channel_id": "987654321",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
        
        # Obter contexto
        result = self.enhanced_session_manager.get_session_context(session_id)
        
        # Verificar resultado
        self.assertEqual(result["user_id"], "111111111")
        self.assertEqual(result["guild_id"], "123456789")
        self.assertEqual(result["channel_id"], "987654321")
        self.assertEqual(result["personality"]["name"], "Nina")
        self.assertEqual(result["personality"]["personality"]["tone"], "neutro")
        
        # Verificar chamadas
        self.mock_session_manager.get_session_context.assert_called_once_with(session_id)
        self.mock_context_selector.select_context.assert_called_once_with(
            "123456789", "987654321"
        )

if __name__ == "__main__":
    unittest.main()
```

## Conclusão

A integração do sistema de personalidade por canal com o sistema Nina IA existente permite que a IA adapte seu comportamento de forma diferente em diferentes canais do Discord, mantendo a compatibilidade com todos os componentes existentes. Os principais componentes implementados são:

1. **Módulo de Integração**: Conecta o sistema de personalidade por canal com o sistema Nina IA
2. **Adaptador de Orquestração**: Modifica o orquestrador principal para suportar contextos de canal
3. **Gerenciador de Sessão Aprimorado**: Estende o gerenciador de sessão para incluir informações de canal
4. **Ponte de Comunicação Discord**: Conecta o cliente Discord com o sistema Nina IA

Esses componentes trabalham em conjunto para permitir que a Nina IA desenvolva "personas" distintas com base nas interações específicas de cada canal, tornando suas respostas mais naturais e apropriadas para diferentes contextos de comunicação, enquanto mantém a funcionalidade completa do sistema original.

A arquitetura modular e as interfaces bem definidas garantem que o sistema possa ser facilmente estendido no futuro, adicionando suporte para novos canais de comunicação ou aprimorando os algoritmos de aprendizado de personalidade.
