# Sistema de Coleta de Dados do Discord

## Arquitetura do Sistema

### Componentes Principais
1. **Cliente Discord**: Conecta-se aos canais de voz e captura o áudio
2. **Processador de Áudio**: Gerencia a gravação e o processamento do áudio capturado
3. **Sistema de Diarização**: Identifica diferentes falantes no áudio
4. **Transcritor**: Converte o áudio em texto usando Whisper
5. **Armazenamento**: Salva as transcrições organizadas por usuário, data e canal

### Fluxo de Dados
1. Bot se conecta ao canal de voz do Discord
2. Áudio é capturado e armazenado temporariamente
3. Áudio é processado para diarização (identificação de falantes)
4. Segmentos de áudio são transcritos com Whisper
5. Transcrições são organizadas e armazenadas localmente

## Implementação

### Cliente Discord
```python
import discord
from discord.ext import commands
import asyncio
from discord_ext_voice_recv import VoiceRecvClient

class NinaDiscordClient(commands.Bot):
    def __init__(self, command_prefix="!"):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.voice_clients = {}
        self.audio_processors = {}
        
    async def on_ready(self):
        print(f'Bot conectado como {self.user}')
        
    async def join_voice_channel(self, channel_id):
        """Conecta o bot a um canal de voz específico"""
        channel = self.get_channel(channel_id)
        if not channel or not isinstance(channel, discord.VoiceChannel):
            raise ValueError("Canal de voz inválido")
            
        # Conectar ao canal de voz
        voice_client = await channel.connect(cls=VoiceRecvClient)
        self.voice_clients[channel.id] = voice_client
        
        # Iniciar processador de áudio para este canal
        self.audio_processors[channel.id] = AudioProcessor(
            channel_id=channel.id,
            guild_id=channel.guild.id,
            channel_name=channel.name
        )
        
        # Configurar callback para receber áudio
        voice_client.listen(self._audio_receiver_callback)
        
        return voice_client
        
    async def leave_voice_channel(self, channel_id):
        """Desconecta o bot de um canal de voz"""
        if channel_id in self.voice_clients:
            await self.voice_clients[channel_id].disconnect()
            del self.voice_clients[channel_id]
            
        if channel_id in self.audio_processors:
            self.audio_processors[channel_id].cleanup()
            del self.audio_processors[channel_id]
    
    def _audio_receiver_callback(self, user, audio_data):
        """Callback chamado quando áudio é recebido de um usuário"""
        # Identificar o canal de voz
        for channel_id, voice_client in self.voice_clients.items():
            if user in voice_client.channel.members:
                # Processar o áudio recebido
                if channel_id in self.audio_processors:
                    self.audio_processors[channel_id].process_audio(user.id, user.name, audio_data)
                break
```

### Processador de Áudio
```python
import os
import wave
import time
import threading
from datetime import datetime
import numpy as np

class AudioProcessor:
    def __init__(self, channel_id, guild_id, channel_name, 
                 base_dir="./data/audio", 
                 sample_rate=48000, 
                 sample_width=2,
                 channels=2):
        self.channel_id = channel_id
        self.guild_id = guild_id
        self.channel_name = channel_name
        self.sample_rate = sample_rate
        self.sample_width = sample_width
        self.channels = channels
        
        # Criar diretórios para armazenamento
        self.session_dir = os.path.join(
            base_dir, 
            f"{guild_id}",
            f"{channel_id}",
            datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        )
        os.makedirs(self.session_dir, exist_ok=True)
        
        # Dicionário para armazenar buffers de áudio por usuário
        self.user_buffers = {}
        self.buffer_lock = threading.Lock()
        
        # Arquivo para gravação completa da sessão
        self.session_file_path = os.path.join(self.session_dir, "session_audio.wav")
        self.session_file = self._create_wave_file(self.session_file_path)
        
        # Metadados da sessão
        self.metadata = {
            "guild_id": guild_id,
            "channel_id": channel_id,
            "channel_name": channel_name,
            "start_time": datetime.now().isoformat(),
            "users": {},
            "segments": []
        }
        
        # Iniciar thread para processamento periódico
        self.running = True
        self.process_thread = threading.Thread(target=self._periodic_processing)
        self.process_thread.daemon = True
        self.process_thread.start()
    
    def process_audio(self, user_id, username, audio_data):
        """Processa o áudio recebido de um usuário"""
        with self.buffer_lock:
            # Registrar usuário se for a primeira vez
            if user_id not in self.user_buffers:
                self.user_buffers[user_id] = {
                    "buffer": bytearray(),
                    "username": username,
                    "last_activity": time.time()
                }
                self.metadata["users"][str(user_id)] = {
                    "username": username,
                    "first_seen": datetime.now().isoformat()
                }
            
            # Adicionar áudio ao buffer do usuário
            self.user_buffers[user_id]["buffer"].extend(audio_data)
            self.user_buffers[user_id]["last_activity"] = time.time()
            
            # Adicionar ao arquivo da sessão
            self.session_file.writeframes(audio_data)
    
    def _periodic_processing(self):
        """Thread para processamento periódico dos buffers de áudio"""
        while self.running:
            # Verificar buffers a cada 5 segundos
            time.sleep(5)
            
            with self.buffer_lock:
                current_time = time.time()
                
                for user_id, data in list(self.user_buffers.items()):
                    # Se houver inatividade por mais de 2 segundos e buffer não vazio
                    if current_time - data["last_activity"] > 2 and len(data["buffer"]) > 0:
                        # Salvar buffer em arquivo
                        self._save_user_audio(user_id, data["username"], bytes(data["buffer"]))
                        # Limpar buffer
                        data["buffer"] = bytearray()
    
    def _save_user_audio(self, user_id, username, audio_data):
        """Salva o áudio de um usuário em um arquivo"""
        if len(audio_data) == 0:
            return
            
        # Criar nome de arquivo baseado em timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{user_id}_{username}_{timestamp}.wav"
        filepath = os.path.join(self.session_dir, filename)
        
        # Criar e salvar arquivo de áudio
        with wave.open(filepath, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.sample_width)
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_data)
        
        # Registrar segmento nos metadados
        segment = {
            "user_id": user_id,
            "username": username,
            "file": filename,
            "timestamp": timestamp,
            "duration": len(audio_data) / (self.sample_rate * self.sample_width * self.channels)
        }
        self.metadata["segments"].append(segment)
        
        # Salvar metadados atualizados
        self._save_metadata()
        
        return filepath
    
    def _create_wave_file(self, filepath):
        """Cria um arquivo WAV para gravação"""
        wf = wave.open(filepath, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.sample_width)
        wf.setframerate(self.sample_rate)
        return wf
    
    def _save_metadata(self):
        """Salva os metadados da sessão em um arquivo JSON"""
        import json
        
        metadata_path = os.path.join(self.session_dir, "metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def cleanup(self):
        """Limpa recursos e finaliza processamento"""
        self.running = False
        
        if hasattr(self, 'process_thread') and self.process_thread.is_alive():
            self.process_thread.join(timeout=2.0)
        
        with self.buffer_lock:
            # Processar buffers restantes
            for user_id, data in self.user_buffers.items():
                if len(data["buffer"]) > 0:
                    self._save_user_audio(user_id, data["username"], bytes(data["buffer"]))
            
            # Fechar arquivo da sessão
            if hasattr(self, 'session_file'):
                self.session_file.close()
            
            # Atualizar metadados
            self.metadata["end_time"] = datetime.now().isoformat()
            self._save_metadata()
```

### Controlador Principal
```python
import asyncio
import os
import json
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("discord_collector.log")
    ]
)
logger = logging.getLogger("DiscordCollector")

class DiscordDataCollector:
    def __init__(self, token, config_path="config.json"):
        self.token = token
        self.config_path = config_path
        self.client = None
        self.config = self._load_config()
        
        # Criar diretórios necessários
        os.makedirs(self.config.get("data_dir", "./data"), exist_ok=True)
        os.makedirs(self.config.get("audio_dir", "./data/audio"), exist_ok=True)
        os.makedirs(self.config.get("transcription_dir", "./data/transcriptions"), exist_ok=True)
    
    def _load_config(self):
        """Carrega configuração do arquivo JSON"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            else:
                # Configuração padrão
                config = {
                    "data_dir": "./data",
                    "audio_dir": "./data/audio",
                    "transcription_dir": "./data/transcriptions",
                    "channels_to_monitor": [],
                    "auto_join": False
                }
                # Salvar configuração padrão
                with open(self.config_path, 'w') as f:
                    json.dump(config, f, indent=2)
                return config
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {e}")
            return {
                "data_dir": "./data",
                "audio_dir": "./data/audio",
                "transcription_dir": "./data/transcriptions"
            }
    
    async def start(self):
        """Inicia o coletor de dados"""
        from discord.ext import commands
        
        # Inicializar cliente Discord
        self.client = NinaDiscordClient()
        
        # Adicionar comandos
        @self.client.command(name="join")
        async def join(ctx):
            """Comando para entrar no canal de voz do autor"""
            if ctx.author.voice and ctx.author.voice.channel:
                channel = ctx.author.voice.channel
                try:
                    await self.client.join_voice_channel(channel.id)
                    await ctx.send(f"Conectado ao canal de voz: {channel.name}")
                except Exception as e:
                    await ctx.send(f"Erro ao conectar: {e}")
            else:
                await ctx.send("Você precisa estar em um canal de voz para usar este comando.")
        
        @self.client.command(name="leave")
        async def leave(ctx):
            """Comando para sair do canal de voz"""
            if ctx.voice_client:
                channel_id = ctx.voice_client.channel.id
                await self.client.leave_voice_channel(channel_id)
                await ctx.send("Desconectado do canal de voz.")
            else:
                await ctx.send("Não estou conectado a nenhum canal de voz.")
        
        # Evento de inicialização
        @self.client.event
        async def on_ready():
            logger.info(f"Bot conectado como {self.client.user}")
            
            # Auto-conectar a canais configurados
            if self.config.get("auto_join", False):
                for channel_id in self.config.get("channels_to_monitor", []):
                    try:
                        channel = self.client.get_channel(int(channel_id))
                        if channel and isinstance(channel, discord.VoiceChannel):
                            await self.client.join_voice_channel(channel.id)
                            logger.info(f"Auto-conectado ao canal: {channel.name}")
                    except Exception as e:
                        logger.error(f"Erro ao auto-conectar ao canal {channel_id}: {e}")
        
        # Iniciar o bot
        await self.client.start(self.token)
    
    def run(self):
        """Executa o coletor de dados em um loop assíncrono"""
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.start())
        except KeyboardInterrupt:
            logger.info("Encerrando coletor de dados...")
        finally:
            loop.close()
```

## Integração com Sistema de Diarização e Transcrição

Este sistema de coleta de dados do Discord será integrado com o sistema de diarização de falantes (próxima etapa) para processar os arquivos de áudio coletados. A implementação acima:

1. Captura o áudio de cada usuário em um canal de voz do Discord
2. Armazena o áudio em arquivos separados por usuário e sessão
3. Mantém metadados detalhados sobre a sessão, usuários e segmentos de áudio
4. Organiza os dados por servidor (guild), canal e data/hora

Na próxima etapa, implementaremos o sistema de diarização que processará esses arquivos de áudio para identificar diferentes falantes, mesmo quando o Discord não fornece essa informação diretamente (por exemplo, quando várias pessoas falam em um único stream de áudio).

## Considerações de Segurança e Privacidade

- Todo o processamento é realizado localmente
- Os dados são armazenados apenas no sistema local
- Metadados incluem apenas IDs e nomes de usuário, sem informações sensíveis
- O sistema pode ser configurado para monitorar apenas canais específicos
- Comandos de controle permitem iniciar e parar a coleta de dados conforme necessário
