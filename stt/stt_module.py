"""
Módulo principal para Speech-to-Text (STT) do projeto Nina IA.
Integra a captura de áudio e transcrição.
"""

import os
import time
import logging
from typing import Optional, Dict, Any, Tuple, Union
import numpy as np

from .audio_capture import AudioCapture
from .transcriber import WhisperTranscriber

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class STTModule:
    """
    Módulo principal para Speech-to-Text (STT).
    Integra captura de áudio e transcrição.
    """
    
    def __init__(self, 
                 model_size: str = "base", 
                 device: str = "cuda", 
                 compute_type: str = "float16",
                 language: str = "pt",
                 sample_rate: int = 16000,
                 vad_threshold: float = 0.03,
                 silence_duration: float = 1.0):
        """
        Inicializa o módulo STT.
        
        Args:
            model_size: Tamanho do modelo Whisper ('tiny', 'base', 'small', 'medium', 'large-v3')
            device: Dispositivo para execução ('cuda' ou 'cpu')
            compute_type: Tipo de computação ('float16', 'float32', 'int8')
            language: Código do idioma para transcrição
            sample_rate: Taxa de amostragem em Hz
            vad_threshold: Limiar para detecção de atividade de voz
            silence_duration: Duração do silêncio para considerar fim da fala (segundos)
        """
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.language = language
        self.sample_rate = sample_rate
        self.vad_threshold = vad_threshold
        self.silence_duration = silence_duration
        
        # Inicializar componentes
        logger.info("Inicializando módulo STT")
        self.audio_capture = AudioCapture(sample_rate=sample_rate)
        
        try:
            self.transcriber = WhisperTranscriber(
                model_size=model_size,
                device=device,
                compute_type=compute_type,
                language=language
            )
            logger.info("Módulo STT inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar transcritor: {e}")
            raise
    
    def listen_and_transcribe(self, 
                              max_duration: float = 30.0,
                              wait_timeout: float = 5.0) -> Tuple[str, Dict[str, Any]]:
        """
        Escuta o microfone e transcreve a fala detectada.
        
        Args:
            max_duration: Duração máxima da gravação em segundos
            wait_timeout: Tempo máximo de espera por fala em segundos
            
        Returns:
            Tuple contendo (texto transcrito, informações adicionais)
        """
        logger.info("Aguardando fala...")
        
        # Esperar por atividade de voz
        speech_detected = self.audio_capture.wait_for_speech(
            timeout=wait_timeout,
            silence_threshold=self.vad_threshold
        )
        
        if not speech_detected:
            logger.info("Nenhuma fala detectada no timeout")
            return "", {"error": "no_speech_detected"}
        
        # Gravar áudio em arquivo temporário
        logger.info(f"Fala detectada, gravando por até {max_duration} segundos...")
        temp_file = self.audio_capture.record_temp_file(max_duration)
        
        # Transcrever o áudio
        try:
            text, info = self.transcriber.transcribe_file(temp_file)
            return text, info
        except Exception as e:
            logger.error(f"Erro na transcrição: {e}")
            return "", {"error": str(e)}
        finally:
            # Limpar arquivo temporário
            if os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except:
                    pass
    
    def transcribe_file(self, 
                        audio_path: str,
                        language: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
        """
        Transcreve um arquivo de áudio existente.
        
        Args:
            audio_path: Caminho para o arquivo de áudio
            language: Código do idioma (None = usar o padrão)
            
        Returns:
            Tuple contendo (texto transcrito, informações adicionais)
        """
        return self.transcriber.transcribe_file(
            audio_path,
            language=language or self.language
        )
    
    def continuous_listen(self, 
                          callback,
                          stop_event=None,
                          max_listen_time: float = 30.0,
                          pause_time: float = 0.5):
        """
        Escuta continuamente o microfone e chama o callback com as transcrições.
        
        Args:
            callback: Função a ser chamada com o texto transcrito
            stop_event: Evento para parar a escuta (threading.Event)
            max_listen_time: Tempo máximo de escuta por iteração
            pause_time: Tempo de pausa entre iterações
        """
        logger.info("Iniciando escuta contínua")
        
        try:
            while stop_event is None or not stop_event.is_set():
                text, info = self.listen_and_transcribe(max_duration=max_listen_time)
                
                if text and not info.get("error"):
                    callback(text, info)
                
                time.sleep(pause_time)
                
        except KeyboardInterrupt:
            logger.info("Escuta contínua interrompida pelo usuário")
        except Exception as e:
            logger.error(f"Erro durante escuta contínua: {e}")
        finally:
            logger.info("Escuta contínua finalizada")


if __name__ == "__main__":
    # Exemplo de uso
    def print_transcription(text, info):
        print(f"Transcrição: {text}")
    
    # Inicializar com CPU para teste
    stt = STTModule(device="cpu", compute_type="float32", model_size="base")
    
    # Escutar uma vez
    text, info = stt.listen_and_transcribe()
    print(f"Texto: {text}")
    
    # Ou escutar continuamente (pressione Ctrl+C para parar)
    # stt.continuous_listen(print_transcription)
