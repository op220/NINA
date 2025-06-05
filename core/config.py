import os
import yaml
import sys

# Determina o diretório raiz do projeto (um nível acima de 'core')
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT_DIR, "config.yaml")

CONFIG = {}
try:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        CONFIG = yaml.safe_load(f)
    if CONFIG is None: # Handle empty YAML file case
        CONFIG = {}
        print(f"AVISO: Arquivo de configuração {CONFIG_PATH} está vazio ou mal formatado.")
except FileNotFoundError:
    print(f"ERRO CRÍTICO: Arquivo de configuração não encontrado em {CONFIG_PATH}")
    # Considerar sair do programa ou lançar uma exceção aqui
    # sys.exit(1)
except yaml.YAMLError as e:
    print(f"ERRO CRÍTICO: Falha ao analisar o arquivo YAML {CONFIG_PATH}: {e}")
    # sys.exit(1)
except Exception as e:
    print(f"ERRO CRÍTICO: Falha inesperada ao carregar o arquivo de configuração {CONFIG_PATH}: {e}")
    # sys.exit(1)

def get_config(key, default=None):
    """Acessa valores aninhados no dicionário CONFIG de forma segura."""
    keys = key.split('.')
    value = CONFIG
    try:
        for k in keys:
            if isinstance(value, dict):
                value = value[k]
            else:
                # Se um valor intermediário não for um dicionário, a chave não pode ser encontrada
                raise KeyError(f"Caminho intermediário inválido para a chave '{key}'")
        return value
    except KeyError:
        # print(f"AVISO: Chave de configuração '{key}' não encontrada em config.yaml. Usando valor padrão: {default}")
        return default
    except TypeError:
        # Lidar com casos onde CONFIG pode não ser um dicionário (ex: erro de carregamento)
        # print(f"AVISO: Estrutura de configuração inesperada ao acessar a chave '{key}'. Usando valor padrão: {default}")
        return default

# Adicionar o diretório raiz ao sys.path para permitir importações absolutas de outros módulos
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Exemplo de como usar (pode ser removido ou comentado)
# if __name__ == "__main__":
#     print(f"Diretório Raiz: {ROOT_DIR}")
#     print(f"Caminho da Configuração: {CONFIG_PATH}")
#     print(f"Host do Servidor: {get_config('server.host', '0.0.0.0')}")
#     print(f"Porta do Servidor: {get_config('server.port', 8000)}")
#     print(f"Módulo TTS Ativado: {get_config('modules.tts', False)}")
#     print(f"Chave Inexistente: {get_config('non.existent.key', 'valor_padrao')}")

