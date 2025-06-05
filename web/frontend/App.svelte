<script>
  import { Router, Route } from 'svelte-navigator';
  import Sidebar from './components/Sidebar.svelte';
  import Header from './components/Header.svelte';
  
  // Importar páginas
  import Home from './routes/Home.svelte';
  import Users from './routes/Users.svelte';
  import UserDetail from './routes/UserDetail.svelte';
  import Channels from './routes/Channels.svelte';
  import ChannelDetail from './routes/ChannelDetail.svelte';
  import Settings from './routes/Settings.svelte';
  import Statistics from './routes/Statistics.svelte';
</script>

<Router>
  <div class="flex h-screen bg-neutral-50">
    <!-- Sidebar -->
    <Sidebar />
    
    <!-- Conteúdo principal -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Header -->
      <Header />
      
      <!-- Área de conteúdo principal -->
      <main class="flex-1 overflow-y-auto p-4">
        <div class="container mx-auto">
          <Route path="/" component={Home} />
          <Route path="/users" component={Users} />
          <Route path="/users/:id" component={UserDetail} />
          <Route path="/channels" component={Channels} />
          <Route path="/channels/:id" component={ChannelDetail} />
          <Route path="/settings" component={Settings} />
          <Route path="/statistics" component={Statistics} />
        </div>
      </main>
    </div>
  </div>
</Router>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    overflow: hidden;
  }
</style>
