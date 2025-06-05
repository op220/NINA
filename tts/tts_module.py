"""
Módulo principal para TTS (Text to Speech) do projeto Nina IA.
Integra a síntese de voz e reprodução de áudio.
"""

import os
import logging
from typing import Optional, Dict, Any, Union

from .tts_synthesizer import TTSSynthesizer
from .audio_player import AudioPlayer

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TTSModule:
    """
    Módulo principal para Text-to-Speech (TTS).
    Integra síntese de voz e reprodução de áudio.
    """
    
    def __init__(self, 
                 model_name: str = "tts_models/pt/cv/vits",
                 vocoder_name: Optional[str] = None,
                 use_cuda: bool = True,
                 speaker: Optional[str] = None,
                 language: Optional[str] = None,
                 output_dir: Optional[str] = None):
        """
        Inicializa o módulo TTS.
        
        Args:
            model_name: Nome do modelo TTS a ser usado
            vocoder_name: Nome do vocoder (None = usar o padrão do modelo)
            use_cuda: Se deve usar GPU para aceleração
            speaker: Nome do locutor para modelos multi-locutor
            language: Código do idioma para modelos multilíngues
            output_dir: Diretório para salvar arquivos de áudio (None = usar temporário)
        """
        self.model_name = model_name
        self.vocoder_name = vocoder_name
        self.use_cuda = use_cuda
        self.speaker = speaker
        self.language = language
        self.output_dir = output_dir
        
        # Criar diretório de saída se não existir
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Diretório de saída criado: {output_dir}")
        
        # Inicializar componentes
        logger.info("Inicializando módulo TTS")
        
        try:
            self.synthesizer = TTSSynthesizer(
                model_name=model_name,
                vocoder_name=vocoder_name,
                use_cuda=use_cuda
            )
            
            self.player = AudioPlayer()
            
            logger.info("Módulo TTS inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar módulo TTS: {e}")
            raise
    
    def speak(self, 
              text: str, 
              blocking: bool = True,
              save_file: bool = False) -> Optional[str]:
        """
        Sintetiza e reproduz texto.
        
        Args:
            text: Texto a ser sintetizado e reproduzido
            blocking: Se True, bloqueia até o fim da reprodução
            save_file: Se True, salva o arquivo de áudio permanentemente
            
        Returns:
            Caminho do arquivo de áudio gerado (se save_file=True) ou None
        """
        try:
            logger.info(f"Falando: '{text[:50]}...'")
            
            # Determinar caminho de saída
            output_path = None
            if save_file and self.output_dir:
                # Gerar nome de arquivo baseado no timestamp
                import time
                timestamp = int(time.time())
                output_path = os.path.join(self.output_dir, f"nina_speech_{timestamp}.wav")
            
            # Sintetizar texto
            audio_file = self.synthesizer.synthesize(
                text=text,
                output_path=output_path,
                speaker=self.speaker,
                language=self.language
            )
            
            # Reproduzir áudio
            self.player.play_file(audio_file, blocking=blocking)
            
            # Se não for para salvar e não for o caminho especificado, programar remoção
            if not save_file and (not output_path or audio_file != output_path):
                if not blocking:
                    # Programar remoção após reprodução
                    import threading
                    def cleanup():
                        # Aguardar o fim da reprodução
                        while self.player.is_busy():
                            import time
                            time.sleep(0.1)
                        
                        # Remover arquivo temporário
                        try:
                            if os.path.exists(audio_file):
                                os.unlink(audio_file)
                        except:
                            pass
                    
                    cleanup_thread = threading.Thread(target=cleanup)
                    cleanup_thread.daemon = True
                    cleanup_thread.start()
                else:
                    # Remover arquivo temporário
                    try:
                        if os.path.exists(audio_file):
                            os.unlink(audio_file)
                    except:
                        pass
                    return None
            
            return audio_file if save_file else None
            
        except Exception as e:
            logger.error(f"Erro ao falar texto: {e}")
            return None
    
    def speak_direct(self, 
                     text: str, 
                     blocking: bool = True) -> bool:
        """
        Sintetiza e reproduz texto diretamente (sem salvar arquivo).
        
        Args:
            text: Texto a ser sintetizado e reproduzido
            blocking: Se True, bloqueia até o fim da reprodução
            
        Returns:
            True se a operação foi bem-sucedida
        """
        try:
            logger.info(f"Falando diretamente: '{text[:50]}...'")
            
            # Sintetizar para array
            wav, sample_rate = self.synthesizer.synthesize_to_array(
                text=text,
                speaker=self.speaker,
                language=self.language
            )
            
            # Reproduzir array
            return self.player.play_array(wav, sample_rate, blocking=blocking)
            
        except Exception as e:
            logger.error(f"Erro ao falar texto diretamente: {e}")
            return False
    
    def stop_speaking(self) -> None:
        """
        Interrompe a fala atual.
        """
        self.player.stop()
    
    def is_speaking(self) -> bool:
        """
        Verifica se está falando.
        
        Returns:
            True se estiver falando
        """
        return self.player.is_busy()
    
    def change_voice(self, 
                     model_name: Optional[str] = None,
                     speaker: Optional[str] = None,
                     language: Optional[str] = None) -> bool:
        """
        Muda a voz usada para síntese.
        
        Args:
            model_name: Nome do novo modelo (None = manter atual)
            speaker: Nome do novo locutor (None = manter atual)
            language: Código do novo idioma (None = manter atual)
            
        Returns:
            True se a mudança foi bem-sucedida
        """
        try:
            # Atualizar modelo se especificado
            if model_name:
                result = self.synthesizer.change_model(model_name)
                if not result:
                    return False
                self.model_name = model_name
            
            # Atualizar locutor e idioma
            if speaker is not None:
                self.speaker = speaker
            
            if language is not None:
                self.language = language
            
            logger.info(f"Voz alterada: modelo={self.model_name}, locutor={self.speaker}, idioma={self.language}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao mudar voz: {e}")
            return False
    
    def list_available_models(self) -> Dict[str, list]:
        """
        Lista os modelos TTS disponíveis, organizados por idioma.
        
        Returns:
            Dicionário com modelos agrupados por idioma
        """
        models = self.synthesizer.list_available_models()
        
        # Organizar por idioma
        models_by_language = {}
        
        for model in models:
            parts = model.split('/')
            if len(parts) >= 2:
                lang = parts[1]  # Extrair código do idioma
                if lang not in models_by_language:
                    models_by_language[lang] = []
                models_by_language[lang].append(model)
        
        return models_by_language


if __name__ == "__main__":
    # Exemplo de uso
    tts = TTSModule(model_name="tts_models/pt/cv/vits", use_cuda=False)
    
    # Falar texto
    tts.speak("Olá, eu sou a Nina, sua assistente de inteligência artificial.", blocking=True)
    
    # Listar modelos disponíveis
    models = tts.list_available_models()
    print("Modelos disponíveis por idioma:")
    for lang, model_list in models.items():
        print(f"  {lang}:")
        for model in model_list:
            print(f"    - {model}")
