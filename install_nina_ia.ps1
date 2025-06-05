# Script de instalação para PowerShell da Nina IA v2.4
# Este script configura o ambiente e instala as dependências necessárias

# Definir cores para o console
$host.UI.RawUI.ForegroundColor = "Green"
Write-Host "============================================"
Write-Host " Instalador da Nina IA v2.4 (PowerShell)"
Write-Host "============================================"
Write-Host ""
Write-Host "Este script irá configurar o ambiente e instalar as dependências para a Nina IA."
Write-Host "Requer Python 3.8+ instalado e adicionado ao PATH."
Write-Host "Para funcionalidades completas de GPU (recomendado), é necessária uma GPU NVIDIA com drivers CUDA 11.8 instalados."
Write-Host ""
Read-Host "Pressione Enter para continuar"

# Verificação de Python
Write-Host "Verificando instalação do Python..."
try {
    $pythonVersion = python --version
    Write-Host "Python encontrado: $pythonVersion"
}
catch {
    Write-Host "ERRO: Python não encontrado no PATH. Por favor, instale Python 3.8+ e adicione-o ao PATH." -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}
Write-Host ""

# Criação do Ambiente Virtual
Write-Host "Criando ambiente virtual na pasta 'venv'..."
if (Test-Path -Path "venv") {
    Write-Host "Ambiente virtual 'venv' já existe. Pulando criação."
}
else {
    try {
        python -m venv venv
        Write-Host "Ambiente virtual criado com sucesso."
    }
    catch {
        Write-Host "ERRO: Falha ao criar o ambiente virtual. Verifique sua instalação do Python." -ForegroundColor Red
        Read-Host "Pressione Enter para sair"
        exit 1
    }
}
Write-Host ""

# Ativação do Ambiente Virtual
Write-Host "Ativando ambiente virtual..."
try {
    & .\venv\Scripts\Activate.ps1
    Write-Host "Ambiente virtual ativado para esta sessão."
}
catch {
    Write-Host "ERRO: Falha ao ativar o ambiente virtual." -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}
Write-Host ""

# Atualização do Pip
Write-Host "Atualizando pip no ambiente virtual..."
try {
    python -m pip install --upgrade pip
    Write-Host "Pip atualizado com sucesso."
}
catch {
    Write-Host "AVISO: Falha ao atualizar o pip. Tentando continuar com a versão atual..." -ForegroundColor Yellow
}
Write-Host ""

# Instalação de Dependências Críticas Primeiro
Write-Host "Instalando dependências críticas..." -ForegroundColor Cyan
try {
    pip install pyyaml
    Write-Host "PyYAML instalado com sucesso." -ForegroundColor Green
}
catch {
    Write-Host "ERRO: Falha ao instalar PyYAML. Este pacote é essencial para o funcionamento da Nina IA." -ForegroundColor Red
    Write-Host "Tente executar manualmente: pip install pyyaml" -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Instalação de sounddevice explicitamente
Write-Host "Instalando sounddevice..." -ForegroundColor Cyan
try {
    pip install sounddevice
    Write-Host "sounddevice instalado com sucesso." -ForegroundColor Green
}
catch {
    Write-Host "ERRO: Falha ao instalar sounddevice. Este pacote é essencial para a captura de áudio." -ForegroundColor Red
    Write-Host "Tente executar manualmente: pip install sounddevice" -ForegroundColor Yellow
    Read-Host "Pressione Enter para continuar mesmo assim"
}

# Instalação de outras dependências críticas
Write-Host "Instalando outras dependências críticas..." -ForegroundColor Cyan
try {
    pip install fastapi uvicorn python-dotenv sqlitedict soundfile
    Write-Host "Dependências críticas instaladas com sucesso." -ForegroundColor Green
}
catch {
    Write-Host "AVISO: Falha ao instalar algumas dependências críticas. Tentando continuar com a instalação completa..." -ForegroundColor Yellow
}

# Instalação de PyTorch
Write-Host "Instalando PyTorch (com suporte a CUDA 11.8)..." -ForegroundColor Cyan
Write-Host "Nota: Se CUDA 11.8 não estiver disponível, tentará instalar a versão CPU."
try {
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    Write-Host "PyTorch instalado com sucesso." -ForegroundColor Green
}
catch {
    Write-Host "AVISO: Falha ao instalar PyTorch com suporte CUDA 11.8." -ForegroundColor Yellow
    Write-Host "Tentando instalar versão CPU do PyTorch..." -ForegroundColor Yellow
    try {
        pip install torch torchvision torchaudio
        Write-Host "PyTorch (versão CPU) instalado com sucesso." -ForegroundColor Green
    }
    catch {
        Write-Host "ERRO: Falha ao instalar PyTorch. Verifique sua conexão e logs do pip." -ForegroundColor Red
        Read-Host "Pressione Enter para continuar mesmo assim"
    }
}

# Instalação de Dependências do requirements.txt
Write-Host "Instalando dependências do arquivo requirements.txt..." -ForegroundColor Cyan
try {
    pip install -r requirements.txt
    Write-Host "Dependências instaladas com sucesso." -ForegroundColor Green
}
catch {
    Write-Host "AVISO: Falha ao instalar todas as dependências do requirements.txt." -ForegroundColor Yellow
    Write-Host "Algumas funcionalidades podem não estar disponíveis." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Verificando se as dependências críticas foram instaladas..." -ForegroundColor Yellow
    
    try {
        python -c "import yaml; print('PyYAML instalado com sucesso')"
    }
    catch {
        Write-Host "ERRO CRÍTICO: PyYAML não foi instalado corretamente. A Nina IA não funcionará sem este pacote." -ForegroundColor Red
        Write-Host "Execute manualmente: pip install pyyaml" -ForegroundColor Yellow
        Read-Host "Pressione Enter para continuar mesmo assim"
    }
    
    try {
        python -c "import sounddevice; print('sounddevice instalado com sucesso')"
    }
    catch {
        Write-Host "ERRO CRÍTICO: sounddevice não foi instalado corretamente. A captura de áudio não funcionará." -ForegroundColor Red
        Write-Host "Execute manualmente: pip install sounddevice" -ForegroundColor Yellow
        Read-Host "Pressione Enter para continuar mesmo assim"
    }
}
Write-Host ""

# Criação de Arquivos Padrão
Write-Host "Verificando arquivos de configuração..." -ForegroundColor Cyan

# Verificar e criar config.yaml
if (-not (Test-Path -Path "config.yaml")) {
    Write-Host "Arquivo 'config.yaml' não encontrado."
    if (Test-Path -Path "config_exemplo.yaml") {
        Write-Host "Criando 'config.yaml' a partir de 'config_exemplo.yaml'..."
        Copy-Item -Path "config_exemplo.yaml" -Destination "config.yaml"
        Write-Host "'config.yaml' criado. Edite-o com suas configurações (ex: tokens de API)."
    }
    else {
        Write-Host "AVISO: 'config_exemplo.yaml' também não encontrado. Criando arquivo config.yaml padrão..." -ForegroundColor Yellow
        @"
server:
  host: "127.0.0.1"
  port: 8000
  debug: true

modules:
  stt: true
  llm: true
  tts: true
  web: true

v2_3:
  enable_learning: true
  enable_coach: true
  enable_analysis: true

v2_4:
  enable_replay_analysis: true
  enable_vision: true
  enable_emotional_feedback: true
"@ | Out-File -FilePath "config.yaml" -Encoding utf8
        Write-Host "'config.yaml' criado com configurações padrão."
    }
}
else {
    Write-Host "Arquivo 'config.yaml' já existe."
}

# Criar diretórios necessários
Write-Host "Criando diretórios necessários..." -ForegroundColor Cyan
if (-not (Test-Path -Path "logs")) { New-Item -Path "logs" -ItemType Directory | Out-Null }
if (-not (Test-Path -Path "profiles")) { New-Item -Path "profiles" -ItemType Directory | Out-Null }
if (-not (Test-Path -Path "memory")) { New-Item -Path "memory" -ItemType Directory | Out-Null }
if (-not (Test-Path -Path "replays")) { New-Item -Path "replays" -ItemType Directory | Out-Null }
if (-not (Test-Path -Path "uploads")) { New-Item -Path "uploads" -ItemType Directory | Out-Null }
Write-Host "Diretórios criados com sucesso."
Write-Host ""

# Verificação Final de Dependências
Write-Host "Verificando instalação de dependências críticas..." -ForegroundColor Cyan
try {
    python -c "import yaml; print('PyYAML: OK')"
}
catch {
    Write-Host "ERRO: PyYAML não foi instalado corretamente." -ForegroundColor Red
    Write-Host "Execute manualmente: pip install pyyaml" -ForegroundColor Yellow
    Write-Host ""
}

try {
    python -c "import sounddevice; print('sounddevice: OK')"
}
catch {
    Write-Host "ERRO: sounddevice não foi instalado corretamente." -ForegroundColor Red
    Write-Host "Execute manualmente: pip install sounddevice" -ForegroundColor Yellow
    Write-Host ""
}

# Conclusão
$host.UI.RawUI.ForegroundColor = "Green"
Write-Host "============================================"
Write-Host " ✅ Instalação concluída!"
Write-Host "============================================"
Write-Host ""
Write-Host "Para iniciar a Nina IA, abra um novo terminal PowerShell,"
Write-Host "navegue até esta pasta (onde o script foi executado) e execute os seguintes comandos:"
Write-Host ""
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host "   python nina.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "Se encontrar erro 'No module named yaml', execute:" -ForegroundColor Yellow
Write-Host "   pip install pyyaml" -ForegroundColor Cyan
Write-Host ""
Write-Host "Se encontrar erro 'No module named sounddevice', execute:" -ForegroundColor Yellow
Write-Host "   pip install sounddevice" -ForegroundColor Cyan
Write-Host ""
Write-Host "Lembre-se de editar o arquivo 'config.yaml' se necessário."
Write-Host ""
$host.UI.RawUI.ForegroundColor = "White"
Read-Host "Pressione Enter para sair"
