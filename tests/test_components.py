"""
Script de teste para componentes individuais do sistema Nina IA.
Verifica a funcionalidade de cada módulo separadamente.
"""

import os
import unittest
import logging
from unittest.mock import MagicMock, patch

# Configurar logging para testes
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Ajustar o caminho para importações relativas
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestSTTModule(unittest.TestCase):
    """
    Testes para o módulo STT (Speech to Text).
    """
    
    @patch('faster_whisper.WhisperModel')
    def test_stt_initialization(self, mock_whisper):
        """
        Testa a inicialização do módulo STT.
        """
        from stt.stt_module import STTModule
        
        # Configurar mock
        mock_whisper.return_value = MagicMock()
        
        # Inicializar módulo STT
        stt = STTModule(
            model_size="base",
            device="cpu",
            compute_type="float32",
            language="pt"
        )
        
        # Verificar se o modelo foi inicializado
        self.assertIsNotNone(stt.model)
        
        # Verificar configurações
        self.assertEqual(stt.language, "pt")
        self.assertEqual(stt.model_size, "base")
    
    @patch('faster_whisper.WhisperModel')
    @patch('stt.audio_capture.AudioCapture')
    def test_listen_and_transcribe(self, mock_capture, mock_whisper):
        """
        Testa a captura e transcrição de áudio.
        """
        from stt.stt_module import STTModule
        
        # Configurar mocks
        mock_model = MagicMock()
        mock_model.transcribe.return_value = (
            [{"text": "Texto transcrito de teste"}],
            {"language": "pt", "language_probability": 0.98}
        )
        mock_whisper.return_value = mock_model
        
        mock_capture_instance = MagicMock()
        mock_capture_instance.record_audio.return_value = ("/tmp/test_audio.wav", 3.5)
        mock_capture.return_value = mock_capture_instance
        
        # Inicializar módulo STT
        stt = STTModule(model_size="base", device="cpu")
        
        # Capturar e transcrever áudio
        text, info = stt.listen_and_transcribe()
        
        # Verificar se o áudio foi capturado
        mock_capture_instance.record_audio.assert_called_once()
        
        # Verificar se o modelo foi chamado para transcrição
        mock_model.transcribe.assert_called_once()
        
        # Verificar resultado
        self.assertEqual(text, "Texto transcrito de teste")
        self.assertIn("language", info)
        self.assertEqual(info["language"], "pt")


class TestLLMModule(unittest.TestCase):
    """
    Testes para o módulo LLM (Language Model).
    """
    
    @patch('llm.ollama_client.OllamaClient')
    def test_llm_initialization(self, mock_ollama):
        """
        Testa a inicialização do módulo LLM.
        """
        from llm.llm_module import LLMModule
        
        # Configurar mock
        mock_ollama.return_value = MagicMock()
        
        # Inicializar módulo LLM
        llm = LLMModule(
            model="mistral",
            personality_file=None,
            conversation_dir=None
        )
        
        # Verificar se o cliente Ollama foi inicializado
        self.assertIsNotNone(llm.client)
        
        # Verificar configurações
        self.assertEqual(llm.model, "mistral")
    
    @patch('llm.ollama_client.OllamaClient')
    def test_process_text(self, mock_ollama):
        """
        Testa o processamento de texto pelo LLM.
        """
        from llm.llm_module import LLMModule
        
        # Configurar mock
        mock_client = MagicMock()
        mock_client.generate.return_value = "Resposta gerada pelo modelo"
        mock_ollama.return_value = mock_client
        
        # Inicializar módulo LLM
        llm = LLMModule(model="mistral")
        
        # Processar texto
        response = llm.process_text("Olá, como você está?")
        
        # Verificar se o cliente foi chamado
        mock_client.generate.assert_called_once()
        
        # Verificar resposta
        self.assertEqual(response, "Resposta gerada pelo modelo")


class TestTTSModule(unittest.TestCase):
    """
    Testes para o módulo TTS (Text to Speech).
    """
    
    @patch('TTS.utils.synthesizer.Synthesizer')
    def test_tts_initialization(self, mock_synthesizer):
        """
        Testa a inicialização do módulo TTS.
        """
        from tts.tts_module import TTSModule
        
        # Configurar mock
        mock_synthesizer.return_value = MagicMock()
        
        # Inicializar módulo TTS
        tts = TTSModule(
            model_name="tts_models/pt/cv/vits",
            use_cuda=False
        )
        
        # Verificar se o sintetizador foi inicializado
        self.assertIsNotNone(tts.synthesizer)
    
    @patch('tts.tts_synthesizer.TTSSynthesizer')
    @patch('tts.audio_player.AudioPlayer')
    def test_speak(self, mock_player, mock_synthesizer):
        """
        Testa a síntese e reprodução de fala.
        """
        from tts.tts_module import TTSModule
        
        # Configurar mocks
        mock_synth = MagicMock()
        mock_synth.synthesize.return_value = "/tmp/test_speech.wav"
        mock_synthesizer.return_value = mock_synth
        
        mock_player_instance = MagicMock()
        mock_player.return_value = mock_player_instance
        
        # Inicializar módulo TTS
        tts = TTSModule(model_name="tts_models/pt/cv/vits", use_cuda=False)
        
        # Sintetizar e reproduzir texto
        audio_file = tts.speak("Olá, este é um teste de síntese de voz.", blocking=True)
        
        # Verificar se o sintetizador foi chamado
        mock_synth.synthesize.assert_called_once()
        
        # Verificar se o player foi chamado
        mock_player_instance.play_file.assert_called_once()
        
        # Verificar resultado
        self.assertEqual(audio_file, "/tmp/test_speech.wav")


class TestPersonalityManager(unittest.TestCase):
    """
    Testes para o gerenciador de personalidade.
    """
    
    def setUp(self):
        """
        Configuração para cada teste individual.
        """
        # Criar diretório temporário para testes
        import tempfile
        self.test_dir = tempfile.mkdtemp(prefix="nina_personality_test_")
        self.profile_path = os.path.join(self.test_dir, "test_profile.json")
    
    def tearDown(self):
        """
        Limpeza após cada teste.
        """
        # Remover diretório temporário
        import shutil
        try:
            shutil.rmtree(self.test_dir)
        except:
            pass
    
    def test_personality_initialization(self):
        """
        Testa a inicialização do gerenciador de personalidade.
        """
        from profiles.personality_manager import PersonalityManager
        
        # Inicializar gerenciador de personalidade
        manager = PersonalityManager(self.profile_path)
        
        # Verificar se o perfil padrão foi criado
        self.assertTrue(os.path.exists(self.profile_path))
        
        # Verificar se o perfil contém as seções esperadas
        profile = manager.get_profile()
        self.assertIn("name", profile)
        self.assertIn("personality", profile)
        self.assertIn("voice", profile)
        self.assertIn("llm", profile)
        self.assertIn("stt", profile)
    
    def test_update_personality(self):
        """
        Testa a atualização de personalidade.
        """
        from profiles.personality_manager import PersonalityManager
        
        # Inicializar gerenciador de personalidade
        manager = PersonalityManager(self.profile_path)
        
        # Atualizar personalidade
        new_personality = {
            "speech_style": "formal",
            "mood": "sério",
            "preferences": ["ciência", "história"],
            "description": "Assistente formal e profissional"
        }
        
        result = manager.update_personality(new_personality)
        
        # Verificar se a atualização foi bem-sucedida
        self.assertTrue(result)
        
        # Verificar se a personalidade foi atualizada
        profile = manager.get_profile()
        self.assertEqual(profile["personality"], new_personality)
    
    def test_build_system_prompt(self):
        """
        Testa a construção do prompt de sistema.
        """
        from profiles.personality_manager import PersonalityManager
        
        # Inicializar gerenciador de personalidade
        manager = PersonalityManager(self.profile_path)
        
        # Definir personalidade específica para teste
        manager.set_name("Aurora")
        manager.set_speech_style("formal")
        manager.set_mood("sério")
        
        # Construir prompt de sistema
        prompt = manager.build_system_prompt()
        
        # Verificar se o prompt contém os elementos esperados
        self.assertIn("Aurora", prompt)
        self.assertIn("formal", prompt.lower())
        self.assertIn("sério", prompt.lower())


class TestMemoryManager(unittest.TestCase):
    """
    Testes para o gerenciador de memória.
    """
    
    def setUp(self):
        """
        Configuração para cada teste individual.
        """
        # Criar diretório temporário para testes
        import tempfile
        self.test_dir = tempfile.mkdtemp(prefix="nina_memory_test_")
    
    def tearDown(self):
        """
        Limpeza após cada teste.
        """
        # Remover diretório temporário
        import shutil
        try:
            shutil.rmtree(self.test_dir)
        except:
            pass
    
    def test_memory_initialization(self):
        """
        Testa a inicialização do gerenciador de memória.
        """
        from memory.memory_manager import MemoryManager
        
        # Inicializar gerenciador de memória
        manager = MemoryManager(self.test_dir)
        
        # Verificar se o banco de dados foi criado
        db_path = os.path.join(self.test_dir, "memory.db")
        self.assertTrue(os.path.exists(db_path))
    
    def test_conversation_history(self):
        """
        Testa o armazenamento e recuperação de histórico de conversas.
        """
        from memory.memory_manager import MemoryManager
        
        # Inicializar gerenciador de memória
        manager = MemoryManager(self.test_dir)
        
        # Gerar ID de sessão
        session_id = manager.generate_session_id()
        
        # Adicionar mensagens
        manager.add_conversation_message(session_id, "user", "Olá, como você está?")
        manager.add_conversation_message(session_id, "assistant", "Estou bem, obrigado por perguntar!")
        
        # Recuperar histórico
        history = manager.get_conversation_history(session_id)
        
        # Verificar se as mensagens foram armazenadas corretamente
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["role"], "user")
        self.assertEqual(history[0]["content"], "Olá, como você está?")
        self.assertEqual(history[1]["role"], "assistant")
        self.assertEqual(history[1]["content"], "Estou bem, obrigado por perguntar!")
    
    def test_user_info(self):
        """
        Testa o armazenamento e recuperação de informações do usuário.
        """
        from memory.memory_manager import MemoryManager
        
        # Inicializar gerenciador de memória
        manager = MemoryManager(self.test_dir)
        
        # Armazenar informações
        manager.store_user_info("nome", "João")
        manager.store_user_info("preferencias", ["música", "tecnologia"])
        
        # Recuperar informações
        nome = manager.get_user_info("nome")
        preferencias = manager.get_user_info("preferencias")
        
        # Verificar se as informações foram armazenadas corretamente
        self.assertEqual(nome, "João")
        self.assertEqual(preferencias, ["música", "tecnologia"])


class TestSessionManager(unittest.TestCase):
    """
    Testes para o gerenciador de sessões.
    """
    
    def setUp(self):
        """
        Configuração para cada teste individual.
        """
        # Criar diretório temporário para testes
        import tempfile
        self.test_dir = tempfile.mkdtemp(prefix="nina_session_test_")
    
    def tearDown(self):
        """
        Limpeza após cada teste.
        """
        # Remover diretório temporário
        import shutil
        try:
            shutil.rmtree(self.test_dir)
        except:
            pass
    
    def test_session_creation(self):
        """
        Testa a criação de sessões.
        """
        from core.session_manager import SessionManager
        
        # Inicializar gerenciador de sessões
        manager = SessionManager(self.test_dir)
        
        # Criar sessão
        session_id = manager.create_session("Sessão de teste")
        
        # Verificar se a sessão foi criada
        self.assertIsNotNone(session_id)
        
        # Verificar se a sessão pode ser recuperada
        session = manager.get_session(session_id)
        self.assertIsNotNone(session)
        self.assertEqual(session["name"], "Sessão de teste")
    
    def test_session_messages(self):
        """
        Testa a adição e recuperação de mensagens em uma sessão.
        """
        from core.session_manager import SessionManager
        
        # Inicializar gerenciador de sessões
        manager = SessionManager(self.test_dir)
        
        # Criar sessão
        session_id = manager.create_session("Sessão de teste")
        
        # Adicionar mensagens
        manager.add_message(session_id, "user", "Olá, como você está?")
        manager.add_message(session_id, "assistant", "Estou bem, obrigado por perguntar!")
        
        # Recuperar mensagens
        messages = manager.get_messages(session_id)
        
        # Verificar se as mensagens foram armazenadas corretamente
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "user")
        self.assertEqual(messages[0]["content"], "Olá, como você está?")
        self.assertEqual(messages[1]["role"], "assistant")
        self.assertEqual(messages[1]["content"], "Estou bem, obrigado por perguntar!")
    
    def test_session_listing(self):
        """
        Testa a listagem de sessões.
        """
        from core.session_manager import SessionManager
        
        # Inicializar gerenciador de sessões
        manager = SessionManager(self.test_dir)
        
        # Criar múltiplas sessões
        session1 = manager.create_session("Sessão 1")
        session2 = manager.create_session("Sessão 2")
        session3 = manager.create_session("Sessão 3")
        
        # Listar sessões
        sessions = manager.list_sessions()
        
        # Verificar se todas as sessões estão na lista
        self.assertEqual(len(sessions), 3)
        
        # Verificar se os IDs estão corretos
        session_ids = [s["id"] for s in sessions]
        self.assertIn(session1, session_ids)
        self.assertIn(session2, session_ids)
        self.assertIn(session3, session_ids)


class TestAudioPlayback(unittest.TestCase):
    """
    Testes para o sistema de playback de áudio.
    """
    
    @patch('pygame.mixer')
    def test_audio_player_initialization(self, mock_mixer):
        """
        Testa a inicialização do player de áudio.
        """
        from tts.audio_player import AudioPlayer
        
        # Configurar mock
        mock_mixer.get_init.return_value = None
        
        # Inicializar player
        player = AudioPlayer()
        
        # Verificar se o mixer foi inicializado
        mock_mixer.init.assert_called_once()
