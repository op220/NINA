# Sistema de Diarização de Falantes

## Arquitetura do Sistema

### Componentes Principais
1. **Processador de Áudio**: Prepara os arquivos de áudio para diarização
2. **Diarizador**: Utiliza pyannote.audio para identificar diferentes falantes
3. **Transcritor**: Utiliza Whisper para transcrever o áudio em texto
4. **Integrador**: Combina diarização e transcrição para criar transcrições com falantes identificados
5. **Armazenamento**: Salva as transcrições organizadas por falante, data e canal

### Fluxo de Dados
1. Arquivos de áudio são carregados do sistema de coleta do Discord
2. Áudio é processado para diarização (identificação de falantes)
3. Segmentos de áudio são atribuídos a falantes específicos
4. Cada segmento é transcrito com Whisper
5. Transcrições são organizadas por falante e armazenadas localmente

## Implementação

### Processador de Diarização
```python
import os
import json
import torch
import numpy as np
import librosa
import wave
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("diarization.log")
    ]
)
logger = logging.getLogger("Diarization")

class SpeakerDiarizer:
    def __init__(self, 
                 model_path="pyannote/speaker-diarization-3.1", 
                 device="cuda" if torch.cuda.is_available() else "cpu",
                 use_auth_token=None):
        """
        Inicializa o sistema de diarização de falantes.
        
        Args:
            model_path: Caminho ou nome do modelo pyannote.audio
            device: Dispositivo para execução (cuda ou cpu)
            use_auth_token: Token de autenticação HuggingFace (se necessário)
        """
        self.device = device
        logger.info(f"Inicializando diarizador no dispositivo: {device}")
        
        try:
            # Carregar pipeline de diarização
            self.pipeline = Pipeline.from_pretrained(
                model_path,
                use_auth_token=use_auth_token
            )
            self.pipeline = self.pipeline.to(self.device)
            logger.info("Pipeline de diarização carregado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao carregar pipeline de diarização: {e}")
            raise
    
    def process_audio_file(self, audio_path, output_dir=None, min_speakers=1, max_speakers=5):
        """
        Processa um arquivo de áudio para diarização.
        
        Args:
            audio_path: Caminho para o arquivo de áudio
            output_dir: Diretório para salvar os resultados (opcional)
            min_speakers: Número mínimo de falantes esperados
            max_speakers: Número máximo de falantes esperados
            
        Returns:
            Dicionário com resultados da diarização
        """
        if not os.path.exists(audio_path):
            logger.error(f"Arquivo de áudio não encontrado: {audio_path}")
            return None
        
        try:
            logger.info(f"Processando arquivo: {audio_path}")
            
            # Definir diretório de saída
            if output_dir is None:
                output_dir = os.path.dirname(audio_path)
            os.makedirs(output_dir, exist_ok=True)
            
            # Obter informações do arquivo de áudio
            audio_info = self._get_audio_info(audio_path)
            
            # Configurar parâmetros da diarização
            with ProgressHook() as hook:
                diarization = self.pipeline(
                    audio_path,
                    min_speakers=min_speakers,
                    max_speakers=max_speakers,
                    hook=hook
                )
            
            # Processar resultados
            results = self._process_diarization_results(diarization, audio_info)
            
            # Salvar resultados
            output_json = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(audio_path))[0]}_diarization.json")
            with open(output_json, 'w') as f:
                json.dump(results, f, indent=2)
            
            logger.info(f"Diarização concluída. Identificados {len(results['speakers'])} falantes.")
            return results
            
        except Exception as e:
            logger.error(f"Erro ao processar arquivo de áudio: {e}")
            return None
    
    def process_session_directory(self, session_dir, output_dir=None):
        """
        Processa todos os arquivos de áudio em um diretório de sessão.
        
        Args:
            session_dir: Diretório contendo arquivos de áudio da sessão
            output_dir: Diretório para salvar os resultados (opcional)
            
        Returns:
            Dicionário com resultados da diarização para todos os arquivos
        """
        if not os.path.exists(session_dir):
            logger.error(f"Diretório de sessão não encontrado: {session_dir}")
            return None
        
        try:
            logger.info(f"Processando diretório de sessão: {session_dir}")
            
            # Definir diretório de saída
            if output_dir is None:
                output_dir = os.path.join(session_dir, "diarization")
            os.makedirs(output_dir, exist_ok=True)
            
            # Carregar metadados da sessão, se disponíveis
            metadata_path = os.path.join(session_dir, "metadata.json")
            metadata = {}
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
            
            # Encontrar arquivos de áudio
            audio_files = []
            for file in os.listdir(session_dir):
                if file.endswith((".wav", ".mp3", ".ogg")):
                    audio_files.append(os.path.join(session_dir, file))
            
            if not audio_files:
                logger.warning(f"Nenhum arquivo de áudio encontrado em: {session_dir}")
                return None
            
            # Processar cada arquivo
            results = {
                "session_dir": session_dir,
                "processed_at": datetime.now().isoformat(),
                "files": {}
            }
            
            for audio_file in audio_files:
                file_results = self.process_audio_file(audio_file, output_dir)
                if file_results:
                    results["files"][os.path.basename(audio_file)] = file_results
            
            # Salvar resultados consolidados
            output_json = os.path.join(output_dir, "session_diarization.json")
            with open(output_json, 'w') as f:
                json.dump(results, f, indent=2)
            
            logger.info(f"Processamento de sessão concluído. Processados {len(results['files'])} arquivos.")
            return results
            
        except Exception as e:
            logger.error(f"Erro ao processar diretório de sessão: {e}")
            return None
    
    def _get_audio_info(self, audio_path):
        """
        Obtém informações sobre o arquivo de áudio.
        
        Args:
            audio_path: Caminho para o arquivo de áudio
            
        Returns:
            Dicionário com informações do áudio
        """
        try:
            # Carregar áudio com librosa
            y, sr = librosa.load(audio_path, sr=None)
            duration = librosa.get_duration(y=y, sr=sr)
            
            # Obter informações adicionais do arquivo WAV
            if audio_path.endswith(".wav"):
                with wave.open(audio_path, 'rb') as wf:
                    channels = wf.getnchannels()
                    sample_width = wf.getsampwidth()
                    framerate = wf.getframerate()
                    n_frames = wf.getnframes()
            else:
                channels = 1
                sample_width = 2
                framerate = sr
                n_frames = len(y)
            
            return {
                "path": audio_path,
                "duration": duration,
                "sample_rate": sr,
                "channels": channels,
                "sample_width": sample_width,
                "framerate": framerate,
                "n_frames": n_frames
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter informações do áudio: {e}")
            return {
                "path": audio_path,
                "error": str(e)
            }
    
    def _process_diarization_results(self, diarization, audio_info):
        """
        Processa os resultados da diarização.
        
        Args:
            diarization: Objeto de diarização do pyannote.audio
            audio_info: Informações do arquivo de áudio
            
        Returns:
            Dicionário com resultados processados
        """
        # Extrair segmentos por falante
        speakers = {}
        segments = []
        
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            start = turn.start
            end = turn.end
            
            # Registrar falante
            if speaker not in speakers:
                speakers[speaker] = {
                    "id": speaker,
                    "total_duration": 0,
                    "segments_count": 0
                }
            
            # Atualizar estatísticas do falante
            duration = end - start
            speakers[speaker]["total_duration"] += duration
            speakers[speaker]["segments_count"] += 1
            
            # Adicionar segmento
            segment = {
                "speaker": speaker,
                "start": start,
                "end": end,
                "duration": duration
            }
            segments.append(segment)
        
        # Ordenar segmentos por tempo de início
        segments.sort(key=lambda x: x["start"])
        
        # Calcular porcentagens de fala
        total_duration = audio_info.get("duration", 0)
        if total_duration > 0:
            for speaker in speakers:
                speakers[speaker]["percentage"] = (speakers[speaker]["total_duration"] / total_duration) * 100
        
        # Construir resultado final
        result = {
            "audio_info": audio_info,
            "speakers": speakers,
            "segments": segments,
            "processed_at": datetime.now().isoformat()
        }
        
        return result
```

### Transcritor com Whisper
```python
import os
import json
import torch
import numpy as np
import librosa
import whisper
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("transcription.log")
    ]
)
logger = logging.getLogger("Transcription")

class WhisperTranscriber:
    def __init__(self, 
                 model_size="base", 
                 device="cuda" if torch.cuda.is_available() else "cpu",
                 language="pt"):
        """
        Inicializa o sistema de transcrição com Whisper.
        
        Args:
            model_size: Tamanho do modelo Whisper (tiny, base, small, medium, large)
            device: Dispositivo para execução (cuda ou cpu)
            language: Código do idioma para transcrição
        """
        self.model_size = model_size
        self.device = device
        self.language = language
        logger.info(f"Inicializando transcritor Whisper ({model_size}) no dispositivo: {device}")
        
        try:
            # Carregar modelo Whisper
            self.model = whisper.load_model(model_size, device=device)
            logger.info("Modelo Whisper carregado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao carregar modelo Whisper: {e}")
            raise
    
    def transcribe_audio_file(self, audio_path, output_dir=None):
        """
        Transcreve um arquivo de áudio.
        
        Args:
            audio_path: Caminho para o arquivo de áudio
            output_dir: Diretório para salvar os resultados (opcional)
            
        Returns:
            Dicionário com resultados da transcrição
        """
        if not os.path.exists(audio_path):
            logger.error(f"Arquivo de áudio não encontrado: {audio_path}")
            return None
        
        try:
            logger.info(f"Transcrevendo arquivo: {audio_path}")
            
            # Definir diretório de saída
            if output_dir is None:
                output_dir = os.path.dirname(audio_path)
            os.makedirs(output_dir, exist_ok=True)
            
            # Transcrever áudio
            transcription = self.model.transcribe(
                audio_path,
                language=self.language,
                task="transcribe",
                verbose=False
            )
            
            # Processar resultados
            results = {
                "audio_path": audio_path,
                "language": transcription.get("language", self.language),
                "text": transcription.get("text", ""),
                "segments": transcription.get("segments", []),
                "processed_at": datetime.now().isoformat()
            }
            
            # Salvar resultados
            output_json = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(audio_path))[0]}_transcription.json")
            with open(output_json, 'w') as f:
                json.dump(results, f, indent=2)
            
            logger.info(f"Transcrição concluída: {len(results['text'])} caracteres")
            return results
            
        except Exception as e:
            logger.error(f"Erro ao transcrever arquivo de áudio: {e}")
            return None
    
    def transcribe_audio_segment(self, audio_path, start_time, end_time, output_dir=None):
        """
        Transcreve um segmento específico de um arquivo de áudio.
        
        Args:
            audio_path: Caminho para o arquivo de áudio
            start_time: Tempo de início do segmento (segundos)
            end_time: Tempo de fim do segmento (segundos)
            output_dir: Diretório para salvar os resultados (opcional)
            
        Returns:
            Dicionário com resultados da transcrição do segmento
        """
        if not os.path.exists(audio_path):
            logger.error(f"Arquivo de áudio não encontrado: {audio_path}")
            return None
        
        try:
            logger.info(f"Transcrevendo segmento de {start_time:.2f}s a {end_time:.2f}s do arquivo: {audio_path}")
            
            # Carregar áudio
            audio, sr = librosa.load(audio_path, sr=None)
            
            # Extrair segmento
            start_sample = int(start_time * sr)
            end_sample = int(end_time * sr)
            
            if start_sample >= len(audio) or end_sample > len(audio) or start_sample >= end_sample:
                logger.error(f"Segmento inválido: {start_time}s-{end_time}s para áudio de {len(audio)/sr:.2f}s")
                return None
            
            segment_audio = audio[start_sample:end_sample]
            
            # Salvar segmento temporário
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_path = temp_file.name
            
            import soundfile as sf
            sf.write(temp_path, segment_audio, sr)
            
            # Transcrever segmento
            try:
                transcription = self.model.transcribe(
                    temp_path,
                    language=self.language,
                    task="transcribe",
                    
(Content truncated due to size limit. Use line ranges to read in chunks)