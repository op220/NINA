# Solução de Problemas

Nesta seção, abordaremos problemas comuns que podem surgir durante a instalação, configuração e uso da Nina IA, junto com suas soluções. Esta seção é organizada por categorias de problemas para facilitar a localização da solução adequada.

## Problemas de Instalação

### Problemas com Python

**Problema**: Erro "Python não é reconhecido como um comando interno ou externo"  
**Solução**: O Python não foi adicionado ao PATH do sistema. Reinstale o Python marcando a opção "Add Python to PATH" ou adicione manualmente o diretório do Python ao PATH do sistema.

**Problema**: Erro ao instalar pacotes com pip  
**Solução**: 
1. Verifique sua conexão com a internet
2. Atualize o pip: `python -m pip install --upgrade pip`
3. Se estiver atrás de um proxy, configure o pip para usá-lo: `pip install --proxy=http://user:password@proxyserver:port package_name`
4. Tente usar um mirror alternativo: `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple package_name`

**Problema**: Conflitos de dependências durante a instalação  
**Solução**: Use um ambiente virtual para isolar as dependências:
```cmd
python -m venv nina_env_new
nina_env_new\Scripts\activate
pip install -r requirements.txt
```

### Problemas com CUDA

**Problema**: Erro "CUDA not available" ao usar GPU  
**Solução**:
1. Verifique se sua GPU é compatível com CUDA
2. Reinstale o CUDA Toolkit e os drivers NVIDIA mais recentes
3. Verifique a instalação com: `nvcc --version` e `nvidia-smi`
4. Se o problema persistir, configure a Nina IA para usar CPU em vez de GPU editando os arquivos de configuração

**Problema**: Erro "CUDA out of memory"  
**Solução**:
1. Reduza o tamanho do modelo (use "small" em vez de "medium" para Whisper)
2. Feche outros aplicativos que possam estar usando a GPU
3. Reduza o tamanho do batch ou outras configurações de memória
4. Se necessário, configure para usar CPU em vez de GPU

### Problemas com Ollama

**Problema**: Erro de conexão com o Ollama  
**Solução**:
1. Verifique se o Ollama está instalado e em execução
2. Reinicie o serviço Ollama
3. Verifique se não há firewall bloqueando a conexão na porta 11434
4. Reinstale o Ollama se necessário

**Problema**: Erro ao baixar modelos no Ollama  
**Solução**:
1. Verifique sua conexão com a internet
2. Verifique se você tem espaço suficiente em disco
3. Execute como administrador: `ollama pull mistral`
4. Tente um modelo menor se estiver com pouco espaço em disco: `ollama pull phi`

### Problemas com TTS

**Problema**: Erro ao baixar modelos TTS  
**Solução**:
1. Verifique sua conexão com a internet
2. Baixe manualmente o modelo e coloque-o no diretório correto
3. Tente um modelo alternativo: `python -c "from TTS.utils.manage import ModelManager; ModelManager().download_model('tts_models/en/ljspeech/tacotron2-DDC')"`

**Problema**: Erro "No module named 'sounddevice'"  
**Solução**: Instale as dependências de áudio:
```cmd
pip install sounddevice soundfile
```

## Problemas de Configuração

### Problemas com Arquivos de Configuração

**Problema**: Erro "File not found" ao carregar configuração  
**Solução**:
1. Verifique se os diretórios de configuração existem:
```cmd
mkdir -p nina_ia\data\config
```
2. Crie os arquivos de configuração manualmente conforme descrito na seção de integração

**Problema**: Configurações não são aplicadas  
**Solução**:
1. Verifique se os arquivos JSON estão formatados corretamente (sem erros de sintaxe)
2. Reinicie a Nina IA completamente após alterar configurações
3. Verifique os logs para ver se há erros ao carregar configurações

### Problemas com Estrutura de Diretórios

**Problema**: Erro "Module not found" ao executar a Nina IA  
**Solução**:
1. Verifique se a estrutura de diretórios está correta:
```cmd
dir C:\NinaIA\nina_ia
```
2. Verifique se todos os arquivos Python foram criados nos locais corretos
3. Verifique se você está executando os comandos do diretório raiz (C:\NinaIA)
4. Verifique se o ambiente virtual está ativado

## Problemas de Execução

### Problemas de Reconhecimento de Voz

**Problema**: Microfone não detectado  
**Solução**:
1. Verifique se o microfone está conectado e funcionando nas configurações do Windows
2. Verifique as permissões de acesso ao microfone nas configurações de privacidade do Windows
3. Tente um dispositivo de áudio diferente
4. Especifique o índice do dispositivo manualmente no código:
```python
# Em nina_ia/stt/audio_capture.py, modifique a linha:
self.device_index = None
# Para:
self.device_index = 1  # Tente diferentes números (0, 1, 2, etc.)
```

**Problema**: Transcrição de baixa qualidade  
**Solução**:
1. Reduza o ruído de fundo
2. Fale mais claramente e mais perto do microfone
3. Ajuste o `silence_threshold` no arquivo `audio_capture.py` para um valor mais baixo se a gravação parar muito cedo
4. Use um modelo maior (como "large") para melhor precisão, se tiver recursos suficientes

### Problemas de Processamento de Linguagem Natural

**Problema**: Respostas muito lentas  
**Solução**:
1. Use um modelo menor (como "phi" em vez de "mistral")
2. Verifique se o modelo está sendo executado na GPU
3. Reduza o valor de `max_tokens` na configuração do LLM
4. Feche outros aplicativos que possam estar consumindo recursos

**Problema**: Respostas inadequadas ou sem sentido  
**Solução**:
1. Verifique se o modelo correto está sendo usado
2. Ajuste o valor de `temperature` na configuração (valores mais baixos produzem respostas mais determinísticas)
3. Modifique o `system_prompt` para ser mais específico sobre o comportamento desejado
4. Verifique se há contexto suficiente sendo fornecido para o modelo

### Problemas de Síntese de Voz

**Problema**: Sem saída de áudio  
**Solução**:
1. Verifique se os alto-falantes estão conectados e funcionando nas configurações do Windows
2. Verifique o volume do sistema
3. Tente um dispositivo de saída de áudio diferente
4. Verifique se as bibliotecas de áudio estão instaladas: `pip install sounddevice soundfile pydub`

**Problema**: Qualidade de voz ruim  
**Solução**:
1. Tente um modelo TTS diferente
2. Ajuste a velocidade e o tom na configuração do perfil
3. Use um modelo específico para o idioma que você está usando

## Problemas de Desempenho

**Problema**: Uso excessivo de CPU/GPU  
**Solução**:
1. Use modelos menores para todos os componentes
2. Reduza o tamanho do contexto no LLM
3. Desative recursos não essenciais (como cache de áudio)
4. Feche outros aplicativos que consomem muitos recursos

**Problema**: Uso excessivo de memória  
**Solução**:
1. Use modelos menores
2. Reduza o tamanho do cache de áudio no TTS
3. Limpe periodicamente a memória temporária:
```cmd
rmdir /S /Q C:\NinaIA\nina_ia\data\temp
mkdir C:\NinaIA\nina_ia\data\temp
```

**Problema**: Inicialização muito lenta  
**Solução**:
1. Pré-carregue os modelos e mantenha o serviço Ollama em execução
2. Use modelos menores
3. Armazene os modelos em um SSD em vez de um HDD
4. Desative componentes não essenciais se não forem necessários

## Logs e Diagnóstico

### Como Verificar Logs

A Nina IA gera logs detalhados que podem ajudar a diagnosticar problemas. Os logs são salvos em:
- `C:\NinaIA\nina_ia.log` (log principal)
- Logs de componentes individuais no console

Para visualizar o log principal:
```cmd
type C:\NinaIA\nina_ia.log
```

Para visualizar apenas as últimas linhas do log:
```cmd
powershell -command "Get-Content C:\NinaIA\nina_ia.log -Tail 50"
```

### Níveis de Log

Os logs da Nina IA têm diferentes níveis de severidade:
- **INFO**: Informações gerais sobre a execução
- **WARNING**: Avisos que não impedem a execução, mas podem indicar problemas
- **ERROR**: Erros que podem afetar a funcionalidade
- **CRITICAL**: Erros graves que impedem a execução

Para alterar o nível de log, modifique a linha em cada arquivo Python:
```python
logging.basicConfig(level=logging.INFO, ...)
```
Para um log mais detalhado, use `logging.DEBUG`. Para menos detalhes, use `logging.WARNING` ou `logging.ERROR`.

## Reinstalação e Recuperação

Se você encontrar problemas persistentes que não consegue resolver, pode ser necessário reinstalar a Nina IA:

1. Faça backup de seus dados importantes:
```cmd
xcopy /E /I C:\NinaIA\nina_ia\data C:\NinaIA_backup\data
```

2. Remova a instalação atual:
```cmd
rmdir /S /Q C:\NinaIA
```

3. Siga o tutorial de instalação novamente desde o início

4. Restaure seus dados:
```cmd
xcopy /E /I C:\NinaIA_backup\data C:\NinaIA\nina_ia\data
```

## Recursos Adicionais

Se você continuar enfrentando problemas, aqui estão alguns recursos adicionais que podem ajudar:

- **Documentação do Whisper/Faster-Whisper**: [https://github.com/guillaumekln/faster-whisper/](https://github.com/guillaumekln/faster-whisper/)
- **Documentação do Ollama**: [https://ollama.com/docs](https://ollama.com/docs)
- **Documentação do Coqui TTS**: [https://github.com/coqui-ai/TTS](https://github.com/coqui-ai/TTS)
- **Fóruns de Suporte**:
  - Stack Overflow: [https://stackoverflow.com/](https://stackoverflow.com/) (use as tags relevantes)
  - Reddit: [https://www.reddit.com/r/LocalLLaMA/](https://www.reddit.com/r/LocalLLaMA/)
  - Discord do Ollama: [https://discord.gg/ollama](https://discord.gg/ollama)

## Perguntas Frequentes

**P: A Nina IA funciona sem internet?**  
R: Sim, após a instalação e download dos modelos, a Nina IA funciona 100% offline.

**P: Posso usar a Nina IA em um computador sem GPU?**  
R: Sim, mas o desempenho será significativamente mais lento. Recomendamos usar modelos menores (como "tiny" para Whisper e "phi" para LLM) e configurar todos os componentes para usar CPU.

**P: Quanto espaço em disco a Nina IA ocupa?**  
R: Dependendo dos modelos escolhidos, a Nina IA pode ocupar de 2GB a 15GB de espaço em disco.

**P: Posso usar outros modelos de linguagem além dos mencionados?**  
R: Sim, o Ollama suporta vários modelos. Você pode ver a lista completa com `ollama list` e baixar novos modelos com `ollama pull nome_do_modelo`.

**P: Como posso personalizar a voz da Nina IA?**  
R: Você pode escolher diferentes modelos TTS e ajustar a velocidade e o tom no arquivo de perfil (`default_profile.json`).

**P: A Nina IA pode controlar outros dispositivos ou programas no meu computador?**  
R: Não por padrão. A implementação atual é focada em conversação. Para adicionar controle de dispositivos ou programas, seria necessário desenvolver módulos adicionais.

**P: Como posso contribuir para o desenvolvimento da Nina IA?**  
R: Como este é um projeto local, você pode modificar o código conforme necessário para suas próprias necessidades. Se desejar compartilhar suas melhorias, considere criar um repositório Git para o projeto.

**P: Posso usar a Nina IA em outros idiomas além do português?**  
R: Sim, você pode modificar as configurações para usar outros idiomas. Você precisará:
1. Alterar o idioma no STT (`language` no arquivo de configuração)
2. Usar um modelo TTS para o idioma desejado
3. Modificar o `system_prompt` do LLM para responder no idioma desejado
