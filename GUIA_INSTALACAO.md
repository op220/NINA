# Guia de Instalação e Uso da Nina IA v2.4

## Requisitos do Sistema
- Windows 10 ou superior
- Python 3.8 ou superior
- Conexão com a internet para download de dependências
- (Opcional) GPU NVIDIA com drivers CUDA 11.8 para aceleração

## Instruções de Instalação

### Escolha o Script de Instalação Correto

Dependendo do terminal que você está usando, escolha o script de instalação apropriado:

1. **Para Prompt de Comando (CMD):**
   - Use o arquivo `install_nina_ia_windows.bat`
   - Execute com duplo clique ou via CMD

2. **Para PowerShell:**
   - Use o arquivo `install_nina_ia.ps1`
   - Execute com botão direito → "Executar com PowerShell" ou via PowerShell

### Processo de Instalação

O script de instalação irá:
1. Verificar a instalação do Python
2. Criar um ambiente virtual (venv)
3. Instalar todas as dependências necessárias
4. Configurar os arquivos e diretórios do sistema

### Resolução de Problemas Comuns

Se encontrar erros durante a instalação:

- **Erro "No module named 'yaml'":**
  ```
  pip install pyyaml
  ```

- **Erro "No module named 'sounddevice'":**
  ```
  pip install sounddevice
  ```

- **Erro "No module named 'torch'":**
  ```
  pip install torch torchvision torchaudio
  ```

## Executando a Nina IA

### Inicialização

1. Abra um terminal (CMD ou PowerShell)
2. Navegue até a pasta da Nina IA
3. Ative o ambiente virtual:
   - No CMD: `call venv\Scripts\activate`
   - No PowerShell: `.\venv\Scripts\Activate.ps1`
4. Execute a IA: `python nina.py`

### Opções de Linha de Comando

A Nina IA suporta várias opções de linha de comando:

- `--profile NOME`: Carrega um perfil específico
- `--no-cuda`: Desativa o uso de GPU
- `--debug`: Ativa o modo de depuração
- `--continuous`: Inicia em modo de escuta contínua
- `--text "COMANDO"`: Processa um único comando de texto e sai

Exemplo: `python nina.py --continuous --profile gamer`

## Configuração

Todas as configurações da Nina IA estão no arquivo `config.yaml`. Você pode editar este arquivo para personalizar o comportamento da IA:

- Configurações de servidor (host, porta)
- Módulos ativos (STT, LLM, TTS, web)
- Recursos de coaching e análise
- Recursos de visão e feedback emocional

## Funcionalidades Principais

- **Interface Web**: Acesse via navegador após iniciar a IA
- **Coaching de LoL**: Análise tática e feedback de jogos
- **Leitura de Tela**: Captura e análise de elementos visuais
- **Análise de Replays**: Processamento de replays para insights

## Solução de Problemas

Se encontrar problemas após a instalação:

1. Verifique se o ambiente virtual está ativado
2. Confirme que todas as dependências foram instaladas
3. Verifique os logs em `logs/nina_ia.log`
4. Tente reinstalar dependências específicas manualmente

Para suporte adicional, consulte a documentação ou entre em contato com a equipe de desenvolvimento.
