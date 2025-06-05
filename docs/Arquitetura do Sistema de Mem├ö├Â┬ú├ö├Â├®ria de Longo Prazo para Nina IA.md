# Arquitetura do Sistema de Memória de Longo Prazo para Nina IA

## Visão Geral

O Sistema de Memória de Longo Prazo é um componente modular que permite à Nina IA armazenar, recuperar e utilizar informações sobre usuários e canais do Discord ao longo do tempo. A arquitetura foi projetada para ser completamente local, eficiente e facilmente integrável ao sistema Nina IA existente.

## Diagrama de Arquitetura

```
+---------------------+    +----------------------+    +----------------------+
| Sistema Nina IA     |<-->| Gerenciador de       |<-->| Banco de Dados       |
| (Existente)         |    | Memória              |    | (SQLite + JSON)      |
+---------------------+    +----------------------+    +----------------------+
                                    ^                            ^
                                    |                            |
                                    v                            v
+---------------------+    +----------------------+    +----------------------+
| Interface Web       |<-->| API de Acesso        |<-->| Analisador de        |
| (Svelte + FastAPI)  |    | à Memória            |    | Padrões              |
+---------------------+    +----------------------+    +----------------------+
```

## Componentes Principais

### 1. Gerenciador de Memória

O Gerenciador de Memória é o componente central que coordena o armazenamento, recuperação e atualização das informações na memória de longo prazo.

#### Responsabilidades:
- Gerenciar o ciclo de vida dos dados na memória
- Coordenar a persistência dos dados
- Fornecer uma API para acesso aos dados
- Implementar políticas de retenção e atualização de dados

#### Subcomponentes:
- **UserMemoryManager**: Gerencia memórias relacionadas a usuários
- **ChannelMemoryManager**: Gerencia memórias relacionadas a canais
- **InteractionMemoryManager**: Gerencia registros de interações
- **MemoryIndexer**: Indexa memórias para recuperação eficiente

### 2. Banco de Dados

O sistema utiliza uma combinação de SQLite e JSON para armazenamento persistente de dados.

#### Estrutura do SQLite:

```sql
-- Tabela de Usuários
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    username TEXT,
    first_seen TIMESTAMP,
    last_seen TIMESTAMP,
    interaction_count INTEGER DEFAULT 0,
    voice_participation_count INTEGER DEFAULT 0,
    metadata_path TEXT  -- Caminho para o arquivo JSON com dados adicionais
);

-- Tabela de Canais
CREATE TABLE channels (
    channel_id TEXT PRIMARY KEY,
    guild_id TEXT,
    channel_name TEXT,
    channel_type TEXT,
    first_activity TIMESTAMP,
    last_activity TIMESTAMP,
    message_count INTEGER DEFAULT 0,
    metadata_path TEXT,  -- Caminho para o arquivo JSON com dados adicionais
    FOREIGN KEY (guild_id) REFERENCES guilds(guild_id)
);

-- Tabela de Servidores (Guilds)
CREATE TABLE guilds (
    guild_id TEXT PRIMARY KEY,
    guild_name TEXT,
    first_activity TIMESTAMP,
    last_activity TIMESTAMP,
    metadata_path TEXT  -- Caminho para o arquivo JSON com dados adicionais
);

-- Tabela de Interações
CREATE TABLE interactions (
    interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    channel_id TEXT,
    timestamp TIMESTAMP,
    interaction_type TEXT,
    content_summary TEXT,
    sentiment_score REAL,
    topics TEXT,  -- Tópicos separados por vírgula ou JSON serializado
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id)
);

-- Tabela de Relações Usuário-Canal
CREATE TABLE user_channel_stats (
    user_id TEXT,
    channel_id TEXT,
    message_count INTEGER DEFAULT 0,
    last_interaction TIMESTAMP,
    participation_score REAL DEFAULT 0.0,
    PRIMARY KEY (user_id, channel_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id)
);

-- Tabela de Palavras Frequentes por Usuário
CREATE TABLE user_frequent_words (
    user_id TEXT,
    word TEXT,
    count INTEGER DEFAULT 0,
    last_used TIMESTAMP,
    PRIMARY KEY (user_id, word),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Tabela de Tópicos por Usuário
CREATE TABLE user_topics (
    user_id TEXT,
    topic TEXT,
    relevance_score REAL DEFAULT 0.0,
    last_discussed TIMESTAMP,
    PRIMARY KEY (user_id, topic),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Tabela de Tópicos por Canal
CREATE TABLE channel_topics (
    channel_id TEXT,
    topic TEXT,
    relevance_score REAL DEFAULT 0.0,
    last_discussed TIMESTAMP,
    PRIMARY KEY (channel_id, topic),
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id)
);
```

#### Estrutura dos Arquivos JSON:

**Metadados de Usuário** (`user_{id}.json`):
```json
{
  "user_id": "123456789",
  "username": "ExemploUsuário",
  "frequent_expressions": [
    {"expression": "nossa senhora", "count": 15, "last_used": "2025-04-24T12:34:56"},
    {"expression": "caramba meu", "count": 8, "last_used": "2025-04-23T10:20:30"}
  ],
  "emotions": {
    "predominant": "feliz",
    "distribution": {
      "feliz": 0.6,
      "neutro": 0.3,
      "bravo": 0.05,
      "triste": 0.05
    },
    "last_updated": "2025-04-24T15:30:45"
  },
  "topics": [
    {"name": "animes", "relevance": 0.85, "last_discussed": "2025-04-24T14:20:10"},
    {"name": "música", "relevance": 0.65, "last_discussed": "2025-04-23T18:45:30"},
    {"name": "trabalho", "relevance": 0.45, "last_discussed": "2025-04-22T09:15:00"}
  ],
  "voice_activity": {
    "total_time": 7200,  // segundos
    "average_session": 1200,  // segundos
    "last_session": "2025-04-24T20:00:00",
    "preferred_channels": [
      {"channel_id": "987654321", "time_spent": 5400},
      {"channel_id": "123789456", "time_spent": 1800}
    ]
  },
  "interaction_patterns": {
    "active_hours": [20, 21, 22, 23],  // horas do dia (UTC)
    "active_days": [1, 3, 5, 6],  // dias da semana (0=domingo)
    "response_rate": 0.75,  // taxa de resposta a menções
    "average_message_length": 42  // caracteres
  }
}
```

**Metadados de Canal** (`channel_{id}.json`):
```json
{
  "channel_id": "987654321",
  "guild_id": "456789123",
  "name": "geral",
  "tone": {
    "predominant": "informal",
    "distribution": {
      "informal": 0.7,
      "técnico": 0.2,
      "caótico": 0.1
    },
    "last_updated": "2025-04-24T15:30:45"
  },
  "recurring_themes": [
    {"name": "jogos", "relevance": 0.9, "last_discussed": "2025-04-24T14:20:10"},
    {"name": "tecnologia", "relevance": 0.75, "last_discussed": "2025-04-23T18:45:30"},
    {"name": "filmes", "relevance": 0.6, "last_discussed": "2025-04-22T09:15:00"}
  ],
  "activity_patterns": {
    "peak_hours": [19, 20, 21, 22],  // horas do dia (UTC)
    "peak_days": [0, 5, 6],  // dias da semana (0=domingo)
    "messages_per_day": 125,
    "average_participants": 8
  },
  "nina_personality": {
    "formality_level": 30,  // 0-100
    "humor_level": 70,      // 0-100
    "technicality_level": 50,  // 0-100
    "response_speed": "rápido",  // lento, médio, rápido
    "verbosity": "médio",  // conciso, médio, detalhado
    "last_updated": "2025-04-24T12:00:00"
  },
  "active_users": [
    {"user_id": "123456789", "message_count": 350, "last_active": "2025-04-24T14:20:10"},
    {"user_id": "987123456", "message_count": 275, "last_active": "2025-04-24T15:30:45"}
  ]
}
```

### 3. Analisador de Padrões

O Analisador de Padrões processa as mensagens e interações para extrair informações relevantes sobre usuários e canais.

#### Responsabilidades:
- Analisar o conteúdo das mensagens
- Identificar emoções e sentimentos
- Extrair tópicos e palavras-chave
- Detectar padrões de comunicação
- Atualizar perfis de usuários e canais

#### Subcomponentes:
- **SentimentAnalyzer**: Analisa sentimentos e emoções nas mensagens
- **TopicExtractor**: Extrai tópicos e palavras-chave
- **PatternDetector**: Identifica padrões de comunicação
- **ProfileUpdater**: Atualiza perfis com base nas análises

### 4. API de Acesso à Memória

A API de Acesso à Memória fornece uma interface para que outros componentes do sistema possam acessar e manipular os dados da memória de longo prazo.

#### Endpoints Principais:
- `/users/{user_id}`: Acesso a informações de usuários
- `/channels/{channel_id}`: Acesso a informações de canais
- `/interactions`: Acesso a registros de interações
- `/search`: Busca por informações específicas
- `/update`: Atualização de informações

#### Métodos:
- `GET`: Recuperação de informações
- `POST`: Criação de novos registros
- `PUT`: Atualização de registros existentes
- `DELETE`: Remoção de registros

### 5. Interface Web

A Interface Web permite visualizar e editar as informações armazenadas na memória de longo prazo.

#### Funcionalidades:
- Visualização de perfis de usuários
- Visualização de informações de canais
- Edição de memórias e configurações
- Visualização de estatísticas e gráficos
- Controle de personalidade da IA

## Fluxos de Dados

### 1. Captura e Armazenamento de Memória

```
1. Nina IA recebe uma mensagem do Discord
2. Gerenciador de Memória extrai informações relevantes
3. Analisador de Padrões processa o conteúdo
4. Informações são armazenadas no banco de dados
5. Índices são atualizados para facilitar recuperação futura
```

### 2. Recuperação e Uso de Memória

```
1. Nina IA precisa gerar uma resposta
2. Gerenciador de Memória consulta informações relevantes
3. Informações são recuperadas do banco de dados
4. Nina IA utiliza as informações para contextualizar a resposta
5. A resposta é enviada ao usuário
```

### 3. Atualização de Memória via Interface Web

```
1. Usuário acessa a interface web
2. Interface web consulta informações via API
3. Usuário edita informações
4. Interface web envia atualizações via API
5. Gerenciador de Memória atualiza o banco de dados
```

## Integração com o Sistema Nina IA Existente

A integração com o sistema Nina IA existente será feita através de uma interface de plugin que permitirá:

1. **Captura de Eventos**: O sistema Nina IA enviará eventos de mensagens e interações para o Gerenciador de Memória.

2. **Consulta de Contexto**: Antes de gerar uma resposta, o sistema Nina IA consultará o Gerenciador de Memória para obter informações relevantes sobre o usuário e o canal.

3. **Adaptação de Personalidade**: O sistema Nina IA ajustará sua personalidade com base nas informações do canal armazenadas na memória.

4. **Feedback de Interações**: Após cada interação, o sistema Nina IA enviará feedback para o Gerenciador de Memória para atualização das informações.

## Considerações de Desempenho e Escalabilidade

1. **Indexação Eficiente**: Implementação de índices no SQLite para consultas rápidas.

2. **Cache em Memória**: Uso de cache para informações frequentemente acessadas.

3. **Processamento Assíncrono**: Análise de padrões e atualizações de perfil realizadas de forma assíncrona para não bloquear o fluxo principal.

4. **Compactação de Dados**: Armazenamento eficiente de dados históricos com compactação.

5. **Políticas de Retenção**: Implementação de políticas para limitar o crescimento do banco de dados, priorizando informações mais recentes e relevantes.

## Segurança e Privacidade

1. **Armazenamento Local**: Todos os dados são armazenados localmente, sem envio para servidores externos.

2. **Criptografia**: Opção para criptografar dados sensíveis no banco de dados.

3. **Controle de Acesso**: Interface web protegida por autenticação.

4. **Anonimização**: Opção para anonimizar dados para análise estatística.

5. **Exclusão de Dados**: Funcionalidade para excluir dados de usuários específicos quando solicitado.

## Próximos Passos

1. Implementar o esquema do banco de dados SQLite
2. Desenvolver o Gerenciador de Memória
3. Implementar o Analisador de Padrões
4. Desenvolver a API de Acesso à Memória
5. Integrar com o sistema Nina IA existente
6. Desenvolver a Interface Web
