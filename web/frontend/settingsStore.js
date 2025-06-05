import { writable } from 'svelte/store';

// Store para configurações da aplicação
export const appSettings = writable({
  // Configurações gerais
  system: {
    db_path: "memory.db",
    data_dir: "memory_data",
    backup_dir: "backups",
    auto_backup: true,
    auto_backup_interval: 24 // horas
  },
  
  // Configurações de memória
  memory: {
    max_interactions_per_user: 1000,
    max_interactions_per_channel: 5000,
    retention_period: 90 // dias
  },
  
  // Configurações de interface
  ui: {
    theme: 'light',
    language: 'pt-BR',
    notifications_enabled: true
  }
});

// Store para controle de plugins
export const plugins = writable([
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
]);

// Store para backups disponíveis
export const backups = writable([]);

// Função para atualizar configurações da aplicação
export function updateAppSettings(newSettings) {
  appSettings.update(settings => {
    return {
      ...settings,
      ...newSettings
    };
  });
}

// Função para atualizar configurações de sistema
export function updateSystemSettings(newSystemSettings) {
  appSettings.update(settings => {
    return {
      ...settings,
      system: {
        ...settings.system,
        ...newSystemSettings
      }
    };
  });
}

// Função para atualizar configurações de memória
export function updateMemorySettings(newMemorySettings) {
  appSettings.update(settings => {
    return {
      ...settings,
      memory: {
        ...settings.memory,
        ...newMemorySettings
      }
    };
  });
}

// Função para atualizar configurações de UI
export function updateUISettings(newUISettings) {
  appSettings.update(settings => {
    return {
      ...settings,
      ui: {
        ...settings.ui,
        ...newUISettings
      }
    };
  });
}

// Função para alternar status de plugin
export function togglePlugin(pluginId) {
  plugins.update(currentPlugins => {
    return currentPlugins.map(plugin => {
      if (plugin.id === pluginId) {
        return { ...plugin, enabled: !plugin.enabled };
      }
      return plugin;
    });
  });
}

// Função para adicionar backup à lista
export function addBackup(backup) {
  backups.update(currentBackups => {
    return [backup, ...currentBackups];
  });
}

// Função para remover backup da lista
export function removeBackup(backupPath) {
  backups.update(currentBackups => {
    return currentBackups.filter(backup => backup.path !== backupPath);
  });
}
