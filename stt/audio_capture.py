"""
Módulo para captura de áudio do microfone.
Parte do projeto Nina IA para captura de entrada de voz.
"""

import os
import wave
import tempfile
import sounddevice as sd
import soundfile as sf
import numpy as np
from typing import Optional, Tuple, Union

class AudioCapture:
    """
    Classe para captura de áudio do microfone e gravação em arquivo.
    """
    
    def __init__(self, 
                 sample_rate: int = 16000, 
                 channels: int = 1,
                 device: Optional[int] = None):
        """
        Inicializa o capturador de áudio.
        
        Args:
            sample_rate: Taxa de amostragem em Hz (padrão: 16000)
            channels: Número de canais (padrão: 1 - mono)
            device: ID do dispositivo de áudio (padrão: None - dispositivo padrão)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.device = device
        self.recording = False
        self.audio_data = None
        
    def list_devices(self) -> None:
        """
        Lista todos os dispositivos de áudio disponíveis.
        """
        devices = sd.query_devices()
        print("Dispositivos de áudio disponíveis:")
        for i, device in enumerate(devices):
            print(f"{i}: {device['name']} (Entradas: {device['max_input_channels']}, Saídas: {device['max_output_channels']})")
    
    def start_recording(self, duration: Optional[float] = None) -> None:
        """
        Inicia a gravação de áudio.
        
        Args:
            duration: Duração da gravação em segundos (None para gravação contínua)
        """
        self.recording = True
        self.audio_data = sd.rec(
            int(duration * self.sample_rate) if duration else None,
            samplerate=self.sample_rate,
            channels=self.channels,
            device=self.device,
            blocking=False
        )
        
        if duration:
            sd.sleep(int(duration * 1000))
            self.stop_recording()
    
    def stop_recording(self) -> np.ndarray:
        """
        Para a gravação de áudio.
        
        Returns:
            Dados de áudio gravados como array numpy
        """
        if self.recording:
            sd.stop()
            self.recording = False
            return self.audio_data
        return None
    
    def record_to_file(self, 
                       file_path: str, 
                       duration: float,
                       format: str = 'wav') -> str:
        """
        Grava áudio diretamente para um arquivo.
        
        Args:
            file_path: Caminho para salvar o arquivo
            duration: Duração da gravação em segundos
            format: Formato do arquivo (padrão: 'wav')
            
        Returns:
            Caminho do arquivo gravado
        """
        print(f"Gravando áudio por {duration} segundos...")
        audio_data = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            device=self.device,
            blocking=True
        )
        
        sf.write(file_path, audio_data, self.sample_rate, format=format)
        print(f"Áudio gravado em: {file_path}")
        return file_path
    
    def record_temp_file(self, 
                         duration: float,
                         format: str = 'wav') -> str:
        """
        Grava áudio para um arquivo temporário.
        
        Args:
            duration: Duração da gravação em segundos
            format: Formato do arquivo (padrão: 'wav')
            
        Returns:
            Caminho do arquivo temporário
        """
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, f"nina_recording_{os.getpid()}.{format}")
        return self.record_to_file(temp_file, duration, format)
    
    def is_silent(self, 
                  audio_data: np.ndarray, 
                  threshold: float = 0.03) -> bool:
        """
        Verifica se o áudio está em silêncio.
        
        Args:
            audio_data: Dados de áudio como array numpy
            threshold: Limiar de amplitude para considerar como silêncio
            
        Returns:
            True se o áudio estiver em silêncio, False caso contrário
        """
        return np.max(np.abs(audio_data)) < threshold
    
    def wait_for_speech(self, 
                        timeout: float = 10.0, 
                        silence_threshold: float = 0.03,
                        check_interval: float = 0.1) -> bool:
        """
        Aguarda até detectar fala no microfone.
        
        Args:
            timeout: Tempo máximo de espera em segundos
            silence_threshold: Limiar para considerar como silêncio
            check_interval: Intervalo entre verificações em segundos
            
        Returns:
            True se detectou fala, False se atingiu timeout
        """
        elapsed = 0.0
        while elapsed < timeout:
            audio_chunk = sd.rec(
                int(check_interval * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                device=self.device,
                blocking=True
            )
            
            if not self.is_silent(audio_chunk, silence_threshold):
                return True
                
            elapsed += check_interval
            
        return False


if __name__ == "__main__":
    # Exemplo de uso
    capture = AudioCapture()
    capture.list_devices()
    
    # Gravar 5 segundos de áudio para um arquivo temporário
    temp_file = capture.record_temp_file(5.0)
    print(f"Arquivo temporário: {temp_file}")
