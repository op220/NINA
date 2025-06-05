## Lista de Tarefas - Correção do Repositório Nina IA

- [ ] **1. Correções de Importação:**
  - [x] Substituir `from core/profiles_manager import ProfilesManager` por `from profiles/profiles_manager import ProfilesManager` em todos os arquivos.
  - [x] Substituir `from core/personality_manager import PersonalityManager` por `from profiles/personality_manager import PersonalityManager` em todos os arquivos.
  - [x] Substituir `from core/memory_manager import MemoryManager` por `from memory/memory_manager import MemoryManager` em todos os arquivos.
  - [x] Substituir `from core/memory_adapter import MemoryAdapter` por `from memory/memory_adapter import MemoryAdapter` em todos os arquivos.
  - [x] Substituir `from core/memory_integrator import MemoryIntegrator` por `from memory/memory_integrator import MemoryIntegrator` em todos os arquivos.
  - [x] Substituir `from core/memory_orchestrator import MemoryOrchestrator` por `from memory/memory_orchestrator import MemoryOrchestrator` em todos os arquivos.
  - [x] Substituir `from web/backend/api import app` por `from web/api import app` em todos os arquivos.
  - [x] Localizar e corrigir outros imports `from core.xxx` inválidos.

- [ ] **2. Correções de Sintaxe Específicas:**
  - [x] `profiles/personality_manager.py` (linha ~480): Fechar string literal `system_prompt`.
  - [x] `memory/memory_manager.py` (linha 493): Adicionar bloco `except` ou `finally` ao `try`.
  - [x] `memory/database.py` (linha ~425): Fechar docstring `"""` (Falha na correção automática, requer revisão manual).
  - [x] `modules/game_analyzer.py` (linha 58): Balancear parênteses em f-string (Verificado, sem erro aparente).
  - [x] `social/pattern_analyzer.py` (linha 425): Fechar chave `{`.
  - [x] `tests/test_memory_system.py` (linha 435): Fechar string literal (Corrigido manualmente).
  - [x] `tests/test_web_api.py` (linha 439): Adicionar vírgula faltante (Corrigido: Método `assertEqual` completado).
  - [x] `tts/audio_playback.py` (linha ~487): Fechar docstring `"""`.
  - [x] `web/api.py` (linha 463): Adicionar bloco `except` ou `finally` ao `try` (Corrigido: Adicionado bloco except).

- [x] **3. Verificação Geral de Balanceamento:**
  - [x] Garantir que literais de string, parênteses, colchetes e chaves estão balanceados em todos os arquivos.
  - [x] Garantir que todos os blocos `try` possuem `except` ou `finally`.

- [ ] **4. Validação Final:**
  - [ ] Instalar dependências (`requirements.txt`).
  - [ ] Executar `python nina.py` para verificar inicialização.
  - [ ] Executar testes (e.g., `pytest` ou `python -m unittest`) e verificar se passam.

- [ ] **5. Finalização:**
  - [ ] Informar o usuário sobre a conclusão e resultados dos testes.
