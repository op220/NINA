# Configuração dos Componentes

Nesta seção, vamos configurar cada um dos componentes principais da Nina IA para que funcionem corretamente no seu sistema Windows. Certifique-se de que todos os componentes foram instalados conforme as instruções da seção anterior.

## Configuração do Sistema de Reconhecimento de Voz

Vamos criar os arquivos necessários para o sistema de reconhecimento de voz (STT).

### Criação do Módulo de Captura de Áudio

1. Crie o arquivo `C:\NinaIA\nina_ia\stt\audio_capture.py` com o seguinte conteúdo:

```python
import pyaudio
import wave
import numpy as np
import threading
import time
import os
from datetime import datetime

class AudioCapture:
    def __init__(self, rate=16000, chunk_size=1024, channels=1, device_index=None):
        self.rate = rate
        self.chunk_size = chunk_size
        self.channels = channels
        self.device_index = device_index
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_recording = False
        self.frames = []
        self.silence_threshold = 300  # Ajuste conforme necessário
        self.silence_duration = 1.5   # Segundos de silêncio para parar a gravação
        self.min_record_time = 1.0    # Tempo mínimo de gravação em segundos
        self.temp_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "temp")
        
        # Criar diretório temporário se não existir
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
    
    def list_devices(self):
        """Lista todos os dispositivos de áudio disponíveis."""
        info = []
        for i in range(self.audio.get_device_count()):
            device_info = self.audio.get_device_info_by_index(i)
            info.append(f"Device {i}: {device_info['name']}")
        return info
    
    def start_recording(self):
        """Inicia a gravação de áudio."""
        if self.is_recording:
            return
        
        self.frames = []
        self.is_recording = True
        self.start_time = time.time()
        self.last_sound_time = time.time()
        
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.rate,
            input=True,
            input_device_index=self.device_index,
            frames_per_buffer=self.chunk_size
        )
        
        # Iniciar thread de gravação
        self.record_thread = threading.Thread(target=self._record)
        self.record_thread.daemon = True
        self.record_thread.start()
        
        return True
    
    def _record(self):
        """Função interna para gravação contínua."""
        while self.is_recording:
            data = self.stream.read(self.chunk_size, exception_on_overflow=False)
            self.frames.append(data)
            
            # Verificar nível de áudio para detecção de silêncio
            audio_data = np.frombuffer(data, dtype=np.int16)
            volume_norm = np.linalg.norm(audio_data) / self.chunk_size
            
            if volume_norm > self.silence_threshold:
                self.last_sound_time = time.time()
            elif time.time() - self.start_time > self.min_record_time and time.time() - self.last_sound_time > self.silence_duration:
                # Parar gravação após silêncio prolongado
                self.stop_recording()
                break
    
    def stop_recording(self):
        """Para a gravação de áudio."""
        if not self.is_recording:
            return None
        
        self.is_recording = False
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        
        # Salvar o áudio gravado
        if len(self.frames) > 0:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.temp_dir, f"audio_{timestamp}.wav")
            
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(self.frames))
            
            return filename
        
        return None
    
    def close(self):
        """Libera recursos."""
        if self.stream:
            self.stream.close()
        self.audio.terminate()

# Função para teste
def test_audio_capture():
    print("Testando captura de áudio...")
    
    # Listar dispositivos
    audio_capture = AudioCapture()
    devices = audio_capture.list_devices()
    print("Dispositivos de áudio disponíveis:")
    for device in devices:
        print(device)
    
    # Iniciar gravação
    print("\nIniciando gravação... Fale algo!")
    audio_capture.start_recording()
    
    # Aguardar até que a gravação pare automaticamente ou por 10 segundos
    timeout = time.time() + 10
    while audio_capture.is_recording and time.time() < timeout:
        time.sleep(0.1)
    
    # Parar gravação se ainda estiver gravando
    if audio_capture.is_recording:
        filename = audio_capture.stop_recording()
    else:
        filename = audio_capture.frames and os.path.join(audio_capture.temp_dir, "audio_test.wav") or None
    
    # Fechar recursos
    audio_capture.close()
    
    if filename:
        print(f"Áudio gravado em: {filename}")
        return filename
    else:
        print("Nenhum áudio foi gravado.")
        return None

if __name__ == "__main__":
    test_audio_capture()
```

### Criação do Módulo de Transcrição

2. Crie o arquivo `C:\NinaIA\nina_ia\stt\transcriber.py` com o seguinte conteúdo:

```python
import os
import time
import logging
from faster_whisper import WhisperModel

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("transcriber")

class Transcriber:
    def __init__(self, model_size="medium", device="cuda", compute_type="float16"):
        """
        Inicializa o transcritor com o modelo Whisper.
        
        Args:
            model_size: Tamanho do modelo (tiny, base, small, medium, large)
            device: Dispositivo para inferência (cuda, cpu)
            compute_type: Tipo de computação (float16, float32, int8)
        """
        # Ajustar configurações com base no dispositivo disponível
        try:
            import torch
            if not torch.cuda.is_available() and device == "cuda":
                logger.warning("CUDA não disponível. Usando CPU.")
                device = "cpu"
                compute_type = "float32"
        except ImportError:
            logger.warning("PyTorch não encontrado. Usando CPU.")
            device = "cpu"
            compute_type = "float32"
        
        logger.info(f"Inicializando modelo Whisper ({model_size}) no dispositivo {device} com tipo {compute_type}")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        logger.info("Modelo inicializado com sucesso")
    
    def transcribe(self, audio_path, language="pt"):
        """
        Transcreve um arquivo de áudio.
        
        Args:
            audio_path: Caminho para o arquivo de áudio
            language: Código do idioma (pt, en, etc.)
            
        Returns:
            Texto transcrito
        """
        if not os.path.exists(audio_path):
            logger.error(f"Arquivo de áudio não encontrado: {audio_path}")
            return ""
        
        try:
            start_time = time.time()
            logger.info(f"Iniciando transcrição do arquivo: {audio_path}")
            
            # Realizar transcrição
            segments, info = self.model.transcribe(audio_path, language=language, beam_size=5)
            
            # Juntar todos os segmentos
            transcript = " ".join([segment.text for segment in segments])
            
            elapsed_time = time.time() - start_time
            logger.info(f"Transcrição concluída em {elapsed_time:.2f} segundos")
            logger.info(f"Texto: {transcript}")
            
            return transcript.strip()
        except Exception as e:
            logger.error(f"Erro durante a transcrição: {str(e)}")
            return ""

# Alternativa: Implementação para Whisper.cpp
class WhisperCppTranscriber:
    def __init__(self, model_path="C:\\NinaIA\\whisper.cpp\\models\\ggml-medium.bin"):
        """
        Inicializa o transcritor com o modelo Whisper.cpp.
        
        Args:
            model_path: Caminho para o arquivo do modelo
        """
        self.model_path = model_path
        self.whisper_cpp_path = "C:\\NinaIA\\whisper.cpp\\build\\bin\\Release\\main.exe"
        
        if not os.path.exists(self.model_path):
            logger.error(f"Arquivo de modelo não encontrado: {self.model_path}")
        
        if not os.path.exists(self.whisper_cpp_path):
            logger.error(f"Executável whisper.cpp não encontrado: {self.whisper_cpp_path}")
    
    def transcribe(self, audio_path, language="pt"):
        """
        Transcreve um arquivo de áudio usando whisper.cpp.
        
        Args:
            audio_path: Caminho para o arquivo de áudio
            language: Código do idioma (pt, en, etc.)
            
        Returns:
            Texto transcrito
        """
        if not os.path.exists(audio_path):
            logger.error(f"Arquivo de áudio não encontrado: {audio_path}")
            return ""
        
        try:
            start_time = time.time()
            logger.info(f"Iniciando transcrição do arquivo: {audio_path}")
            
            # Arquivo temporário para saída
            output_file = audio_path + ".txt"
            
            # Comando para executar whisper.cpp
            cmd = f'"{self.whisper_cpp_path}" -m "{self.model_path}" -f "{audio_path}" -l {language} -otxt'
            
            # Executar comando
            os.system(cmd)
            
            # Ler resultado
            if os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8') as f:
                    transcript = f.read().strip()
                
                # Remover arquivo temporário
                try:
                    os.remove(output_file)
                except:
                    pass
                
                elapsed_time = time.time() - start_time
                logger.info(f"Transcrição concluída em {elapsed_time:.2f} segundos")
                logger.info(f"Texto: {transcript}")
                
                return transcript
            else:
                logger.error("Arquivo de saída não foi gerado")
                return ""
        except Exception as e:
            logger.error(f"Erro durante a transcrição: {str(e)}")
            return ""

# Função para teste
def test_transcriber():
    from audio_capture import test_audio_capture
    
    # Testar gravação de áudio
    audio_file = test_audio_capture()
    if not audio_file:
        print("Não foi possível gravar áudio para teste.")
        return
    
    # Testar transcrição
    print("\nIniciando transcrição...")
    
    # Escolher implementação com base na disponibilidade
    try:
        transcriber = Transcriber(model_size="medium")
        use_faster_whisper = True
    except Exception as e:
        print(f"Erro ao inicializar Faster Whisper: {str(e)}")
        print("Tentando usar Whisper.cpp...")
        transcriber = WhisperCppTranscriber()
        use_faster_whisper = False
    
    # Realizar transcrição
    transcript = transcriber.transcribe(audio_file)
    
    print(f"\nImplementação: {'Faster Whisper' if use_faster_whisper else 'Whisper.cpp'}")
    print(f"Texto transcrito: {transcript}")

if __name__ == "__main__":
    test_transcriber()
```

### Criação do Módulo Principal de STT

3. Crie o arquivo `C:\NinaIA\nina_ia\stt\stt_module.py` com o seguinte conteúdo:

```python
import os
import logging
from .audio_capture import AudioCapture
from .transcriber import Transcriber, WhisperCppTranscriber

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("stt_module")

class STTModule:
    def __init__(self, use_faster_whisper=True, model_size="medium", device="cuda", language="pt"):
        """
        Inicializa o módulo de reconhecimento de voz.
        
        Args:
            use_faster_whisper: Se True, usa Faster Whisper; se False, usa Whisper.cpp
            model_size: Tamanho do modelo (tiny, base, small, medium, large)
            device: Dispositivo para inferência (cuda, cpu)
            language: Código do idioma (pt, en, etc.)
        """
        self.language = language
        self.audio_capture = AudioCapture()
        
        # Inicializar transcritor
        if use_faster_whisper:
            try:
                logger.info(f"Inicializando Faster Whisper ({model_size}) no dispositivo {device}")
                self.transcriber = Transcriber(model_size=model_size, device=device)
                logger.info("Faster Whisper inicializado com sucesso")
            except Exception as e:
                logger.warning(f"Erro ao inicializar Faster Whisper: {str(e)}")
                logger.info("Usando Whisper.cpp como alternativa")
                self.transcriber = WhisperCppTranscriber()
        else:
            logger.info("Inicializando Whisper.cpp")
            self.transcriber = WhisperCppTranscriber()
    
    def listen(self):
        """
        Escuta o microfone e retorna o texto transcrito.
        
        Returns:
            Texto transcrito ou None se nenhum áudio foi capturado
        """
        logger.info("Iniciando captura de áudio...")
        self.audio_capture.start_recording()
        
        # Aguardar até que a gravação pare automaticamente
        while self.audio_capture.is_recording:
            pass
        
        # Obter o arquivo de áudio gravado
        audio_file = self.audio_capture.stop_recording()
        
        if not audio_file:
            logger.warning("Nenhum áudio foi capturado")
            return None
        
        logger.info(f"Áudio capturado: {audio_file}")
        
        # Transcrever o áudio
        logger.info("Transcrevendo áudio...")
        transcript = self.transcriber.transcribe(audio_file, language=self.language)
        
        # Remover arquivo temporário
        try:
            os.remove(audio_file)
        except:
            pass
        
        return transcript
    
    def transcribe_file(self, audio_file):
        """
        Transcreve um arquivo de áudio existente.
        
        Args:
            audio_file: Caminho para o arquivo de áudio
            
        Returns:
            Texto transcrito
        """
        if not os.path.exists(audio_file):
            logger.error(f"Arquivo de áudio não encontrado: {audio_file}")
            return ""
        
        logger.info(f"Transcrevendo arquivo: {audio_file}")
        return self.transcriber.transcribe(audio_file, language=self.language)
    
    def close(self):
        """Libera recursos."""
        self.audio_capture.close()

# Função para teste
def test_stt_module():
    print("Testando módulo de reconhecimento de voz...")
    
    # Inicializar módulo STT
    stt = STTModule(use_faster_whisper=True, model_size="medium")
    
    # Testar reconhecimento de voz
    print("\nFale algo quando estiver pronto...")
    transcript = stt.listen()
    
    if transcript:
        print(f"\nTexto reconhecido: {transcript}")
    else:
        print("\nNenhum texto foi reconhecido.")
    
    # Liberar recursos
    stt.close()

if __name__ == "__main__":
    test_stt_module()
```

## Configuração do Sistema de Processamento de Linguagem Natural

Vamos criar os arquivos necessários para o sistema de processamento de linguagem natural (LLM).

### Criação d
(Content truncated due to size limit. Use line ranges to read in chunks)