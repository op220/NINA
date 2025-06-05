# Testes e Verificação

Nesta seção, vamos testar cada componente da Nina IA individualmente e depois o sistema completo para garantir que tudo está funcionando corretamente.

## Teste do Reconhecimento de Voz

Vamos testar o sistema de reconhecimento de voz (STT) para verificar se ele está capturando e transcrevendo áudio corretamente:

1. Abra o Prompt de Comando como administrador

2. Navegue até o diretório da Nina IA e ative o ambiente virtual:

```cmd
cd C:\NinaIA
nina_env\Scripts\activate
```

3. Execute o teste do módulo de captura de áudio:

```cmd
python -c "from nina_ia.stt.audio_capture import test_audio_capture; test_audio_capture()"
```

Este comando iniciará a gravação de áudio. Fale algo no microfone e aguarde até que a gravação pare automaticamente (após um breve período de silêncio) ou atinja o tempo limite.

Se o teste for bem-sucedido, você verá uma mensagem indicando o caminho do arquivo de áudio gravado.

4. Execute o teste do transcritor:

```cmd
python -c "from nina_ia.stt.transcriber import test_transcriber; test_transcriber()"
```

Este comando gravará um áudio e tentará transcrevê-lo. Se o teste for bem-sucedido, você verá o texto transcrito na tela.

5. Execute o teste do módulo STT completo:

```cmd
python -c "from nina_ia.stt.stt_module import test_stt_module; test_stt_module()"
```

Este comando testará o módulo STT completo, incluindo captura de áudio e transcrição.

### Solução de Problemas Comuns do STT

- **Erro de dispositivo de áudio não encontrado**: Verifique se o microfone está conectado e funcionando corretamente. Você pode testar o microfone nas configurações do Windows.

- **Erro ao carregar o modelo Whisper**: Verifique se o CUDA está instalado corretamente (para GPU) ou tente usar a CPU como dispositivo alterando a configuração.

- **Nenhum texto transcrito**: Verifique o volume do microfone e tente falar mais alto ou mais perto do microfone.

## Teste do Processamento de Linguagem Natural

Vamos testar o sistema de processamento de linguagem natural (LLM) para verificar se ele está gerando respostas adequadas:

1. Verifique se o serviço Ollama está em execução:
   - Procure o ícone do Ollama na bandeja do sistema (área de notificação)
   - Se não estiver em execução, inicie-o pelo menu Iniciar

2. Execute o teste do cliente Ollama:

```cmd
python -c "from nina_ia.llm.ollama_client import test_ollama_client; test_ollama_client()"
```

Este comando testará a conexão com o Ollama e a geração de texto. Se o teste for bem-sucedido, você verá uma resposta gerada pelo modelo.

3. Execute o teste do processador LLM:

```cmd
python -c "from nina_ia.llm.llm_processor import test_llm_processor; test_llm_processor()"
```

Este comando testará o processador LLM, que adiciona contexto e personalidade às solicitações. Se o teste for bem-sucedido, você verá uma resposta gerada com base no contexto fornecido.

4. Execute o teste do módulo LLM completo:

```cmd
python -c "from nina_ia.llm.llm_module import test_llm_module; test_llm_module()"
```

Este comando testará o módulo LLM completo, incluindo carregamento de configuração e processamento de entrada.

### Solução de Problemas Comuns do LLM

- **Erro de conexão com o Ollama**: Verifique se o serviço Ollama está em execução. Você pode reiniciá-lo pelo menu Iniciar ou pela bandeja do sistema.

- **Modelo não encontrado**: Verifique se o modelo especificado foi baixado. Você pode baixá-lo manualmente com o comando `ollama pull mistral` (ou outro modelo).

- **Respostas muito lentas**: Verifique se o modelo está sendo executado na GPU. Se estiver usando CPU, considere usar um modelo menor como "phi" em vez de "mistral".

## Teste da Síntese de Voz

Vamos testar o sistema de síntese de voz (TTS) para verificar se ele está gerando e reproduzindo áudio corretamente:

1. Execute o teste do sintetizador TTS:

```cmd
python -c "from nina_ia.tts.tts_synthesizer import test_tts_synthesizer; test_tts_synthesizer()"
```

Este comando testará o sintetizador TTS, que converte texto em áudio. Se o teste for bem-sucedido, você ouvirá uma mensagem de áudio sintetizada.

2. Execute o teste do player de áudio:

```cmd
python -c "from nina_ia.tts.audio_player import test_audio_player; test_audio_player()"
```

Este comando testará o player de áudio, que reproduz arquivos de áudio. Se o teste for bem-sucedido, você ouvirá um som de beep.

3. Execute o teste do módulo TTS completo:

```cmd
python -c "from nina_ia.tts.tts_module import test_tts_module; test_tts_module()"
```

Este comando testará o módulo TTS completo, incluindo síntese e reprodução de áudio.

### Solução de Problemas Comuns do TTS

- **Erro ao carregar o modelo TTS**: Verifique se o modelo foi baixado corretamente. Você pode tentar baixá-lo novamente com o comando fornecido na seção de instalação.

- **Nenhum áudio reproduzido**: Verifique se os alto-falantes estão conectados e funcionando corretamente. Verifique também o volume do sistema.

- **Erro de dispositivo de áudio não encontrado**: Verifique se o dispositivo de saída de áudio está configurado corretamente nas configurações do Windows.

## Teste dos Componentes de Integração

Vamos testar os componentes de integração para verificar se eles estão funcionando corretamente:

1. Execute o teste do gerenciador de personalidade:

```cmd
python -c "from nina_ia.core.personality_manager import test_personality_manager; test_personality_manager()"
```

Este comando testará o gerenciador de personalidade, que carrega e gerencia perfis. Se o teste for bem-sucedido, você verá informações sobre o perfil padrão e operações de criação/exclusão de perfis.

2. Execute o teste do gerenciador de sessão:

```cmd
python -c "from nina_ia.core.session_manager import test_session_manager; test_session_manager()"
```

Este comando testará o gerenciador de sessão, que mantém o contexto da conversa. Se o teste for bem-sucedido, você verá informações sobre a sessão criada e as interações adicionadas.

3. Execute o teste do orquestrador:

```cmd
python -c "from nina_ia.core.orchestrator import test_orchestrator; test_orchestrator()"
```

Este comando testará o orquestrador, que coordena os componentes da Nina IA. Este teste inclui processamento de texto e síntese de voz, e opcionalmente entrada de voz se você escolher testá-la.

### Solução de Problemas Comuns dos Componentes de Integração

- **Erro ao carregar perfil**: Verifique se o arquivo de perfil padrão existe no diretório `nina_ia\data\profiles`.

- **Erro ao criar sessão**: Verifique se o diretório `nina_ia\data\sessions` existe e se você tem permissão para escrever nele.

- **Erro no orquestrador**: Verifique se todos os componentes individuais (STT, LLM, TTS) estão funcionando corretamente.

## Teste do Sistema Completo

Finalmente, vamos testar o sistema completo para verificar se todos os componentes estão funcionando juntos corretamente:

1. Execute a Nina IA:

```cmd
python nina_ia\interface\nina_ia.py
```

Ou use o script batch:

```cmd
start_nina.bat
```

2. A Nina IA iniciará e reproduzirá uma saudação. Em seguida, ela entrará em modo de escuta, aguardando sua entrada de voz.

3. Fale algo quando solicitado e aguarde a resposta. A Nina IA deve:
   - Capturar sua voz
   - Transcrever o áudio em texto
   - Processar o texto e gerar uma resposta
   - Sintetizar a resposta em áudio
   - Reproduzir o áudio

4. Continue a conversa ou pressione Ctrl+C para encerrar o programa.

### Testes Adicionais

Você também pode testar a Nina IA com entrada de texto direta:

```cmd
python nina_ia\interface\nina_ia.py --text "Olá, como você está?"
```

Ou testar apenas a entrada de voz:

```cmd
python nina_ia\interface\nina_ia.py --voice
```

### Solução de Problemas do Sistema Completo

- **Erro ao iniciar**: Verifique se todos os componentes foram instalados corretamente e se os arquivos de configuração existem.

- **Nenhuma resposta à entrada de voz**: Verifique se o microfone está funcionando e se o módulo STT está configurado corretamente.

- **Nenhuma resposta de áudio**: Verifique se os alto-falantes estão funcionando e se o módulo TTS está configurado corretamente.

- **Respostas inadequadas**: Verifique se o modelo LLM está carregado corretamente e se o serviço Ollama está em execução.

## Verificação de Logs

A Nina IA gera logs detalhados que podem ajudar a diagnosticar problemas. Verifique o arquivo de log:

```cmd
type nina_ia\nina_ia.log
```

Os logs incluem informações sobre inicialização, processamento de entrada, geração de resposta e erros encontrados.

## Verificação de Recursos do Sistema

A Nina IA pode ser intensiva em recursos, especialmente ao usar GPU para aceleração. Verifique o uso de recursos:

1. Abra o Gerenciador de Tarefas (pressione Ctrl+Shift+Esc)

2. Verifique o uso de CPU, memória e GPU durante a execução da Nina IA

3. Se o uso de recursos for muito alto, considere:
   - Usar modelos menores (por exemplo, "phi" em vez de "mistral" para o LLM)
   - Reduzir o tamanho do modelo Whisper (por exemplo, "small" em vez de "medium")
   - Desativar o cache de áudio do TTS se estiver com pouca memória

Agora que você verificou que todos os componentes estão funcionando corretamente, você pode começar a usar a Nina IA para suas necessidades diárias. Na próxima seção, abordaremos problemas comuns e suas soluções.
