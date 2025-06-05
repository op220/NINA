<script>
  import { onMount } from 'svelte';
  import { Link } from 'svelte-navigator';
  import { Doughnut, Bar } from 'svelte-chartjs';
  import { 
    Chart, 
    Title, 
    Tooltip, 
    Legend, 
    ArcElement, 
    CategoryScale,
    LinearScale,
    BarElement
  } from 'chart.js';
  
  // Registrar componentes do Chart.js
  Chart.register(
    Title, 
    Tooltip, 
    Legend, 
    ArcElement, 
    CategoryScale,
    LinearScale,
    BarElement
  );
  
  // Dados para os gráficos
  let userStats = {
    count: 0,
    active: 0
  };
  
  let channelStats = {
    count: 0,
    active: 0
  };
  
  let interactionStats = {
    count: 0,
    today: 0
  };
  
  let topicData = {
    labels: [],
    datasets: [{
      label: 'Tópicos Populares',
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
  
  let activityData = {
    labels: [],
    datasets: [{
      label: 'Atividade Diária',
      data: [],
      backgroundColor: 'rgba(54, 162, 235, 0.5)',
      borderColor: 'rgba(54, 162, 235, 1)',
      borderWidth: 1
    }]
  };
  
  // Opções para os gráficos
  const doughnutOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom',
      },
      title: {
        display: true,
        text: 'Tópicos Populares'
      }
    }
  };
  
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
  
  // Atividades recentes simuladas
  let recentActivities = [];
  
  onMount(async () => {
    try {
      // Em uma implementação real, buscaríamos esses dados da API
      // Simulando dados para demonstração
      
      // Estatísticas básicas
      userStats = {
        count: 45,
        active: 12
      };
      
      channelStats = {
        count: 8,
        active: 5
      };
      
      interactionStats = {
        count: 1243,
        today: 87
      };
      
      // Dados de tópicos
      topicData = {
        labels: ['Tecnologia', 'Jogos', 'Música', 'Filmes', 'Animes'],
        datasets: [{
          label: 'Tópicos Populares',
          data: [35, 25, 20, 15, 5],
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
      
      // Dados de atividade
      const days = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'];
      activityData = {
        labels: days,
        datasets: [{
          label: 'Mensagens',
          data: [65, 78, 52, 91, 43, 36, 87],
          backgroundColor: 'rgba(54, 162, 235, 0.5)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        }]
      };
      
      // Atividades recentes
      recentActivities = [
        { 
          id: 1, 
          type: 'message', 
          user: 'João Silva', 
          channel: 'geral', 
          time: '5 minutos atrás',
          content: 'Alguém pode me ajudar com um problema de configuração?'
        },
        { 
          id: 2, 
          type: 'voice', 
          user: 'Maria Oliveira', 
          channel: 'voz-1', 
          time: '15 minutos atrás',
          duration: '23 minutos'
        },
        { 
          id: 3, 
          type: 'personality', 
          channel: 'suporte', 
          time: '1 hora atrás',
          change: 'Personalidade ajustada para mais técnica'
        },
        { 
          id: 4, 
          type: 'message', 
          user: 'Carlos Mendes', 
          channel: 'tecnologia', 
          time: '2 horas atrás',
          content: 'Acabei de instalar o novo sistema e está funcionando perfeitamente!'
        },
        { 
          id: 5, 
          type: 'system', 
          time: '3 horas atrás',
          content: 'Backup automático realizado com sucesso'
        }
      ];
      
    } catch (error) {
      console.error('Erro ao carregar dados do dashboard:', error);
    }
  });
  
  // Função para obter ícone com base no tipo de atividade
  function getActivityIcon(type) {
    switch(type) {
      case 'message': return 'fas fa-comment';
      case 'voice': return 'fas fa-microphone';
      case 'personality': return 'fas fa-sliders-h';
      case 'system': return 'fas fa-cog';
      default: return 'fas fa-info-circle';
    }
  }
  
  // Função para obter cor com base no tipo de atividade
  function getActivityColor(type) {
    switch(type) {
      case 'message': return 'bg-blue-100 text-blue-800';
      case 'voice': return 'bg-green-100 text-green-800';
      case 'personality': return 'bg-purple-100 text-purple-800';
      case 'system': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  }
</script>

<div class="fade-in">
  <h1>Dashboard</h1>
  
  <!-- Cards de estatísticas -->
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
    <!-- Usuários -->
    <div class="card flex items-center">
      <div class="rounded-full bg-blue-100 p-3 mr-4">
        <i class="fas fa-users text-blue-600 text-xl"></i>
      </div>
      <div>
        <h3 class="text-lg font-semibold m-0">{userStats.count}</h3>
        <p class="text-neutral-500 text-sm m-0">Usuários</p>
        <p class="text-xs text-green-600 m-0">{userStats.active} ativos hoje</p>
      </div>
    </div>
    
    <!-- Canais -->
    <div class="card flex items-center">
      <div class="rounded-full bg-purple-100 p-3 mr-4">
        <i class="fas fa-comments text-purple-600 text-xl"></i>
      </div>
      <div>
        <h3 class="text-lg font-semibold m-0">{channelStats.count}</h3>
        <p class="text-neutral-500 text-sm m-0">Canais</p>
        <p class="text-xs text-green-600 m-0">{channelStats.active} ativos hoje</p>
      </div>
    </div>
    
    <!-- Interações -->
    <div class="card flex items-center">
      <div class="rounded-full bg-green-100 p-3 mr-4">
        <i class="fas fa-exchange-alt text-green-600 text-xl"></i>
      </div>
      <div>
        <h3 class="text-lg font-semibold m-0">{interactionStats.count}</h3>
        <p class="text-neutral-500 text-sm m-0">Interações</p>
        <p class="text-xs text-green-600 m-0">{interactionStats.today} hoje</p>
      </div>
    </div>
    
    <!-- Memória -->
    <div class="card flex items-center">
      <div class="rounded-full bg-yellow-100 p-3 mr-4">
        <i class="fas fa-brain text-yellow-600 text-xl"></i>
      </div>
      <div>
        <h3 class="text-lg font-semibold m-0">100%</h3>
        <p class="text-neutral-500 text-sm m-0">Memória</p>
        <p class="text-xs text-blue-600 m-0">Funcionando normalmente</p>
      </div>
    </div>
  </div>
  
  <!-- Gráficos -->
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
    <!-- Gráfico de tópicos -->
    <div class="card p-4">
      <h2 class="text-lg font-semibold mb-4">Tópicos Populares</h2>
      <div class="h-64">
        <Doughnut data={topicData} options={doughnutOptions} />
      </div>
    </div>
    
    <!-- Gráfico de atividade -->
    <div class="card p-4">
      <h2 class="text-lg font-semibold mb-4">Atividade Semanal</h2>
      <div class="h-64">
        <Bar data={activityData} options={barOptions} />
      </div>
    </div>
  </div>
  
  <!-- Atividades recentes -->
  <div class="card p-4">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-lg font-semibold m-0">Atividades Recentes</h2>
      <Link to="/statistics" class="text-primary-600 hover:text-primary-800 text-sm">
        Ver todas
      </Link>
    </div>
    
    <div class="overflow-hidden">
      <ul class="divide-y divide-neutral-200">
        {#each recentActivities as activity}
          <li class="py-3 flex items-start">
            <div class="rounded-full {getActivityColor(activity.type)} p-2 mr-3">
              <i class="{getActivityIcon(activity.type)}"></i>
            </div>
            <div class="flex-1 min-w-0">
              {#if activity.type === 'message'}
                <p class="text-sm font-medium text-neutral-900 truncate">
                  <span class="font-semibold">{activity.user}</span> em <span class="font-semibold">#{activity.channel}</span>
                </p>
                <p class="text-sm text-neutral-500 truncate">{activity.content}</p>
              {:else if activity.type === 'voice'}
                <p class="text-sm font-medium text-neutral-900 truncate">
                  <span class="font-semibold">{activity.user}</span> esteve em <span class="font-semibold">#{activity.channel}</span>
                </p>
                <p class="text-sm text-neutral-500 truncate">Duração: {activity.duration}</p>
              {:else if activity.type === 'personality'}
                <p class="text-sm font-medium text-neutral-900 truncate">
                  Personalidade atualizada em <span class="font-semibold">#{activity.channel}</span>
                </p>
                <p class="text-sm text-neutral-500 truncate">{activity.change}</p>
              {:else}
                <p class="text-sm font-medium text-neutral-900 truncate">
                  Evento do sistema
                </p>
                <p class="text-sm text-neutral-500 truncate">{activity.content}</p>
              {/if}
              <p class="text-xs text-neutral-400">{activity.time}</p>
            </div>
          </li>
        {/each}
      </ul>
    </div>
  </div>
  
  <!-- Links rápidos -->
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
    <Link to="/users" class="card p-4 hover:bg-neutral-50 transition-colors duration-200">
      <div class="flex items-center">
        <div class="rounded-full bg-blue-100 p-3 mr-4">
          <i class="fas fa-users text-blue-600"></i>
        </div>
        <div>
          <h3 class="font-semibold">Gerenciar Usuários</h3>
          <p class="text-sm text-neutral-500 m-0">Visualizar e editar perfis de usuários</p>
        </div>
      </div>
    </Link>
    
    <Link to="/channels" class="card p-4 hover:bg-neutral-50 transition-colors duration-200">
      <div class="flex items-center">
        <div class="rounded-full bg-purple-100 p-3 mr-4">
          <i class="fas fa-comments text-purple-600"></i>
        </div>
        <div>
          <h3 class="font-semibold">Gerenciar Canais</h3>
          <p class="text-sm text-neutral-500 m-0">Configurar personalidades por canal</p>
        </div>
      </div>
    </Link>
    
    <Link to="/settings" class="card p-4 hover:bg-neutral-50 transition-colors duration-200">
      <div class="flex items-center">
        <div class="rounded-full bg-green-100 p-3 mr-4">
          <i class="fas fa-cog text-green-600"></i>
        </div>
        <div>
          <h3 class="font-semibold">Configurações</h3>
          <p class="text-sm text-neutral-500 m-0">Ajustar configurações do sistema</p>
        </div>
      </div>
    </Link>
  </div>
</div>
