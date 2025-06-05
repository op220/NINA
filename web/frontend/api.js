import axios from 'axios';

// URL base da API
const API_BASE_URL = 'http://localhost:8000/api';

// Cliente Axios configurado
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API de Usuários
export const userApi = {
  // Obter todos os usuários
  getUsers: async (limit = 100, offset = 0) => {
    try {
      const response = await apiClient.get(`/users?limit=${limit}&offset=${offset}`);
      return response.data;
    } catch (error) {
      console.error('Erro ao obter usuários:', error);
      throw error;
    }
  },
  
  // Obter detalhes de um usuário específico
  getUser: async (userId) => {
    try {
      const response = await apiClient.get(`/users/${userId}`);
      return response.data;
    } catch (error) {
      console.error(`Erro ao obter usuário ${userId}:`, error);
      throw error;
    }
  },
  
  // Atualizar perfil de usuário
  updateUser: async (userId, userData) => {
    try {
      const response = await apiClient.put(`/users/${userId}`, userData);
      return response.data;
    } catch (error) {
      console.error(`Erro ao atualizar usuário ${userId}:`, error);
      throw error;
    }
  },
  
  // Remover interações específicas de um usuário
  deleteUserInteractions: async (userId, interactionIds) => {
    try {
      const response = await apiClient.delete(`/users/${userId}/interactions`, {
        data: { interaction_ids: interactionIds }
      });
      return response.data;
    } catch (error) {
      console.error(`Erro ao remover interações do usuário ${userId}:`, error);
      throw error;
    }
  },
  
  // Limpar toda a memória de um usuário
  clearUserMemory: async (userId) => {
    try {
      const response = await apiClient.delete(`/users/${userId}`);
      return response.data;
    } catch (error) {
      console.error(`Erro ao limpar memória do usuário ${userId}:`, error);
      throw error;
    }
  },
  
  // Obter estatísticas de um usuário
  getUserStatistics: async (userId) => {
    try {
      const response = await apiClient.get(`/statistics/users/${userId}`);
      return response.data;
    } catch (error) {
      console.error(`Erro ao obter estatísticas do usuário ${userId}:`, error);
      throw error;
    }
  }
};

// API de Canais
export const channelApi = {
  // Obter todos os canais
  getChannels: async (limit = 100, offset = 0) => {
    try {
      const response = await apiClient.get(`/channels?limit=${limit}&offset=${offset}`);
      return response.data;
    } catch (error) {
      console.error('Erro ao obter canais:', error);
      throw error;
    }
  },
  
  // Obter detalhes de um canal específico
  getChannel: async (channelId) => {
    try {
      const response = await apiClient.get(`/channels/${channelId}`);
      return response.data;
    } catch (error) {
      console.error(`Erro ao obter canal ${channelId}:`, error);
      throw error;
    }
  },
  
  // Atualizar personalidade de um canal
  updateChannelPersonality: async (channelId, personality) => {
    try {
      const response = await apiClient.put(`/channels/${channelId}/personality`, personality);
      return response.data;
    } catch (error) {
      console.error(`Erro ao atualizar personalidade do canal ${channelId}:`, error);
      throw error;
    }
  },
  
  // Atualizar configurações de aprendizado de um canal
  updateChannelSettings: async (channelId, settings) => {
    try {
      const response = await apiClient.put(`/channels/${channelId}/settings`, settings);
      return response.data;
    } catch (error) {
      console.error(`Erro ao atualizar configurações do canal ${channelId}:`, error);
      throw error;
    }
  },
  
  // Limpar toda a memória de um canal
  clearChannelMemory: async (channelId) => {
    try {
      const response = await apiClient.delete(`/channels/${channelId}`);
      return response.data;
    } catch (error) {
      console.error(`Erro ao limpar memória do canal ${channelId}:`, error);
      throw error;
    }
  },
  
  // Obter estatísticas de um canal
  getChannelStatistics: async (channelId) => {
    try {
      const response = await apiClient.get(`/statistics/channels/${channelId}`);
      return response.data;
    } catch (error) {
      console.error(`Erro ao obter estatísticas do canal ${channelId}:`, error);
      throw error;
    }
  }
};

// API de Interações
export const interactionApi = {
  // Obter interações com filtros opcionais
  getInteractions: async (options = {}) => {
    try {
      const { limit = 100, offset = 0, userId, channelId } = options;
      let url = `/interactions?limit=${limit}&offset=${offset}`;
      
      if (userId) url += `&user_id=${userId}`;
      if (channelId) url += `&channel_id=${channelId}`;
      
      const response = await apiClient.get(url);
      return response.data;
    } catch (error) {
      console.error('Erro ao obter interações:', error);
      throw error;
    }
  },
  
  // Remover uma interação específica
  deleteInteraction: async (interactionId) => {
    try {
      const response = await apiClient.delete(`/interactions/${interactionId}`);
      return response.data;
    } catch (error) {
      console.error(`Erro ao remover interação ${interactionId}:`, error);
      throw error;
    }
  }
};

// API de Estatísticas
export const statisticsApi = {
  // Obter estatísticas do sistema
  getSystemStatistics: async () => {
    try {
      const response = await apiClient.get('/statistics/system');
      return response.data;
    } catch (error) {
      console.error('Erro ao obter estatísticas do sistema:', error);
      throw error;
    }
  }
};

// API de Configurações
export const settingsApi = {
  // Obter configurações atuais
  getSettings: async () => {
    try {
      const response = await apiClient.get('/settings');
      return response.data;
    } catch (error) {
      console.error('Erro ao obter configurações:', error);
      throw error;
    }
  },
  
  // Atualizar configurações
  updateSettings: async (settings) => {
    try {
      const response = await apiClient.put('/settings', settings);
      return response.data;
    } catch (error) {
      console.error('Erro ao atualizar configurações:', error);
      throw error;
    }
  }
};

// API de Backups
export const backupApi = {
  // Criar um novo backup
  createBackup: async () => {
    try {
      const response = await apiClient.post('/backups');
      return response.data;
    } catch (error) {
      console.error('Erro ao criar backup:', error);
      throw error;
    }
  },
  
  // Listar backups disponíveis
  listBackups: async () => {
    try {
      const response = await apiClient.get('/backups');
      return response.data;
    } catch (error) {
      console.error('Erro ao listar backups:', error);
      throw error;
    }
  },
  
  // Restaurar a partir de um backup
  restoreBackup: async (backupPath) => {
    try {
      const response = await apiClient.post('/backups/restore', { backup_path: backupPath });
      return response.data;
    } catch (error) {
      console.error('Erro ao restaurar backup:', error);
      throw error;
    }
  }
};

// API de Status
export const statusApi = {
  // Verificar status do sistema
  getStatus: async () => {
    try {
      const response = await apiClient.get('/status');
      return response.data;
    } catch (error) {
      console.error('Erro ao verificar status:', error);
      throw error;
    }
  }
};

// Exportar todas as APIs
export default {
  user: userApi,
  channel: channelApi,
  interaction: interactionApi,
  statistics: statisticsApi,
  settings: settingsApi,
  backup: backupApi,
  status: statusApi
};
