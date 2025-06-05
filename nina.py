"""
Módulo principal para integração de todos os componentes do projeto Nina IA.
Fornece uma interface unificada para o assistente de voz.
"""

import os
import sys
import logging
import threading
import time
import argparse
from typing import Dict, Any, Optional, List, Union, Callable

# --- Adicionar diretório raiz ao sys.path --- START
# Isso garante que os imports absolutos (ex: from core.config) funcionem
# quando o script é executado diretamente (python nina.py).
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)
# --- Adicionar diretório raiz ao sys.path --- END

# Importar configuração primeiro para definir caminhos e sys.path
try:
    from core.config import get_config, ROOT_DIR
except ImportError as e:
    print(f"ERRO CRÍTICO: Não foi possível importar a configuração de core.config. Verifique a estrutura de pastas e __init__.py. Detalhes: {e}")
    # Tentar importar de forma diferente se o sys.path falhou
    try:
        import core.config
        get_config = core.config.get_config
        ROOT_DIR = core.config.ROOT_DIR
        print("AVISO: Importação de config funcionou de forma alternativa. Verifique o sys.path.")
    except ImportError:
        print("ERRO CRÍTICO: Falha na importação alternativa de config também.")
        sys.exit(1)

# Importar componentes do projeto usando caminhos absolutos
from core.orchestrator import NinaOrchestrator

# --- Configuração de logging --- 
LOG_DIR = get_config("paths.logs", os.path.join(ROOT_DIR, "logs"))
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_DIR, "nina_ia.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE_PATH)
    ]
)
logger = logging.getLogger(__name__)

# --- Verificação de arquivos movidos --- 
# Os arquivos AudioPlaybackManager e AudioPlayer foram movidos para tts/
from tts.audio_playback import AudioPlaybackManager
from tts.audio_player import AudioPlayer

class NinaIA:
    """
    Classe principal do projeto Nina IA.
    Integra todos os componentes e fornece uma interface unificada.
    """

    def __init__(self,
                 profile_name: str = "default_profile",
                 use_cuda: bool = True,
                 debug: bool = False):
        """
        Inicializa o assistente Nina IA.

        Args:
            profile_name: Nome do perfil a ser carregado
            use_cuda: Se deve usar GPU para aceleração
            debug: Se deve ativar modo de depuração
        """
        # Configurar logging
        if debug:
            logging.getLogger().setLevel(logging.DEBUG)
            logger.debug("Modo de depuração ativado")

        # Obter diretórios do config.yaml
        self.data_dir = get_config("paths.database", os.path.join(ROOT_DIR, "database"))
        self.profiles_dir = get_config("paths.profiles", os.path.join(ROOT_DIR, "profiles"))
        self.profile_name = profile_name
        self.use_cuda = use_cuda

        # Criar diretórios se não existirem
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.profiles_dir, exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, "audio"), exist_ok=True) # Diretório para áudio

        # Inicializar componentes
        logger.info("Inicializando Nina IA")
        self._init_components()

        # Estado do sistema
        self.running = False
        self.continuous_mode = False

        logger.info("Nina IA inicializada com sucesso")

    def _init_components(self) -> None:
        """
        Inicializa todos os componentes do sistema.
        """
        try:
            # Inicializar orquestrador principal
            logger.info("Inicializando orquestrador")
            self.orchestrator = NinaOrchestrator(
                data_dir=self.data_dir,
                profile_name=self.profile_name,
                use_cuda=self.use_cuda
            )

            # Inicializar gerenciador de playback avançado
            logger.info("Inicializando gerenciador de playback")
            self.playback_manager = AudioPlaybackManager(
                audio_dir=os.path.join(self.data_dir, "audio")
            )

            # Configurar callbacks de playback
            self.playback_manager.set_on_start_callback(self._on_playback_start)
            self.playback_manager.set_on_complete_callback(self._on_playback_complete)

            logger.info("Componentes inicializados com sucesso")

        except Exception as e:
            logger.exception(f"Erro CRÍTICO ao inicializar componentes: {e}")
            raise

    def _on_playback_start(self, audio_path: str) -> None:
        """
        Callback chamado quando um áudio começa a ser reproduzido.
        """
        logger.debug(f"Iniciando reprodução: {os.path.basename(audio_path)}")

    def _on_playback_complete(self, audio_path: str) -> None:
        """
        Callback chamado quando um áudio termina de ser reproduzido.
        """
        logger.debug(f"Reprodução concluída: {os.path.basename(audio_path)}")

    def process_voice_command(self) -> Optional[str]:
        """
        Processa um comando de voz: escuta, transcreve, processa e responde.
        """
        try:
            # Capturar e transcrever áudio
            text = self.orchestrator.process_voice_input()

            if not text:
                logger.info("Nenhuma fala detectada ou erro na transcrição")
                return None

            # Processar texto e gerar resposta
            response = self.process_text_command(text)

            return response

        except Exception as e:
            logger.exception(f"Erro ao processar comando de voz: {e}")
            return None

    def process_text_command(self, text: str) -> Optional[str]:
        """
        Processa um comando de texto: processa e responde.
        """
        try:
            if not text:
                return None

            logger.info(f"Processando comando: 	{text}	")

            # Processar texto com o orquestrador
            response = self.orchestrator.process_text_input(text)

            if not response:
                logger.warning("Nenhuma resposta gerada")
                return None

            # Sintetizar resposta em áudio
            audio_file = self.orchestrator.tts.speak(response, blocking=False, save_file=True)

            # Reproduzir com o gerenciador de playback avançado
            if audio_file:
                self.playback_manager.play(audio_file)

            return response

        except AttributeError as e:
             logger.error(f"Erro de atributo ao processar comando: {e}. Verifique se todos os módulos (como TTS) estão corretamente inicializados no Orchestrator.")
             return None
        except Exception as e:
            logger.exception(f"Erro ao processar comando de texto: {e}")
            return None

    def start_continuous_mode(self) -> None:
        """
        Inicia o modo contínuo de escuta e resposta.
        """
        if self.continuous_mode:
            logger.warning("Modo contínuo já está ativo")
            return

        try:
            self.continuous_mode = True
            self.running = True

            logger.info("Iniciando modo contínuo")

            # Iniciar thread de interação contínua
            def interaction_loop():
                logger.info("Loop de interação contínua iniciado")

                # Falar mensagem de boas-vindas
                welcome_message = "Olá, eu sou a Nina, sua assistente de inteligência artificial. Como posso ajudar?"
                try:
                    self.orchestrator.speak_response(welcome_message)
                except AttributeError as e:
                    logger.error(f"Não foi possível falar a mensagem de boas-vindas: {e}")

                while self.running and self.continuous_mode:
                    try:
                        # Processar comando de voz
                        self.process_voice_command()

                        # Pequena pausa para evitar uso excessivo de CPU
                        time.sleep(0.1)

                    except Exception as e:
                        logger.exception(f"Erro no loop de interação: {e}")
                        time.sleep(1)  # Evitar loop infinito em caso de erro

                logger.info("Loop de interação contínua encerrado")

            # Iniciar thread
            self.interaction_thread = threading.Thread(target=interaction_loop)
            self.interaction_thread.daemon = True
            self.interaction_thread.start()

        except Exception as e:
            logger.exception(f"Erro ao iniciar modo contínuo: {e}")
            self.continuous_mode = False

    def stop_continuous_mode(self) -> None:
        """
        Para o modo contínuo de escuta e resposta.
        """
        if not self.continuous_mode:
            logger.warning("Modo contínuo não está ativo")
            return

        try:
            logger.info("Parando modo contínuo")

            self.continuous_mode = False

            # Parar componentes ativos
            if hasattr(self.orchestrator, "stop_continuous_interaction"):
                 self.orchestrator.stop_continuous_interaction()
            self.playback_manager.stop()

            # Aguardar thread terminar
            if hasattr(self, 'interaction_thread') and self.interaction_thread.is_alive():
                logger.debug("Aguardando thread de interação terminar...")
                self.interaction_thread.join(timeout=2.0)
                if self.interaction_thread.is_alive():
                    logger.warning("Thread de interação não terminou a tempo.")

            logger.info("Modo contínuo parado")

        except Exception as e:
            logger.exception(f"Erro ao parar modo contínuo: {e}")

    def shutdown(self) -> None:
        """
        Encerra o sistema Nina IA.
        """
        try:
            logger.info("Encerrando Nina IA")

            # Parar modo contínuo se estiver ativo
            if self.continuous_mode:
                self.stop_continuous_mode()

            # Marcar como não executando
            self.running = False

            # Encerrar componentes
            self.playback_manager.shutdown()
            if hasattr(self.orchestrator, "cleanup"):
                self.orchestrator.cleanup()

            logger.info("Nina IA encerrada com sucesso")

        except Exception as e:
            logger.exception(f"Erro ao encerrar Nina IA: {e}")

    def change_profile(self, profile_name: str) -> bool:
        """
        Muda o perfil ativo.
        """
        try:
            result = self.orchestrator.change_profile(profile_name)

            if result:
                self.profile_name = profile_name
                logger.info(f"Perfil alterado para: {profile_name}")

            return result

        except Exception as e:
            logger.exception(f"Erro ao mudar perfil: {e}")
            return False

    def get_status(self) -> Dict[str, Any]:
        """
        Obtém o status atual do sistema.
        """
        try:
            # Obter status do orquestrador (se disponível)
            orchestrator_status = {}
            if hasattr(self.orchestrator, "get_status"):
                orchestrator_status = self.orchestrator.get_status()

            # Adicionar informações adicionais
            status = {
                **orchestrator_status,
                "continuous_mode": self.continuous_mode,
                "running": self.running,
                "playback_busy": self.playback_manager.is_busy(),
                "playback_volume": self.playback_manager.get_volume()
            }

            return status

        except Exception as e:
            logger.exception(f"Erro ao obter status: {e}")
            return {
                "error": str(e),
                "running": self.running,
                "continuous_mode": self.continuous_mode
            }

    def set_volume(self, volume: float) -> None:
        """
        Define o volume de reprodução.
        """
        try:
            self.playback_manager.set_volume(volume)
            logger.info(f"Volume definido: {volume}")

        except Exception as e:
            logger.exception(f"Erro ao definir volume: {e}")

def main():
    """
    Função principal para execução do assistente Nina IA.
    """
    # Configurar argumentos de linha de comando
    parser = argparse.ArgumentParser(description='Nina IA - Assistente de Inteligência Artificial')
    parser.add_argument('--profile', type=str, default='default_profile', help='Nome do perfil a ser carregado (dentro da pasta profiles)')
    parser.add_argument('--no-cuda', action='store_true', help='Desativar uso de GPU')
    parser.add_argument('--debug', action='store_true', help='Ativar modo de depuração (logging mais detalhado)')
    parser.add_argument('--continuous', action='store_true', help='Iniciar em modo contínuo (escuta ativa)')
    parser.add_argument('--text', type=str, help='Processar um único comando de texto e sair')

    args = parser.parse_args()

    try:
        # Inicializar Nina IA
        nina = NinaIA(
            profile_name=args.profile,
            use_cuda=not args.no_cuda,
            debug=args.debug
        )

        # Processar comando de texto se fornecido
        if args.text:
            response = nina.process_text_command(args.text)
            if response:
                print(f"Resposta: {response}")

            # Aguardar reprodução terminar
            while nina.playback_manager.is_busy():
                time.sleep(0.1)

            nina.shutdown()
            return

        # Iniciar modo contínuo se solicitado
        if args.continuous:
            nina.start_continuous_mode()

            print("Nina IA iniciada em modo contínuo. Pressione Ctrl+C para encerrar.")

            try:
                # Manter programa em execução
                while nina.running:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                print("\nEncerrando Nina IA...")
            finally:
                nina.shutdown()

            return

        # Modo interativo simples (padrão se --text ou --continuous não forem usados)
        print("Nina IA iniciada. Digite 'sair' para encerrar, 'voz' para comando de voz.")

        while True:
            try:
                command = input("\nDigite um comando: ")

                if command.lower() in ['sair', 'exit', 'quit']:
                    break

                if command.lower() in ['voz', 'voice']:
                    print("Aguardando comando de voz...")
                    response = nina.process_voice_command()
                else:
                    response = nina.process_text_command(command)

                if response:
                    print(f"Resposta: {response}")

                # Aguardar reprodução terminar
                while nina.playback_manager.is_busy():
                    time.sleep(0.1)

            except KeyboardInterrupt:
                print("\nEncerrando Nina IA...")
                break
            except Exception as e:
                logger.exception("Erro no loop interativo")
                print(f"Ocorreu um erro: {e}")

        nina.shutdown()

    except Exception as e:
        logger.exception(f"Erro fatal na execução da Nina IA: {e}")
        print(f"Erro fatal: {e}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())

