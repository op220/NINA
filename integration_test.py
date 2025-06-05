import os
import sys
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "integration_test.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("nina_integration_test")

# Adicionar diretório raiz ao path para importações
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Importar módulos para teste de integração
try:
    from core.config import get_config
    logger.info("✓ Módulo core.config importado com sucesso")
except ImportError as e:
    logger.error(f"✗ Falha ao importar core.config: {e}")

# Testar importações dos novos módulos v2.4
modules_to_test = [
    ("modules.combat_simulator", "CombatSimulator"),
    ("vision.hud_stream", "HUDStream"),
    ("vision.minimap_tracker", "MinimapTracker"),
    ("observer.reflection_trainer", "ReflectionTrainer"),
    ("emotional.emotional_feedback_engine", "EmotionalFeedbackEngine"),
    ("replay.replay_analyzer", "ReplayAnalyzer"),
    ("modules.team_coach", "TeamCoach")
]

for module_path, class_name in modules_to_test:
    try:
        module = __import__(module_path, fromlist=[class_name])
        class_obj = getattr(module, class_name)
        logger.info(f"✓ Módulo {module_path} importado com sucesso")
        
        # Tentar instanciar a classe (sem argumentos)
        try:
            instance = class_obj()
            logger.info(f"✓ Classe {class_name} instanciada com sucesso")
        except Exception as e:
            logger.warning(f"⚠ Não foi possível instanciar {class_name} sem argumentos: {e}")
    except ImportError as e:
        logger.error(f"✗ Falha ao importar {module_path}: {e}")
    except AttributeError as e:
        logger.error(f"✗ Classe {class_name} não encontrada em {module_path}: {e}")
    except Exception as e:
        logger.error(f"✗ Erro desconhecido ao testar {module_path}.{class_name}: {e}")

# Verificar arquivos de dados JSON
json_files = [
    "database/draft_synergy.json",
    "database/comp_strengths.json",
    "profiles/team_profiles.json"
]

for json_file in json_files:
    file_path = os.path.join(ROOT_DIR, json_file)
    if os.path.exists(file_path):
        try:
            import json
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"✓ Arquivo JSON {json_file} carregado com sucesso")
        except json.JSONDecodeError as e:
            logger.error(f"✗ Erro de formato no arquivo JSON {json_file}: {e}")
        except Exception as e:
            logger.error(f"✗ Erro ao ler arquivo JSON {json_file}: {e}")
    else:
        logger.error(f"✗ Arquivo JSON {json_file} não encontrado")

# Verificar arquivos HTML
html_files = [
    "uploads/analyze_replay.html",
    "web/map_overlay.html"
]

for html_file in html_files:
    file_path = os.path.join(ROOT_DIR, html_file)
    if os.path.exists(file_path):
        logger.info(f"✓ Arquivo HTML {html_file} encontrado")
    else:
        logger.error(f"✗ Arquivo HTML {html_file} não encontrado")

# Verificar configuração v2.4 no config.yaml
try:
    v2_4_enabled = get_config("v2_4.enable_replay_analysis", None)
    if v2_4_enabled is not None:
        logger.info(f"✓ Configuração v2_4 encontrada em config.yaml")
    else:
        logger.warning("⚠ Configuração v2_4 não encontrada em config.yaml")
except Exception as e:
    logger.error(f"✗ Erro ao verificar configuração v2_4: {e}")

logger.info("Teste de integração concluído")
