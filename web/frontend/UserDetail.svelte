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
  
  // Estado para armazenar dados do usuário
  let user = null;
  let interactions = [];
  let topics = [];
  let emotions = [];
  let expressions = [];
  let activityData = null;
  
  // Estado para edição
  let editingNotes = false;
  let userNotes = '';
  
  // Estado para remoção de memórias
  let selectedInteractions = [];
  let confirmDelete = false;
  
  // Estado para UI
  let loading = true;
  let error = null;
  let saveSuccess = false;
  let saveError = null;
  let deleteSuccess = false;
  let deleteError = null;
  let activeTab = 'overview';
  
  // Função para carregar dados do usuário
  async function loadUserData() {
    try {
      loading = true;
      error = null;
      
      // Em uma implementação real, buscaríamos esses dados da API
      // Simulando dados para demonstração
      await new Promise(resolve => setTimeout(resolve, 800)); // Simular delay de rede
      
      // Simular dados do usuário
      user = {
        user_id: params.id,
        username: `Usuário ${params.id.replace('user', '')}`,
        first_seen: new Date(2025, 0, 15).toLocaleDateString('pt-BR'),
        last_seen: new Date(2025, 3, 23).toLocaleDateString('pt-BR'),
        interaction_count: 156,
        voice_time: 120, // minutos
        notes: 'Este usuário prefere explicações técnicas e detalhadas. Geralmente participa mais nos canais de tecnologia e programação.'
      };
      
      userNotes = user.notes;
      
      // Simular interações
      interactions = Array(10).fill().map((_, i) => ({
        id: `int_${i+1}`,
        content: `Esta é uma mensagem de exemplo ${i+1} do usuário ${params.id}. ${i % 2 === 0 ? 'Contém uma pergunta sobre programação.' : 'É um comentário sobre tecnologia.'}`,
        channel: i % 3 === 0 ? 'geral' : (i % 3 === 1 ? 'tecnologia' : 'jogos'),
        timestamp: new Date(2025, 3, 24 - i).toLocaleString('pt-BR'),
        sentiment: Math.random() > 0.7 ? 'positivo' : (Math.random() > 0.4 ? 'neutro' : 'negativo')
      }));
      
      // Simular tópicos
      topics = [
        { name: 'Programação', count: 45, percentage: 35 },
        { name: 'Inteligência Artificial', count: 32, percentage: 25 },
        { name: 'Jogos', count: 25, percentage: 20 },
        { name: 'Hardware', count: 15, percentage: 12 },
        { name: 'Filmes', count: 10, percentage: 8 }
      ];
      
      // Simular emoções
      emotions = [
        { name: 'Neutro', count: 78, percentage: 50 },
        { name: 'Entusiasmo', count: 31, percentage: 20 },
        { name: 'Curiosidade', count: 23, percentage: 15 },
        { name: 'Satisfação', count: 16, percentage: 10 },
        { name: 'Frustração', count: 8, percentage: 5 }
      ];
      
      // Simular expressões frequentes
      expressions = [
        { text: 'interessante', count: 12 },
        { text: 'como funciona', count: 8 },
        { text: 'muito bom', count: 7 },
        { text: 'não entendi', count: 5 },
        { text: 'obrigado pela ajuda', count: 4 }
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
        values.push(Math.floor(Math.random() * 10));
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
      console.error('Erro ao carregar dados do usuário:', err);
      error = 'Não foi possível carregar os dados do usuário. Tente novamente mais tarde.';
    } finally {
      loading = false;
    }
  }
  
  // Função para salvar notas do usuário
  async function saveUserNotes() {
    try {
      loading = true;
      saveSuccess = false;
      saveError = null;
      
      // Em uma implementação real, enviaríamos esses dados para a API
      // Simulando requisição para demonstração
      await new Promise(resolve => setTimeout(resolve, 600)); // Simular delay de rede
      
      // Atualizar dados locais
      user.notes = userNotes;
      
      // Simular sucesso
      saveSuccess = true;
      editingNotes = false;
      
      // Resetar mensagem de sucesso após 3 segundos
      setTimeout(() => {
        saveSuccess = false;
      }, 3000);
      
    } catch (error) {
      console.error('Erro ao salvar notas:', error);
      saveError = 'Não foi possível salvar as notas. Tente novamente mais tarde.';
    } finally {
      loading = false;
    }
  }
  
  // Função para cancelar edição de notas
  function cancelEditNotes() {
    userNotes = user.notes;
    editingNotes = false;
  }
  
  // Função para alternar seleção de interação
  function toggleInteractionSelection(id) {
    if (selectedInteractions.includes(id)) {
      selectedInteractions = selectedInteractions.filter(item => item !== id);
    } else {
      selectedInteractions = [...selectedInteractions, id];
    }
  }
  
  // Função para excluir interações selecionadas
  async function deleteSelectedInteractions() {
    try {
      loading = true;
      deleteSuccess = false;
      deleteError = null;
      
      // Em uma implementação real, enviaríamos esses dados para a API
      // Simulando requisição para demonstração
      await new Promise(resolve => setTimeout(resolve, 800)); // Simular delay de rede
      
      // Atualizar dados locais
      interactions = interactions.filter(interaction => !selectedInteractions.includes(interaction.id));
      
      // Simular sucesso
      deleteSuccess = true;
      selectedInteractions = [];
      confirmDelete = false;
      
      // Resetar mensagem de sucesso após 3 segundos
      setTimeout(() => {
        deleteSuccess = false;
      }, 3000);
      
    } catch (error) {
      console.error('Erro ao excluir interações:', error);
      deleteError = 'Não foi possível excluir as interações. Tente novamente mais tarde.';
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
  
  // Opções para o gráfico
  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: 'Atividade do Usuário'
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
  
  // Carregar dados do usuário ao montar o componente
  onMount(() => {
    loadUserData();
  });
</script>

<div class="fade-in">
  <div class="flex justify-between items-center mb-6">
    <div class="flex items-center">
      <Link to="/users" class="text-primary-600 hover:text-primary-800 mr-2">
        <i class="fas fa-arrow-left"></i>
      </Link>
      <h1 class="m-0">Detalhes do Usuário</h1>
    </div>
  </div>
  
  {#if loading && !user}
    <div class="card p-8 text-center">
      <i class="fas fa-spinner fa-spin text-primary-500 text-2xl mb-2"></i>
      <p class="text-neutral-600">Carregando dados do usuário...</p>
    </div>
  {:else if error}
    <div class="card p-8 text-center">
      <i class="fas fa-exclamation-circle text-red-500 text-2xl mb-2"></i>
      <p class="text-neutral-600">{error}</p>
      <button 
        class="mt-4 btn btn-primary"
        on:click={loadUserData}
      >
        Tentar novamente
      </button>
    </div>
  {:else if user}
    <!-- Cabeçalho do usuário -->
    <div class="card p-6 mb-6">
      <div class="flex items-center">
        <div class="flex-shrink-0 h-16 w-16 rounded-full bg-primary-100 flex items-center justify-center">
          <span class="text-primary-800 font-medium text-2xl">{user.username.charAt(0).toUpperCase()}</span>
        </div>
        <div class="ml-4 flex-1">
          <h2 class="text-xl font-semibold m-0">{user.username}</h2>
          <p class="text-neutral-500 m-0">ID: {user.user_id}</p>
          <div class="flex mt-1">
            <span class="text-sm text-neutral-500 mr-4">
              <i class="fas fa-calendar-alt mr-1"></i> Primeiro contato: {user.first_seen}
            </span>
            <span class="text-sm text-neutral-500">
              <i class="fas fa-clock mr-1"></i> Última atividade: {user.last_seen}
            </span>
          </div>
        </div>
        <div class="text-right">
          <div class="text-2xl font-semibold text-primary-600">{user.interaction_count}</div>
          <div class="text-sm text-neutral-500">interações</div>
          <div class="text-sm text-neutral-500 mt-1">{user.voice_time} min em canais de voz</div>
        </div>
      </div>
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
          class="py-2 px-1 border-b-2 {activeTab === 'interactions' ? 'border-primary-500 text-primary-600' : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300'} transition-colors duration-200"
          on:click={() => activeTab = 'interactions'}
        >
          Interações
        </button>
        <button 
          class="py-2 px-1 border-b-2 {activeTab === 'topics' ? 'border-primary-500 text-primary-600' : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300'} transition-colors duration-200"
          on:click={() => activeTab = 'topics'}
        >
          Tópicos e Emoções
        </button>
        <button 
          class="py-2 px-1 border-b-2 {activeTab === 'notes' ? 'border-primary-500 text-primary-600' : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300'} transition-colors duration-200"
          on:click={() => activeTab = 'notes'}
        >
          Notas
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
        
        <!-- Emoções principais -->
        <div class="card p-6">
          <h2 class="text-lg font-semibold mb-4">Emoções Detectadas</h2>
          <ul class="space-y-3">
            {#each emotions as emotion}
              <li>
                <div class="flex justify-between mb-1">
                  <span class="text-sm font-medium text-neutral-700">{emotion.name}</span>
                  <span class="text-sm text-neutral-500">{emotion.count} ocorrências ({emotion.percentage}%)</span>
                </div>
                <div class="w-full bg-neutral-200 rounded-full h-2">
                  <div 
                    class="bg-secondary-600 h-2 rounded-full" 
                    style="width: {emotion.percentage}%"
                  ></div>
                </div>
              </li>
            {/each}
          </ul>
        </div>
      </div>
      
      <!-- Expressões frequentes -->
      <div class="card p-6 mt-6">
        <h2 class="text-lg font-semibold mb-4">Expressões Frequentes</h2>
        <div class="flex flex-wrap gap-2">
          {#each expressions as expression}
            <div class="px-3 py-1 bg-neutral-100 rounded-full text-sm">
              {expression.text} <span class="text-neutral-500">({expression.count}x)</span>
            </div>
          {/each}
        </div>
      </div>
    {:else if activeTab === 'interactions'}
      <div class="card overflow-hidden">
        <div class="p-4 border-b border-neutral-200 flex justify-between items-center">
          <h2 class="text-lg font-semibold m-0">Histórico de Interações</h2>
          
          {#if selectedInteractions.length > 0}
            <div class="flex items-center">
              <span class="text-sm text-neutral-600 mr-3">
                {selectedInteractions.length} {selectedInteractions.length === 1 ? 'item selecionado' : 'itens selecionados'}
              </span>
              {#if confirmDelete}
                <div class="flex items-center bg-red-50 border border-red-200 rounded-md p-2">
                  <span class="text-sm text-red-600 mr-2">Confirmar exclusão?</span>
                  <button 
                    class="text-white bg-red-600 hover:bg-red-700 px-2 py-1 rounded text-xs mr-1"
                    on:click={deleteSelectedInteractions}
                    disabled={loading}
                  >
                    Sim
                  </button>
                  <button 
                    class="text-red-600 bg-white hover:bg-red-50 border border-red-300 px-2 py-1 rounded text-xs"
                    on:click={() => confirmDelete = false}
                  >
                    Não
                  </button>
                </div>
              {:else}
                <button 
                  class="text-red-600 hover:text-red-800"
                  on:click={() => confirmDelete = true}
                >
                  <i class="fas fa-trash-alt"></i> Excluir
                </button>
              {/if}
            </div>
          {/if}
        </div>
        
        {#if deleteSuccess}
          <div class="p-3 bg-green-50 border-b border-green-200">
            <p class="text-sm text-green-600 m-0">
              <i class="fas fa-check-circle mr-1"></i>
              Interações excluídas com sucesso!
            </p>
          </div>
        {/if}
        
        {#if deleteError}
          <div class="p-3 bg-red-50 border-b border-red-200">
            <p class="text-sm text-red-600 m-0">
              <i class="fas fa-exclamation-circle mr-1"></
(Content truncated due to size limit. Use line ranges to read in chunks)