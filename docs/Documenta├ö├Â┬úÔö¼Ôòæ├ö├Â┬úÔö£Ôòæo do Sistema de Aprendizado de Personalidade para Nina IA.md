# Documentação do Sistema de Aprendizado de Personalidade para Nina IA

## Visão Geral

O Sistema de Aprendizado de Personalidade é uma extensão para a Nina IA que permite que a assistente adapte seu comportamento com base nas conversas do Discord. O sistema coleta dados de interações, analisa padrões de comunicação, e evolui a personalidade da IA para se adequar melhor ao contexto de cada canal ou grupo de usuários.

Esta documentação descreve a arquitetura, componentes, fluxos de dados e instruções de uso do sistema, fornecendo uma referência completa para desenvolvedores e usuários.

## Arquitetura do Sistema

O sistema é composto por seis módulos principais que trabalham em conjunto para proporcionar uma experiência de IA adaptativa:

1. **Sistema de Coleta de Dados do Discord**: Captura mensagens de texto e áudio dos canais do Discord.
2. **Sistema de Diarização de Falantes**: Identifica e separa diferentes falantes em conversas de áudio.
3. **Sistema de Análise de Padrões de Conversas**: Analisa o conteúdo das conversas para extrair insights.
4. **Sistema de Personalidade Dinâmica**: Gerencia e evolui a personalidade da IA com base nos insights.
5. **Sistema de Controle e Segurança**: Garante que as mudanças de personalidade sejam seguras e apropriadas.
6. **Sistema de Personalidade por Canal**: Mantém perfis de personalidade distintos para diferentes canais.

### Diagrama de Arquitetura

```
+---------------------+    +----------------------+    +----------------------+
| Coleta de Dados do  |    | Diarização de        |    | Análise de Padrões   |
| Discord             |--->| Falantes             |--->| de Conversas         |
+---------------------+    +----------------------+    +----------------------+
                                                              |
                                                              v
+---------------------+    +----------------------+    +----------------------+
| Personalidade por   |<---| Controle e           |<---| Personalidade        |
| Canal               |    | Segurança            |    | Dinâmica             |
+---------------------+    +----------------------+    +----------------------+
        |
        v
+---------------------+
| Sistema Nina IA     |
| (Existente)         |
+---------------------+
```

### Fluxo de Dados

1. O Sistema de Coleta de Dados captura mensagens de texto e áudio dos canais do Discord.
2. Para dados de áudio, o Sistema de Diarização de Falantes identifica e separa os diferentes falantes.
3. O Sistema de Análise de Padrões processa as mensagens para extrair insights sobre personalidade, tópicos e estilo de comunicação.
4. O Sistema de Personalidade Dinâmica recebe os insights e evolui a personalidade da IA.
5. O Sistema de Controle e Segurança valida as mudanças para garantir que sejam apropriadas.
6. O Sistema de Personalidade por Canal mantém perfis distintos para diferentes contextos.
7. O Sistema Nina IA utiliza os perfis de personalidade para adaptar suas respostas.

## Componentes do Sistema

### 1. Sistema de Coleta de Dados do Discord

#### Descrição

Este componente é responsável por capturar mensagens de texto e áudio dos canais do Discord, fornecendo os dados brutos para análise.

#### Módulos Principais

- **DiscordCollector**: Coleta mensagens de texto dos canais do Discord.
- **AudioCapture**: Captura áudio de canais de voz do Discord.
- **DataPreprocessor**: Prepara os dados para análise.

#### Exemplo de Uso

```python
from discord_collector import DiscordCollector

# Inicializar coletor
collector = DiscordCollector(bot_token="SEU_TOKEN_AQUI")

# Coletar mensagens de um canal
messages = collector.collect_messages(
    guild_id="123456789",
    channel_id="987654321",
    limit=100
)

# Processar mensagens
for message in messages:
    print(f"Usuário: {message['username']}")
    print(f"Conteúdo: {message['content']}")
    print(f"Timestamp: {message['timestamp']}")
    print("---")
```

### 2. Sistema de Diarização de Falantes

#### Descrição

Este componente identifica e separa diferentes falantes em conversas de áudio, permitindo a análise individualizada de cada participante.

#### Módulos Principais

- **SpeakerDiarizer**: Identifica diferentes falantes em um arquivo de áudio.
- **AudioProcessor**: Processa arquivos de áudio para melhorar a qualidade.
- **TranscriptionManager**: Gerencia a transcrição de áudio para texto.

#### Exemplo de Uso

```python
from speaker_diarizer import SpeakerDiarizer
from audio_processor import AudioProcessor

# Processar áudio
processor = AudioProcessor()
processed_audio = processor.process_audio(
    audio_data=audio_bytes,
    output_path="./processed_audio.wav"
)

# Diarizar falantes
diarizer = SpeakerDiarizer(model_path="./models/diarization")
segments = diarizer.diarize(audio_path=processed_audio["file_path"])

# Exibir segmentos
for segment in segments:
    print(f"Falante: {segment['speaker']}")
    print(f"Início: {segment['start']} segundos")
    print(f"Fim: {segment['end']} segundos")
    print("---")
```

### 3. Sistema de Análise de Padrões de Conversas

#### Descrição

Este componente analisa o conteúdo das conversas para extrair insights sobre personalidade, tópicos e estilo de comunicação dos participantes.

#### Módulos Principais

- **SentimentAnalyzer**: Analisa o sentimento das mensagens.
- **TopicExtractor**: Identifica os tópicos discutidos.
- **PersonalityExtractor**: Extrai traços de personalidade dos participantes.
- **ConversationAnalyzer**: Coordena a análise completa das conversas.

#### Exemplo de Uso

```python
from conversation_analyzer import ConversationAnalyzer

# Inicializar analisador
analyzer = ConversationAnalyzer()

# Analisar conversas
insights = analyzer.analyze(messages=messages)

# Exibir insights
print("Insights de Falantes:")
for user_id, user_insights in insights["speaker_insights"].items():
    print(f"Usuário: {user_id}")
    print(f"Traços de Personalidade: {user_insights['personality_traits']}")
    print(f"Estilo de Comunicação: {user_insights['communication_style']}")
    print(f"Tópicos de Interesse: {user_insights['topics_of_interest']}")
    print("---")

print("Insights do Canal:")
print(f"Clima do Canal: {insights['channel_insights']['channel_mood']}")
print(f"Tópicos do Canal: {insights['channel_insights']['channel_topics']}")
```

### 4. Sistema de Personalidade Dinâmica

#### Descrição

Este componente gerencia e evolui a personalidade da IA com base nos insights extraídos das conversas, permitindo que a IA se adapte ao contexto.

#### Módulos Principais

- **PersonalityManager**: Gerencia o arquivo de personalidade.
- **EvolutionController**: Controla a evolução da personalidade.
- **VocabularyManager**: Gerencia o vocabulário personalizado.
- **TopicManager**: Gerencia os tópicos de interesse.

#### Exemplo de Uso

```python
from personality_manager import PersonalityManager
from evolution_controller import EvolutionController

# Inicializar gerenciador de personalidade
personality_manager = PersonalityManager(
    persona_file_path="./data/persona/persona.json"
)

# Inicializar controlador de evolução
evolution_controller = EvolutionController(
    personality_manager=personality_manager
)

# Configurar controlador
evolution_controller.set_evolution_settings(
    max_change_per_session=5,
    min_interactions_for_change=10,
    restricted_traits=["tone"],
    locked_traits=[]
)

# Registrar interações
evolution_controller.register_interaction()

# Evoluir personalidade
changes = evolution_controller.evolve_personality(insights)

# Exibir mudanças
print("Mudanças na Personalidade:")
for trait, change in changes.items():
    print(f"{trait}: {change['old_value']} -> {change['new_value']}")
```

### 5. Sistema de Controle e Segurança

#### Descrição

Este componente garante que as mudanças de personalidade sejam seguras e apropriadas, evitando comportamentos indesejados.

#### Módulos Principais

- **SafetySystem**: Valida mudanças de personalidade e mensagens.
- **ContentFilter**: Filtra conteúdo inadequado.
- **ChangeValidator**: Valida mudanças de personalidade.
- **AuditLogger**: Registra mudanças para auditoria.

#### Exemplo de Uso

```python
from safety_system import SafetySystem

# Inicializar sistema de segurança
safety_system = SafetySystem()

# Validar mensagem
message = "Olá, como posso ajudar você hoje?"
validated_message, is_safe = safety_system.validate_message(message)

if is_safe:
    print(f"Mensagem segura: {validated_message}")
else:
    print("Mensagem bloqueada por segurança")

# Validar atualização de personalidade
personality_update = {
    "formality_level": 60,
    "humor_level": 40
}

validated_update, is_safe = safety_system.validate_personality_update(personality_update)

if is_safe:
    print(f"Atualização segura: {validated_update}")
else:
    print("Atualização bloqueada por segurança")
```

### 6. Sistema de Personalidade por Canal

#### Descrição

Este componente mantém perfis de personalidade distintos para diferentes canais, permitindo que a IA se adapte a diferentes contextos.

#### Módulos Principais

- **ChannelProfileManager**: Gerencia perfis de canal.
- **ContextSelector**: Seleciona o contexto apropriado para cada canal.
- **ChannelAdapter**: Adapta respostas com base no perfil do canal.
- **ProfileSynchronizer**: Sincroniza perfis entre canais relacionados.

#### Exemplo de Uso

```python
from channel_profile_manager import ChannelProfileManager
from context_selector import ContextSelector
from channel_adapter import ChannelAdapter

# Inicializar gerenciador de perfis
profile_manager = ChannelProfileManager(
    profiles_dir="./data/profiles/channels"
)

# Inicializar seletor de contexto
context_selector = ContextSelector(
    channel_profile_manager=profile_manager
)

# Inicializar adaptador de canal
channel_adapter = ChannelAdapter(
    context_selector=context_selector
)

# Carregar perfil de canal
guild_id = "123456789"
channel_id = "987654321"

profile = profile_manager.load_profile(guild_id, channel_id)

# Selecionar contexto
context = context_selector.select_context(guild_id, channel_id)

# Adaptar resposta
response = "Esta é uma resposta original."
adapted_response = channel_adapter.adapt_response(response, guild_id, channel_id)

print(f"Resposta adaptada: {adapted_response}")
```

## Integração com o Sistema Nina IA

### Descrição

A integração com o sistema Nina IA existente permite que a IA adapte seu comportamento com base nos perfis de personalidade por canal.

### Componentes de Integração

- **NinaIntegration**: Conecta o sistema de personalidade com o sistema Nina IA.
- **OrchestrationAdapter**: Adapta o orquestrador principal para suportar contextos de canal.
- **EnhancedSessionManager**: Estende o gerenciador de sessão para incluir informações de canal.
- **DiscordBridge**: Conecta o cliente Discord com o sistema Nina IA.

### Exemplo de Uso

```python
from nina_integration import NinaIntegration
from discord_bridge import DiscordBridge

# Inicializar sistema Nina IA e sistema de personalidade
nina_system = initialize_nina_system()
personality_system = initialize_personality_system()

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

# Carregar token do Discord
with open("config/discord_token.json", "r") as f:
    config = json.load(f)
    token = config["token"]

# Iniciar bot do Discord
discord_bridge.initialize_bot(token)
```

## Configuração do Sistema

### Arquivo de Configuração Principal

O arquivo `config.json` contém as configurações principais do sistema:

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

O arquivo `discord_token.json` contém o token de autenticação do bot do Discord:

```json
{
  "token": "SEU_TOKEN_DO_DISCORD_AQUI",
  "client_id": "SEU_CLIENT_ID_AQUI",
  "permissions": 3072
}
```

### Arquivo de Personalidade

O arquivo `persona.json` contém a personalidade global da IA:

```json
{
  "global": {
    "name": "Nina",
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
      "avoided_topics": []
    },
    "interaction_history": {
      "total_interactions": 0,
      "last_updated": "2023-01-01T00:00:00"
    }
  }
}
```

### Perfil de Canal

Os perfis de canal são armazenados em arquivos JSON no diretório `data/profiles/channels`:

```json
{
  "guild_id": "123456789",
  "channel_id": "987654321",
  "name": "test-channel",
  "description": "Canal de teste",
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
    "avoided_topics": []
  },
  "interaction_history": {
    "total_interactions": 0,
    "last_updated": "2023-01-01T00:00:00"
  }
}
```

## Instalação e Uso

### Requisitos

- Python 3.8 ou superior
- NVIDIA GPU com CUDA (recomendado para melhor desempenho)
- Biblioteca Discord.py
- Biblioteca PyAnnote Audio
- Biblioteca Faster-Whisper
- Biblioteca Ollama
- Biblioteca Coqui TTS

### Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/nina-ia.git
cd nina-ia
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure o token do Discord:

```bash
cp config/discord_token.example.json config/discord_token.json
# Edite o arquivo config/discord_token.json com seu token
```

4. Inicialize o sistema:

```bash
python main.py
```

### Uso

#### Comandos do Discord

- `!nina_help`: Mostra informações de ajuda sobre a Nina IA.
- `!nina_status`: Verifica o status da Nina IA.
- `!nina_reset`: Reseta a personalidade do canal atual.
- `!nina_personality`: Mostra a personalidade atual do canal.

#### Interação com a IA

Para interagir com a Nina IA, mencione o bot ou use o prefixo "Nina, ":

```
@Nina Como está o tempo hoje?
```

ou

```
Nina, como está o tempo hoje?
```

## Extensão do Sistema

### Adição de Novos Plugins

Para adicionar um novo plugin ao sistema, crie um arquivo Python no diretório `plugins` com a seguinte estrutura:

```python
class MyPlugin:
    def __init__(self):
        self.name = "my_plugin"
        self.description = "Meu plugin personalizado"
        self.personality_context = None
    
    def set_personality_context(self, context):
        self.personality_context = context
    
    def process_text(self, text):
        # Processar texto com base na personalidade
        if self.personality_context and "personality" in self.personality_context:
            formality = self.personality_context["personality"].get("formality_level", 50)
            
            if formality > 70:
                # Tornar o texto mais formal
                return text.replace("oi", "olá").replace("valeu", "obrigado")
            elif formality < 30:
                # Tornar o texto mais informal
                return text.replace("olá", "oi").replace("obrigado", "valeu")
        
        return text
```

Em seguida, adicione o plugin ao arquivo de configuração `config/plugins.json`:

```json
{
  "enabled_plugins": ["my_plugin"],
  "plugin_configs": {
    "my_plugin": {
      "option1": "value1",
      "option2": "value2"
    }
  }
}
```

### Personalização da Evolução de Personalidade

Para personalizar a evolução de personalidade, edite as configurações no arquivo `config.json`:

```json
"evolution": {
  "max_change_per_session": 5,
  "min_interactions_for_change": 10,
  "restricted_traits": ["tone"],
  "locked_traits": []
}
```

- `max_change_per_session`: Número máximo de mudanças por sessão.
- `min_interactions_for_change`: Número mínimo de interações necessárias para permitir mudanças.
- `restricted_traits`: Traços que só podem mudar lentamente.
- `locked_traits`: Traços que não podem ser alterados.

## Solução de Problemas

### Problemas Comuns

#### O bot não responde às mensagens

- Verifique se o token do Discord está correto.
- Verifique se o bot tem as permissões necessárias no servidor.
- Verifique os logs para erros específicos.

#### A personalidade não evolui

- Verifique se o número mínimo de interações foi atingido.
- Verifique se os traços estão bloqueados ou restritos.
- Verifique se o arquivo de personalidade tem permissões de escrita.

#### Erros de diarização de falantes

- Verifique se a biblioteca PyAnnote Audio está instalada corretamente.
- Verifique se o modelo de diarização está disponível.
- Verifique a qualidade do áudio capturado.

### Logs

Os logs do sistema são armazenados nos seguintes arquivos:

- `nina_system.log`: Logs gerais do sistema.
- `nina_integration.log`: Logs da integração.
- `discord_bridge.log`: Logs da ponte de comunicação Discord.
- `personality_system.log`: Logs do sistema de personalidade.

## Referências

### Bibliotecas Utilizadas

- [Discord.py](https://discordpy.readthedocs.io/): Biblioteca para interação com o Discord.
- [PyAnnote Audio](https://github.com/pyannote/pyannote-audio): Biblioteca para diarização de falantes.
- [Faster-Whisper](https://github.com/guillaumekln/faster-whisper): Biblioteca para reconhecimento de fala.
- [Ollama](https://github.com/ollama/ollama): Biblioteca para modelos de linguagem.
- [Coqui TTS](https://github.com/coqui-ai/TTS): Biblioteca para síntese de fala.

### Documentação Adicional

- [Documentação do Discord API](https://discord.com/developers/docs/intro)
- [Documentação do PyAnnote Audio](https://github.com/pyannote/pyannote-audio/tree/develop/docs)
- [Documentação do Faster-Whisper](https://github.com/guillaumekln/faster-whisper/blob/master/README.md)
- [Documentação do Ollama](https://github.com/ollama/ollama/blob/main/README.md)
- [Documentação do Coqui TTS](https://github.com/coqui-ai/TTS/tree/main/docs)

## Conclusão

O Sistema de Aprendizado de Personalidade para a Nina IA permite que a assistente adapte seu comportamento com base nas conversas do Discord, proporcionando uma experiência mais natural e personalizada para os usuários. O sistema é modular, extensível e seguro, garantindo que a IA evolua de forma controlada e apropriada.

Esta documentação fornece uma referência completa para desenvolvedores e usuários, facilitando a manutenção e extensão do sistema no futuro.
