# Pesquisa de Tecnologias para Sistema de Aprendizado de Personalidade

## Diarização de Falantes
- **pyannote.audio**: Biblioteca Python de código aberto para diarização de falantes
  - Baseada no framework PyTorch
  - Fornece blocos de construção neurais para identificação de diferentes falantes
  - Documentação: https://github.com/pyannote/pyannote-audio
  - Pode ser integrada com Whisper para transcrição + diarização

## Integração com Discord
- **discord.py**: Biblioteca principal para interação com a API do Discord
  - Suporta conexão a canais de voz
- **discord-ext-voice-recv**: Extensão para discord.py que permite capturar áudio
  - API espelha a API de envio de áudio do discord.py
  - Disponível em: https://pypi.org/project/discord-ext-voice-recv/
- Exemplos práticos disponíveis em repositórios como:
  - https://github.com/realhardik18/discord.py-voice-recorder

## Análise de Sentimentos e Padrões
- **Processamento de Linguagem Natural (NLP)** para análise de sentimentos
  - Identificação de polaridade (positiva, negativa, neutra)
  - Extração de informações subjetivas do texto
  - Classificação de tom emocional das mensagens
- Bibliotecas potenciais:
  - NLTK
  - spaCy
  - Transformers (HuggingFace)
  - TextBlob para análise de sentimentos simples

## Armazenamento de Personalidade
- **JSON Schema** para definir a estrutura do arquivo persona.json
  - Permite definir regras e restrições para cada campo
  - Facilita a validação dos dados
  - Suporta tipos específicos para cada campo

## Próximos Passos
1. Explorar em detalhes a implementação da diarização com pyannote.audio
2. Investigar exemplos práticos de captura de áudio do Discord
3. Testar bibliotecas de análise de sentimentos para identificar a mais adequada
4. Definir o esquema JSON para o arquivo de personalidade dinâmica
