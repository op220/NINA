# Instalação dos Componentes Principais

Nesta seção, vamos instalar os três componentes principais da Nina IA:
1. Sistema de Reconhecimento de Voz (STT - Speech-to-Text)
2. Sistema de Processamento de Linguagem Natural (LLM - Large Language Model)
3. Sistema de Síntese de Voz (TTS - Text-to-Speech)

Certifique-se de que seu ambiente virtual Python está ativado antes de prosseguir:

```cmd
cd C:\NinaIA
nina_env\Scripts\activate
```

## Reconhecimento de Voz (STT)

Para o reconhecimento de voz, usaremos o Faster-Whisper, uma implementação otimizada do modelo Whisper da OpenAI.

### Instalação do Faster-Whisper

1. Instale as dependências necessárias:

```cmd
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install faster-whisper
pip install pyaudio
```

2. Verifique se a instalação foi bem-sucedida:

```cmd
python -c "import faster_whisper; print('Faster-Whisper instalado com sucesso!')"
```

Se você ver a mensagem "Faster-Whisper instalado com sucesso!", a instalação foi concluída corretamente.

### Alternativa: Whisper.cpp (para computadores com recursos limitados)

Se você tiver um computador com recursos limitados ou preferir uma solução mais leve, pode usar o Whisper.cpp:

1. Baixe o repositório Whisper.cpp:
   - Acesse [https://github.com/ggerganov/whisper.cpp/releases](https://github.com/ggerganov/whisper.cpp/releases)
   - Baixe o arquivo ZIP da versão mais recente

2. Extraia o arquivo ZIP para `C:\NinaIA\whisper.cpp`

3. Baixe um modelo pré-treinado:
   - Abra o Prompt de Comando como administrador
   - Navegue até o diretório do Whisper.cpp:
   ```cmd
   cd C:\NinaIA\whisper.cpp
   ```
   - Execute o script para baixar um modelo (recomendamos o modelo "medium" para um bom equilíbrio entre precisão e desempenho):
   ```cmd
   .\models\download-ggml-model.cmd medium
   ```

4. Compile o Whisper.cpp:
   ```cmd
   mkdir build
   cd build
   cmake ..
   cmake --build . --config Release
   ```

5. Teste a instalação:
   ```cmd
   cd C:\NinaIA\whisper.cpp
   .\build\bin\Release\main.exe -m .\models\ggml-medium.bin -f samples\jfk.wav
   ```

Se você ver a transcrição do áudio de exemplo, a instalação foi bem-sucedida.

## Processamento de Linguagem Natural (LLM)

Para o processamento de linguagem natural, usaremos o Ollama, que permite executar modelos de linguagem localmente.

### Instalação do Ollama

1. Baixe o instalador do Ollama para Windows:
   - Acesse [https://ollama.com/download/windows](https://ollama.com/download/windows)
   - Baixe o instalador mais recente

2. Execute o instalador e siga as instruções na tela:
   - Aceite os termos de licença
   - Escolha o diretório de instalação (recomendado manter o padrão)
   - Conclua a instalação

3. Após a instalação, o Ollama será iniciado automaticamente e estará disponível na bandeja do sistema (área de notificação)

4. Baixe um modelo de linguagem. Abra o Prompt de Comando e execute:

```cmd
ollama pull mistral
```

Isso baixará o modelo Mistral, que é um bom equilíbrio entre desempenho e recursos. Alternativamente, você pode escolher outros modelos:

```cmd
ollama pull phi      # Modelo mais leve, bom para computadores com recursos limitados
ollama pull llama2   # Alternativa popular
```

5. Teste o modelo:

```cmd
ollama run mistral "Olá, como você está?"
```

Se você receber uma resposta do modelo, a instalação foi bem-sucedida.

### Instalação da API Python para Ollama

Para integrar o Ollama com o resto do sistema, instale a biblioteca Python:

```cmd
pip install ollama
```

## Síntese de Voz (TTS)

Para a síntese de voz, usaremos o Coqui TTS, uma biblioteca de código aberto para síntese de voz de alta qualidade.

### Instalação do Coqui TTS

1. Instale as dependências necessárias:

```cmd
pip install TTS
```

Este comando instalará a versão mais recente do Coqui TTS e suas dependências.

2. Baixe um modelo de voz pré-treinado:

```cmd
mkdir -p C:\NinaIA\models\tts
python -c "from TTS.utils.manage import ModelManager; ModelManager().download_model('tts_models/pt/cv/vits')"
```

Este comando baixará um modelo de voz em português brasileiro. Se preferir outro idioma, você pode substituir `pt` pelo código do idioma desejado (por exemplo, `en` para inglês).

3. Verifique se a instalação foi bem-sucedida:

```cmd
python -c "from TTS.api import TTS; tts = TTS('tts_models/pt/cv/vits'); print('Coqui TTS instalado com sucesso!')"
```

Se você ver a mensagem "Coqui TTS instalado com sucesso!", a instalação foi concluída corretamente.

## Instalação de Dependências Adicionais

Além dos componentes principais, precisamos instalar algumas bibliotecas auxiliares:

```cmd
pip install numpy sounddevice soundfile pydub flask requests
```

Estas bibliotecas são necessárias para processamento de áudio, comunicação entre componentes e outras funcionalidades do sistema.

## Criação da Estrutura de Diretórios

Vamos criar a estrutura de diretórios para organizar os componentes da Nina IA:

```cmd
cd C:\NinaIA
mkdir -p nina_ia\stt nina_ia\llm nina_ia\tts nina_ia\core nina_ia\data nina_ia\interface
mkdir -p nina_ia\data\profiles nina_ia\data\memory
```

Agora você tem todos os componentes principais instalados e está pronto para configurá-los e integrá-los.
