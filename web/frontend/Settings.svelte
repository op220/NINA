<script>
  import { onMount } from 'svelte';
  
  // Estado para armazenar as configurações
  let settings = {
    system: {
      db_path: "memory.db",
      data_dir: "memory_data",
      backup_dir: "backups",
      auto_backup: true,
      auto_backup_interval: 24 // horas
    },
    memory: {
      max_interactions_per_user: 1000,
      max_interactions_per_channel: 5000,
      retention_period: 90 // dias
    },
    personality: {
      default_formality_level: 50,
      default_humor_level: 50,
      default_technicality_level: 50,
      default_response_speed: "médio",
      default_verbosity: "médio"
    }
  };
  
  // Estado para backups
  let backups = [];
  let selectedBackup = null;
  let backupFile = null;
  
  // Estado para plugins
  let plugins = [
    {
      id: "voice_capture",
      name: "Captura de Voz",
      description: "Plugin para captura de áudio do Discord",
      enabled: true
    },
    {
      id: "sentiment_analysis",
      name: "Análise de Sentimentos",
      description: "Plugin para análise avançada de sentimentos em mensagens",
      enabled: true
    },
    {
      id: "topic_extraction",
      name: "Extração de Tópicos",
      description: "Plugin para extração avançada de tópicos em mensagens",
      enabled: true
    },
    {
      id: "personality_adaptation",
      name: "Adaptação de Personalidade",
      description: "Plugin para adaptação automática da personalidade da Nina",
      enabled: false
    }
  ];
  
  // Estado para UI
  let loading = false;
  let saveSuccess = false;
  let saveError = null;
  let backupSuccess = false;
  let backupError = null;
  let restoreSuccess = false;
  let restoreError = null;
  let activeTab = 'general';
  
  // Função para carregar configurações
  async function loadSettings() {
    try {
      loading = true;
      
      // Em uma implementação real, buscaríamos esses dados da API
      // Simulando dados para demonstração
      await new Promise(resolve => setTimeout(resolve, 500)); // Simular delay de rede
      
      // Já temos dados simulados em settings
      
      // Carregar backups
      backups = [
        { name: "backup_20250425_080000.db", path: "/backups/backup_20250425_080000.db", size: 1024 * 1024 * 2.5, created_at: new Date(2025, 3, 25, 8, 0, 0).getTime() },
        { name: "backup_20250424_080000.db", path: "/backups/backup_20250424_080000.db", size: 1024 * 1024 * 2.3, created_at: new Date(2025, 3, 24, 8, 0, 0).getTime() },
        { name: "backup_20250423_080000.db", path: "/backups/backup_20250423_080000.db", size: 1024 * 1024 * 2.1, created_at: new Date(2025, 3, 23, 8, 0, 0).getTime() }
      ];
      
    } catch (error) {
      console.error('Erro ao carregar configurações:', error);
    } finally {
      loading = false;
    }
  }
  
  // Função para salvar configurações
  async function saveSettings() {
    try {
      loading = true;
      saveSuccess = false;
      saveError = null;
      
      // Em uma implementação real, enviaríamos esses dados para a API
      // Simulando requisição para demonstração
      await new Promise(resolve => setTimeout(resolve, 800)); // Simular delay de rede
      
      // Simular sucesso
      saveSuccess = true;
      
      // Resetar mensagem de sucesso após 3 segundos
      setTimeout(() => {
        saveSuccess = false;
      }, 3000);
      
    } catch (error) {
      console.error('Erro ao salvar configurações:', error);
      saveError = 'Não foi possível salvar as configurações. Tente novamente mais tarde.';
    } finally {
      loading = false;
    }
  }
  
  // Função para criar backup
  async function createBackup() {
    try {
      loading = true;
      backupSuccess = false;
      backupError = null;
      
      // Em uma implementação real, enviaríamos uma requisição para a API
      // Simulando requisição para demonstração
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simular delay de rede
      
      // Simular sucesso
      const now = new Date();
      const backupName = `backup_${now.getFullYear()}${(now.getMonth()+1).toString().padStart(2, '0')}${now.getDate().toString().padStart(2, '0')}_${now.getHours().toString().padStart(2, '0')}${now.getMinutes().toString().padStart(2, '0')}${now.getSeconds().toString().padStart(2, '0')}.db`;
      
      // Adicionar novo backup à lista
      backups = [
        { 
          name: backupName, 
          path: `/backups/${backupName}`, 
          size: 1024 * 1024 * 2.7, 
          created_at: now.getTime() 
        },
        ...backups
      ];
      
      backupSuccess = true;
      
      // Resetar mensagem de sucesso após 3 segundos
      setTimeout(() => {
        backupSuccess = false;
      }, 3000);
      
    } catch (error) {
      console.error('Erro ao criar backup:', error);
      backupError = 'Não foi possível criar o backup. Tente novamente mais tarde.';
    } finally {
      loading = false;
    }
  }
  
  // Função para restaurar backup
  async function restoreBackup() {
    if (!selectedBackup) return;
    
    try {
      loading = true;
      restoreSuccess = false;
      restoreError = null;
      
      // Em uma implementação real, enviaríamos uma requisição para a API
      // Simulando requisição para demonstração
      await new Promise(resolve => setTimeout(resolve, 1500)); // Simular delay de rede
      
      // Simular sucesso
      restoreSuccess = true;
      
      // Resetar mensagem de sucesso após 3 segundos
      setTimeout(() => {
        restoreSuccess = false;
      }, 3000);
      
    } catch (error) {
      console.error('Erro ao restaurar backup:', error);
      restoreError = 'Não foi possível restaurar o backup. Tente novamente mais tarde.';
    } finally {
      loading = false;
    }
  }
  
  // Função para alternar status de plugin
  function togglePlugin(pluginId) {
    plugins = plugins.map(plugin => {
      if (plugin.id === pluginId) {
        return { ...plugin, enabled: !plugin.enabled };
      }
      return plugin;
    });
  }
  
  // Função para formatar tamanho de arquivo
  function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    if (bytes < 1024 * 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    return (bytes / (1024 * 1024 * 1024)).toFixed(1) + ' GB';
  }
  
  // Função para formatar data
  function formatDate(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleDateString('pt-BR', { 
      day: '2-digit', 
      month: '2-digit', 
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }
  
  // Carregar configurações ao montar o componente
  onMount(() => {
    loadSettings();
  });
</script>

<div class="fade-in">
  <h1>Configurações</h1>
  
  <!-- Abas -->
  <div class="mb-6 border-b border-neutral-200">
    <div class="flex space-x-8">
      <button 
        class="py-2 px-1 border-b-2 {activeTab === 'general' ? 'border-primary-500 text-primary-600' : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300'} transition-colors duration-200"
        on:click={() => activeTab = 'general'}
      >
        Geral
      </button>
      <button 
        class="py-2 px-1 border-b-2 {activeTab === 'memory' ? 'border-primary-500 text-primary-600' : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300'} transition-colors duration-200"
        on:click={() => activeTab = 'memory'}
      >
        Memória
      </button>
      <button 
        class="py-2 px-1 border-b-2 {activeTab === 'personality' ? 'border-primary-500 text-primary-600' : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300'} transition-colors duration-200"
        on:click={() => activeTab = 'personality'}
      >
        Personalidade
      </button>
      <button 
        class="py-2 px-1 border-b-2 {activeTab === 'backup' ? 'border-primary-500 text-primary-600' : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300'} transition-colors duration-200"
        on:click={() => activeTab = 'backup'}
      >
        Backup
      </button>
      <button 
        class="py-2 px-1 border-b-2 {activeTab === 'plugins' ? 'border-primary-500 text-primary-600' : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300'} transition-colors duration-200"
        on:click={() => activeTab = 'plugins'}
      >
        Plugins
      </button>
    </div>
  </div>
  
  {#if loading}
    <div class="card p-8 text-center">
      <i class="fas fa-spinner fa-spin text-primary-500 text-2xl mb-2"></i>
      <p class="text-neutral-600">Carregando...</p>
    </div>
  {:else}
    <!-- Conteúdo das abas -->
    <div class="card p-6">
      {#if activeTab === 'general'}
        <h2 class="text-xl font-semibold mb-4">Configurações Gerais</h2>
        
        <div class="space-y-4">
          <div>
            <label for="db_path" class="block text-sm font-medium text-neutral-700 mb-1">
              Caminho do Banco de Dados
            </label>
            <input 
              type="text" 
              id="db_path" 
              bind:value={settings.system.db_path} 
              class="input"
            />
          </div>
          
          <div>
            <label for="data_dir" class="block text-sm font-medium text-neutral-700 mb-1">
              Diretório de Dados
            </label>
            <input 
              type="text" 
              id="data_dir" 
              bind:value={settings.system.data_dir} 
              class="input"
            />
          </div>
          
          <div>
            <label for="backup_dir" class="block text-sm font-medium text-neutral-700 mb-1">
              Diretório de Backup
            </label>
            <input 
              type="text" 
              id="backup_dir" 
              bind:value={settings.system.backup_dir} 
              class="input"
            />
          </div>
          
          <div class="flex items-center">
            <input 
              type="checkbox" 
              id="auto_backup" 
              bind:checked={settings.system.auto_backup} 
              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-neutral-300 rounded"
            />
            <label for="auto_backup" class="ml-2 block text-sm text-neutral-700">
              Backup automático
            </label>
          </div>
          
          {#if settings.system.auto_backup}
            <div>
              <label for="auto_backup_interval" class="block text-sm font-medium text-neutral-700 mb-1">
                Intervalo de Backup (horas)
              </label>
              <input 
                type="number" 
                id="auto_backup_interval" 
                bind:value={settings.system.auto_backup_interval} 
                min="1" 
                max="168" 
                class="input"
              />
            </div>
          {/if}
        </div>
      {:else if activeTab === 'memory'}
        <h2 class="text-xl font-semibold mb-4">Configurações de Memória</h2>
        
        <div class="space-y-4">
          <div>
            <label for="max_interactions_per_user" class="block text-sm font-medium text-neutral-700 mb-1">
              Máximo de Interações por Usuário
            </label>
            <input 
              type="number" 
              id="max_interactions_per_user" 
              bind:value={settings.memory.max_interactions_per_user} 
              min="100" 
              max="10000" 
              class="input"
            />
            <p class="mt-1 text-sm text-neutral-500">
              Limite de interações armazenadas por usuário. Interações mais antigas serão removidas.
            </p>
          </div>
          
          <div>
            <label for="max_interactions_per_channel" class="block text-sm font-medium text-neutral-700 mb-1">
              Máximo de Interações por Canal
            </label>
            <input 
              type="number" 
              id="max_interactions_per_channel" 
              bind:value={settings.memory.max_interactions_per_channel} 
              min="100" 
              max="50000" 
              class="input"
            />
            <p class="mt-1 text-sm text-neutral-500">
              Limite de interações armazenadas por canal. Interações mais antigas serão removidas.
            </p>
          </div>
          
          <div>
            <label for="retention_period" class="block text-sm font-medium text-neutral-700 mb-1">
              Período de Retenção (dias)
            </label>
            <input 
              type="number" 
              id="retention_period" 
              bind:value={settings.memory.retention_period} 
              min="7" 
              max="365" 
              class="input"
            />
            <p class="mt-1 text-sm text-neutral-500">
              Período máximo de armazenamento de interações. Interações mais antigas serão removidas.
            </p>
          </div>
        </div>
      {:else if activeTab === 'personality'}
        <h2 class="text-xl font-semibold mb-4">Configurações de Personalidade Padrão</h2>
        
        <div class="space-y-6">
          <div>
            <label for="formality_level" class="block text-sm font-medium text-neutral-700 mb-1">
              Nível de Formalidade: {settings.personality.default_formality_level}
            </label>
            <input 
              type="range" 
              id="formality_level" 
              bind:value={settings.personality.default_formality_level} 
              min="0" 
              max="100" 
              class="w-full h-2 bg-neutral-200 rounded-lg appearance-none cursor-pointer"
            />
            <div class="flex justify-between text-xs text-neutral-500 mt-1">
              <span>Informal</span>
              <span>Neutro</span>
              <span>Formal</span>
            </div>
          </div>
          
          <div>
            <label for="humor_level" class="block text-sm font-medium text-neutral-700 mb-1">
              Nível de Humor: {settings.personality.default_humor_level}
            </label>
            <input 
              type="range" 
              id="humor_level" 
              bind:value={settings.personality.default_humor_level} 
              min="0" 
              max="100" 
              class="w-full h-2 bg-neutral-200 rounded-lg appearance-none cursor-pointer"
            />
            <div class="flex justify-between text-xs text-neutral-500 mt-1">
              <span>Sério</span>
              <span>Moderado</span>
              <span>Humorístico</span>
            </div>
          </div>
          
          <div>
            <label for="technicality_level" class="block text-sm font-medium text-neutral-700 mb-1">
              Nível de Tecnicidade: {settings.personality.default_technicality_level}
            </label>
            <input 
              type="range" 
              id="technicality_level" 
              bind:value={settings.personality.default_technicality_level} 
              min="0" 
              max="100" 
              class="w-full h-2 bg-neutral-200 rounded-lg appearance-none cursor-pointer"
            />
            <div class="flex justify-between text-xs text-neutral-500 mt-1">
              <span>Simples</span>
              <span>Moderado</span>
              <span>Técnico</span>
            </div>
          </div>
          
          <div>
            <label for="response_speed" class="block text-sm font-medium text-neutral-700 mb-1">
              Velocidade de Resposta
            </label>
            <select 
              id="response_speed" 
              bind:value={settings.personality.default_response_speed} 
              class="select"
            >
              <option value="lento">Lento</o
(Content truncated due to size limit. Use line ranges to read in chunks)