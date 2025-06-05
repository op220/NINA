# Documentação do Sistema de Memória de Longo Prazo e Interface Web para Nina IA

## Visão Geral

O Sistema de Memória de Longo Prazo e Interface Web para Nina IA é uma extensão que permite que a assistente de inteligência artificial Nina armazene e utilize informações sobre usuários e canais do Discord para contextualizar suas respostas e adaptar sua personalidade com base no histórico de interações.

Este sistema funciona 100% localmente, sem enviar dados para servidores externos, e utiliza apenas ferramentas gratuitas e de código aberto, conforme solicitado.

## Arquitetura do Sistema

O sistema é composto por dois componentes principais:

1. **Sistema de Memória de Longo Prazo**: Responsável por armazenar e processar informações sobre usuários e canais.
2. **Interface Web Local**: Permite visualizar e editar as informações armazenadas através de um navegador.

### Diagrama de Arquitetura

```
+----------------------------------+
|           Nina IA                |
+----------------------------------+
              |
              v
+----------------------------------+
|      Memory Orchestrator         |
+----------------------------------+
              |
              v
+----------------------------------+
|        Memory Adapter            |
+----------------------------------+
              |
              v
+----------------------------------+
|      Memory Integrator           |
+----------------------------------+
              |
              v
+----------------------------------+
|       Memory Manager             |
+----------------------------------+
        /            \
       v              v
+-------------+  +-------------+
| SQLite DB   |  | JSON Files  |
+-------------+  +-------------+
              |
              v
+----------------------------------+
|         FastAPI Backend          |
+----------------------------------+
              |
              v
+----------------------------------+
|         Svelte Frontend          |
+----------------------------------+
```

## Componentes do Sistema

### Sistema de Memória de Longo Prazo

#### Memory Manager

O Memory Manager é responsável pelo armazenamento e recuperação de dados no banco de dados SQLite e nos arquivos JSON. Ele fornece métodos para:

- Armazenar e recuperar perfis de usuários
- Armazenar e recuperar perfis de canais
- Armazenar e recuperar interações
- Analisar padrões de comunicação
- Extrair tópicos e sentimentos

#### Memory Integrator

O Memory Integrator serve como ponte entre o Memory Manager e o resto do sistema. Ele fornece uma interface de alto nível para:

- Processar mensagens de entrada
- Obter contexto para respostas
- Adaptar a personalidade com base no histórico
- Atualizar a memória após respostas

#### Memory Adapter

O Memory Adapter adapta o Memory Integrator para uso com o sistema Nina IA existente. Ele:

- Converte dados entre os formatos usados pelo Memory Integrator e pela Nina IA
- Gerencia configurações
- Controla o fluxo de dados entre os sistemas

#### Memory Orchestrator

O Memory Orchestrator coordena o fluxo de dados entre a Nina IA e o sistema de memória. Ele:

- Processa mensagens de entrada
- Enriquece o contexto com informações de memória
- Formata a memória para uso pelo LLM
- Atualiza a memória após respostas

### Interface Web Local

#### Backend API (FastAPI)

O backend API fornece endpoints RESTful para acessar e manipular os dados do sistema de memória. Ele inclui rotas para:

- Usuários: listar, obter detalhes, atualizar e gerenciar memórias
- Canais: listar, obter detalhes, atualizar e gerenciar configurações
- Interações: listar, obter detalhes e remover
- Estatísticas: obter estatísticas gerais e específicas
- Configurações: gerenciar configurações, backups e plugins

#### Frontend (Svelte)

O frontend fornece uma interface gráfica para visualizar e editar as informações armazenadas no sistema de memória. Ele inclui:

- Painel de navegação
- Visualização de perfis de usuários
- Visualização de perfis de canais
- Edição de configurações de personalidade
- Visualização de estatísticas
- Gerenciamento de backups

## Banco de Dados

O sistema utiliza uma combinação de SQLite e JSON para armazenamento de dados:

### SQLite

O banco de dados SQLite armazena dados estruturados como:

- Usuários
- Canais
- Interações
- Tópicos
- Sentimentos

### JSON

Os arquivos JSON armazenam dados flexíveis como:

- Perfis de personalidade
- Configurações
- Metadados

## Fluxo de Dados

### Processamento de Mensagens

1. A Nina IA recebe uma mensagem do Discord
2. O Memory Orchestrator processa a mensagem
3. O Memory Adapter converte os dados para o formato do Memory Integrator
4. O Memory Integrator processa a entrada e armazena a interação
5. O Memory Manager salva os dados no banco de dados

### Geração de Respostas

1. A Nina IA solicita contexto para uma resposta
2. O Memory Orchestrator solicita informações ao Memory Adapter
3. O Memory Adapter obtém o contexto do Memory Integrator
4. O Memory Integrator recupera dados do Memory Manager
5. O contexto enriquecido é retornado para a Nina IA
6. A Nina IA gera uma resposta com base no contexto
7. A resposta é armazenada no sistema de memória

### Visualização e Edição via Interface Web

1. O usuário acessa a interface web local
2. O frontend Svelte faz requisições ao backend FastAPI
3. O backend FastAPI acessa os dados através do Memory Integrator
4. Os dados são exibidos na interface
5. O usuário pode editar informações, que são salvas de volta no sistema

## Instalação e Configuração

### Requisitos

- Python 3.8 ou superior
- Node.js 14 ou superior
- NVIDIA Quadro P4000 ou equivalente (para componentes que utilizam GPU)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/nina-ia.git
cd nina-ia
```

2. Instale as dependências Python:
```bash
pip install -r requirements.txt
```

3. Instale as dependências do frontend:
```bash
cd web/frontend
npm install
```

4. Configure o token do Discord no arquivo de configuração:
```bash
cp config.example.json config.json
# Edite config.json com seu editor de texto preferido
```

### Configuração

O sistema pode ser configurado através do arquivo `config.json` ou da interface web. As principais configurações incluem:

- `enabled`: Habilita ou desabilita o sistema de memória
- `memory_db_path`: Caminho para o banco de dados SQLite
- `profiles_dir`: Diretório para armazenar perfis
- `max_context_interactions`: Número máximo de interações a incluir no contexto
- `backup_dir`: Diretório para armazenar backups
- `auto_backup`: Habilita ou desabilita backups automáticos
- `auto_backup_interval`: Intervalo entre backups automáticos (em horas)

## Uso

### Iniciar o Sistema

1. Inicie o backend:
```bash
cd nina-ia
python -m web.backend.api
```

2. Inicie o frontend:
```bash
cd nina-ia/web/frontend
npm run dev
```

3. Acesse a interface web em `http://localhost:5000`

### Funcionalidades da Interface Web

#### Visualização de Usuários

A página de usuários permite visualizar todos os usuários conhecidos pelo sistema e seus detalhes, incluindo:

- Informações básicas (nome, primeira e última interação)
- Tópicos de interesse
- Emoções predominantes
- Expressões frequentes
- Histórico de interações

#### Visualização de Canais

A página de canais permite visualizar todos os canais conhecidos pelo sistema e seus detalhes, incluindo:

- Informações básicas (nome, tipo, atividade)
- Tópicos recorrentes
- Usuários ativos
- Personalidade adaptada
- Histórico de interações

#### Edição de Personalidade

A página de detalhes de canal permite editar a personalidade da Nina IA para esse canal, incluindo:

- Nível de formalidade
- Nível de humor
- Nível de tecnicidade
- Velocidade de resposta
- Verbosidade

#### Configurações

A página de configurações permite gerenciar as configurações do sistema, incluindo:

- Habilitar/desabilitar o sistema de memória
- Configurar backups automáticos
- Gerenciar plugins
- Exportar e importar dados

#### Backups

A página de backups permite:

- Criar backups manuais
- Restaurar a partir de backups
- Excluir backups antigos

## Segurança e Privacidade

O sistema foi projetado com foco em segurança e privacidade:

- Todos os dados são armazenados localmente
- Nenhuma informação é enviada para servidores externos
- O acesso à interface web é restrito a localhost por padrão
- Backups são criptografados (opcional)

## Limitações e Considerações

- O sistema requer acesso ao Discord para coletar dados
- O desempenho pode variar dependendo do hardware
- A adaptação de personalidade é baseada em heurísticas e pode não ser perfeita
- O armazenamento de dados pode crescer significativamente com o tempo

## Solução de Problemas

### Problemas Comuns

#### O sistema de memória não está funcionando

- Verifique se o sistema está habilitado no arquivo de configuração
- Verifique se o banco de dados SQLite existe e é acessível
- Verifique os logs para erros específicos

#### A interface web não está acessível

- Verifique se o backend está em execução
- Verifique se o frontend está em execução
- Verifique se as portas não estão bloqueadas por firewall

#### A adaptação de personalidade não está funcionando como esperado

- Verifique se há interações suficientes para análise
- Ajuste os parâmetros de adaptação nas configurações
- Considere redefinir a personalidade para o padrão

### Logs

Os logs do sistema são armazenados em:

- Backend: `logs/backend.log`
- Frontend: `logs/frontend.log`
- Sistema de memória: `logs/memory.log`

## Desenvolvimento e Extensão

### Estrutura de Diretórios

```
nina-ia/
├── core/
│   ├── memory_adapter.py
│   ├── memory_integrator.py
│   ├── memory_orchestrator.py
│   └── ...
├── memory/
│   ├── database.py
│   ├── memory_manager.py
│   ├── pattern_analyzer.py
│   └── ...
├── web/
│   ├── backend/
│   │   ├── api.py
│   │   ├── routers/
│   │   └── ...
│   └── frontend/
│       ├── src/
│       ├── public/
│       └── ...
├── tests/
│   ├── test_memory_system.py
│   ├── test_web_api.py
│   ├── test_integration.py
│   └── ...
└── ...
```

### Adicionar Novos Recursos

Para adicionar novos recursos ao sistema:

1. Implemente a funcionalidade no componente apropriado
2. Adicione endpoints à API se necessário
3. Atualize a interface web para expor a funcionalidade
4. Adicione testes para a nova funcionalidade
5. Atualize a documentação

### Personalização

O sistema pode ser personalizado de várias maneiras:

- Modificar os algoritmos de análise de padrões
- Ajustar os parâmetros de adaptação de personalidade
- Adicionar novos tipos de dados para armazenamento
- Personalizar a interface web

## Referências

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Svelte Documentation](https://svelte.dev/docs)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [NLTK Documentation](https://www.nltk.org/)
- [SpaCy Documentation](https://spacy.io/api/doc)

## Suporte

Para suporte, entre em contato com a equipe de desenvolvimento ou abra uma issue no repositório do projeto.

---

Documentação gerada em 25 de abril de 2025.
