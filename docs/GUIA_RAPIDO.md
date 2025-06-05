# Guia de Instalação e Uso Rápido - Sistema de Memória e Interface Web para Nina IA

Este guia fornece instruções rápidas para instalar e começar a usar o Sistema de Memória de Longo Prazo e Interface Web para a Nina IA.

## Instalação Rápida

### Pré-requisitos

- Python 3.8 ou superior
- Node.js 14 ou superior
- NVIDIA Quadro P4000 ou equivalente (para componentes que utilizam GPU)
- Discord Bot configurado e funcionando

### Passos para Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/nina-ia.git
   cd nina-ia
   ```

2. **Instale as dependências Python**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Instale as dependências do frontend**:
   ```bash
   cd web/frontend
   npm install
   cd ../..
   ```

4. **Configure o token do Discord**:
   ```bash
   cp config.example.json config.json
   # Edite config.json com seu editor de texto preferido para adicionar seu token
   ```

## Iniciar o Sistema

1. **Inicie o backend**:
   ```bash
   cd nina-ia
   python -m web.backend.api
   ```

2. **Inicie o frontend em outro terminal**:
   ```bash
   cd nina-ia/web/frontend
   npm run dev
   ```

3. **Acesse a interface web**:
   Abra seu navegador e acesse `http://localhost:5000`

## Funcionalidades Principais

- **Visualização de Usuários**: Veja informações sobre usuários, tópicos de interesse e histórico
- **Visualização de Canais**: Veja informações sobre canais, tópicos recorrentes e personalidade adaptada
- **Edição de Personalidade**: Ajuste a personalidade da Nina IA para cada canal
- **Configurações**: Gerencie as configurações do sistema e backups
- **Memória Persistente**: Todas as interações são armazenadas localmente para contextualização futura

## Solução de Problemas Rápida

- **Backend não inicia**: Verifique se todas as dependências estão instaladas e se as portas não estão em uso
- **Frontend não carrega**: Verifique se o backend está rodando e se as configurações de URL estão corretas
- **Erros de conexão**: Verifique se o token do Discord está configurado corretamente

Para documentação completa, consulte o arquivo `docs/sistema_memoria_interface_web.md`.

---

Guia rápido gerado em 25 de abril de 2025.
