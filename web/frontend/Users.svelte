<script>
  import { onMount } from 'svelte';
  import { Link } from 'svelte-navigator';
  
  // Estado para armazenar a lista de usuários
  let users = [];
  let loading = true;
  let error = null;
  
  // Estado para paginação
  let currentPage = 1;
  let totalPages = 1;
  let limit = 10;
  
  // Estado para busca
  let searchQuery = '';
  let searching = false;
  
  // Função para carregar usuários
  async function loadUsers(page = 1, query = '') {
    try {
      loading = true;
      error = null;
      
      // Em uma implementação real, buscaríamos esses dados da API
      // Simulando dados para demonstração
      await new Promise(resolve => setTimeout(resolve, 500)); // Simular delay de rede
      
      if (query) {
        // Simular busca
        users = Array(5).fill().map((_, i) => ({
          user_id: `user${i+1}`,
          username: `Usuário ${query} ${i+1}`,
          interaction_count: Math.floor(Math.random() * 100),
          last_seen: new Date(Date.now() - Math.floor(Math.random() * 7 * 24 * 60 * 60 * 1000)).toLocaleDateString('pt-BR')
        }));
        totalPages = 1;
      } else {
        // Simular lista paginada
        users = Array(limit).fill().map((_, i) => ({
          user_id: `user${(page-1)*limit + i + 1}`,
          username: `Usuário ${(page-1)*limit + i + 1}`,
          interaction_count: Math.floor(Math.random() * 100),
          last_seen: new Date(Date.now() - Math.floor(Math.random() * 7 * 24 * 60 * 60 * 1000)).toLocaleDateString('pt-BR')
        }));
        totalPages = 5; // Simular 5 páginas
      }
      
      currentPage = page;
      
    } catch (err) {
      console.error('Erro ao carregar usuários:', err);
      error = 'Não foi possível carregar a lista de usuários. Tente novamente mais tarde.';
      users = [];
    } finally {
      loading = false;
      searching = false;
    }
  }
  
  // Função para buscar usuários
  function searchUsers() {
    if (searchQuery.trim()) {
      searching = true;
      loadUsers(1, searchQuery);
    } else {
      loadUsers(currentPage);
    }
  }
  
  // Função para limpar busca
  function clearSearch() {
    searchQuery = '';
    loadUsers(1);
  }
  
  // Função para navegar entre páginas
  function goToPage(page) {
    if (page >= 1 && page <= totalPages) {
      loadUsers(page);
    }
  }
  
  // Carregar usuários ao montar o componente
  onMount(() => {
    loadUsers();
  });
</script>

<div class="fade-in">
  <div class="flex justify-between items-center mb-6">
    <h1>Usuários</h1>
    
    <!-- Barra de busca -->
    <div class="flex">
      <div class="relative">
        <input 
          type="text" 
          bind:value={searchQuery}
          placeholder="Buscar usuários..." 
          class="input pr-10"
          on:keydown={(e) => e.key === 'Enter' && searchUsers()}
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
          on:click={searchUsers}
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
  
  <!-- Tabela de usuários -->
  <div class="card overflow-hidden">
    {#if loading}
      <div class="p-8 text-center">
        <i class="fas fa-spinner fa-spin text-primary-500 text-2xl mb-2"></i>
        <p class="text-neutral-600">Carregando usuários...</p>
      </div>
    {:else if error}
      <div class="p-8 text-center">
        <i class="fas fa-exclamation-circle text-red-500 text-2xl mb-2"></i>
        <p class="text-neutral-600">{error}</p>
        <button 
          class="mt-4 btn btn-primary"
          on:click={() => loadUsers()}
        >
          Tentar novamente
        </button>
      </div>
    {:else if users.length === 0}
      <div class="p-8 text-center">
        <i class="fas fa-users text-neutral-400 text-2xl mb-2"></i>
        <p class="text-neutral-600">Nenhum usuário encontrado.</p>
      </div>
    {:else}
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-neutral-200">
          <thead class="bg-neutral-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                Usuário
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                Interações
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                Última atividade
              </th>
              <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-neutral-500 uppercase tracking-wider">
                Ações
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-neutral-200">
            {#each users as user}
              <tr class="hover:bg-neutral-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 h-10 w-10 rounded-full bg-primary-100 flex items-center justify-center">
                      <span class="text-primary-800 font-medium">{user.username.charAt(0).toUpperCase()}</span>
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-medium text-neutral-900">{user.username}</div>
                      <div class="text-sm text-neutral-500">ID: {user.user_id}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-neutral-900">{user.interaction_count}</div>
                  <div class="text-xs text-neutral-500">mensagens</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-neutral-900">{user.last_seen}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <Link to={`/users/${user.user_id}`} class="text-primary-600 hover:text-primary-900 mr-3">
                    Detalhes
                  </Link>
                  <button class="text-red-600 hover:text-red-900">
                    Limpar memória
                  </button>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
      
      <!-- Paginação -->
      {#if totalPages > 1}
        <div class="px-6 py-3 flex items-center justify-between border-t border-neutral-200">
          <div class="flex-1 flex justify-between items-center">
            <p class="text-sm text-neutral-700">
              Mostrando <span class="font-medium">{(currentPage - 1) * limit + 1}</span> a <span class="font-medium">{Math.min(currentPage * limit, (currentPage - 1) * limit + users.length)}</span> de <span class="font-medium">{totalPages * limit}</span> resultados
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
        </div>
      {/if}
    {/if}
  </div>
</div>
