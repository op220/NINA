import { writable } from 'svelte/store';

// Store para memória de usuários
export const userMemories = writable({});

// Store para memória de canais
export const channelMemories = writable({});

// Store para interações recentes
export const recentInteractions = writable([]);

// Store para estatísticas globais
export const globalStats = writable({
  user_count: 0,
  channel_count: 0,
  interaction_count: 0,
  topic_count: 0
});

// Função para adicionar ou atualizar memória de usuário
export function updateUserMemory(userId, userData) {
  userMemories.update(memories => {
    return {
      ...memories,
      [userId]: {
        ...(memories[userId] || {}),
        ...userData
      }
    };
  });
}

// Função para adicionar ou atualizar memória de canal
export function updateChannelMemory(channelId, channelData) {
  channelMemories.update(memories => {
    return {
      ...memories,
      [channelId]: {
        ...(memories[channelId] || {}),
        ...channelData
      }
    };
  });
}

// Função para adicionar interação
export function addInteraction(interaction) {
  recentInteractions.update(interactions => {
    // Adicionar nova interação no início da lista
    const newInteractions = [interaction, ...interactions];
    // Limitar a 100 interações mais recentes
    return newInteractions.slice(0, 100);
  });
  
  // Atualizar estatísticas globais
  globalStats.update(stats => {
    return {
      ...stats,
      interaction_count: stats.interaction_count + 1
    };
  });
}

// Função para remover interações de um usuário
export function removeUserInteractions(userId, interactionIds) {
  recentInteractions.update(interactions => {
    return interactions.filter(interaction => 
      !(interaction.user_id === userId && interactionIds.includes(interaction.id))
    );
  });
  
  // Atualizar memória do usuário para refletir a remoção
  userMemories.update(memories => {
    if (memories[userId] && memories[userId].interactions) {
      const updatedInteractions = memories[userId].interactions.filter(
        interaction => !interactionIds.includes(interaction.id)
      );
      
      return {
        ...memories,
        [userId]: {
          ...memories[userId],
          interactions: updatedInteractions,
          interaction_count: updatedInteractions.length
        }
      };
    }
    return memories;
  });
}

// Função para remover interações de um canal
export function removeChannelInteractions(channelId, interactionIds) {
  recentInteractions.update(interactions => {
    return interactions.filter(interaction => 
      !(interaction.channel_id === channelId && interactionIds.includes(interaction.id))
    );
  });
  
  // Atualizar memória do canal para refletir a remoção
  channelMemories.update(memories => {
    if (memories[channelId] && memories[channelId].interactions) {
      const updatedInteractions = memories[channelId].interactions.filter(
        interaction => !interactionIds.includes(interaction.id)
      );
      
      return {
        ...memories,
        [channelId]: {
          ...memories[channelId],
          interactions: updatedInteractions,
          message_count: updatedInteractions.length
        }
      };
    }
    return memories;
  });
}

// Função para limpar toda a memória de um canal
export function clearChannelMemory(channelId) {
  // Remover interações do canal da lista de interações recentes
  recentInteractions.update(interactions => {
    return interactions.filter(interaction => interaction.channel_id !== channelId);
  });
  
  // Limpar memória do canal
  channelMemories.update(memories => {
    if (memories[channelId]) {
      return {
        ...memories,
        [channelId]: {
          ...memories[channelId],
          interactions: [],
          message_count: 0,
          topics: {},
          users: {}
        }
      };
    }
    return memories;
  });
}

// Função para limpar toda a memória de um usuário
export function clearUserMemory(userId) {
  // Remover interações do usuário da lista de interações recentes
  recentInteractions.update(interactions => {
    return interactions.filter(interaction => interaction.user_id !== userId);
  });
  
  // Limpar memória do usuário
  userMemories.update(memories => {
    if (memories[userId]) {
      return {
        ...memories,
        [userId]: {
          ...memories[userId],
          interactions: [],
          interaction_count: 0,
          topics: {},
          emotions: {},
          expressions: []
        }
      };
    }
    return memories;
  });
}
