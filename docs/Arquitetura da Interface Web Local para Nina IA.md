# Arquitetura da Interface Web Local para Nina IA

## Visão Geral

A Interface Web Local é um componente que permite visualizar e editar as informações armazenadas no sistema de memória de longo prazo da Nina IA através de um navegador. A interface é acessível via localhost e fornece uma experiência de usuário intuitiva para gerenciar perfis de usuários, memórias de canais e configurações de personalidade.

## Diagrama de Arquitetura

```
+---------------------+    +----------------------+    +----------------------+
| Frontend            |<-->| Backend API          |<-->| Sistema de Memória   |
| (Svelte + TailwindCSS) |    | (FastAPI)            |    | (Existente)          |
+---------------------+    +----------------------+    +----------------------+
        |                           |
        v                           v
+---------------------+    +----------------------+
| Componentes de UI   |    | Endpoints da API     |
| - Painéis           |    | - Usuários           |
| - Gráficos          |    | - Canais             |
| - Formulários       |    | - Interações         |
+---------------------+    +----------------------+
```

## Componentes Principais

### 1. Backend API (FastAPI)

O Backend API é responsável por fornecer endpoints para acessar e manipular os dados do sistema de memória.

#### Responsabilidades:
- Fornecer endpoints RESTful para acesso aos dados
- Validar requisições e respostas
- Gerenciar autenticação e autorização (básica para acesso local)
- Integrar com o sistema de memória existente

#### Estrutura de Diretórios:
```
/nina_ia/web/backend/
  ├── main.py                # Ponto de entrada da aplicação
  ├── config.py              # Configurações da API
  ├── auth.py                # Autenticação básica
  ├── routers/
  │   ├── users.py           # Endpoints de usuários
  │   ├── channels.py        # Endpoints de canais
  │   ├── interactions.py    # Endpoints de interações
  │   ├── statistics.py      # Endpoints de estatísticas
  │   └── settings.py        # Endpoints de configurações
  ├── models/
  │   ├── user.py            # Modelos de dados de usuários
  │   ├── channel.py         # Modelos de dados de canais
  │   ├── interaction.py     # Modelos de dados de interações
  │   └── settings.py        # Modelos de dados de configurações
  └── utils/
      ├── memory_client.py   # Cliente para o sistema de memória
      └── response.py        # Utilitários para formatação de respostas
```

#### Endpoints Principais:

**Usuários:**
- `GET /api/users` - Lista todos os usuários
- `GET /api/users/{user_id}` - Obtém detalhes de um usuário
- `PUT /api/users/{user_id}` - Atualiza informações de um usuário
- `DELETE /api/users/{user_id}/memory` - Remove memórias de um usuário
- `GET /api/users/{user_id}/interactions` - Lista interações de um usuário
- `GET /api/users/{user_id}/topics` - Lista tópicos de interesse de um usuário
- `GET /api/users/{user_id}/expressions` - Lista expressões frequentes de um usuário

**Canais:**
- `GET /api/channels` - Lista todos os canais
- `GET /api/channels/{channel_id}` - Obtém detalhes de um canal
- `PUT /api/channels/{channel_id}` - Atualiza informações de um canal
- `GET /api/channels/{channel_id}/interactions` - Lista interações em um canal
- `GET /api/channels/{channel_id}/topics` - Lista tópicos recorrentes em um canal
- `GET /api/channels/{channel_id}/users` - Lista usuários ativos em um canal
- `GET /api/channels/{channel_id}/personality` - Obtém personalidade da Nina para o canal
- `PUT /api/channels/{channel_id}/personality` - Atualiza personalidade da Nina para o canal

**Interações:**
- `GET /api/interactions` - Lista interações recentes
- `GET /api/interactions/{interaction_id}` - Obtém detalhes de uma interação
- `DELETE /api/interactions/{interaction_id}` - Remove uma interação

**Estatísticas:**
- `GET /api/statistics` - Obtém estatísticas gerais
- `GET /api/statistics/users` - Obtém estatísticas de usuários
- `GET /api/statistics/channels` - Obtém estatísticas de canais
- `GET /api/statistics/topics` - Obtém estatísticas de tópicos

**Configurações:**
- `GET /api/settings` - Obtém configurações do sistema
- `PUT /api/settings` - Atualiza configurações do sistema
- `POST /api/settings/backup` - Cria um backup do sistema
- `POST /api/settings/restore` - Restaura o sistema a partir de um backup

### 2. Frontend (Svelte + TailwindCSS)

O Frontend é responsável por fornecer uma interface de usuário intuitiva para visualizar e editar os dados do sistema de memória.

#### Responsabilidades:
- Fornecer uma interface de usuário responsiva e intuitiva
- Comunicar-se com o Backend API
- Visualizar dados em formatos adequados (tabelas, gráficos, etc.)
- Fornecer formulários para edição de dados

#### Estrutura de Diretórios:
```
/nina_ia/web/frontend/
  ├── public/                # Arquivos estáticos
  │   ├── index.html         # Página HTML principal
  │   ├── favicon.ico        # Ícone do site
  │   └── assets/            # Outros ativos estáticos
  ├── src/
  │   ├── main.js            # Ponto de entrada da aplicação
  │   ├── App.svelte         # Componente principal
  │   ├── routes/            # Componentes de rotas
  │   │   ├── Home.svelte    # Página inicial
  │   │   ├── Users.svelte   # Página de usuários
  │   │   ├── Channels.svelte # Página de canais
  │   │   ├── Settings.svelte # Página de configurações
  │   │   └── Statistics.svelte # Página de estatísticas
  │   ├── components/        # Componentes reutilizáveis
  │   │   ├── Sidebar.svelte # Barra lateral
  │   │   ├── Header.svelte  # Cabeçalho
  │   │   ├── UserCard.svelte # Card de usuário
  │   │   ├── ChannelCard.svelte # Card de canal
  │   │   ├── TopicList.svelte # Lista de tópicos
  │   │   ├── InteractionList.svelte # Lista de interações
  │   │   ├── PersonalityEditor.svelte # Editor de personalidade
  │   │   └── Charts/        # Componentes de gráficos
  │   │       ├── BarChart.svelte # Gráfico de barras
  │   │       ├── LineChart.svelte # Gráfico de linhas
  │   │       └── PieChart.svelte # Gráfico de pizza
  │   ├── stores/            # Stores Svelte
  │   │   ├── users.js       # Store de usuários
  │   │   ├── channels.js    # Store de canais
  │   │   ├── settings.js    # Store de configurações
  │   │   └── statistics.js  # Store de estatísticas
  │   ├── services/          # Serviços de API
  │   │   ├── api.js         # Cliente de API
  │   │   ├── users.js       # Serviço de usuários
  │   │   ├── channels.js    # Serviço de canais
  │   │   └── settings.js    # Serviço de configurações
  │   └── utils/             # Utilitários
  │       ├── formatters.js  # Formatadores de dados
  │       └── validators.js  # Validadores de formulários
  ├── package.json           # Dependências do projeto
  ├── rollup.config.js       # Configuração do bundler
  └── tailwind.config.js     # Configuração do TailwindCSS
```

#### Páginas Principais:

**Dashboard (Home):**
- Visão geral do sistema
- Estatísticas principais
- Atividade recente
- Links rápidos para outras seções

**Usuários:**
- Lista de usuários
- Detalhes de usuário
- Tópicos de interesse
- Expressões frequentes
- Histórico de interações
- Opções para editar ou remover memórias

**Canais:**
- Lista de canais
- Detalhes de canal
- Tópicos recorrentes
- Usuários ativos
- Personalidade da Nina para o canal
- Opções para editar configurações de personalidade

**Configurações:**
- Configurações gerais do sistema
- Opções de backup e restauração
- Controles de plugins
- Configurações de personalidade global

**Estatísticas:**
- Gráficos de atividade
- Distribuição de tópicos
- Usuários mais ativos
- Canais mais ativos

### 3. Integração com o Sistema de Memória

A integração com o sistema de memória existente é feita através de um cliente que acessa diretamente as funções do módulo de memória.

#### Classe MemoryClient:
```python
class MemoryClient:
    """
    Cliente para o sistema de memória.
    Fornece métodos para acessar e manipular os dados do sistema de memória.
    """
    
    def __init__(self):
        """
        Inicializa o cliente de memória.
        """
        from nina_ia.memory import get_memory_system
        self.memory_system = get_memory_system()
    
    def get_users(self):
        """
        Obtém a lista de usuários.
        """
        # Implementação
    
    def get_user(self, user_id):
        """
        Obtém detalhes de um usuário.
        """
        return self.memory_system.get_user_profile(user_id)
    
    def update_user(self, user_id, data):
        """
        Atualiza informações de um usuário.
        """
        # Implementação
    
    def delete_user_memory(self, user_id):
        """
        Remove memórias de um usuário.
        """
        return self.memory_system.delete_user_memory(user_id)
    
    # Outros métodos para acessar e manipular dados
```

## Fluxos de Dados

### 1. Visualização de Perfil de Usuário

```
1. Usuário acessa a página de usuários
2. Frontend faz requisição GET /api/users
3. Backend consulta o sistema de memória
4. Sistema de memória retorna lista de usuários
5. Backend formata e retorna dados
6. Frontend exibe lista de usuários
7. Usuário seleciona um usuário específico
8. Frontend faz requisição GET /api/users/{user_id}
9. Backend consulta o sistema de memória
10. Sistema de memória retorna detalhes do usuário
11. Backend formata e retorna dados
12. Frontend exibe perfil completo do usuário
```

### 2. Edição de Personalidade da Nina para um Canal

```
1. Usuário acessa a página de canais
2. Frontend faz requisição GET /api/channels
3. Backend consulta o sistema de memória
4. Sistema de memória retorna lista de canais
5. Backend formata e retorna dados
6. Frontend exibe lista de canais
7. Usuário seleciona um canal específico
8. Frontend faz requisição GET /api/channels/{channel_id}
9. Backend consulta o sistema de memória
10. Sistema de memória retorna detalhes do canal
11. Backend formata e retorna dados
12. Frontend exibe perfil completo do canal
13. Usuário edita configurações de personalidade
14. Frontend faz requisição PUT /api/channels/{channel_id}/personality
15. Backend valida dados e atualiza o sistema de memória
16. Sistema de memória atualiza configurações
17. Backend retorna confirmação
18. Frontend exibe mensagem de sucesso
```

### 3. Remoção de Memórias de um Usuário

```
1. Usuário acessa a página de usuários
2. Frontend faz requisição GET /api/users
3. Backend consulta o sistema de memória
4. Sistema de memória retorna lista de usuários
5. Backend formata e retorna dados
6. Frontend exibe lista de usuários
7. Usuário seleciona um usuário específico
8. Frontend faz requisição GET /api/users/{user_id}
9. Backend consulta o sistema de memória
10. Sistema de memória retorna detalhes do usuário
11. Backend formata e retorna dados
12. Frontend exibe perfil completo do usuário
13. Usuário seleciona opção para remover memórias
14. Frontend solicita confirmação
15. Usuário confirma
16. Frontend faz requisição DELETE /api/users/{user_id}/memory
17. Backend remove memórias no sistema de memória
18. Sistema de memória remove dados
19. Backend retorna confirmação
20. Frontend exibe mensagem de sucesso e atualiza a página
```

## Interface de Usuário

### Layout Geral

A interface de usuário segue um layout de painel de administração com uma barra lateral para navegação e uma área principal para exibição de conteúdo.

```
+-------------------------------------------------------+
| Header (Logo, Título, Controles)                      |
+----------+--------------------------------------------+
| Sidebar  | Conteúdo Principal                         |
| - Home   |                                            |
| - Users  |                                            |
| - Channels|                                           |
| - Settings|                                           |
| - Stats  |                                            |
|          |                                            |
|          |                                            |
|          |                                            |
|          |                                            |
+----------+--------------------------------------------+
```

### Componentes Principais

#### Barra Lateral (Sidebar)
- Links para as principais seções
- Indicador de seção atual
- Botão para recolher/expandir

#### Cabeçalho (Header)
- Logo da Nina IA
- Título da página atual
- Controles globais (ex: botão de backup)

#### Cards de Usuário/Canal
- Informações básicas
- Links para detalhes
- Ações rápidas

#### Editores de Personalidade
- Controles deslizantes para níveis de formalidade, humor, tecnicidade
- Seletores para velocidade de resposta e verbosidade
- Botões para salvar/cancelar

#### Visualizações de Dados
- Tabelas para listas
- Gráficos para estatísticas
- Cards para informações resumidas

## Considerações de Segurança

1. **Autenticação Básica**: Como a interface é apenas para acesso local, uma autenticação básica é suficiente.

2. **Validação de Dados**: Todos os dados de entrada devem ser validados tanto no frontend quanto no backend.

3. **Confirmação de Ações Destrutivas**: Ações como remoção de memórias devem exigir confirmação do usuário.

4. **Logs de Auditoria**: Manter logs de todas as alterações feitas através da interface.

5. **Backups Automáticos**: Implementar backups automáticos antes de alterações significativas.

## Considerações de Desempenho

1. **Paginação**: Implementar paginação para listas longas de usuários, canais e interações.

2. **Carregamento Assíncrono**: Carregar dados de forma assíncrona para melhorar a experiência do usuário.

3. **Caching**: Implementar cache de dados frequentemente acessados.

4. **Otimização de Consultas**: Garantir que as consultas ao sistema de memória sejam eficientes.

5. **Compressão**: Utilizar compressão para reduzir o tamanho das respostas da API.

## Próximos Passos

1. Implementar o backend da API com FastAPI
2. Desenvolver o frontend com Svelte e TailwindCSS
3. Integrar o backend com o sistema de memória existente
4. Implementar funcionalidades de edição de memória
5. Implementar controles de personalidade
6. Testar o sistema completo
7. Documentar a implementação
