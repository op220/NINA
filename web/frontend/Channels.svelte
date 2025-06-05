<script>
  import { onMount } from 'svelte';
  import { Link } from 'svelte-navigator';
  
  // Estado para armazenar a lista de canais
  let channels = [];
  let loading = true;
  let error = null;
  
  // Estado para paginação
  let currentPage = 1;
  let totalPages = 1;
  let limit = 10;
  
  // Estado para busca
  let searchQuery = '';
  let searching = false;
  
  // Função para carregar canais
  async function loadChannels(page = 1, query = '') {
    try {
      loading = true;
      error = null;
      
      // Em uma implementação real, buscaríamos esses dados da API
      // Simulando dados para demonstração
      await new Promise(resolve => setTimeout(resolve, 500)); // Simular delay de rede
      
      if (query) {
        // Simular busca
        channels = Array(5).fill().map((_, i) => ({
          channel_id: `channel${i+1}`,
          channel_name: `Canal ${query} ${i+1}`,
          message_count: Math.floor(Math.random() * 1000),
          last_activity: new Date(Date.now() - Math.floor(Math.random() * 7 * 24 * 60 * 60 * 1000)).toLocaleDateString('pt-BR'),
          type: i % 2 === 0 ? 'texto' : 'voz',
          personality: {
            formality_level: Math.floor(Math.random() * 100),
            humor_level: Math.floor(Math.random() * 100),
            technicality_level: Math.floor(Math.random() * 100)
          }
        }));
        totalPages = 1;
      } else {
        // Simular lista paginada
        channels = Array(limit).fill().map((_, i) => ({
          channel_id: `channel${(page-1)*limit + i + 1}`,
          channel_name: `Canal ${(page-1)*limit + i + 1}`,
          message_count: Math.floor(Math.random() * 1000),
          last_activity: new Date(Date.now() - Math.floor(Math.random() * 7 * 24 * 60 * 60 * 1000)).toLocaleDateString('pt-BR'),
          type: i % 3 === 0 ? 'voz' : 'texto',
          personality: {
            formality_level: Math.floor(Math.random() * 100),
            humor_level: Math.floor(Math.random() * 100),
            technicality_level: Math.floor(Math.random() * 100)
          }
        }));
        totalPages = 3; // Simular 3 páginas
      }
      
      currentPage = page;
      
    } catch (err) {
      console.error('Erro ao carregar canais:', err);
      error = 'Não foi possível carregar a lista de canais. Tente novamente mais tarde.';
      channels = [];
    } finally {
      loading = false;
      searching = false;
    }
  }
  
  // Função para buscar canais
  function searchChannels() {
    if (searchQuery.trim()) {
      searching = true;
      loadChannels(1, searchQuery);
    } else {
      loadChannels(currentPage);
    }
  }
  
  // Função para limpar busca
  function clearSearch() {
    searchQuery = '';
    loadChannels(1);
  }
  
  // Função para navegar entre páginas
  function goToPage(page) {
    if (page >= 1 && page <= totalPages) {
      loadChannels(page);
    }
  }
  
  // Função para obter cor com base no nível
  function getLevelColor(level) {
    if (level < 30) return 'bg-blue-100 text-blue-800';
    if (level < 70) return 'bg-green-100 text-green-800';
    return 'bg-red-100 text-red-800';
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
  
  // Carregar canais ao montar o componente
  onMount(() => {
    loadChannels();
  });
</script>

<div class="fade-in">
  <div class="flex justify-between items-center mb-6">
    <h1>Canais</h1>
    
    <!-- Barra de busca -->
    <div class="flex">
      <div class="relative">
        <input 
          type="text" 
          bind:value={searchQuery}
          placeholder="Buscar canais..." 
          class="input pr-10"
          on:keydown={(e) => e.key === 'Enter' && searchChannels()}
        />
        {#if searchQuery}
          <button 
            class="absolute right-10 top-1/2 transform -translate-y-1/2 text-neutral-400 hover:text-neutral-600"
            on:click={clearSearch}
          >
            <i class="fas fa-times"></i>
          </button>
        {/if}
        <button 
          class="absolute right-3 top-1/2 transform -translate-y-1/2 text-neutral-400 hover:text-neutral-600"
          on:click={searchChannels}
        >
          <i class="fas fa-search"></i>
        </button>
      </div>
    </div>
  </div>
  
  <!-- Mensagem de busca -->
  {#if searching}
    <div class="mb-4">
      <p class="text-sm text-neutral-600">
        Resultados para: <span class="font-medium">{searchQuery}</span>
        <button 
          class="ml-2 text-primary-600 hover:text-primary-800"
          on:click={clearSearch}
        >
          Limpar busca
        </button>
      </p>
    </div>
  {/if}
  
  <!-- Grid de canais -->
  {#if loading}
    <div class="card p-8 text-center">
      <i class="fas fa-spinner fa-spin text-primary-500 text-2xl mb-2"></i>
      <p class="text-neutral-600">Carregando canais...</p>
    </div>
  {:else if error}
    <div class="card p-8 text-center">
      <i class="fas fa-exclamation-circle text-red-500 text-2xl mb-2"></i>
      <p class="text-neutral-600">{error}</p>
      <button 
        class="mt-4 btn btn-primary"
        on:click={() => loadChannels()}
      >
        Tentar novamente
      </button>
    </div>
  {:else if channels.length === 0}
    <div class="card p-8 text-center">
      <i class="fas fa-comments text-neutral-400 text-2xl mb-2"></i>
      <p class="text-neutral-600">Nenhum canal encontrado.</p>
    </div>
  {:else}
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {#each channels as channel}
        <div class="card hover:shadow-lg transition-shadow duration-200">
          <div class="flex justify-between items-start mb-3">
            <div class="flex items-center">
              <div class="flex-shrink-0 h-10 w-10 rounded-full bg-primary-100 flex items-center justify-center">
                <i class={channel.type === 'voz' ? 'fas fa-microphone text-primary-800' : 'fas fa-hashtag text-primary-800'}></i>
              </div>
              <div class="ml-3">
                <h3 class="text-lg font-semibold">{channel.channel_name}</h3>
                <div class="flex items-center">
                  <span class="badge badge-neutral mr-2">{channel.type}</span>
                  <span class="text-xs text-neutral-500">{channel.message_count} mensagens</span>
                </div>
              </div>
            </div>
            <Link to={`/channels/${channel.channel_id}`} class="text-primary-600 hover:text-primary-800">
              <i class="fas fa-cog"></i>
            </Link>
          </div>
          
          <div class="border-t border-neutral-200 pt-3 mb-3">
            <h4 class="text-sm font-medium text-neutral-700 mb-2">Personalidade da Nina</h4>
            <div class="space-y-2">
              <div>
                <div class="flex justify-between text-xs mb-1">
                  <span>Formalidade</span>
                  <span class={getLevelColor(channel.personality.formality_level)}>
                    {getLevelDescription('formality_level', channel.personality.formality_level)}
                  </span>
                </div>
                <div class="w-full bg-neutral-200 rounded-full h-2">
                  <div 
                    class="bg-primary-600 h-2 rounded-full" 
                    style="width: {channel.personality.formality_level}%"
                  ></div>
                </div>
              </div>
              
              <div>
                <div class="flex justify-between text-xs mb-1">
                  <span>Humor</span>
                  <span class={getLevelColor(channel.personality.humor_level)}>
                    {getLevelDescription('humor_level', channel.personality.humor_level)}
                  </span>
                </div>
                <div class="w-full bg-neutral-200 rounded-full h-2">
                  <div 
                    class="bg-secondary-600 h-2 rounded-full" 
                    style="width: {channel.personality.humor_level}%"
                  ></div>
                </div>
              </div>
              
              <div>
                <div class="flex justify-between text-xs mb-1">
                  <span>Tecnicidade</span>
                  <span class={getLevelColor(channel.personality.technicality_level)}>
                    {getLevelDescription('technicality_level', channel.personality.technicality_level)}
                  </span>
                </div>
                <div class="w-full bg-neutral-200 rounded-full h-2">
                  <div 
                    class="bg-green-600 h-2 rounded-full" 
                    style="width: {channel.personality.technicality_level}%"
                  ></div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="text-xs text-neutral-500">
            Última atividade: {channel.last_activity}
          </div>
          
          <div class="mt-3 flex justify-end">
            <Link to={`/channels/${channel.channel_id}`} class="btn btn-outline text-sm">
              Gerenciar
            </Link>
          </div>
        </div>
      {/each}
    </div>
    
    <!-- Paginação -->
    {#if totalPages > 1}
      <div class="mt-6 flex items-center justify-between">
        <p class="text-sm text-neutral-700">
          Mostrando <span class="font-medium">{(currentPage - 1) * limit + 1}</span> a <span class="font-medium">{Math.min(currentPage * limit, (currentPage - 1) * limit + channels.length)}</span> de <span class="font-medium">{totalPages * limit}</span> resultados
        </p>
        <div class="flex space-x-2">
          <button 
            class="btn btn-outline {currentPage === 1 ? 'opacity-50 cursor-not-allowed' : ''}"
            disabled={currentPage === 1}
            on:click={() => goToPage(currentPage - 1)}
          >
            Anterior
          </button>
          <button 
            class="btn btn-outline {currentPage === totalPages ? 'opacity-50 cursor-not-allowed' : ''}"
            disabled={currentPage === totalPages}
            on:click={() => goToPage(currentPage + 1)}
          >
            Próxima
          </button>
        </div>
      </div>
    {/if}
  {/if}
</div>
