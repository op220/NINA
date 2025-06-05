<script>
  import { Link } from 'svelte-navigator';
  
  // Estado para controlar se o menu de usuário está aberto
  let userMenuOpen = false;
  
  // Função para alternar o menu de usuário
  function toggleUserMenu() {
    userMenuOpen = !userMenuOpen;
  }
  
  // Função para fechar o menu de usuário quando clicar fora dele
  function closeUserMenu() {
    userMenuOpen = false;
  }
  
  // Simular notificações
  const notifications = [
    { id: 1, message: 'Nova atualização de personalidade disponível', time: '5 min atrás' },
    { id: 2, message: 'Backup automático concluído', time: '1 hora atrás' }
  ];
</script>

<header class="bg-white border-b border-neutral-200 h-16 flex items-center justify-between px-4 shadow-sm">
  <!-- Título da página -->
  <div>
    <h1 class="text-xl font-semibold text-neutral-800 m-0">Sistema de Memória Nina IA</h1>
  </div>
  
  <!-- Ações do cabeçalho -->
  <div class="flex items-center space-x-4">
    <!-- Botão de busca -->
    <button class="text-neutral-500 hover:text-neutral-700 focus:outline-none">
      <i class="fas fa-search"></i>
    </button>
    
    <!-- Botão de notificações -->
    <div class="relative">
      <button class="text-neutral-500 hover:text-neutral-700 focus:outline-none">
        <i class="fas fa-bell"></i>
        {#if notifications.length > 0}
          <span class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-4 w-4 flex items-center justify-center">
            {notifications.length}
          </span>
        {/if}
      </button>
    </div>
    
    <!-- Menu de usuário -->
    <div class="relative">
      <button 
        on:click={toggleUserMenu} 
        class="flex items-center text-neutral-700 hover:text-neutral-900 focus:outline-none"
      >
        <div class="w-8 h-8 rounded-full bg-primary-500 text-white flex items-center justify-center mr-2">
          <span class="font-medium">A</span>
        </div>
        <span class="font-medium">Admin</span>
        <i class="fas fa-chevron-down ml-1 text-xs"></i>
      </button>
      
      {#if userMenuOpen}
        <div 
          class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10"
          on:click|stopPropagation
        >
          <Link to="/settings" class="block px-4 py-2 text-sm text-neutral-700 hover:bg-neutral-100">
            Configurações
          </Link>
          <button class="block w-full text-left px-4 py-2 text-sm text-neutral-700 hover:bg-neutral-100">
            Sair
          </button>
        </div>
        
        <!-- Overlay para fechar o menu quando clicar fora -->
        <div 
          class="fixed inset-0 z-0" 
          on:click={closeUserMenu}
        ></div>
      {/if}
    </div>
  </div>
</header>
