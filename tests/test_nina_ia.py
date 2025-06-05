"""
Script de teste para o sistema Nina IA.
Verifica a funcionalidade de todos os componentes integrados.
"""

import os
import time
import unittest
import logging
from unittest.mock import MagicMock, patch

# Ajustar o caminho para importações relativas
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar logging para testes
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class TestNinaIA(unittest.TestCase):
    """
    Testes para o sistema Nina IA completo.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Configuração inicial para todos os testes.
        """
        # Criar diretório temporário para testes
        import tempfile
        cls.test_dir = tempfile.mkdtemp(prefix="nina_test_")
        logger.info(f"Diretório de teste criado: {cls.test_dir}")
        
        # Criar subdiretórios necessários
        os.makedirs(os.path.join(cls.test_dir, "profiles"), exist_ok=True)
        os.makedirs(os.path.join(cls.test_dir, "memory"), exist_ok=True)
        os.makedirs(os.path.join(cls.test_dir, "audio"), exist_ok=True)
    
    @classmethod
    def tearDownClass(cls):
        """
        Limpeza após todos os testes.
        """
        # Remover diretório temporário
        import shutil
        try:
            shutil.rmtree(cls.test_dir)
            logger.info(f"Diretório de teste removido: {cls.test_dir}")
        except Exception as e:
            logger.error(f"Erro ao remover diretório de teste: {e}")
    
    def setUp(self):
        """
        Configuração para cada teste individual.
        """
        # Criar perfil de teste
        self.create_test_profile()
    
    def create_test_profile(self):
        """
        Cria um perfil de teste para os testes.
        """
        import json
        
        profile_path = os.path.join(self.test_dir, "profiles", "test_profile.json")
        
        profile_data = {
            "name": "TestNina",
            "version": "1.0.0",
            "created_at": "2025-04-24T17:19:00.000Z",
            "updated_at": "2025-04-24T17:19:00.000Z",
            "personality": {
                "speech_style": "amigável",
                "mood": "neutro",
                "preferences": ["tecnologia", "testes"],
                "description": "Assistente de IA para testes"
            },
            "voice": {
                "model": "tts_models/pt/cv/vits",
                "speaker": None,
                "language": "pt",
                "speed": 1.0,
                "pitch": 1.0
            },
            "llm": {
                "model": "mistral",
                "temperature": 0.7,
                "max_tokens": 500
            },
            "stt": {
                "model": "base",
                "language": "pt"
            },
            "interface": {
                "theme": "dark",
                "wake_word": "Nina",
                "response_format": "voice_and_text"
            }
        }
        
        with open(profile_path, 'w', encoding='utf-8') as f:
            json.dump(profile_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Perfil de teste criado: {profile_path}")
    
    @patch('stt.stt_module.STTModule')
    @patch('llm.llm_module.LLMModule')
    @patch('tts.tts_module.TTSModule')
    def test_orchestrator_initialization(self, mock_tts, mock_llm, mock_stt):
        """
        Testa a inicialização do orquestrador.
        """
        from core.orchestrator import NinaOrchestrator
        
        # Configurar mocks
        mock_stt.return_value = MagicMock()
        mock_llm.return_value = MagicMock()
        mock_tts.return_value = MagicMock()
        
        # Inicializar orquestrador
        orchestrator = NinaOrchestrator(
            data_dir=self.test_dir,
            profile_name="test_profile",
            use_cuda=False
        )
        
        # Verificar se os componentes foram inicializados
        self.assertIsNotNone(orchestrator.stt)
        self.assertIsNotNone(orchestrator.llm)
        self.assertIsNotNone(orchestrator.tts)
        self.assertIsNotNone(orchestrator.profiles_manager)
        self.assertIsNotNone(orchestrator.session_manager)
        
        # Verificar se o perfil foi carregado
        self.assertEqual(orchestrator.profile_name, "test_profile")
        
        # Verificar se uma sessão foi criada
        self.assertIsNotNone(orchestrator.active_session_id)
    
    @patch('core.orchestrator.NinaOrchestrator')
    @patch('core.audio_playback.AudioPlaybackManager')
    def test_nina_ia_initialization(self, mock_playback, mock_orchestrator):
        """
        Testa a inicialização da classe principal NinaIA.
        """
        from interface.nina_ia import NinaIA
        
        # Configurar mocks
        mock_orchestrator.return_value = MagicMock()
        mock_playback.return_value = MagicMock()
        
        # Inicializar Nina IA
        nina = NinaIA(
            data_dir=self.test_dir,
            profile_name="test_profile",
            use_cuda=False,
            debug=True
        )
        
        # Verificar se os componentes foram inicializados
        self.assertIsNotNone(nina.orchestrator)
        self.assertIsNotNone(nina.playback_manager)
        
        # Verificar estado inicial
        self.assertFalse(nina.running)
        self.assertFalse(nina.continuous_mode)
    
    @patch('core.orchestrator.NinaOrchestrator')
    @patch('core.audio_playback.AudioPlaybackManager')
    def test_process_text_command(self, mock_playback, mock_orchestrator):
        """
        Testa o processamento de comandos de texto.
        """
        from interface.nina_ia import NinaIA
        
        # Configurar mocks
        mock_orch = MagicMock()
        mock_orch.process_text_input.return_value = "Resposta de teste"
        mock_orch.tts.speak.return_value = "/tmp/test_audio.wav"
        
        mock_orchestrator.return_value = mock_orch
        mock_playback.return_value = MagicMock()
        
        # Inicializar Nina IA
        nina = NinaIA(
            data_dir=self.test_dir,
            profile_name="test_profile",
            use_cuda=False
        )
        
        # Processar comando de texto
        response = nina.process_text_command("Olá, como você está?")
        
        # Verificar se o comando foi processado
        mock_orch.process_text_input.assert_called_once_with("Olá, como você está?")
        
        # Verificar se a resposta foi sintetizada
        mock_orch.tts.speak.assert_called_once()
        
        # Verificar se o áudio foi reproduzido
        nina.playback_manager.play.assert_called_once()
        
        # Verificar resposta
        self.assertEqual(response, "Resposta de teste")
    
    @patch('core.orchestrator.NinaOrchestrator')
    @patch('core.audio_playback.AudioPlaybackManager')
    def test_process_voice_command(self, mock_playback, mock_orchestrator):
        """
        Testa o processamento de comandos de voz.
        """
        from interface.nina_ia import NinaIA
        
        # Configurar mocks
        mock_orch = MagicMock()
        mock_orch.process_voice_input.return_value = "Comando de voz"
        mock_orch.process_text_input.return_value = "Resposta ao comando de voz"
        mock_orch.tts.speak.return_value = "/tmp/test_audio.wav"
        
        mock_orchestrator.return_value = mock_orch
        mock_playback.return_value = MagicMock()
        
        # Inicializar Nina IA
        nina = NinaIA(
            data_dir=self.test_dir,
            profile_name="test_profile",
            use_cuda=False
        )
        
        # Processar comando de voz
        response = nina.process_voice_command()
        
        # Verificar se o áudio foi capturado e transcrito
        mock_orch.process_voice_input.assert_called_once()
        
        # Verificar se o texto transcrito foi processado
        mock_orch.process_text_input.assert_called_once_with("Comando de voz")
        
        # Verificar se a resposta foi sintetizada
        mock_orch.tts.speak.assert_called_once()
        
        # Verificar se o áudio foi reproduzido
        nina.playback_manager.play.assert_called_once()
        
        # Verificar resposta
        self.assertEqual(response, "Resposta ao comando de voz")
    
    @patch('core.orchestrator.NinaOrchestrator')
    @patch('core.audio_playback.AudioPlaybackManager')
    def test_continuous_mode(self, mock_playback, mock_orchestrator):
        """
        Testa o modo contínuo de interação.
        """
        from interface.nina_ia import NinaIA
        import threading
        
        # Configurar mocks
        mock_orch = MagicMock()
        mock_orch.speak_response.return_value = True
        
        mock_orchestrator.return_value = mock_orch
        mock_playback.return_value = MagicMock()
        
        # Inicializar Nina IA
        nina = NinaIA(
            data_dir=self.test_dir,
            profile_name="test_profile",
            use_cuda=False
        )
        
        # Iniciar modo contínuo
        nina.start_continuous_mode()
        
        # Verificar se o modo contínuo foi iniciado
        self.assertTrue(nina.continuous_mode)
        self.assertTrue(nina.running)
        
        # Verificar se a mensagem de boas-vindas foi falada
        mock_orch.speak_response.assert_called_once()
        
        # Aguardar um pouco para o thread iniciar
        time.sleep(0.5)
        
        # Verificar se o thread está em execução
        self.assertTrue(hasattr(nina, 'interaction_thread'))
        self.assertTrue(nina.interaction_thread.is_alive())
        
        # Parar modo contínuo
        nina.stop_continuous_mode()
        
        # Verificar se o modo contínuo foi parado
        self.assertFalse(nina.continuous_mode)
        
        # Verificar se o orquestrador foi parado
        mock_orch.stop_continuous_interaction.assert_called_once()
        
        # Verificar se o playback foi parado
        mock_playback.return_value.stop.assert_called_once()
    
    @patch('core.orchestrator.NinaOrchestrator')
    @patch('core.audio_playback.AudioPlaybackManager')
    def test_change_profile(self, mock_playback, mock_orchestrator):
        """
        Testa a mudança de perfil.
        """
        from interface.nina_ia import NinaIA
        
        # Configurar mocks
        mock_orch = MagicMock()
        mock_orch.change_profile.return_value = True
        
        mock_orchestrator.return_value = mock_orch
        mock_playback.return_value = MagicMock()
        
        # Inicializar Nina IA
        nina = NinaIA(
            data_dir=self.test_dir,
            profile_name="test_profile",
            use_cuda=False
        )
        
        # Mudar perfil
        result = nina.change_profile("new_profile")
        
        # Verificar se o perfil foi alterado
        self.assertTrue(result)
        mock_orch.change_profile.assert_called_once_with("new_profile")
        self.assertEqual(nina.profile_name, "new_profile")
    
    @patch('core.orchestrator.NinaOrchestrator')
    @patch('core.audio_playback.AudioPlaybackManager')
    def test_set_volume(self, mock_playback, mock_orchestrator):
        """
        Testa a configuração de volume.
        """
        from interface.nina_ia import NinaIA
        
        # Configurar mocks
        mock_orchestrator.return_value = MagicMock()
        mock_playback.return_value = MagicMock()
        
        # Inicializar Nina IA
        nina = NinaIA(
            data_dir=self.test_dir,
            profile_name="test_profile",
            use_cuda=False
        )
        
        # Definir volume
        nina.set_volume(0.8)
        
        # Verificar se o volume foi alterado
        nina.playback_manager.set_volume.assert_called_once_with(0.8)
    
    @patch('core.orchestrator.NinaOrchestrator')
    @patch('core.audio_playback.AudioPlaybackManager')
    def test_shutdown(self, mock_playback, mock_orchestrator):
        """
        Testa o encerramento do sistema.
        """
        from interface.nina_ia import NinaIA
        
        # Configurar mocks
        mock_orchestrator.return_value = MagicMock()
        mock_playback.return_value = MagicMock()
        
        # Inicializar Nina IA
        nina = NinaIA(
            data_dir=self.test_dir,
            profile_name="test_profile",
            use_cuda=False
        )
        
        # Iniciar modo contínuo para testar encerramento completo
        nina.continuous_mode = True
        nina.running = True
        
        # Encerrar sistema
        nina.shutdown()
        
        # Verificar se o sistema foi encerrado
        self.assertFalse(nina.running)
        self.assertFalse(nina.continuous_mode)
        
        # Verificar se o playback foi encerrado
        nina.playback_manager.shutdown.assert_called_once()


if __name__ == "__main__":
    unittest.main()
