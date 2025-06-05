"""
Módulo para reprodução de áudio sintetizado.
Parte do projeto Nina IA para playback de voz.
"""

import os
import logging
import tempfile
import threading
from typing import Optional, Union, Tuple

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AudioPlayer:
    """
    Classe para reprodução de áudio.
    """
    
    def __init__(self):
        """
        Inicializa o reprodutor de áudio.
        """
        self.current_playback = None
        self.is_playing = False
    
    def play_file(self, 
                  audio_path: str, 
                  blocking: bool = False) -> bool:
        """
        Reproduz um arquivo de áudio.
        
        Args:
            audio_path: Caminho para o arquivo de áudio
            blocking: Se True, bloqueia até o fim da reprodução
            
        Returns:
            True se a reprodução foi iniciada com sucesso
        """
        if not os.path.exists(audio_path):
            logger.error(f"Arquivo de áudio não encontrado: {audio_path}")
            return False
        
        try:
            # Interromper reprodução atual se houver
            self.stop()
            
            logger.info(f"Reproduzindo áudio: {audio_path}")
            
            # Usar pygame para reprodução
            try:
                import pygame
                
                # Inicializar pygame mixer se necessário
                if not pygame.mixer.get_init():
                    pygame.mixer.init()
                
                # Carregar e reproduzir
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play()
                
                self.is_playing = True
                
                # Se for bloqueante, aguardar o fim da reprodução
                if blocking:
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)
                    self.is_playing = False
                
                return True
                
            except ImportError:
                logger.warning("pygame não encontrado, tentando pydub")
                
                # Alternativa usando pydub
                try:
                    from pydub import AudioSegment
                    from pydub.playback import play
                    
                    # Carregar áudio
                    sound = AudioSegment.from_file(audio_path)
                    
                    if blocking:
                        # Reprodução bloqueante
                        play(sound)
                        self.is_playing = False
                    else:
                        # Reprodução não bloqueante
                        self.current_playback = threading.Thread(
                            target=self._play_thread, 
                            args=(sound,)
                        )
                        self.current_playback.daemon = True
                        self.current_playback.start()
                        self.is_playing = True
                    
                    return True
                    
                except ImportError:
                    logger.error("Nenhuma biblioteca de reprodução de áudio encontrada")
                    logger.error("Instale pygame ou pydub: pip install pygame pydub")
                    return False
                
        except Exception as e:
            logger.error(f"Erro ao reproduzir áudio: {e}")
            return False
    
    def _play_thread(self, sound) -> None:
        """
        Função para reprodução em thread separada.
        
        Args:
            sound: Objeto AudioSegment do pydub
        """
        from pydub.playback import play
        play(sound)
        self.is_playing = False
    
    def play_array(self, 
                   audio_array, 
                   sample_rate: int = 22050,
                   blocking: bool = False) -> bool:
        """
        Reproduz um array de áudio.
        
        Args:
            audio_array: Array numpy com dados de áudio
            sample_rate: Taxa de amostragem em Hz
            blocking: Se True, bloqueia até o fim da reprodução
            
        Returns:
            True se a reprodução foi iniciada com sucesso
        """
        try:
            # Salvar array em arquivo temporário
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Salvar array como arquivo WAV
            try:
                import soundfile as sf
                sf.write(temp_path, audio_array, sample_rate)
            except ImportError:
                try:
                    from scipy.io import wavfile
                    import numpy as np
                    
                    # Normalizar para int16
                    if audio_array.dtype != np.int16:
                        audio_array = (audio_array * 32767).astype(np.int16)
                    
                    wavfile.write(temp_path, sample_rate, audio_array)
                except ImportError:
                    logger.error("Nenhuma biblioteca para salvar áudio encontrada")
                    logger.error("Instale soundfile ou scipy: pip install soundfile scipy")
                    return False
            
            # Reproduzir o arquivo temporário
            result = self.play_file(temp_path, blocking)
            
            # Se não for bloqueante, programar a remoção do arquivo temporário
            if not blocking:
                def cleanup():
                    # Aguardar o fim da reprodução
                    if hasattr(self, 'current_playback') and self.current_playback:
                        self.current_playback.join()
                    
                    # Remover arquivo temporário
                    try:
                        if os.path.exists(temp_path):
                            os.unlink(temp_path)
                    except:
                        pass
                
                cleanup_thread = threading.Thread(target=cleanup)
                cleanup_thread.daemon = True
                cleanup_thread.start()
            else:
                # Remover arquivo temporário
                try:
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
                except:
                    pass
            
            return result
            
        except Exception as e:
            logger.error(f"Erro ao reproduzir array de áudio: {e}")
            return False
    
    def stop(self) -> None:
        """
        Interrompe a reprodução atual.
        """
        if self.is_playing:
            try:
                # Tentar parar com pygame
                try:
                    import pygame
                    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                except ImportError:
                    pass
                
                # Marcar como não reproduzindo
                self.is_playing = False
                
                logger.info("Reprodução interrompida")
            except Exception as e:
                logger.error(f"Erro ao interromper reprodução: {e}")
    
    def is_busy(self) -> bool:
        """
        Verifica se há reprodução em andamento.
        
        Returns:
            True se estiver reproduzindo áudio
        """
        # Verificar com pygame
        try:
            import pygame
            if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                return True
        except ImportError:
            pass
        
        # Verificar thread de reprodução
        if hasattr(self, 'current_playback') and self.current_playback and self.current_playback.is_alive():
            return True
        
        return self.is_playing


if __name__ == "__main__":
    # Exemplo de uso
    import sys
    
    player = AudioPlayer()
    
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        print(f"Reproduzindo {audio_file}...")
        player.play_file(audio_file, blocking=True)
        print("Reprodução concluída")
    else:
        print("Uso: python audio_player.py <arquivo_audio>")
