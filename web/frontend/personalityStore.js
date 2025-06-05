import { writable } from 'svelte/store';

// Store para personalidade global padrão
export const defaultPersonality = writable({
  formality_level: 50,
  humor_level: 50,
  technicality_level: 50,
  response_speed: 'médio',
  verbosity: 'médio'
});

// Store para personalidades por canal
export const channelPersonalities = writable({});

// Store para configurações de aprendizado
export const learningSettings = writable({
  enabled: true,
  learning_rate: 0.5,
  adaptation_speed: 'médio',
  memory_weight: 0.7
});

// Store para usuário atual
export const currentUser = writable(null);

// Store para canal atual
export const currentChannel = writable(null);

// Função para atualizar personalidade de um canal
export function updateChannelPersonality(channelId, personality) {
  channelPersonalities.update(personalities => {
    return {
      ...personalities,
      [channelId]: personality
    };
  });
}

// Função para obter personalidade de um canal
export function getChannelPersonality(channelId) {
  let result;
  channelPersonalities.subscribe(personalities => {
    result = personalities[channelId] || null;
  })();
  
  if (!result) {
    defaultPersonality.subscribe(value => {
      result = value;
    })();
  }
  
  return result;
}

// Função para resetar personalidade de um canal para o padrão
export function resetChannelPersonality(channelId) {
  let defaultValue;
  defaultPersonality.subscribe(value => {
    defaultValue = value;
  })();
  
  updateChannelPersonality(channelId, defaultValue);
}

// Função para atualizar configurações de aprendizado
export function updateLearningSettings(settings) {
  learningSettings.update(() => settings);
}
