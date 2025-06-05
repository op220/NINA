<script>
  import { onMount } from 'svelte';
  import { Link } from 'svelte-navigator';
  import { Bar, Line } from 'svelte-chartjs';
  import { 
    Chart, 
    Title, 
    Tooltip, 
    Legend, 
    CategoryScale,
    LinearScale,
    BarElement,
    LineElement,
    PointElement
  } from 'chart.js';
  
  // Registrar componentes do Chart.js
  Chart.register(
    Title, 
    Tooltip, 
    Legend, 
    CategoryScale,
    LinearScale,
    BarElement,
    LineElement,
    PointElement
  );
  
  // Estado para armazenar estatísticas
  let generalStats = {};
  let userStats = {};
  let channelStats = {};
  let topicStats = {};
  let activityStats = {};
  
  let loading = true;
  let error = null;
  
  // Dados para os gráficos
  let activityData = {
    labels: [],
    datasets: [{
      label: 'Mensagens',
      data: [],
      backgroundColor: 'rgba(54, 162, 235, 0.5)',
      borderColor: 'rgba(54, 162, 235, 1)',
      borderWidth: 1
    }]
  };
  
  let topicsData = {
    labels: [],
    datasets: [{
      label: 'Tópicos',
      data: [],
      backgroundColor: [
        'rgba(54, 162, 235, 0.8)',
        'rgba(255, 99, 132, 0.8)',
        'rgba(255, 206, 86, 0.8)',
        'rgba(75, 192, 192, 0.8)',
        'rgba(153, 102, 255, 0.8)'
      ],
      borderWidth: 1
    }]
  };
  
  let usersData = {
    labels: [],
    datasets: [{
      label: 'Usuários Mais Ativos',
      data: [],
      backgroundColor: 'rgba(75, 192, 192, 0.5)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 1
    }]
  };
  
  let channelsData = {
    labels: [],
    datasets: [{
      label: 'Canais Mais Ativos',
      data: [],
      backgroundColor: 'rgba(153, 102, 255, 0.5)',
      borderColor: 'rgba(153, 102, 255, 1)',
      borderWidth: 1
    }]
  };
  
  // Opções para os gráficos
  const barOptions = {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: 'Atividade Diária'
      }
    },
    scales: {
      y: {
        beginAtZero: true
      }
    }
  };
  
  const lineOptions = {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: 'Tendência de Atividade'
      }
    },
    scales: {
      y: {
        beginAtZero: true
      }
    }
  };
  
  // Período de tempo para estatísticas
  let timePeriod = '7'; // dias
  
  // Função para carregar estatísticas
  async function loadStatistics(days = 7) {
    try {
      loading = true;
      error = null;
      
      // Em uma implementação real, buscaríamos esses dados da API
      // Simulando dados para demonstração
      await new Promise(resolve => setTimeout(resolve, 800)); // Simular delay de rede
      
      // Estatísticas gerais
      generalStats = {
        user_count: 45,
        channel_count: 8,
        interaction_count: 1243,
        topic_count: 15
      };
      
      // Estatísticas de usuários
      userStats = {
        top_users: [
          { username: 'João Silva', interaction_count: 156 },
          { username: 'Maria Oliveira', interaction_count: 132 },
          { username: 'Carlos Mendes', interaction_count: 98 },
          { username: 'Ana Santos', interaction_count: 87 },
          { username: 'Pedro Costa', interaction_count: 76 }
        ],
        average_interactions_per_user: 27.6
      };
      
      // Estatísticas de canais
      channelStats = {
        top_channels: [
          { channel_name: 'geral', message_count: 345 },
          { channel_name: 'tecnologia', message_count: 287 },
          { channel_name: 'jogos', message_count: 198 },
          { channel_name: 'música', message_count: 176 },
          { channel_name: 'filmes', message_count: 143 }
        ],
        average_interactions_per_channel: 155.4
      };
      
      // Estatísticas de tópicos
      topicStats = {
        top_topics: [
          { topic: 'Tecnologia', count: 356 },
          { topic: 'Jogos', count: 245 },
          { topic: 'Música', count: 187 },
          { topic: 'Filmes', count: 156 },
          { topic: 'Animes', count: 98 }
        ]
      };
      
      // Estatísticas de atividade
      const dateLabels = [];
      const activityValues = [];
      
      // Gerar datas para os últimos X dias
      const today = new Date();
      for (let i = days - 1; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        dateLabels.push(date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' }));
        
        // Gerar valores aleatórios para atividade
        activityValues.push(Math.floor(Math.random() * 100) + 50);
      }
      
      activityStats = {
        dates: dateLabels,
        values: activityValues,
        total: activityValues.reduce((sum, val) => sum + val, 0)
      };
      
      // Atualizar dados dos gráficos
      activityData = {
        labels: activityStats.dates,
        datasets: [{
          label: 'Mensagens',
          data: activityStats.values,
          backgroundColor: 'rgba(54, 162, 235, 0.5)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        }]
      };
      
      topicsData = {
        labels: topicStats.top_topics.map(t => t.topic),
        datasets: [{
          label: 'Tópicos',
          data: topicStats.top_topics.map(t => t.count),
          backgroundColor: [
            'rgba(54, 162, 235, 0.8)',
            'rgba(255, 99, 132, 0.8)',
            'rgba(255, 206, 86, 0.8)',
            'rgba(75, 192, 192, 0.8)',
            'rgba(153, 102, 255, 0.8)'
          ],
          borderWidth: 1
        }]
      };
      
      usersData = {
        labels: userStats.top_users.map(u => u.username),
        datasets: [{
          label: 'Interações',
          data: userStats.top_users.map(u => u.interaction_count),
          backgroundColor: 'rgba(75, 192, 192, 0.5)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        }]
      };
      
      channelsData = {
        labels: channelStats.top_channels.map(c => c.channel_name),
        datasets: [{
          label: 'Mensagens',
          data: channelStats.top_channels.map(c => c.message_count),
          backgroundColor: 'rgba(153, 102, 255, 0.5)',
          borderColor: 'rgba(153, 102, 255, 1)',
          borderWidth: 1
        }]
      };
      
    } catch (err) {
      console.error('Erro ao carregar estatísticas:', err);
      error = 'Não foi possível carregar as estatísticas. Tente novamente mais tarde.';
    } finally {
      loading = false;
    }
  }
  
  // Função para atualizar período de tempo
  function updateTimePeriod() {
    loadStatistics(parseInt(timePeriod));
  }
  
  // Carregar estatísticas ao montar o componente
  onMount(() => {
    loadStatistics(parseInt(timePeriod));
  });
</script>

<div class="fade-in">
  <div class="flex justify-between items-center mb-6">
    <h1>Estatísticas</h1>
    
    <!-- Seletor de período -->
    <div class="flex items-center">
      <label for="time-period" class="mr-2 text-sm font-medium text-neutral-700">Período:</label>
      <select 
        id="time-period" 
        bind:value={timePeriod} 
        on:change={updateTimePeriod}
        class="select w-auto"
      >
        <option value="7">Últimos 7 dias</option>
        <option value="14">Últimos 14 dias</option>
        <option value="30">Últimos 30 dias</option>
        <option value="90">Últimos 90 dias</option>
      </select>
    </div>
  </div>
  
  {#if loading}
    <div class="card p-8 text-center">
      <i class="fas fa-spinner fa-spin text-primary-500 text-2xl mb-2"></i>
      <p class="text-neutral-600">Carregando estatísticas...</p>
    </div>
  {:else if error}
    <div class="card p-8 text-center">
      <i class="fas fa-exclamation-circle text-red-500 text-2xl mb-2"></i>
      <p class="text-neutral-600">{error}</p>
      <button 
        class="mt-4 btn btn-primary"
        on:click={() => loadStatistics(parseInt(timePeriod))}
      >
        Tentar novamente
      </button>
    </div>
  {:else}
    <!-- Cards de estatísticas -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <!-- Usuários -->
      <div class="card flex items-center">
        <div class="rounded-full bg-blue-100 p-3 mr-4">
          <i class="fas fa-users text-blue-600 text-xl"></i>
        </div>
        <div>
          <h3 class="text-lg font-semibold m-0">{generalStats.user_count}</h3>
          <p class="text-neutral-500 text-sm m-0">Usuários</p>
          <p class="text-xs text-neutral-500 m-0">~{userStats.average_interactions_per_user.toFixed(1)} interações/usuário</p>
        </div>
      </div>
      
      <!-- Canais -->
      <div class="card flex items-center">
        <div class="rounded-full bg-purple-100 p-3 mr-4">
          <i class="fas fa-comments text-purple-600 text-xl"></i>
        </div>
        <div>
          <h3 class="text-lg font-semibold m-0">{generalStats.channel_count}</h3>
          <p class="text-neutral-500 text-sm m-0">Canais</p>
          <p class="text-xs text-neutral-500 m-0">~{channelStats.average_interactions_per_channel.toFixed(1)} mensagens/canal</p>
        </div>
      </div>
      
      <!-- Interações -->
      <div class="card flex items-center">
        <div class="rounded-full bg-green-100 p-3 mr-4">
          <i class="fas fa-exchange-alt text-green-600 text-xl"></i>
        </div>
        <div>
          <h3 class="text-lg font-semibold m-0">{generalStats.interaction_count}</h3>
          <p class="text-neutral-500 text-sm m-0">Interações</p>
          <p class="text-xs text-green-600 m-0">{activityStats.total} nos últimos {timePeriod} dias</p>
        </div>
      </div>
      
      <!-- Tópicos -->
      <div class="card flex items-center">
        <div class="rounded-full bg-yellow-100 p-3 mr-4">
          <i class="fas fa-tags text-yellow-600 text-xl"></i>
        </div>
        <div>
          <h3 class="text-lg font-semibold m-0">{generalStats.topic_count}</h3>
          <p class="text-neutral-500 text-sm m-0">Tópicos</p>
          <p class="text-xs text-neutral-500 m-0">Detectados nas conversas</p>
        </div>
      </div>
    </div>
    
    <!-- Gráficos principais -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <!-- Gráfico de atividade -->
      <div class="card p-4">
        <h2 class="text-lg font-semibold mb-4">Atividade Diária</h2>
        <div class="h-64">
          <Bar data={activityData} options={barOptions} />
        </div>
      </div>
      
      <!-- Gráfico de tópicos -->
      <div class="card p-4">
        <h2 class="text-lg font-semibold mb-4">Tópicos Populares</h2>
        <div class="h-64">
          <Bar data={topicsData} options={barOptions} />
        </div>
      </div>
    </div>
    
    <!-- Gráficos secundários -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <!-- Usuários mais ativos -->
      <div class="card p-4">
        <h2 class="text-lg font-semibold mb-4">Usuários Mais Ativos</h2>
        <div class="h-64">
          <Bar data={usersData} options={barOptions} />
        </div>
      </div>
      
      <!-- Canais mais ativos -->
      <div class="card p-4">
        <h2 class="text-lg font-semibold mb-4">Canais Mais Ativos</h2>
        <div class="h-64">
          <Bar data={channelsData} options={barOptions} />
        </div>
      </div>
    </div>
    
    <!-- Tendência de atividade -->
    <div class="card p-4 mb-6">
      <h2 class="text-lg font-semibold mb-4">Tendência de Atividade</h2>
      <div class="h-64">
        <Line data={activityData} options={lineOptions} />
      </div>
    </div>
    
    <!-- Tabelas de estatísticas -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Usuários mais ativos -->
      <div class="card overflow-hidden">
        <div class="p-4 border-b border-neutral-200">
          <h2 class="text-lg font-semibold m-0">Usuários Mais Ativos</h2>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-neutral-200">
            <thead class="bg-neutral-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                  Usuário
                </th>
                <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-neutral-500 uppercase tracking-wider">
                  Interações
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-neutral-200">
              {#each userStats.top_users as user, i}
                <tr class="hover:bg-neutral-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="flex-shrink-0 h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center">
                        <span class="text-primary-800 font-medium">{user.username.charAt(0).toUpperCase()}</span>
                      </div>
                      <div class="ml-3">
                        <div class="text-sm font-medium text-neutral-900">{user.username}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right">
                    <div class="text-sm font-medium text-neutral-900">{user.interaction_count}</div>
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Canais mais ativos -->
      <div class="card overflow-hidden">
        <div class="p-4 border-b border-neutral-200">
          <h2 class="text-lg font-semibold m-0">Canais Mais Ativos</h2>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-neutral-200">
            <thead class="bg-neutral-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                  Canal
                </th>
                <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-neutral-500 uppercase tracking-wider">
                  Mensagens
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-neutral-200">
              {#each channelStats.top_channels as channel, i}
                <tr class="hover:bg-neutral-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="flex-shrink-0 h-8 w-8 rounded-full bg-purple-100 flex items-center justify-center">
                        <i class="fas fa-hashtag text-purple-800"></i>
                      </div>
                      <div class="ml-3">
                        <div class="text-sm font-medium text-neutral-900">{channel.channel_name}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right">
                    <div class="text-sm font-medium text-neutral-900">{channel.message_count}</div>
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  {/if}
</div>
