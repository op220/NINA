<script>
  import { onMount } from 'svelte';
  import { useParams, Link } from 'svelte-navigator';
  import { Line } from 'svelte-chartjs';
  import { 
    Chart, 
    Title, 
    Tooltip, 
    Legend, 
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement
  } from 'chart.js';
  
  // Registrar componentes do Chart.js
  Chart.register(
    Title, 
    Tooltip, 
    Legend, 
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement
  );
  
  // Obter parâmetros da URL
  const params = useParams();
  
  // Estado para armazenar dados do canal
  let channel = null;
  let interactions = [];
  let topics = [];
  let users = [];
  let activityData = null;
  
  // Estado para edição de personalidade
  let editingPersonality = false;
  let personality = {
    formality_level: 50,
    humor_level: 50,
    technicality_level: 50,
    response_speed: 'médio',
    verbosity: 'médio'
  };
  
  // Estado para edição de configurações
  let editingSettings = false;
  let settings = {
    enabled: true,
    learning_rate: 0.5,
    adaptation_speed: 'médio',
    memory_weight: 0.7
  };
  
  // Estado para UI
  let loading = true;
  let error = null;
  let saveSuccess = false;
  let saveError = null;
  let activeTab = 'overview';
  
  // Função para carregar dados do canal
  async function loadChannelData() {
    try {
      loading = true;
      error = null;
      
      // Em uma implementação real, buscaríamos esses dados da API
      // Simulando dados para demonstração
      await new Promise(resolve => setTimeout(resolve, 800)); // Simular delay de rede
      
      // Simular dados do canal
      channel = {
        channel_id: params.id,
        channel_name: `Canal ${params.id.replace('channel', '')}`,
        type: Math.random() > 0.5 ? 'texto' : 'voz',
        created_at: new Date(2025, 0, 15).toLocaleDateString('pt-BR'),
        last_activity: new Date(2025, 3, 23).toLocaleDateString('pt-BR'),
        message_count: 1243,
        user_count: 45,
        description: 'Canal para discussões sobre tecnologia e programação.'
      };
      
      // Simular personalidade
      personality = {
        formality_level: Math.floor(Math.random() * 100),
        humor_level: Math.floor(Math.random() * 100),
        technicality_level: Math.floor(Math.random() * 100),
        response_speed: ['lento', 'médio', 'rápido'][Math.floor(Math.random() * 3)],
        verbosity: ['conciso', 'médio', 'detalhado'][Math.floor(Math.random() * 3)]
      };
      
      // Simular configurações
      settings = {
        enabled: true,
        learning_rate: Math.random().toFixed(1),
        adaptation_speed: ['lento', 'médio', 'rápido'][Math.floor(Math.random() * 3)],
        memory_weight: Math.random().toFixed(1)
      };
      
      // Simular interações
      interactions = Array(10).fill().map((_, i) => ({
        id: `int_${i+1}`,
        user: `Usuário ${i % 5 + 1}`,
        content: `Esta é uma mensagem de exemplo ${i+1} no canal ${params.id}. ${i % 2 === 0 ? 'Contém uma pergunta sobre programação.' : 'É um comentário sobre tecnologia.'}`,
        timestamp: new Date(2025, 3, 24 - i).toLocaleString('pt-BR'),
        sentiment: Math.random() > 0.7 ? 'positivo' : (Math.random() > 0.4 ? 'neutro' : 'negativo')
      }));
      
      // Simular tópicos
      topics = [
        { name: 'Programação', count: 345, percentage: 35 },
        { name: 'Inteligência Artificial', count: 245, percentage: 25 },
        { name: 'Jogos', count: 196, percentage: 20 },
        { name: 'Hardware', count: 118, percentage: 12 },
        { name: 'Filmes', count: 78, percentage: 8 }
      ];
      
      // Simular usuários ativos
      users = [
        { username: 'João Silva', interaction_count: 156, last_seen: new Date(2025, 3, 24).toLocaleDateString('pt-BR') },
        { username: 'Maria Oliveira', interaction_count: 132, last_seen: new Date(2025, 3, 23).toLocaleDateString('pt-BR') },
        { username: 'Carlos Mendes', interaction_count: 98, last_seen: new Date(2025, 3, 22).toLocaleDateString('pt-BR') },
        { username: 'Ana Santos', interaction_count: 87, last_seen: new Date(2025, 3, 21).toLocaleDateString('pt-BR') },
        { username: 'Pedro Costa', interaction_count: 76, last_seen: new Date(2025, 3, 20).toLocaleDateString('pt-BR') }
      ];
      
      // Simular dados de atividade
      const dates = [];
      const values = [];
      
      // Gerar datas para os últimos 30 dias
      const today = new Date();
      for (let i = 29; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        dates.push(date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' }));
        
        // Gerar valores aleatórios para atividade
        values.push(Math.floor(Math.random() * 50) + 10);
      }
      
      activityData = {
        labels: dates,
        datasets: [{
          label: 'Mensagens',
          data: values,
          backgroundColor: 'rgba(54, 162, 235, 0.5)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1,
          tension: 0.3
        }]
      };
      
    } catch (err) {
      console.error('Erro ao carregar dados do canal:', err);
      error = 'Não foi possível carregar os dados do canal. Tente novamente mais tarde.';
    } finally {
      loading = false;
    }
  }
  
  // Função para salvar personalidade
  async function savePersonality() {
    try {
      loading = true;
      saveSuccess = false;
      saveError = null;
      
      // Em uma implementação real, enviaríamos esses dados para a API
      // Simulando requisição para demonstração
      await new Promise(resolve => setTimeout(resolve, 600)); // Simular delay de rede
      
      // Simular sucesso
      saveSuccess = true;
      editingPersonality = false;
      
      // Resetar mensagem de sucesso após 3 segundos
      setTimeout(() => {
        saveSuccess = false;
      }, 3000);
      
    } catch (error) {
      console.error('Erro ao salvar personalidade:', error);
      saveError = 'Não foi possível salvar a personalidade. Tente novamente mais tarde.';
    } finally {
      loading = false;
    }
  }
  
  // Função para cancelar edição de personalidade
  function cancelEditPersonality() {
    // Recarregar dados originais
    loadChannelData();
    editingPersonality = false;
  }
  
  // Função para salvar configurações
  async function saveSettings() {
    try {
      loading = true;
      saveSuccess = false;
      saveError = null;
      
      // Em uma implementação real, enviaríamos esses dados para a API
      // Simulando requisição para demonstração
      await new Promise(resolve => setTimeout(resolve, 600)); // Simular delay de rede
      
      // Simular sucesso
      saveSuccess = true;
      editingSettings = false;
      
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
  
  // Função para cancelar edição de configurações
  function cancelEditSettings() {
    // Recarregar dados originais
    loadChannelData();
    editingSettings = false;
  }
  
  // Função para limpar memória do canal
  async function clearChannelMemory() {
    try {
      loading = true;
      saveSuccess = false;
      saveError = null;
      
      // Em uma implementação real, enviaríamos esses dados para a API
      // Simulando requisição para demonstração
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simular delay de rede
      
      // Simular sucesso
      interactions = [];
      saveSuccess = true;
      
      // Resetar mensagem de sucesso após 3 segundos
      setTimeout(() => {
        saveSuccess = false;
      }, 3000);
      
    } catch (error) {
      console.error('Erro ao limpar memória:', error);
      saveError = 'Não foi possível limpar a memória do canal. Tente novamente mais tarde.';
    } finally {
      loading = false;
    }
  }
  
  // Função para obter cor com base no sentimento
  function getSentimentColor(sentiment) {
    switch(sentiment) {
      case 'positivo': return 'bg-green-100 text-green-800';
      case 'negativo': return 'bg-red-100 text-red-800';
      default: return 'bg-blue-100 text-blue-800';
    }
  }
  
  // Função para obter descrição do nível
  function getLevelDescription(type, level) {
    if (type === 'formality_level') {
      if (level < 30) return 'Informal';
      if (level < 70) return 'Neutro';
      return 'Formal';
    } else if (type === 'humor_level') {
      if (level < 30) return 'Sério';
      if (level < 70) return 'Moderado';
      return 'Humorístico';
    } else if (type === 'technicality_level') {
      if (level < 30) return 'Simples';
      if (level < 70) return 'Moderado';
      return 'Técnico';
    }
    return '';
  }
  
  // Função para obter cor com base no nível
  function getLevelColor(level) {
    if (level < 30) return 'bg-blue-100 text-blue-800';
    if (level < 70) return 'bg-green-100 text-green-800';
    return 'bg-red-100 text-red-800';
  }
  
  // Opções para o gráfico
  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: 'Atividade do Canal'
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          precision: 0
        }
      }
    }
  };
  
  // Carregar dados do canal ao montar o componente
  onMount(() => {
    loadChannelData();
  });
</script>

<div class="fade-in">
  <div class="flex justify-between items-center mb-6">
    <div class="flex items-center">
      <Link to="/channels" class="text-primary-600 hover:text-primary-800 mr-2">
        <i class="fas fa-arrow-left"></i>
      </Link>
      <h1 class="m-0">Detalhes do Canal</h1>
    </div>
  </div>
  
  {#if loading && !channel}
    <div class="card p-8 text-center">
      <i class="fas fa-spinner fa-spin text-primary-500 text-2xl mb-2"></i>
      <p class="text-neutral-600">Carregando dados do canal...</p>
    </div>
  {:else if error}
    <div class="card p-8 text-center">
      <i class="fas fa-exclamation-circle text-red-500 text-2xl mb-2"></i>
      <p class="text-neutral-600">{error}</p>
      <button 
        class="mt-4 btn btn-primary"
        on:click={loadChannelData}
      >
        Tentar novamente
      </button>
    </div>
  {:else if channel}
    <!-- Cabeçalho do canal -->
    <div class="card p-6 mb-6">
      <div class="flex items-center">
        <div class="flex-shrink-0 h-16 w-16 rounded-full bg-primary-100 flex items-center justify-center">
          <i class={channel.type === 'voz' ? 'fas fa-microphone text-primary-800 text-2xl' : 'fas fa-hashtag text-primary-800 text-2xl'}></i>
        </div>
        <div class="ml-4 flex-1">
          <h2 class="text-xl font-semibold m-0">{channel.channel_name}</h2>
          <p class="text-neutral-500 m-0">ID: {channel.channel_id}</p>
          <div class="flex mt-1">
            <span class="badge badge-neutral mr-2">{channel.type}</span>
            <span class="text-sm text-neutral-500 mr-4">
              <i class="fas fa-calendar-alt mr-1"></i> Criado em: {channel.created_at}
            </span>
            <span class="text-sm text-neutral-500">
              <i class="fas fa-clock mr-1"></i> Última atividade: {channel.last_activity}
            </span>
          </div>
        </div>
        <div class="text-right">
          <div class="text-2xl font-semibold text-primary-600">{channel.message_count}</div>
          <div class="text-sm text-neutral-500">mensagens</div>
          <div class="text-sm text-neutral-500 mt-1">{channel.user_count} usuários</div>
        </div>
      </div>
      {#if channel.description}
        <div class="mt-3 pt-3 border-t border-neutral-200">
          <p class="text-neutral-700 m-0">{channel.description}</p>
        </div>
      {/if}
    </div>
    
    <!-- Abas -->
    <div class="mb-6 border-b border-neutral-200">
      <div class="flex space-x-8">
        <button 
          class="py-2 px-1 border-b-2 {activeTab === 'overview' ? 'border-primary-500 text-primary-600' : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300'} transition-colors duration-200"
          on:click={() => activeTab = 'overview'}
        >
          Visão Geral
        </button>
        <button 
          class="py-2 px-1 border-b-2 {activeTab === 'personality' ? 'border-primary-500 text-primary-600' : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300'} transition-colors duration-200"
          on:click={() => activeTab = 'personality'}
        >
          Personalidade
        </button>
        <button 
          class="py-2 px-1 border-b-2 {activeTab === 'interactions' ? 'border-primary-500 text-primary-600' : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300'} transition-colors duration-200"
          on:click={() => activeTab = 'interactions'}
        >
          Interações
        </button>
        <button 
          class="py-2 px-1 border-b-2 {activeTab === 'settings' ? 'border-primary-500 text-primary-600' : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300'} transition-colors duration-200"
          on:click={() => activeTab = 'settings'}
        >
          Configurações
        </button>
      </div>
    </div>
    
    <!-- Conteúdo das abas -->
    {#if activeTab === 'overview'}
      <div class="card p-6 mb-6">
        <h2 class="text-lg font-semibold mb-4">Atividade Recente</h2>
        <div class="h-64">
          <Line data={activityData} options={chartOptions} />
        </div>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Tópicos principais -->
        <div class="card p-6">
          <h2 class="text-lg font-semibold mb-4">Tópicos Principais</h2>
          <ul class="space-y-3">
            {#each topics as topic}
              <li>
                <div class="flex justify-between mb-1">
                  <span class="text-sm font-medium text-neutral-700">{topic.name}</span>
                  <span class="text-sm text-neutral-500">{topic.count} mensagens ({topic.percentage}%)</span>
                </div>
                <div class="w-full bg-neutral-200 rounded-full h-2">
                  <div 
                    class="bg-primary-600 h-2 rounded-full" 
                    style="width: {topic.percentage}%"
                  ></div>
                </div>
              </li>
            {/each}
          </ul>
        </div>
        
        <!-- Usuários ativos -->
        <div class="card p-6">
          <h2 class="text-lg font-semibold mb-4">Usuários Mais Ativos</h2>
          <div class="overflow-hidden">
            <table class="min-w-full divide-y divide-neutral-200">
              <thead class="bg-neutral-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                    Usuário
                  </th>
                  <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-neutral-500 uppercase tracking-wider">
                    Interações
                  </th>
                  <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-neutral-500 uppercase tracking-wider">
                    Última Atividade
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-neutral-200">
                {#each users as user}
                  <tr class="hover:bg-neutral-50">
                    <td class="px-6 py-4 whitespace-nowrap">
                  
(Content truncated due to size limit. Use line ranges to read in chunks)