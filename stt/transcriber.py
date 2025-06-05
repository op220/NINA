"""
Módulo para transcrição de áudio usando faster-whisper.
Parte do projeto Nina IA para reconhecimento de fala.
"""

import os
import logging
from typing import Optional, Dict, Any, List, Tuple, Union
import numpy as np

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WhisperTranscriber:
    """
    Classe para transcrição de áudio usando faster-whisper.
    """
    
    def __init__(self, 
                 model_size: str = "base", 
                 device: str = "cuda", 
                 compute_type: str = "float16",
                 download_root: Optional[str] = None,
                 language: Optional[str] = "pt",
                 beam_size: int = 5):
        """
        Inicializa o transcritor de áudio.
        
        Args:
            model_size: Tamanho do modelo Whisper ('tiny', 'base', 'small', 'medium', 'large-v3')
            device: Dispositivo para execução ('cuda' ou 'cpu')
            compute_type: Tipo de computação ('float16', 'float32', 'int8')
            download_root: Diretório para download do modelo (None = padrão)
            language: Código do idioma para transcrição (None = detecção automática)
            beam_size: Tamanho do beam search
        """
        try:
            from faster_whisper import WhisperModel
            self.model_size = model_size
            self.device = device
            self.compute_type = compute_type
            self.language = language
            self.beam_size = beam_size
            
            logger.info(f"Inicializando modelo Whisper {model_size} no dispositivo {device} com tipo {compute_type}")
            
            # Verificar disponibilidade de GPU para CUDA
            if device == "cuda":
                try:
                    import torch
                    if not torch.cuda.is_available():
                        logger.warning("CUDA não disponível, usando CPU")
                        self.device = "cpu"
                        if compute_type == "float16":
                            self.compute_type = "float32"  # float16 pode não ser suportado em CPU
                except ImportError:
                    logger.warning("PyTorch não instalado, usando CPU")
                    self.device = "cpu"
                    if compute_type == "float16":
                        self.compute_type = "float32"
            
            # Inicializar o modelo
            self.model = WhisperModel(
                model_size,
                device=self.device,
                compute_type=self.compute_type,
                download_root=download_root
            )
            
            logger.info("Modelo Whisper inicializado com sucesso")
            
        except ImportError as e:
            logger.error(f"Erro ao importar faster-whisper: {e}")
            logger.error("Por favor, instale faster-whisper: pip install faster-whisper")
            raise
        except Exception as e:
            logger.error(f"Erro ao inicializar modelo Whisper: {e}")
            raise
    
    def transcribe_file(self, 
                        audio_path: str, 
                        language: Optional[str] = None,
                        task: str = "transcribe",
                        initial_prompt: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
        """
        Transcreve um arquivo de áudio.
        
        Args:
            audio_path: Caminho para o arquivo de áudio
            language: Código do idioma (None = usar o padrão ou detecção automática)
            task: Tarefa a ser realizada ('transcribe' ou 'translate')
            initial_prompt: Prompt inicial para melhorar a transcrição
            
        Returns:
            Tuple contendo (texto transcrito, informações adicionais)
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Arquivo de áudio não encontrado: {audio_path}")
        
        lang = language or self.language
        
        try:
            logger.info(f"Transcrevendo arquivo: {audio_path}")
            segments, info = self.model.transcribe(
                audio_path,
                language=lang,
                task=task,
                beam_size=self.beam_size,
                initial_prompt=initial_prompt
            )
            
            # Coletar todos os segmentos
            segments_list = list(segments)
            
            # Extrair texto completo
            full_text = " ".join([segment.text for segment in segments_list])
            
            # Informações adicionais
            additional_info = {
                "language": info.language,
                "language_probability": info.language_probability,
                "duration": info.duration,
                "segments": [
                    {
                        "id": i,
                        "start": segment.start,
                        "end": segment.end,
                        "text": segment.text.strip(),
                        "words": [{"word": word.word, "start": word.start, "end": word.end, "probability": word.probability} 
                                 for word in (segment.words or [])]
                    }
                    for i, segment in enumerate(segments_list)
                ]
            }
            
            logger.info(f"Transcrição concluída: {len(full_text)} caracteres")
            return full_text, additional_info
            
        except Exception as e:
            logger.error(f"Erro ao transcrever áudio: {e}")
            raise
    
    def transcribe_array(self, 
                         audio_array: np.ndarray,
                         sample_rate: int = 16000,
                         language: Optional[str] = None,
                         task: str = "transcribe",
                         initial_prompt: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
        """
        Transcreve um array de áudio.
        
        Args:
            audio_array: Array numpy contendo dados de áudio
            sample_rate: Taxa de amostragem do áudio
            language: Código do idioma (None = usar o padrão ou detecção automática)
            task: Tarefa a ser realizada ('transcribe' ou 'translate')
            initial_prompt: Prompt inicial para melhorar a transcrição
            
        Returns:
            Tuple contendo (texto transcrito, informações adicionais)
        """
        import tempfile
        import soundfile as sf
        
        # Salvar array em arquivo temporário
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            # Normalizar áudio se necessário
            if audio_array.dtype != np.float32:
                audio_array = audio_array.astype(np.float32)
                
            if audio_array.ndim > 1 and audio_array.shape[1] > 1:
                # Converter para mono se for multicanal
                audio_array = audio_array.mean(axis=1)
            
            # Salvar no arquivo temporário
            sf.write(temp_path, audio_array, sample_rate)
            
            # Transcrever o arquivo
            return self.transcribe_file(
                temp_path, 
                language=language,
                task=task,
                initial_prompt=initial_prompt
            )
            
        finally:
            # Limpar arquivo temporário
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def get_available_models(self) -> List[str]:
        """
        Retorna a lista de modelos disponíveis.
        
        Returns:
            Lista de nomes de modelos disponíveis
        """
        return [
            "tiny", "tiny.en",
            "base", "base.en",
            "small", "small.en",
            "medium", "medium.en",
            "large-v1", "large-v2", "large-v3"
        ]


if __name__ == "__main__":
    # Exemplo de uso
    import sys
    
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        
        # Usar CPU para teste se não houver GPU
        transcriber = WhisperTranscriber(model_size="base", device="cpu", compute_type="float32")
        
        text, info = transcriber.transcribe_file(audio_file)
        print(f"Idioma detectado: {info['language']} (probabilidade: {info['language_probability']:.2f})")
        print(f"Texto transcrito: {text}")
    else:
        print("Uso: python transcriber.py <arquivo_audio>")
