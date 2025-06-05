"""
Módulo para gerenciamento avançado de playback de áudio.
Parte do projeto Nina IA para reprodução de áudio com recursos adicionais.
"""

import os
import logging
import threading
import queue
import time
from typing import Optional, Callable # Removed Dict, Any, List, Union as they were not used in type hints here after review

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AudioPlaybackManager:
    """
    Gerenciador avançado de playback de áudio com fila e controles.
    """
    
    def __init__(self, audio_dir: str = None):
        """
        Inicializa o gerenciador de playback.
        
        Args:
            audio_dir: Diretório para armazenar arquivos de áudio (None = usar temporário)
        """
        self.audio_dir = audio_dir or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data", "audio"
        )
        
        # Criar diretório se não existir
        os.makedirs(self.audio_dir, exist_ok=True)
        
        # Fila de reprodução
        self.playback_queue = queue.Queue()
        
        # Estado
        self.is_playing = False
        self.current_audio = None
        self.should_stop = False
        self.paused = False
        self.volume = 1.0
        
        # Posição para sounddevice, será reinicializado por play
        self._sd_position = 0
        
        # Inicializar thread de reprodução
        self.playback_thread = threading.Thread(target=self._playback_worker)
        self.playback_thread.daemon = True
        self.playback_thread.start()
        
        # Callbacks
        self.on_start_callback = None
        self.on_complete_callback = None
        
        logger.info(f"Gerenciador de playback inicializado: {self.audio_dir}")
        
        # Inicializar bibliotecas de áudio
        self._init_audio_libraries()

    def set_on_start_callback(self, callback: Optional[Callable]):
        """
        Define uma função de callback para ser chamada quando o áudio começar a tocar.
        
        Args:
            callback: função que será executada no início do áudio (recebe audio_path)
        """
        self.on_start_callback = callback

    def set_on_complete_callback(self, callback: Optional[Callable]):
        """
        Define uma função de callback para ser chamada quando o áudio terminar de tocar.
        
        Args:
            callback: função que será executada no final do áudio (recebe audio_path)
        """
        self.on_complete_callback = callback
    
    def _init_audio_libraries(self) -> None:
        """
        Inicializa as bibliotecas de áudio disponíveis.
        """
        self.pygame_available = False
        self.pydub_available = False
        self.sounddevice_available = False
        
        # Tentar inicializar pygame
        try:
            import pygame
            pygame.mixer.init()
            self.pygame_available = True
            logger.info("Biblioteca pygame inicializada")
        except ImportError: # ModuleNotFoundError is a subclass of ImportError
            logger.debug("Biblioteca pygame não disponível")
        except Exception as e:
            logger.warning(f"Erro ao inicializar pygame: {e}")
        
        # Verificar pydub
        try:
            import pydub
            self.pydub_available = True
            logger.info("Biblioteca pydub disponível")
        except ImportError:
            logger.debug("Biblioteca pydub não disponível")
        
        # Verificar sounddevice
        try:
            import sounddevice # soundfile will be needed by _play_with_sounddevice
            import soundfile # Explicitly check for soundfile as well
            self.sounddevice_available = True
            logger.info("Biblioteca sounddevice e soundfile disponíveis")
        except ImportError:
            logger.debug("Biblioteca sounddevice ou soundfile não disponível")
        
        if not any([self.pygame_available, self.pydub_available, self.sounddevice_available]):
            logger.warning("Nenhuma biblioteca de áudio disponível. Instale pygame, ou pydub, ou sounddevice e soundfile.")
    
    def _playback_worker(self) -> None:
        """
        Worker thread para reprodução de áudio da fila.
        """
        while True:
            try:
                audio_item = self.playback_queue.get()
                
                if audio_item is None:
                    break
                
                audio_path = audio_item.get("path")
                specific_callback = audio_item.get("callback")
                
                if not os.path.exists(audio_path):
                    logger.error(f"Arquivo de áudio não encontrado: {audio_path}")
                    if specific_callback:
                        try:
                            specific_callback(audio_path, "error", "File not found")
                        except Exception as cb_e:
                            logger.error(f"Erro ao executar callback específico (file not found): {cb_e}")
                    self.playback_queue.task_done()
                    continue
                
                self.current_audio = audio_path
                self.is_playing = True
                self.should_stop = False
                self.paused = False
                
                if self.on_start_callback:
                    try:
                        self.on_start_callback(audio_path)
                    except Exception as cb_e:
                        logger.error(f"Erro ao executar on_start_callback: {cb_e}")
                
                if specific_callback:
                    try:
                        specific_callback(audio_path, "start")
                    except Exception as cb_e:
                        logger.error(f"Erro ao executar callback específico (start): {cb_e}")
                
                logger.debug(f"Reproduzindo: {audio_path}")
                
                self._play_audio_file(audio_path)
                
                if not self.should_stop:
                    if self.on_complete_callback:
                        try:
                            self.on_complete_callback(audio_path)
                        except Exception as cb_e:
                            logger.error(f"Erro ao executar on_complete_callback: {cb_e}")
                    
                    if specific_callback:
                        try:
                            specific_callback(audio_path, "complete")
                        except Exception as cb_e:
                            logger.error(f"Erro ao executar callback específico (complete): {cb_e}")
                else: # Playback was stopped
                    if specific_callback:
                        try:
                            specific_callback(audio_path, "stopped")
                        except Exception as cb_e:
                            logger.error(f"Erro ao executar callback específico (stopped): {cb_e}")

                self.current_audio = None
                self.is_playing = False
                # self.should_stop is reset at the start of playing new audio
                # self.paused is reset at the start of playing new audio
                
                self.playback_queue.task_done()
                
            except Exception as e:
                logger.error(f"Erro no worker de playback: {e}", exc_info=True)
                self.is_playing = False
                self.current_audio = None
                # Ensure task_done is called even if an unexpected error occurs before it.
                # However, if audio_item was None or get() failed, task_done might not be appropriate.
                # The current structure calls task_done within the happy path or known error paths.
                # If an error happens after get() but before task_done(), it needs to be handled.
                # Adding a check if the item was successfully retrieved before calling task_done in exception.
                if 'audio_item' in locals() and audio_item is not None:
                    try:
                        self.playback_queue.task_done()
                    except ValueError: # if task_done called too many times
                        logger.warning("Tentativa de chamar task_done() em erro, mas a tarefa já pode ter sido marcada como concluída.")
                    except Exception as td_e:
                         logger.error(f"Erro ao chamar task_done() no manipulador de exceção do worker: {td_e}")

    def _play_audio_file(self, audio_path: str) -> None:
        """
        Reproduz um arquivo de áudio usando a biblioteca disponível.
        
        Args:
            audio_path: Caminho para o arquivo de áudio
        """
        if self.pygame_available:
            self._play_with_pygame(audio_path)
            return
        
        if self.pydub_available:
            self._play_with_pydub(audio_path)
            return
        
        if self.sounddevice_available:
            self._play_with_sounddevice(audio_path)
            return
        
        logger.error("Nenhuma biblioteca de áudio disponível para reprodução")
    
    def _play_with_pygame(self, audio_path: str) -> None:
        """
        Reproduz áudio usando pygame.
        
        Args:
            audio_path: Caminho para o arquivo de áudio
        """
        import pygame # Import here to ensure it's only accessed if available
        
        try:
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy() and not self.should_stop:
                if self.paused:
                    # pygame.mixer.music.pause() # Already called by self.pause()
                    while self.paused and not self.should_stop:
                        time.sleep(0.1)
                    if not self.should_stop and not self.paused: # Check if pause state changed by resume()
                        pass # pygame.mixer.music.unpause() # Already called by self.resume()
                    elif self.should_stop: # If stopped while paused
                        break 
                
                pygame.time.Clock().tick(10)
            
            # If loop exited due to should_stop, ensure music is stopped
            # If music finished naturally, get_busy() is false, no need to stop again.
            # If should_stop became true, self.stop() already called pygame.mixer.music.stop().
            # This explicit stop here might be redundant if self.stop() is always the source of should_stop.
            # However, if should_stop could be set by other means or if there's a race, it's a safeguard.
            if self.should_stop:
                if pygame.mixer.music.get_busy(): # Check if it's still busy before stopping
                    pygame.mixer.music.stop()
                
        except Exception as e:
            logger.error(f"Erro ao reproduzir com pygame: {e}")
    
    def _play_with_pydub(self, audio_path: str) -> None:
        """
        Reproduz áudio usando pydub.
        
        Args:
            audio_path: Caminho para o arquivo de áudio
        """
        from pydub import AudioSegment
        from pydub.playback import play
        
        try:
            sound = AudioSegment.from_file(audio_path)
            
            if self.volume == 0.0: # Handle true silence for pydub
                # Play a very short silent segment or just wait for the duration
                # For simplicity, we can just loop and sleep if volume is zero.
                duration_s = len(sound) / 1000.0
                start_time = time.time()
                while time.time() - start_time < duration_s and not self.should_stop:
                    time.sleep(0.1) # Check for stop/pause
                    while self.paused and not self.should_stop:
                        time.sleep(0.1)
                return

            # Adjust volume (pydub uses dB)
            # A volume of 1.0 is 0dB (no change). A volume of 0.0 could be -infinity dB.
            # The original formula 20 * (self.volume - 1) gives -20dB for volume=0.
            # For a more intuitive linear volume to dB, gain = 20 * log10(self.volume) if volume > 0
            # Or simply: sound_to_play = sound - (60 * (1.0 - self.volume)) # e.g. 0dB at 1.0, -60dB at 0.0
            # Keeping original approach for now as it's not a bug, just a characteristic.
            # However, for pydub, applying gain might change duration slightly if not careful.
            # A common way is sound + gain_in_db.
            # gain = 0
            # if self.volume < 1.0 and self.volume > 0: # Avoid log(0)
            #     gain = 20 * math.log10(self.volume)
            # elif self.volume == 0: # Effectively mute for pydub
            #     # This case is handled above now
            #     pass 
            # sound_to_play = sound + gain

            # Using the original gain logic as it was specified implicitly:
            if self.volume != 1.0:
                 # Convert linear volume (0-1) to dB adjustment.
                 # volume = 0.5 -> -6dB (half perceived loudness approx)
                 # volume = 0.1 -> -20dB
                 # Avoid log(0) if self.volume is 0.
                if self.volume > 0:
                    # A common formula for linear perceived loudness to dB is:
                    # gain_db = 20 * math.log10(self.volume)
                    # However, pydub's apply_gain might not be what we want here.
                    # Let's use the simpler: sound_to_play = sound + db_change
                    # For volume 0.5, -6dB; for 0.25, -12dB
                    # db = 10 * math.log10(self.volume ** 2)  # Power ratio
                    # Let's stick to a simple modification of the original gain logic for less drastic changes
                    # and to avoid math import if not strictly necessary.
                    # The original gain method for pydub: sound.apply_gain(20 * (self.volume - 1))
                    # For volume = 0.5, gain is -10. For volume = 0, gain is -20.
                    # This is a valid approach, just note it's not linear perceptual loudness.
                    sound = sound.apply_gain(20 * (self.volume - 1.0))


            # Play with control manual
            chunk_size_ms = 100  # ms
            
            played_ms = 0
            while played_ms < len(sound):
                if self.should_stop:
                    break
                
                while self.paused and not self.should_stop:
                    time.sleep(0.1)
                
                if self.should_stop: # Re-check after pause
                    break

                chunk = sound[played_ms : played_ms + chunk_size_ms]
                play(chunk) # This is blocking for the chunk duration
                played_ms += chunk_size_ms
                
        except Exception as e:
            logger.error(f"Erro ao reproduzir com pydub: {e}")
    
    def _play_with_sounddevice(self, audio_path: str) -> None:
        """
        Reproduz áudio usando sounddevice.
        
        Args:
            audio_path: Caminho para o arquivo de áudio
        """
        import sounddevice as sd
        import soundfile as sf
        
        try:
            data, samplerate = sf.read(audio_path, dtype='float32')
            
            # Reset position for the current file
            self._sd_position = 0 
            
            current_frame = 0

            def sd_callback(outdata, frames, time_info, status):
                nonlocal current_frame # Use nonlocal to modify outer scope variable
                if status:
                    logger.warning(f"Status sounddevice: {status}")
                
                if self.paused or self.should_stop:
                    outdata.fill(0)
                    return

                chunk_end = current_frame + frames
                remaining_frames_in_file = len(data) - current_frame

                if remaining_frames_in_file <= 0:
                    outdata.fill(0)
                    # Optional: raise sd.CallbackStop() if we want to signal end of stream this way
                    # However, the main loop below will also detect completion.
                    return

                valid_frames_to_write = min(frames, remaining_frames_in_file)
                
                # Apply volume directly to the data chunk being sent
                audio_chunk = data[current_frame : current_frame + valid_frames_to_write] * self.volume
                
                outdata[:valid_frames_to_write] = audio_chunk
                
                # If fewer frames were written than requested, fill the rest with silence
                if valid_frames_to_write < frames:
                    outdata[valid_frames_to_write:].fill(0)
                
                current_frame += valid_frames_to_write
                self._sd_position = current_frame # Keep self._sd_position updated for external checks if needed

            channels = data.shape[1] if data.ndim > 1 else 1
            
            stream = sd.OutputStream(
                samplerate=samplerate,
                channels=channels,
                callback=sd_callback,
                blocksize=1024 # Or another suitable blocksize, 0 means device preferred
            )
            
            with stream:
                while not self.should_stop and current_frame < len(data):
                    if self.paused:
                        # While paused, the callback itself handles silence.
                        # We just need to wait here without consuming CPU heavily.
                        time.sleep(0.1) 
                    else:
                        # Stream is active, callback is feeding data.
                        # Sleep to allow other threads and to check for stop/pause.
                        time.sleep(0.1) 
                
                # If stopped, the stream will be closed by the 'with' statement.
                # Callback will serve silence if self.should_stop is true.
                
        except Exception as e:
            logger.error(f"Erro ao reproduzir com sounddevice: {e}", exc_info=True)

    # _sd_callback is now an inner function within _play_with_sounddevice
    # def _sd_callback(self, outdata, frames, time, status, data_ref): ...
    
    def play(self, 
             audio_path: str, 
             callback: Optional[Callable] = None) -> bool:
        """
        Adiciona um áudio à fila de reprodução.
        
        Args:
            audio_path: Caminho para o arquivo de áudio
            callback: Função a ser chamada (path, event_type, details=None)
                      event_type: "start", "complete", "error", "stopped"
            
        Returns:
            True se o áudio foi adicionado à fila
        """
        if not os.path.isabs(audio_path): # Best to work with absolute paths
            audio_path = os.path.abspath(audio_path)

        if not os.path.exists(audio_path):
            logger.error(f"Arquivo de áudio não encontrado: {audio_path}")
            if callback:
                try:
                    callback(audio_path, "error", "File not found")
                except Exception as cb_e:
                    logger.error(f"Erro ao executar callback (file not found): {cb_e}")
            return False
        
        try:
            self.playback_queue.put({
                "path": audio_path,
                "callback": callback
            })
            
            logger.debug(f"Áudio adicionado à fila: {audio_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao adicionar áudio à fila: {e}")
            return False
    
    def play_now(self, 
                 audio_path: str, 
                 callback: Optional[Callable] = None) -> bool:
        """
        Interrompe a reprodução atual e reproduz um áudio imediatamente.
        
        Args:
            audio_path: Caminho para o arquivo de áudio
            callback: Função a ser chamada (ver play())
            
        Returns:
            True se o áudio foi adicionado à fila
        """
        if not os.path.isabs(audio_path):
             audio_path = os.path.abspath(audio_path)

        if not os.path.exists(audio_path):
            logger.error(f"Arquivo de áudio não encontrado: {audio_path}")
            if callback:
                try:
                    callback(audio_path, "error", "File not found")
                except Exception as cb_e:
                    logger.error(f"Erro ao executar callback (file not found): {cb_e}")
            return False
        
        try:
            logger.debug("Interrompendo áudio atual e limpando fila para play_now...")
            self.stop() # Signal current playback to stop
            
            # Wait briefly for the current audio to acknowledge stop and worker to finish
            # This is a bit tricky; ideally, stop() would be synchronous or provide a future.
            # For now, a small sleep might help, but not guaranteed.
            # time.sleep(0.2) # Short delay

            self.clear_queue() # Clear any pending items

            # The worker thread might still be finishing the previous track or in its stop logic.
            # Putting a new item immediately is generally fine as the worker loop will pick it up next.
            
            self.playback_queue.put({
                "path": audio_path,
                "callback": callback
            })
            
            logger.debug(f"Áudio para reprodução imediata adicionado: {audio_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao reproduzir áudio imediatamente: {e}")
            return False
    
    def stop(self) -> None:
        """
        Para a reprodução atual.
        """
        if self.is_playing: # Only act if something is considered playing by the manager
            self.should_stop = True # Signal all playback loops to stop
            
            # Specific stop for pygame if it's the active player.
            # Pygame's music module has its own state.
            if self.pygame_available:
                try:
                    import pygame
                    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                except Exception as e: # Catch pygame-specific errors
                    logger.warning(f"Erro ao tentar parar pygame explicitamente: {e}")
            
            # For pydub and sounddevice, the should_stop flag is primary.
            # If they are in a paused state, setting should_stop will break their loops.
            if self.paused: # If paused, wake up any sleeps to ensure quick stop
                self.paused = False # This will unblock pause loops

            logger.debug("Sinal de interrupção enviado para a reprodução atual.")
        else:
            logger.debug("Nenhum áudio tocando para interromper.")
            # Ensure should_stop is true even if is_playing was false, to prevent race conditions
            # where is_playing might flip after the check but before should_stop is set.
            self.should_stop = True 


    def pause(self) -> None:
        """
        Pausa a reprodução atual.
        """
        if self.is_playing and not self.paused:
            self.paused = True
            if self.pygame_available:
                try:
                    import pygame
                    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                except Exception as e:
                     logger.warning(f"Erro ao tentar pausar pygame: {e}")
            logger.debug("Reprodução pausada")
    
    def resume(self) -> None:
        """
        Retoma a reprodução pausada.
        """
        if self.is_playing and self.paused:
            self.paused = False # Set this first
            if self.pygame_available:
                try:
                    import pygame
                    if pygame.mixer.get_init(): # No need to check get_busy for unpause
                         pygame.mixer.music.unpause()
                except Exception as e:
                    logger.warning(f"Erro ao tentar retomar pygame: {e}")
            logger.debug("Reprodução retomada")
    
    def set_volume(self, volume: float) -> None:
        """
        Define o volume de reprodução.
        
        Args:
            volume: Nível de volume (0.0 a 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))
        
        if self.pygame_available:
            try:
                import pygame
                if pygame.mixer.get_init():
                    pygame.mixer.music.set_volume(self.volume)
            except Exception as e:
                 logger.warning(f"Erro ao definir volume do pygame: {e}")
        
        logger.debug(f"Volume definido para: {self.volume}")
    
    def get_volume(self) -> float:
        """
        Obtém o volume atual.
        
        Returns:
            Nível de volume atual
        """
        return self.volume
    
    def clear_queue(self) -> None:
        """
        Limpa a fila de reprodução.
        Não para o áudio atual.
        """
        try:
            while not self.playback_queue.empty():
                try:
                    self.playback_queue.get_nowait()
                    self.playback_queue.task_done()
                except queue.Empty:
                    break 
                except Exception as e_get:
                    logger.error(f"Erro ao obter item da fila durante a limpeza: {e_get}")
                    break # Avoid potential infinite loop if task_done fails unexpectedly
            
            logger.debug("Fila de reprodução limpa")
            
        except Exception as e:
            logger.error(f"Erro ao limpar fila de reprodução: {e}")
    
    def is_busy(self) -> bool:
        """
        Verifica se há áudio na fila ou sendo reproduzido ativamente.
        """
        return self.is_playing or not self.playback_queue.empty()

    def shutdown(self, wait_for_queue: bool = False) -> None:
        """
        Encerra o gerenciador de áudio.
        Para o áudio atual, opcionalmente aguarda a fila e para a thread worker.
        """
        logger.info("Iniciando encerramento do AudioPlaybackManager...")
        self.stop() # Para o áudio atual

        if wait_for_queue:
            logger.info("Aguardando a conclusão da fila de reprodução...")
            self.playback_queue.join() # Espera que todos os itens sejam processados (se não limpos)
        else:
            self.clear_queue() # Limpa a fila se não for para esperar

        # Envia sinal de término para o worker
        self.playback_queue.put(None)
        
        if self.playback_thread.is_alive():
            logger.info("Aguardando a thread de playback finalizar...")
            self.playback_thread.join(timeout=5.0) # Espera pela thread com timeout
            if self.playback_thread.is_alive():
                logger.warning("Thread de playback não finalizou no tempo esperado.")

        # Desinicializar Pygame Mixer se foi inicializado
        if self.pygame_available:
            try:
                import pygame
                if pygame.mixer.get_init():
                    pygame.mixer.quit()
                # pygame.quit() # Se pygame geral foi inicializado, mas aqui só o mixer
                logger.info("Pygame mixer desinicializado.")
            except Exception as e:
                logger.warning(f"Erro ao desinicializar pygame mixer: {e}")
        
        logger.info("AudioPlaybackManager encerrado.")

# Exemplo de uso (opcional, para teste)
if __name__ == '__main__':
    # Criar um diretório de áudio de teste e um arquivo de áudio dummy
    test_audio_dir = os.path.join(os.path.dirname(__file__), "test_audio_data")
    os.makedirs(test_audio_dir, exist_ok=True)
    
    # Você precisará de um arquivo de áudio real (ex: .wav, .mp3) para testar.
    # Crie um arquivo dummy se soundfile e numpy estiverem disponíveis:
    dummy_audio_file = os.path.join(test_audio_dir, "dummy_sound.wav")
    
    try:
        import soundfile as sf
        import numpy as np
        samplerate = 44100
        duration = 1 # seconds
        frequency = 440 # Hz (A4 note)
        amplitude = 0.5
        t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
        wave_data = amplitude * np.sin(2 * np.pi * frequency * t)
        # Ensure stereo if sounddevice callback expects it, or mono
        # wave_data_stereo = np.array([wave_data, wave_data]).T # For stereo
        sf.write(dummy_audio_file, wave_data, samplerate)
        print(f"Arquivo de áudio dummy criado em: {dummy_audio_file}")
        has_dummy_file = True
    except ImportError:
        print("soundfile ou numpy não instalados. Não foi possível criar arquivo de áudio dummy.")
        print(f"Por favor, crie um arquivo de áudio em '{dummy_audio_file}' manualmente para testar.")
        has_dummy_file = False
    except Exception as e:
        print(f"Erro ao criar arquivo de áudio dummy: {e}")
        has_dummy_file = False

    # --- Callbacks de Exemplo ---
    def generic_audio_event_callback(audio_path, event_type, details=None):
        print(f"[Callback Genérico] Áudio: {os.path.basename(audio_path)}, Evento: {event_type}, Detalhes: {details or ''}")

    def specific_track_callback(audio_path, event_type, details=None):
        print(f"[Callback Específico] Áudio: {os.path.basename(audio_path)}, Evento: {event_type}, Detalhes: {details or ''}")

    manager = AudioPlaybackManager(audio_dir=test_audio_dir)
    manager.set_on_start_callback(lambda path: generic_audio_event_callback(path, "manager_start"))
    manager.set_on_complete_callback(lambda path: generic_audio_event_callback(path, "manager_complete"))
    manager.set_volume(0.5)

    if has_dummy_file:
        print(f"Testando com: {dummy_audio_file}")
        manager.play(dummy_audio_file, callback=specific_track_callback)
        # Adicionar outro para testar a fila
        manager.play(dummy_audio_file, callback=lambda p, e, d: print(f"Track 2: {e}"))

        print("Áudios adicionados à fila. Esperando 5 segundos...")
        time.sleep(1) # Dê tempo para o primeiro começar
        
        if manager.is_playing:
            print("Pausando em 1 segundo...")
            time.sleep(1)
            manager.pause()
            print("Pausado. Esperando 1 segundo...")
            time.sleep(1)
            print("Retomando...")
            manager.resume()

        time.sleep(4) # Deixe tocar mais um pouco

        # Teste play_now
        print("Testando play_now...")
        another_dummy_file = os.path.join(test_audio_dir, "another_dummy.wav")
        try:
            # Create slightly different dummy file
            sf.write(another_dummy_file, amplitude * np.sin(2 * np.pi * (frequency * 1.5) * t), samplerate)
            manager.play_now(another_dummy_file, callback=lambda p, e, d: print(f"PlayNow Track: {e}"))
            print(f"PlayNow com {another_dummy_file}. Esperando 3 segundos...")
            time.sleep(3)
        except NameError: # sf not defined
            print("Não foi possível criar 'another_dummy.wav' para testar play_now.")
        except Exception as e:
            print(f"Erro ao criar 'another_dummy.wav': {e}")


        print("Testando stop...")
        manager.stop()
        print("Playback interrompido.")
        time.sleep(1)

    else:
        print("Nenhum arquivo de áudio para testar.")

    print("Aguardando finalização da fila antes de encerrar (se houver algo)...")
    manager.shutdown(wait_for_queue=True)
    print("Teste concluído.")