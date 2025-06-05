@echo off
setlocal
chcp 65001 >nul

echo ============================================
echo  INSTALADOR AUTOMÁTICO Nina IA v2.4 (Win)
echo ============================================

:: Navega para o diretório do script
cd /d "%~dp0"

:: Verifica se Python está instalado e obtém o caminho
echo Verificando instalacao do Python...
for /f "delims=" %%i in (
    'where python 2^>nul'
) do set "PYTHON_PATH=%%i"

if not defined PYTHON_PATH (
    echo ERRO: Python nao encontrado. Instale o Python 3.8 a 3.10 e adicione ao PATH.
    pause
    exit /b
)

echo Python encontrado em: %PYTHON_PATH%

:: Cria ambiente virtual se não existir
if not exist "venv" (
    echo Criando ambiente virtual...
    "%PYTHON_PATH%" -m venv venv
) else (
    echo Ambiente virtual "venv" ja existe. Pulando criacao.
)

:: Ativa o ambiente virtual
call ".\venv\Scripts\activate.bat"

:: Atualiza pip
echo Atualizando pip dentro do venv...
python -m pip install --upgrade pip

:: Instala dependências principais
echo Instalando dependencias de requirements.txt...
pip install -r requirements.txt || (
    echo AVISO: Falha em alguma instalacao via requirements.txt.
)

:: Instala dependências críticas manualmente (se ainda forem necessárias)
echo Instalando modulos essenciais manualmente...
pip install numpy pyyaml sounddevice soundfile requests faster-whisper torch torchvision torchaudio

:: Corrige problemas comuns com TTS
echo Instalando Coqui TTS...
pip install TTS==0.17.1 || (
    echo AVISO: Falha ao instalar TTS. Tente instalar manualmente com: pip install TTS==0.17.1
)

:: Cria config.yaml a partir de config_exemplo.yaml se nao existir
if not exist "config.yaml" (
    echo Criando config.yaml a partir de config_exemplo.yaml...
    if exist "config_exemplo.yaml" (
        copy "config_exemplo.yaml" "config.yaml"
    ) else (
        echo AVISO: config_exemplo.yaml nao encontrado. Nao foi possivel criar config.yaml.
    )
) else (
    echo config.yaml ja existe. Pulando criacao.
)

:: Opcional: Executar a IA ao final
echo.
set /p run_now="Deseja iniciar a Nina IA agora? (s/n): "
if /i "%run_now%"=="s" (
    python nina.py
) else (
    echo Instalacao concluida. Rode "venv\Scripts\activate.bat" e depois "python nina.py" para iniciar manualmente.
)

endlocal
pause


