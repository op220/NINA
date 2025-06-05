"""
Módulo para síntese de voz usando Coqui TTS.
Parte do projeto Nina IA para conversão de texto em fala.
"""

import os
import logging
import tempfile
from typing import Optional, Dict, Any, List, Union

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TTSSynthesizer:
    """
    Classe para síntese de voz usando Coqui TTS.
    """
    
    def __init__(self, 
                 model_name: str = "tts_models/pt/cv/vits",
                 vocoder_name: Optional[str] = None,
                 use_cuda: bool = True,
                 speaker_idx: Optional[int] = None,
                 language_idx: Optional[str] = None):
        """
        Inicializa o sintetizador de voz.
        
        Args:
            model_name: Nome do modelo TTS a ser usado
            vocoder_name: Nome do vocoder (None = usar o padrão do modelo)
            use_cuda: Se deve usar GPU para aceleração
            speaker_idx: Índice do locutor para modelos multi-locutor
            language_idx: Código do idioma para modelos multilíngues
        """
        self.model_name = model_name
        self.vocoder_name = vocoder_name
        self.use_cuda = use_cuda
        self.speaker_idx = speaker_idx
        self.language_idx = language_idx
        self.tts = None
        
        # Verificar disponibilidade de GPU
        if use_cuda:
            try:
                import torch
                if not torch.cuda.is_available():
                    logger.warning("CUDA não disponível, usando CPU")
                    self.use_cuda = False
            except ImportError:
                logger.warning("PyTorch não instalado, usando CPU")
                self.use_cuda = False
        
        # Inicializar o modelo TTS
        try:
            self._initialize_tts()
        except Exception as e:
            logger.error(f"Erro ao inicializar TTS: {e}")
            raise
    
    def _initialize_tts(self) -> None:
        """
        Inicializa o modelo TTS.
        """
        try:
            from TTS.api import TTS
            
            logger.info(f"Inicializando modelo TTS: {self.model_name}")
            
            # Determinar o dispositivo
            device = "cuda" if self.use_cuda else "cpu"
            
            # Inicializar o modelo
            self.tts = TTS(model_name=self.model_name).to(device)

            
            logger.info("Modelo TTS inicializado com sucesso")
            
        except ImportError as e:
            logger.error(f"Erro ao importar TTS: {e}")
            logger.error("Por favor, instale Coqui TTS: pip install TTS")
            raise
        except Exception as e:
            logger.error(f"Erro ao inicializar modelo TTS: {e}")
            raise
    
    def list_available_models(self) -> List[str]:
        """
        Lista os modelos TTS disponíveis.
        
        Returns:
            Lista de modelos disponíveis
        """
        try:
            from TTS.api import TTS
            return TTS().list_models()
        except Exception as e:
            logger.error(f"Erro ao listar modelos: {e}")
            return []
    
    def synthesize(self, 
                   text: str, 
                   output_path: Optional[str] = None,
                   speaker: Optional[str] = None,
                   language: Optional[str] = None) -> str:
        """
        Sintetiza texto em fala.
        
        Args:
            text: Texto a ser sintetizado
            output_path: Caminho para salvar o áudio (None = gerar arquivo temporário)
            speaker: Nome do locutor para modelos multi-locutor
            language: Código do idioma para modelos multilíngues
            
        Returns:
            Caminho do arquivo de áudio gerado
        """
        if not self.tts:
            raise RuntimeError("Modelo TTS não inicializado")
        
        # Criar arquivo temporário se não for especificado
        if not output_path:
            temp_dir = tempfile.gettempdir()
            output_path = os.path.join(temp_dir, f"nina_tts_{os.getpid()}.wav")
        
        try:
            logger.info(f"Sintetizando texto: '{text[:50]}...' para {output_path}")
            
            # Preparar argumentos para síntese
            kwargs = {}
            if speaker is not None:
                kwargs["speaker"] = speaker
            elif self.speaker_idx is not None:
                kwargs["speaker_id"] = self.speaker_idx
                
            if language is not None:
                kwargs["language"] = language
            elif self.language_idx is not None:
                kwargs["language_id"] = self.language_idx
            
            # Sintetizar e salvar
            self.tts.tts_to_file(text=text, file_path=output_path, **kwargs)
            
            logger.info(f"Síntese concluída: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Erro na síntese de voz: {e}")
            raise
    
    def synthesize_to_array(self, 
                            text: str,
                            speaker: Optional[str] = None,
                            language: Optional[str] = None) -> tuple:
        """
        Sintetiza texto em um array de áudio.
        
        Args:
            text: Texto a ser sintetizado
            speaker: Nome do locutor para modelos multi-locutor
            language: Código do idioma para modelos multilíngues
            
        Returns:
            Tuple contendo (array de áudio, taxa de amostragem)
        """
        if not self.tts:
            raise RuntimeError("Modelo TTS não inicializado")
        
        try:
            logger.info(f"Sintetizando texto para array: '{text[:50]}...'")
            
            # Preparar argumentos para síntese
            kwargs = {}
            if speaker is not None:
                kwargs["speaker"] = speaker
            elif self.speaker_idx is not None:
                kwargs["speaker_id"] = self.speaker_idx
                
            if language is not None:
                kwargs["language"] = language
            elif self.language_idx is not None:
                kwargs["language_id"] = self.language_idx
            
            # Sintetizar
            wav = self.tts.tts(text=text, **kwargs)
            
            # A API TTS retorna apenas o array, a taxa de amostragem é fixa em 22050 Hz
            sample_rate = 22050
            
            logger.info(f"Síntese para array concluída")
            return wav, sample_rate
            
        except Exception as e:
            logger.error(f"Erro na síntese de voz para array: {e}")
            raise
    
    def change_model(self, 
                     model_name: str,
                     vocoder_name: Optional[str] = None) -> bool:
        """
        Muda o modelo TTS.
        
        Args:
            model_name: Nome do novo modelo
            vocoder_name: Nome do novo vocoder (None = usar o padrão do modelo)
            
        Returns:
            True se a mudança for bem-sucedida
        """
        try:
            self.model_name = model_name
            self.vocoder_name = vocoder_name
            
            # Reinicializar o modelo
            self._initialize_tts()
            
            logger.info(f"Modelo alterado para {model_name}")
            return True
        except Exception as e:
            logger.error(f"Erro ao mudar modelo: {e}")
            return False


if __name__ == "__main__":
    # Exemplo de uso
    synthesizer = TTSSynthesizer(model_name="tts_models/pt/cv/vits", use_cuda=False)
    
    # Listar modelos disponíveis
    models = synthesizer.list_available_models()
    print("Modelos disponíveis:")
    for model in models:
        if "pt" in model:  # Filtrar apenas modelos em português
            print(f"  - {model}")
    
    # Sintetizar texto
    output_file = synthesizer.synthesize(
        text="Olá, eu sou a Nina, sua assistente de inteligência artificial.",
        output_path="./teste_tts.wav"
    )
    print(f"Áudio gerado em: {output_file}")
