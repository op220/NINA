<script>
  import { Link, useLocation } from 'svelte-navigator';
  
  // Ícones (simulados com classes - em uma implementação real usaríamos um pacote de ícones)
  const icons = {
    home: "fas fa-home",
    users: "fas fa-users",
    channels: "fas fa-comments",
    settings: "fas fa-cog",
    statistics: "fas fa-chart-bar"
  };
  
  // Itens do menu
  const menuItems = [
    { id: 'home', label: 'Dashboard', path: '/', icon: icons.home },
    { id: 'users', label: 'Usuários', path: '/users', icon: icons.users },
    { id: 'channels', label: 'Canais', path: '/channels', icon: icons.channels },
    { id: 'statistics', label: 'Estatísticas', path: '/statistics', icon: icons.statistics },
    { id: 'settings', label: 'Configurações', path: '/settings', icon: icons.settings }
  ];
  
  // Obter localização atual para destacar o item ativo
  const location = useLocation();
  
  // Estado para controlar se a sidebar está expandida ou não
  let expanded = true;
  
  // Função para alternar o estado da sidebar
  function toggleSidebar() {
    expanded = !expanded;
  }
  
  // Função para verificar se um item está ativo
  function isActive(path) {
    return $location.pathname === path || 
           ($location.pathname.startsWith(path) && path !== '/');
  }
</script>

<aside class="bg-neutral-800 text-white {expanded ? 'w-64' : 'w-20'} transition-all duration-300 flex flex-col">
  <!-- Logo e título -->
  <div class="p-4 flex items-center justify-between border-b border-neutral-700">
    {#if expanded}
      <div class="flex items-center">
        <span class="text-primary-400 text-2xl mr-2">N</span>
        <span class="font-semibold">Nina IA</span>
      </div>
    {:else}
      <div class="mx-auto">
        <span class="text-primary-400 text-2xl">N</span>
      </div>
    {/if}
    
    <button 
      on:click={toggleSidebar} 
      class="text-neutral-400 hover:text-white focus:outline-none"
      aria-label={expanded ? 'Recolher menu' : 'Expandir menu'}
    >
      <i class={expanded ? "fas fa-chevron-left" : "fas fa-chevron-right"}></i>
    </button>
  </div>
  
  <!-- Links de navegação -->
  <nav class="flex-1 overflow-y-auto py-4">
    <ul>
      {#each menuItems as item}
        <li class="mb-1">
          <Link 
            to={item.path} 
            class="flex items-center px-4 py-3 {isActive(item.path) ? 'bg-primary-700 text-white' : 'text-neutral-300 hover:bg-neutral-700'} transition-colors duration-200"
          >
            <i class="{item.icon} {expanded ? 'mr-3' : 'mx-auto'} text-lg"></i>
            {#if expanded}
              <span>{item.label}</span>
            {/if}
          </Link>
        </li>
      {/each}
    </ul>
  </nav>
  
  <!-- Rodapé da sidebar -->
  <div class="p-4 border-t border-neutral-700 text-neutral-400 text-sm">
    {#if expanded}
      <p>Nina IA v1.0.0</p>
    {:else}
      <p class="text-center">v1.0</p>
    {/if}
  </div>
</aside>
