@echo off
setlocal enabledelayedexpansion

title Instalador Nina IA v2.4 (Windows) - DEBUG
color 0A

echo ============================================
echo  Instalador da Nina IA v2.4 (Windows) - DEBUG
echo ============================================
echo(
echo Este script ira configurar o ambiente e instalar as dependencias para a Nina IA.
echo Requer Python 3.8+ instalado e adicionado ao PATH.
echo Para funcionalidades completas de GPU (recomendado), e necessaria uma GPU NVIDIA com drivers CUDA 11.8 instalados.
echo(
pause

REM --- Verificacao de Python ---
echo(
echo Verificando instalacao do Python...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado no PATH. Por favor, instale Python 3.8+ e adicione-o ao PATH.
    pause
    exit /b 1
)
echo Python encontrado.
echo(

REM --- Criacao do Ambiente Virtual ---
echo Criando ambiente virtual na pasta 'venv'...
if exist venv (
    echo Ambiente virtual 'venv' ja existe. Pulando criacao.
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERRO: Falha ao criar o ambiente virtual. Verifique sua instalacao do Python.
        pause
        exit /b 1
    )
    echo Ambiente virtual criado com sucesso.
)
echo(

REM --- Ativacao do Ambiente Virtual ---
echo Ativando ambiente virtual...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo ERRO: Falha ao ativar o ambiente virtual.
    pause
    exit /b 1
)
echo Ambiente virtual ativado para esta sessao.
echo(

REM --- Atualizacao do Pip ---
echo Atualizando pip no ambiente virtual...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo AVISO: Falha ao atualizar o pip. Tentando continuar com a versao atual...
) else (
    echo Pip atualizado com sucesso.
)
echo(

REM --- Instalacao de Dependencias Criticas Primeiro ---
echo Instalando dependencias criticas...
echo Instalando PyYAML...
pip install pyyaml
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar PyYAML. Este pacote e essencial.
    echo Tente executar manualmente: pip install pyyaml
    pause
    exit /b 1
)
echo PyYAML instalado com sucesso.
echo(

echo Instalando sounddevice...
pip install sounddevice
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar sounddevice. Essencial para captura de audio.
    echo Tente executar manualmente: pip install sounddevice
    pause
    exit /b 1
)
echo sounddevice instalado com sucesso.
echo(

REM --- Instalacao de Outras Dependencias Criticas ---
echo Instalando outras dependencias criticas (FastAPI, Uvicorn, etc.)...
echo DEBUG MARKER 1 - Antes de pip install fastapi...
pip install fastapi uvicorn python-dotenv sqlitedict soundfile
if %errorlevel% neq 0 (
    echo DEBUG MARKER 2 - Dentro do IF de erro do pip install fastapi...
    echo AVISO: Falha ao instalar algumas dependencias criticas (FastAPI, Uvicorn, etc.).
) else (
    echo DEBUG MARKER 3 - Dentro do ELSE de sucesso do pip install fastapi...
    echo Outras dependencias criticas instaladas.
)
echo DEBUG MARKER 4 - Antes do echo( apos pip install fastapi...
echo(
echo DEBUG MARKER 5 - Depois do echo( apos pip install fastapi...

REM --- Instalacao de PyTorch ---
echo Instalando PyTorch (com suporte a CUDA 11.8)...
echo Nota: Se CUDA 11.8 nao estiver disponivel ou falhar, tentara instalar a versao CPU.
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
if %errorlevel% neq 0 (
    echo AVISO: Falha ao instalar PyTorch com suporte CUDA 11.8.
    echo Tentando instalar versao CPU do PyTorch...
    pip install torch torchvision torchaudio
    if %errorlevel% neq 0 (
        echo ERRO: Falha ao instalar PyTorch (versao CPU). Verifique sua conexao e logs do pip.
        pause
        REM Nao sair aqui, requirements.txt ainda pode funcionar
    ) else (
        echo PyTorch (versao CPU) instalado com sucesso.
    )
) else (
    echo PyTorch (CUDA 11.8) instalado com sucesso.
)
echo(

REM --- Instalacao de Dependencias do requirements.txt ---
echo Instalando dependencias do arquivo requirements.txt...
if not exist requirements.txt (
    echo ERRO: Arquivo requirements.txt nao encontrado na pasta atual.
    pause
    exit /b 1
)
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo AVISO: Falha ao instalar algumas dependencias do requirements.txt.
    echo Algumas funcionalidades podem nao estar disponiveis. Verifique os logs do pip acima.
    echo(
    echo Verificando novamente dependencias criticas apos falha no requirements.txt...
    python -c "import yaml" > nul 2>&1
    if %errorlevel% neq 0 (
        echo ERRO CRITICO: PyYAML nao foi instalado corretamente apesar da tentativa inicial.
        echo Execute manualmente: pip install pyyaml
        pause
    )
    python -c "import sounddevice" > nul 2>&1
    if %errorlevel% neq 0 (
        echo ERRO CRITICO: sounddevice nao foi instalado corretamente apesar da tentativa inicial.
        echo Execute manualmente: pip install sounddevice
        pause
    )
) else (
    echo Dependencias do requirements.txt instaladas com sucesso.
)
echo(

REM --- Criacao de Arquivos Padrao ---
echo Verificando arquivos de configuracao e diretorios...

REM Verificar e criar config.yaml
if not exist config.yaml (
    echo Arquivo 'config.yaml' nao encontrado.
    if exist config_exemplo.yaml (
        echo Criando 'config.yaml' a partir de 'config_exemplo.yaml'...
        copy config_exemplo.yaml config.yaml > nul
        echo 'config.yaml' criado. Edite-o com suas configuracoes.
    ) else (
        echo AVISO: 'config_exemplo.yaml' tambem nao encontrado. Criando arquivo config.yaml padrao...
        REM Usando echo individual para evitar problemas com parenteses e echo.
        (echo server:) > config.yaml
        (echo   host: "127.0.0.1") >> config.yaml
        (echo   port: 8000) >> config.yaml
        (echo   debug: true) >> config.yaml
        (echo() >> config.yaml
        (echo modules:) >> config.yaml
        (echo   stt: true) >> config.yaml
        (echo   llm: true) >> config.yaml
        (echo   tts: true) >> config.yaml
        (echo   web: true) >> config.yaml
        (echo() >> config.yaml
        (echo v2_3:) >> config.yaml
        (echo   enable_learning: true) >> config.yaml
        (echo   enable_coach: true) >> config.yaml
        (echo   enable_analysis: true) >> config.yaml
        (echo() >> config.yaml
        (echo v2_4:) >> config.yaml
        (echo   enable_replay_analysis: true) >> config.yaml
        (echo   enable_vision: true) >> config.yaml
        (echo   enable_emotional_feedback: true) >> config.yaml
        echo 'config.yaml' criado com configuracoes padrao.
    )
) else (
    echo Arquivo 'config.yaml' ja existe.
)
echo(

REM Criar diretorios necessarios
echo Criando diretorios necessarios (logs, profiles, etc.)...
if not exist logs mkdir logs
if not exist profiles mkdir profiles
if not exist memory mkdir memory
if not exist replays mkdir replays
if not exist uploads mkdir uploads
echo Diretorios verificados/criados.
echo(

REM --- Verificacao Final de Dependencias ---
echo Verificacao final de dependencias criticas...
python -c "import yaml" > nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO FINAL: PyYAML nao esta instalado corretamente.
    echo Execute manualmente: pip install pyyaml
) else (
    echo PyYAML: OK
)

python -c "import sounddevice" > nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO FINAL: sounddevice nao esta instalado corretamente.
    echo Execute manualmente: pip install sounddevice
) else (
    echo sounddevice: OK
)
echo(

REM --- Conclusao ---
echo ============================================
echo  ✅ Instalacao concluida!
echo ============================================
echo(
echo Para iniciar a Nina IA, abra um novo terminal ou prompt de comando,
echo navegue ate esta pasta e execute os seguintes comandos:
echo(
echo   call venv\Scripts\activate
echo   python nina.py
echo(
echo Se encontrar erros de modulos ausentes (ex: 'yaml', 'sounddevice'),
echo ative o ambiente (call venv\Scripts\activate) e instale manualmente:
echo   pip install nome_do_modulo
echo(
echo Lembre-se de editar o arquivo 'config.yaml' se necessario.
echo(
echo NOTA: Se estiver usando PowerShell, use o script 'install_nina_ia.ps1'.
echo(
pause
exit /b 0

