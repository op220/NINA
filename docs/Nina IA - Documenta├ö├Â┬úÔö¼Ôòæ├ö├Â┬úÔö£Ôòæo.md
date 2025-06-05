# Nina IA - Documentação

## Visão Geral

Nina IA é um assistente de inteligência artificial local com capacidades de reconhecimento de voz, processamento de linguagem natural e síntese de fala. O sistema foi projetado para funcionar completamente offline em uma workstation, utilizando apenas ferramentas gratuitas e de código aberto.

## Arquitetura

O sistema Nina IA é composto por vários módulos independentes que trabalham juntos para fornecer uma experiência de assistente de voz completa:

1. **Módulo STT (Speech to Text)**: Responsável pela captura de áudio e transcrição de voz para texto.
2. **Módulo LLM (Language Model)**: Processa o texto transcrito e gera respostas utilizando modelos de linguagem.
3. **Módulo TTS (Text to Speech)**: Converte as respostas de texto em fala sintetizada.
4. **Sistema de Personalidade**: Gerencia perfis de personalidade para o assistente.
5. **Sistema de Memória**: Armazena histórico de conversas e informações do usuário.
6. **Orquestrador**: Coordena todos os módulos e gerencia o fluxo de interação.
7. **Sistema de Playback**: Gerencia a reprodução de áudio sintetizado.

## Requisitos do Sistema

### Hardware
- CPU: Intel Core i5 ou superior
- RAM: 8GB ou mais
- GPU: NVIDIA Quadro P4000 ou equivalente com 8GB VRAM
- Microfone e alto-falantes

### Software
- Sistema Operacional: Linux, Windows ou macOS
- Python 3.8 ou superior
- Bibliotecas Python (instaladas automaticamente via requirements.txt)
- Ollama (para modelos de linguagem)
- Drivers CUDA (para aceleração GPU)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/nina-ia.git
cd nina-ia
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Instale o Ollama seguindo as instruções em [ollama.ai](https://ollama.ai).

4. Baixe os modelos necessários:
```bash
# Baixar modelo Mistral para Ollama
ollama pull mistral

# Os modelos de STT e TTS serão baixados automaticamente na primeira execução
```

## Estrutura do Projeto

```
nina_ia/
├── core/                   # Componentes principais
│   ├── audio_playback.py   # Sistema de playback de áudio
│   ├── memory_manager.py   # Gerenciador de memória e contexto
│   ├── orchestrator.py     # Orquestrador principal
│   ├── personality_manager.py  # Gerenciador de personalidade
│   ├── profiles_manager.py # Gerenciador de perfis
│   └── session_manager.py  # Gerenciador de sessões
├── data/                   # Dados e configurações
│   ├── audio/              # Arquivos de áudio gerados
│   ├── memory/             # Banco de dados de memória
│   └── profiles/           # Perfis de personalidade
├── interface/              # Interface do usuário
│   └── nina_ia.py          # Ponto de entrada principal
├── llm/                    # Módulo de processamento de linguagem
│   ├── llm_module.py       # Módulo principal LLM
│   ├── llm_processor.py    # Processador de texto
│   └── ollama_client.py    # Cliente para Ollama
├── stt/                    # Módulo de reconhecimento de voz
│   ├── audio_capture.py    # Captura de áudio
│   ├── stt_module.py       # Módulo principal STT
│   └── transcriber.py      # Transcritor de áudio
├── tests/                  # Testes unitários e de integração
│   ├── test_components.py  # Testes de componentes individuais
│   └── test_nina_ia.py     # Testes do sistema integrado
├── tts/                    # Módulo de síntese de voz
│   ├── audio_player.py     # Reprodutor de áudio
│   ├── tts_module.py       # Módulo principal TTS
│   └── tts_synthesizer.py  # Sintetizador de voz
├── README.md               # Documentação principal
└── requirements.txt        # Dependências do projeto
```

## Uso

### Linha de Comando

O sistema Nina IA pode ser iniciado através da linha de comando:

```bash
python -m nina_ia.interface.nina_ia
```

Opções disponíveis:
- `--profile NOME`: Especifica o perfil a ser carregado (padrão: default_profile)
- `--data-dir CAMINHO`: Especifica o diretório para armazenar dados
- `--no-cuda`: Desativa o uso de GPU
- `--debug`: Ativa o modo de depuração
- `--continuous`: Inicia em modo contínuo de escuta
- `--text "TEXTO"`: Processa um comando de texto específico

### Modo Interativo

Ao iniciar o sistema sem argumentos, ele entrará no modo interativo:

```
Nina IA iniciada. Digite 'sair' para encerrar.

Digite um comando: Olá, como você está?
Resposta: Olá! Estou bem, obrigada por perguntar. Como posso ajudar você hoje?

Digite um comando: voz
Aguardando comando de voz...
```

### Modo Contínuo

O modo contínuo permite que o sistema fique constantemente escutando por comandos de voz:

```bash
python -m nina_ia.interface.nina_ia --continuous
```

## Módulos Detalhados

### Módulo STT (Speech to Text)

O módulo STT utiliza a biblioteca faster-whisper para transcrição de voz para texto. Ele é composto por:

- **audio_capture.py**: Responsável pela captura de áudio do microfone.
- **transcriber.py**: Gerencia a transcrição do áudio utilizando o modelo Whisper.
- **stt_module.py**: Integra captura e transcrição em uma interface unificada.

Exemplo de uso:
```python
from nina_ia.stt.stt_module import STTModule

# Inicializar módulo STT
stt = STTModule(model_size="base", device="cuda")

# Capturar e transcrever áudio
text, info = stt.listen_and_transcribe()
print(f"Texto transcrito: {text}")
```

### Módulo LLM (Language Model)

O módulo LLM utiliza o Ollama para processar texto e gerar respostas. Ele é composto por:

- **ollama_client.py**: Cliente para comunicação com o Ollama.
- **llm_processor.py**: Processa o texto e gerencia o contexto da conversa.
- **llm_module.py**: Fornece uma interface unificada para processamento de texto.

Exemplo de uso:
```python
from nina_ia.llm.llm_module import LLMModule

# Inicializar módulo LLM
llm = LLMModule(model="mistral")

# Processar texto
response = llm.process_text("Qual é a capital do Brasil?")
print(f"Resposta: {response}")
```

### Módulo TTS (Text to Speech)

O módulo TTS utiliza o Coqui TTS para converter texto em fala. Ele é composto por:

- **tts_synthesizer.py**: Gerencia a síntese de voz utilizando modelos TTS.
- **audio_player.py**: Reproduz o áudio sintetizado.
- **tts_module.py**: Integra síntese e reprodução em uma interface unificada.

Exemplo de uso:
```python
from nina_ia.tts.tts_module import TTSModule

# Inicializar módulo TTS
tts = TTSModule(model_name="tts_models/pt/cv/vits", use_cuda=True)

# Sintetizar e reproduzir texto
tts.speak("Olá, eu sou a Nina, sua assistente de inteligência artificial.")
```

### Sistema de Personalidade

O sistema de personalidade gerencia os perfis do assistente. Ele é composto por:

- **personality_manager.py**: Gerencia um único perfil de personalidade.
- **profiles_manager.py**: Gerencia múltiplos perfis.

Exemplo de uso:
```python
from nina_ia.core.profiles_manager import ProfilesManager

# Inicializar gerenciador de perfis
profiles = ProfilesManager()

# Listar perfis disponíveis
available_profiles = profiles.list_profiles()
print(f"Perfis disponíveis: {available_profiles}")

# Carregar um perfil
profiles.load_profile("formal")

# Obter prompt de sistema baseado na personalidade
system_prompt = profiles.build_system_prompt()
```

### Sistema de Memória

O sistema de memória armazena histórico de conversas e informações do usuário. Ele é composto por:

- **memory_manager.py**: Gerencia o armazenamento de dados em SQLite.
- **session_manager.py**: Gerencia sessões de conversa.

Exemplo de uso:
```python
from nina_ia.core.session_manager import SessionManager

# Inicializar gerenciador de sessões
sessions = SessionManager()

# Criar uma nova sessão
session_id = sessions.create_session("Conversa de teste")

# Adicionar mensagens
sessions.add_message(session_id, "user", "Olá, como você está?")
sessions.add_message(session_id, "assistant", "Estou bem, obrigada por perguntar!")

# Obter histórico de mensagens
messages = sessions.get_messages(session_id)
```

### Orquestrador

O orquestrador coordena todos os módulos e gerencia o fluxo de interação. Ele é implementado em:

- **orchestrator.py**: Integra STT, LLM, TTS, personalidade e memória.

Exemplo de uso:
```python
from nina_ia.core.orchestrator import NinaOrchestrator

# Inicializar orquestrador
orchestrator = NinaOrchestrator(use_cuda=True)

# Processar comando de texto
response = orchestrator.process_text_input("Qual é o seu nome?")

# Falar resposta
orchestrator.speak_response(response)
```

### Sistema de Playback

O sistema de playback gerencia a reprodução de áudio sintetizado. Ele é implementado em:

- **audio_playback.py**: Gerencia fila de reprodução e controles de áudio.

Exemplo de uso:
```python
from nina_ia.core.audio_playback import AudioPlaybackManager

# Inicializar gerenciador de playback
playback = AudioPlaybackManager()

# Reproduzir arquivo de áudio
playback.play("/caminho/para/audio.wav")

# Ajustar volume
playback.set_volume(0.8)
```

## Personalização

### Criação de Perfis

Você pode criar perfis personalizados para o assistente:

1. Crie um arquivo JSON na pasta `data/profiles/` com o seguinte formato:
```json
{
  "name": "MeuPerfil",
  "personality": {
    "speech_style": "amigável",
    "mood": "alegre",
    "preferences": ["música", "tecnologia"],
    "description": "Assistente de IA amigável e prestativa"
  },
  "voice": {
    "model": "tts_models/pt/cv/vits",
    "language": "pt"
  },
  "llm": {
    "model": "mistral",
    "temperature": 0.7
  },
  "stt": {
    "model": "base",
    "language": "pt"
  }
}
```

2. Carregue o perfil ao iniciar o sistema:
```bash
python -m nina_ia.interface.nina_ia --profile MeuPerfil
```

### Modelos Alternativos

O sistema suporta diferentes modelos para cada componente:

- **STT**: Modelos Whisper (tiny, base, small, medium, large)
- **LLM**: Qualquer modelo suportado pelo Ollama (mistral, phi, llama2, etc.)
- **TTS**: Modelos Coqui TTS (vários idiomas e vozes disponíveis)

## Testes

O projeto inclui testes unitários e de integração:

```bash
# Executar todos os testes
python -m unittest discover -s nina_ia/tests

# Executar testes específicos
python -m unittest nina_ia.tests.test_components
python -m unittest nina_ia.tests.test_nina_ia
```

## Solução de Problemas

### Problemas Comuns

1. **Erro ao inicializar STT**: Verifique se o CUDA está instalado corretamente para aceleração GPU.
2. **Erro ao inicializar LLM**: Verifique se o Ollama está instalado e o modelo foi baixado.
3. **Erro ao inicializar TTS**: Verifique se os modelos TTS foram baixados corretamente.
4. **Problemas de captura de áudio**: Verifique se o microfone está configurado corretamente.

### Logs

Os logs do sistema são armazenados em `nina_ia.log` e podem ser úteis para diagnóstico.

## Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

## Licença

Este projeto é licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

## Créditos

Nina IA utiliza os seguintes projetos de código aberto:

- [faster-whisper](https://github.com/guillaumekln/faster-whisper) - Transcrição de voz
- [Ollama](https://github.com/ollama/ollama) - Modelos de linguagem
- [Coqui TTS](https://github.com/coqui-ai/TTS) - Síntese de voz
- [PyAudio](https://github.com/jleb/pyaudio) - Captura de áudio
- [pygame](https://github.com/pygame/pygame) - Reprodução de áudio
