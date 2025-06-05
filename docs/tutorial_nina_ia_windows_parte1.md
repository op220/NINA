# Tutorial Completo: Instalação da IA Nina do Zero no Windows

## Introdução

A Nina IA é um assistente de inteligência artificial que funciona completamente offline em sua máquina local. Ela combina reconhecimento de voz, processamento de linguagem natural e síntese de fala para criar uma experiência de assistente virtual completa sem necessidade de conexão com servidores externos.

Este tutorial irá guiá-lo através do processo completo de instalação da Nina IA em um sistema Windows, desde a preparação do ambiente até a configuração final e testes. Como o repositório Git não está disponível, forneceremos alternativas para obtenção de todos os componentes necessários.

## Requisitos de Sistema

Antes de começar, verifique se seu sistema atende aos seguintes requisitos mínimos:

- **Sistema Operacional**: Windows 10/11 (64 bits)
- **Processador**: Intel Core i5 de 8ª geração ou AMD Ryzen 5 ou superior
- **Memória RAM**: Mínimo de 8GB (16GB recomendado)
- **Espaço em Disco**: Mínimo de 20GB livres
- **GPU**: NVIDIA com suporte a CUDA (recomendado para melhor desempenho)
  - Modelos recomendados: NVIDIA GTX 1060 6GB ou superior
  - Para usuários com GPU NVIDIA Quadro P4000 ou similar, o desempenho será excelente
- **Conexão à Internet**: Necessária apenas para download dos componentes (a execução é 100% offline)
- **Microfone e Alto-falantes**: Para entrada e saída de áudio

## Preparação do Ambiente

### Instalação do Python

A Nina IA requer Python 3.8 ou superior. Siga estes passos para instalar:

1. Acesse o site oficial do Python: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)

2. Baixe a versão mais recente do Python 3.10 (recomendado para melhor compatibilidade)

3. Execute o instalador baixado e marque as seguintes opções:
   - ✅ Install launcher for all users (recommended)
   - ✅ Add Python to PATH
   - ✅ Install for all users

4. Clique em "Install Now" para uma instalação padrão ou "Customize installation" se desejar personalizar

5. Se escolher instalação personalizada, certifique-se de selecionar:
   - ✅ pip
   - ✅ tcl/tk and IDLE
   - ✅ Python test suite
   - ✅ py launcher
   - ✅ Documentation

6. Na tela de opções avançadas, selecione:
   - ✅ Install for all users
   - ✅ Associate files with Python
   - ✅ Create shortcuts for installed applications
   - ✅ Add Python to environment variables
   - ✅ Precompile standard library
   - Diretório de instalação: `C:\Python310` (ou similar)

7. Clique em "Install" para iniciar a instalação

8. Após a instalação, abra o Prompt de Comando (CMD) e verifique se o Python foi instalado corretamente:

```cmd
python --version
pip --version
```

Você deve ver a versão do Python (3.10.x) e do pip (21.x ou superior) exibidas no terminal.

### Instalação do Node.js

O Node.js é necessário para a interface web opcional da Nina IA:

1. Acesse o site oficial do Node.js: [https://nodejs.org/en/download/](https://nodejs.org/en/download/)

2. Baixe a versão LTS (Long Term Support) para Windows (x64)

3. Execute o instalador e siga as instruções padrão:
   - Aceite os termos de licença
   - Escolha o diretório de instalação (recomendado manter o padrão)
   - Mantenha as configurações padrão de recursos
   - Marque a opção "Automatically install the necessary tools"

4. Após a instalação, abra o Prompt de Comando (CMD) e verifique se o Node.js foi instalado corretamente:

```cmd
node --version
npm --version
```

Você deve ver a versão do Node.js (16.x ou superior) e do npm (8.x ou superior) exibidas no terminal.

### Configuração do CUDA

Para aproveitar a aceleração por GPU (altamente recomendado para melhor desempenho), você precisará instalar o CUDA Toolkit:

1. Verifique a compatibilidade da sua GPU NVIDIA:
   - Abra o Gerenciador de Dispositivos (clique com o botão direito no menu Iniciar e selecione "Gerenciador de Dispositivos")
   - Expanda "Adaptadores de vídeo" e verifique se você tem uma GPU NVIDIA listada

2. Acesse o site da NVIDIA para baixar o CUDA Toolkit: [https://developer.nvidia.com/cuda-downloads](https://developer.nvidia.com/cuda-downloads)

3. Selecione as seguintes opções:
   - Operating System: Windows
   - Architecture: x86_64
   - Version: Windows 10 ou Windows 11 (conforme seu sistema)
   - Installer Type: exe (local)

4. Baixe o instalador e execute-o

5. Escolha "Express Installation" para uma configuração padrão

6. Aguarde a conclusão da instalação (pode levar alguns minutos)

7. Reinicie o computador após a instalação

8. Verifique se o CUDA foi instalado corretamente abrindo o Prompt de Comando e digitando:

```cmd
nvcc --version
```

Você deve ver a versão do CUDA Toolkit exibida (11.x ou superior).

### Configuração do Visual C++ Build Tools

Alguns componentes da Nina IA requerem compilação, então você precisará das ferramentas de build do Visual C++:

1. Baixe o Visual Studio Build Tools do site oficial: [https://visualstudio.microsoft.com/visual-cpp-build-tools/](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

2. Execute o instalador baixado

3. Na janela do instalador, selecione "Desenvolvimento para desktop com C++" e clique em "Instalar"

4. Aguarde a conclusão da instalação (pode levar alguns minutos)

5. Reinicie o computador após a instalação

Alternativamente, você pode instalar apenas as ferramentas de build necessárias usando o seguinte comando no PowerShell (como administrador):

```powershell
npm install --global --production windows-build-tools
```

Este comando instalará automaticamente o Python 2.7 (necessário para algumas ferramentas de build) e as ferramentas de build do Visual C++.

### Configuração do Ambiente Virtual Python

É uma boa prática usar ambientes virtuais para projetos Python. Vamos criar um para a Nina IA:

1. Abra o Prompt de Comando (CMD) como administrador

2. Navegue até o diretório onde deseja instalar a Nina IA:

```cmd
cd C:\
mkdir NinaIA
cd NinaIA
```

3. Crie um ambiente virtual:

```cmd
python -m venv nina_env
```

4. Ative o ambiente virtual:

```cmd
nina_env\Scripts\activate
```

Você verá o nome do ambiente virtual no início da linha de comando, indicando que está ativo.

5. Atualize o pip para a versão mais recente:

```cmd
python -m pip install --upgrade pip
```

Agora você tem um ambiente Python isolado para instalar os componentes da Nina IA sem afetar seu sistema principal.
