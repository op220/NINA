"""
Módulo orquestrador principal do projeto Nina IA.
Integra todos os componentes para criar um assistente de voz completo.
"""

import os
import logging
import threading
import time
from typing import Dict, Any, Optional, List, Union, Callable

# Importar componentes do projeto usando caminhos absolutos
from stt.stt_module import STTModule
from llm.llm_module import LLMModule
from tts.tts_module import TTSModule
from profiles.profiles_manager import ProfilesManager
from core.session_manager import SessionManager

# Configuração de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class NinaOrchestrator:
    """
    Orquestrador principal do projeto Nina IA.
    Integra STT, LLM, TTS, perfis e sessões.
    """
    
    def __init__(self, 
                 data_dir: str = None,
                 profile_name: str = "default_profile",
                 use_cuda: bool = True):
        """
        Inicializa o orquestrador.
        
        Args:
            data_dir: Diretório para armazenar dados (None = usar padrão)
            profile_name: Nome do perfil a ser carregado
            use_cuda: Se deve usar GPU para aceleração
        """
        self.data_dir = data_dir or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data"
        )
        self.profile_name = profile_name
        self.use_cuda = use_cuda
        
        # Diretórios para componentes
        self.profiles_dir = get_config("paths.profiles", os.path.join(ROOT_DIR, "profiles"))
        self.memory_dir = os.path.join(self.data_dir, "memory")
        
        # Criar diretórios se não existirem
        os.makedirs(self.profiles_dir, exist_ok=True)
        os.makedirs(self.memory_dir, exist_ok=True)
        
        # Estado do sistema
        self.is_listening = False
        self.is_processing = False
        self.is_speaking = False
        self.should_stop = False
        self.active_session_id = None
        
        # Inicializar gerenciadores
        logger.info("Inicializando orquestrador Nina IA")
        self._init_managers()
        
        # Inicializar componentes
        self._init_components()
        
        logger.info("Orquestrador Nina IA inicializado com sucesso")
    
    def _init_managers(self) -> None:
        """
        Inicializa os gerenciadores de perfil e sessão.
        """
        try:
            # Inicializar gerenciador de perfis
            self.profiles_manager = ProfilesManager(self.profiles_dir)
            
            # Carregar perfil especificado
            if not self.profiles_manager.load_profile(self.profile_name):
                logger.warning(f"Perfil '{self.profile_name}' não encontrado, usando perfil padrão")
                self.profile_name = "default_profile"
            
            # Obter perfil ativo
            self.profile = self.profiles_manager.get_active_profile()
            
            # Inicializar gerenciador de sessões
            self.session_manager = SessionManager(self.memory_dir)
            
            # Criar sessão inicial
            self.active_session_id = self.session_manager.create_session("Sessão Inicial")
            
            logger.info(f"Gerenciadores inicializados: perfil='{self.profile_name}', sessão='{self.active_session_id}'")
            
        except Exception as e:
            logger.error(f"Erro ao inicializar gerenciadores: {e}")
            raise
    
    def _init_components(self) -> None:
        """
        Inicializa os componentes STT, LLM e TTS com base no perfil.
        """
        try:
            # Obter configurações do perfil
            stt_settings = self.profile.get("stt", {})
            llm_settings = self.profile.get("llm", {})
            voice_settings = self.profile.get("voice", {})
            
            # Inicializar STT
            logger.info("Inicializando módulo STT")
            self.stt = STTModule(
                model_size=stt_settings.get("model", "base"),
                device="cuda" if self.use_cuda else "cpu",
                compute_type="float16" if self.use_cuda else "float32",
                language=stt_settings.get("language", "pt")
            )
            
            # Inicializar LLM
            logger.info("Inicializando módulo LLM")
            self.llm = LLMModule(
                model=llm_settings.get("model", "mistral"),
                personality_file=os.path.join(self.profiles_dir, f"{self.profile_name}.json"),
                conversation_dir=os.path.join(self.memory_dir, "conversations")
            )
            
            # Inicializar TTS
            logger.info("Inicializando módulo TTS")
            self.tts = TTSModule(
                model_name=voice_settings.get("model", "tts_models/pt/cv/vits"),
                use_cuda=self.use_cuda,
                speaker=voice_settings.get("speaker"),
                language=voice_settings.get("language", "pt"),
                output_dir=os.path.join(self.memory_dir, "audio")
            )
            
            logger.info("Componentes inicializados com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao inicializar componentes: {e}")
            raise
    
    def process_voice_input(self, 
                            max_duration: float = 30.0,
                            wait_timeout: float = 5.0) -> Optional[str]:
        """
        Processa entrada de voz: escuta, transcreve e processa.
        
        Args:
            max_duration: Duração máxima da gravação em segundos
            wait_timeout: Tempo máximo de espera por fala em segundos
            
        Returns:
            Texto transcrito ou None se falhou
        """
        try:
            self.is_listening = True
            logger.info("Escutando entrada de voz...")
            
            # Escutar e transcrever
            text, info = self.stt.listen_and_transcribe(
                max_duration=max_duration,
                wait_timeout=wait_timeout
            )
            
            self.is_listening = False
            
            if not text:
                logger.info("Nenhuma fala detectada ou erro na transcrição")
                return None
            
            logger.info(f"Texto transcrito: '{text}'")
            
            # Adicionar mensagem à sessão
            self.session_manager.add_message(
                session_id=self.active_session_id,
                role="user",
                content=text,
                metadata=info
            )
            
            return text
            
        except Exception as e:
            logger.error(f"Erro ao processar entrada de voz: {e}")
            self.is_listening = False
            return None
    
    def process_text_input(self, text: str) -> Optional[str]:
        """
        Processa entrada de texto.
        
        Args:
            text: Texto de entrada
            
        Returns:
            Resposta gerada ou None se falhou
        """
        try:
            if not text:
                return None
            
            # Adicionar mensagem à sessão
            self.session_manager.add_message(
                session_id=self.active_session_id,
                role="user",
                content=text
            )
            
            self.is_processing = True
            logger.info(f"Processando texto: '{text}'")
            
            # Obter histórico de mensagens para contexto
            messages = self.session_manager.get_messages_for_llm(
                session_id=self.active_session_id,
                limit=10  # Limitar para as últimas 10 mensagens
            )
            
            # Processar com LLM
            response = self.llm.process_text(text)
            
            self.is_processing = False
            
            if not response:
                logger.warning("Nenhuma resposta gerada")
                return None
            
            logger.info(f"Resposta gerada: '{response[:100]}...'")
            
            # Adicionar resposta à sessão
            self.session_manager.add_message(
                session_id=self.active_session_id,
                role="assistant",
                content=response
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Erro ao processar texto: {e}")
            self.is_processing = False
            return None
    
    def speak_response(self, text: str, blocking: bool = True) -> bool:
        """
        Sintetiza e reproduz uma resposta.
        
        Args:
            text: Texto a ser falado
            blocking: Se True, bloqueia até o fim da fala
            
        Returns:
            True se a operação foi bem-sucedida
        """
        try:
            if not text:
                return False
            
            self.is_speaking = True
            logger.info(f"Falando resposta: '{text[:100]}...'")
            
            # Sintetizar e reproduzir
            self.tts.speak(text, blocking=blocking)
            
            if blocking:
                self.is_speaking = False
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao falar resposta: {e}")
            self.is_speaking = False
            return False
    
    def process_interaction(self, 
                            input_text: Optional[str] = None,
                            speak_response: bool = True,
                            blocking: bool = True) -> Optional[str]:
        """
        Processa uma interação completa: entrada, processamento e resposta.
        
        Args:
            input_text: Texto de entrada (None = usar entrada de voz)
            speak_response: Se deve falar a resposta
            blocking: Se deve bloquear até o fim da fala
            
        Returns:
            Resposta gerada ou None se falhou
        """
        try:
            # Obter entrada
            if input_text is None:
                input_text = self.process_voice_input()
                
                if not input_text:
                    return None
            
            # Processar texto
            response = self.process_text_input(input_text)
            
            if not response:
                return None
            
            # Falar resposta
            if speak_response:
                self.speak_response(response, blocking=blocking)
            
            return response
            
        except Exception as e:
            logger.error(f"Erro ao processar interação: {e}")
            return None
    
    def start_continuous_interaction(self, 
                                     callback: Optional[Callable[[str, str], None]] = None,
                                     use_wake_word: bool = False,
                                     wake_word: str = "Nina") -> None:
        """
        Inicia interação contínua em um thread separado.
        
        Args:
            callback: Função a ser chamada com (entrada, resposta) após cada interação
            use_wake_word: Se deve aguardar palavra de ativação
            wake_word: Palavra de ativação
        """
        def interaction_loop():
            logger.info("Iniciando loop de interação contínua")
            
            self.should_stop = False
            
            while not self.should_stop:
                try:
                    # TODO: Implementar detecção de palavra de ativação
                    # Por enquanto, apenas escuta continuamente
                    
                    # Processar entrada de voz
                    input_text = self.process_voice_input()
                    
                    if not input_text:
                        continue
                    
                    # Processar texto
                    response = self.process_text_input(input_text)
                    
                    if not response:
                        continue
                    
                    # Falar resposta
                    self.speak_response(response, blocking=True)
                    
                    # Chamar callback se fornecido
                    if callback:
                        callback(input_text, response)
                    
                except Exception as e:
                    logger.error(f"Erro no loop de interação: {e}")
                    time.sleep(1)  # Evitar loop infinito em caso de erro
        
        # Iniciar thread
        self.interaction_thread = threading.Thread(target=interaction_loop)
        self.interaction_thread.daemon = True
        self.interaction_thread.start()
    
    def stop_continuous_interaction(self) -> None:
        """
        Para a interação contínua.
        """
        self.should_stop = True
        
        # Parar componentes ativos
        if self.is_listening:
            # TODO: Implementar parada de escuta
            pass
        
        if self.is_speaking:
            self.tts.stop_speaking()
    
    def change_profile(self, profile_name: str) -> bool:
        """
        Muda o perfil ativo.
        
        Args:
            profile_name: Nome do perfil
            
        Returns:
            True se a operação foi bem-sucedida
        """
        try:
            # Verificar se o perfil existe
            if not self.profiles_manager.load_profile(profile_name):
                logger.error(f"Perfil não encontrado: {profile_name}")
                return False
            
            # Atualizar perfil
            self.profile_name = profile_name
            self.profile = self.profiles_manager.get_active_profile()
            
            # Reinicializar componentes
            self._init_components()
            
            logger.info(f"Perfil alterado para: {profile_name}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao mudar perfil: {e}")
            return False
    
    def create_new_session(self, session_name: Optional[str] = None) -> Optional[str]:
        """
        Cria uma nova sessão.
        
        Args:
            session_name: Nome da sessão (opcional)
            
        Returns:
            ID da nova sessão ou None se falhou
        """
        try:
            # Criar nova sessão
            session_id = self.session_manager.create_session(session_name)
            
            # Atualizar sessão ativa
            self.active_session_id = session_id
            
            # Adicionar mensagem de sistema com personalidade
            system_prompt = self.profiles_manager.build_system_prompt()
            self.session_manager.add_message(
                session_id=session_id,
                role="system",
                content=system_prompt
            )
            
            logger.info(f"Nova sessão criada: {session_id}")
            return session_id
            
        except Exception as e:
            logger.error(f"Erro ao criar nova sessão: {e}")
            return None
    
    def switch_session(self, session_id: str) -> bool:
        """
        Muda para outra sessão.
        
        Args:
            session_id: ID da sessão
            
        Returns:
            True se a operação foi bem-sucedida
        """
        try:
            # Verificar se a sessão existe
            if not self.session_manager.get_session(session_id):
                logger.error(f"Sessão não encontrada: {session_id}")
                return False
            
            # Atualizar sessão ativa
            self.active_session_id = session_id
            
            logger.info(f"Sessão alterada para: {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao mudar sessão: {e}")
            return False
    
    def get_active_session_id(self) -> Optional[str]:
        """
        Retorna o ID da sessão ativa.
        
        Returns:
            ID da sessão ativa ou None se não houver
        """
        return self.active_session_id
    
    def get_session_history(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Obtém o histórico de mensagens de uma sessão.
        
        Args:
            session_id: ID da sessão (None = usar sessão ativa)
            
        Returns:
            Lista de mensagens
        """
        try:
            session_id = session_id or self.active_session_id
            
            if not session_id:
                logger.error("Nenhuma sessão ativa")
                return []
            
            return self.session_manager.get_messages(session_id)
            
        except Exception as e:
            logger.error(f"Erro ao obter histórico de sessão: {e}")
            return []
    
    def get_status(self) -> Dict[str, Any]:
        """
        Obtém o status atual do sistema.
        
        Returns:
            Dicionário com informações de status
        """
        return {
            "is_listening": self.is_listening,
            "is_processing": self.is_processing,
            "is_speaking": self.is_speaking,
            "active_session_id": self.active_session_id,
            "profile_name": self.profile_name,
            "use_cuda": self.use_cuda
        }
    
    def cleanup(self) -> None:
        """
        Limpa recursos e finaliza componentes.
        """
        try:
            logger.info("Finalizando componentes...")
            
            # Parar interação contínua
            self.stop_continuous_interaction()
            
            # Finalizar componentes
            if hasattr(self, 'stt'):
                # Finalizar STT se tiver método específico
                if hasattr(self.stt, 'cleanup'):
                    self.stt.cleanup()
                
            if hasattr(self, 'llm'):
                # Finalizar LLM se tiver método específico
                if hasattr(self.llm, 'cleanup'):
                    self.llm.cleanup()
                
            if hasattr(self, 'tts'):
                # Finalizar TTS
                if hasattr(self.tts, 'cleanup'):
                    self.tts.cleanup()
            
            logger.info("Componentes finalizados com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao finalizar componentes: {e}")
