"""
Cliente para o sistema de memória da Nina IA.
Fornece métodos para acessar e manipular os dados do sistema de memória.
"""

import os
import logging
from typing import Dict, List, Any, Optional

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("memory_client.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("MemoryClient")

class MemoryClient:
    """
    Cliente para o sistema de memória.
    Fornece métodos para acessar e manipular os dados do sistema de memória.
    """
    
    def __init__(self):
        """
        Inicializa o cliente de memória.
        """
        try:
            from memory import get_memory_system
            self.memory_system = get_memory_system()
            
            if self.memory_system is None:
                from memory import init_memory_system
                self.memory_system = init_memory_system()
                
            logger.info("Cliente de memória inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar cliente de memória: {e}")
            self.memory_system = None
    
    def get_users(self, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Obtém a lista de usuários.
        
        Args:
            limit: Número máximo de usuários a retornar
            offset: Número de usuários a pular
            
        Returns:
            Lista de usuários
        """
        try:
            if self.memory_system is None:
                return []
            
            # Obter estatísticas para ter a lista de usuários
            statistics = self.memory_system.get_statistics()
            top_users = statistics.get("top_users", [])
            
            # Aplicar paginação
            paginated_users = top_users[offset:offset+limit]
            
            # Para cada usuário na lista, obter detalhes completos
            users = []
            for user_info in paginated_users:
                user_id = user_info.get("user_id")
                if user_id:
                    # Obter apenas informações básicas para a listagem
                    users.append({
                        "user_id": user_id,
                        "username": user_info.get("username", "Unknown User"),
                        "interaction_count": user_info.get("interaction_count", 0),
                        "last_seen": self._get_user_last_seen(user_id)
                    })
            
            return users
        except Exception as e:
            logger.error(f"Erro ao obter usuários: {e}")
            return []
    
    def _get_user_last_seen(self, user_id: str) -> str:
        """
        Obtém a data da última interação de um usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Data da última interação
        """
        try:
            user = self.memory_system.get_user_profile(user_id)
            return user.get("last_seen", "")
        except:
            return ""
    
    def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        Obtém detalhes de um usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Dicionário com informações do usuário
        """
        try:
            if self.memory_system is None:
                return {}
            
            return self.memory_system.get_user_profile(user_id)
        except Exception as e:
            logger.error(f"Erro ao obter usuário {user_id}: {e}")
            return {}
    
    def update_user(self, user_id: str, data: Dict[str, Any]) -> bool:
        """
        Atualiza informações de um usuário.
        
        Args:
            user_id: ID do usuário
            data: Dicionário com atualizações
            
        Returns:
            True se a operação foi bem-sucedida, False caso contrário
        """
        try:
            if self.memory_system is None:
                return False
            
            # Verificar se o usuário existe
            user = self.memory_system.get_user_profile(user_id)
            if not user:
                return False
            
            # Atualizar metadados
            if "metadata" in data:
                return self.memory_system.memory_manager.update_user_metadata(user_id, data["metadata"])
            
            return True
        except Exception as e:
            logger.error(f"Erro ao atualizar usuário {user_id}: {e}")
            return False
    
    def delete_user_memory(self, user_id: str) -> bool:
        """
        Remove memórias de um usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            True se a operação foi bem-sucedida, False caso contrário
        """
        try:
            if self.memory_system is None:
                return False
            
            return self.memory_system.delete_user_memory(user_id)
        except Exception as e:
            logger.error(f"Erro ao remover memórias do usuário {user_id}: {e}")
            return False
    
    def get_user_interactions(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Obtém as interações de um usuário.
        
        Args:
            user_id: ID do usuário
            limit: Número máximo de interações a retornar
            
        Returns:
            Lista de interações
        """
        try:
            if self.memory_system is None:
                return []
            
            return self.memory_system.memory_manager.db.get_user_interactions(user_id, limit)
        except Exception as e:
            logger.error(f"Erro ao obter interações do usuário {user_id}: {e}")
            return []
    
    def get_channels(self, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Obtém a lista de canais.
        
        Args:
            limit: Número máximo de canais a retornar
            offset: Número de canais a pular
            
        Returns:
            Lista de canais
        """
        try:
            if self.memory_system is None:
                return []
            
            # Obter estatísticas para ter a lista de canais
            statistics = self.memory_system.get_statistics()
            top_channels = statistics.get("top_channels", [])
            
            # Aplicar paginação
            paginated_channels = top_channels[offset:offset+limit]
            
            # Para cada canal na lista, obter detalhes básicos
            channels = []
            for channel_info in paginated_channels:
                channel_id = channel_info.get("channel_id")
                if channel_id:
                    # Obter apenas informações básicas para a listagem
                    channels.append({
                        "channel_id": channel_id,
                        "channel_name": channel_info.get("channel_name", "Unknown Channel"),
                        "message_count": channel_info.get("message_count", 0),
                        "last_activity": self._get_channel_last_activity(channel_id)
                    })
            
            return channels
        except Exception as e:
            logger.error(f"Erro ao obter canais: {e}")
            return []
    
    def _get_channel_last_activity(self, channel_id: str) -> str:
        """
        Obtém a data da última atividade em um canal.
        
        Args:
            channel_id: ID do canal
            
        Returns:
            Data da última atividade
        """
        try:
            channel = self.memory_system.get_channel_profile(channel_id)
            return channel.get("last_activity", "")
        except:
            return ""
    
    def get_channel(self, channel_id: str) -> Dict[str, Any]:
        """
        Obtém detalhes de um canal.
        
        Args:
            channel_id: ID do canal
            
        Returns:
            Dicionário com informações do canal
        """
        try:
            if self.memory_system is None:
                return {}
            
            return self.memory_system.get_channel_profile(channel_id)
        except Exception as e:
            logger.error(f"Erro ao obter canal {channel_id}: {e}")
            return {}
    
    def update_channel(self, channel_id: str, data: Dict[str, Any]) -> bool:
        """
        Atualiza informações de um canal.
        
        Args:
            channel_id: ID do canal
            data: Dicionário com atualizações
            
        Returns:
            True se a operação foi bem-sucedida, False caso contrário
        """
        try:
            if self.memory_system is None:
                return False
            
            # Verificar se o canal existe
            channel = self.memory_system.get_channel_profile(channel_id)
            if not channel:
                return False
            
            # Atualizar metadados
            if "metadata" in data:
                return self.memory_system.memory_manager.update_channel_metadata(channel_id, data["metadata"])
            
            return True
        except Exception as e:
            logger.error(f"Erro ao atualizar canal {channel_id}: {e}")
            return False
    
    def get_channel_interactions(self, channel_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Obtém as interações em um canal.
        
        Args:
            channel_id: ID do canal
            limit: Número máximo de interações a retornar
            
        Returns:
            Lista de interações
        """
        try:
            if self.memory_system is None:
                return []
            
            return self.memory_system.memory_manager.db.get_channel_interactions(channel_id, limit)
        except Exception as e:
            logger.error(f"Erro ao obter interações do canal {channel_id}: {e}")
            return []
    
    def update_nina_personality(self, channel_id: str, personality: Dict[str, Any]) -> bool:
        """
        Atualiza a personalidade da Nina para um canal específico.
        
        Args:
            channel_id: ID do canal
            personality: Dicionário com configurações de personalidade
            
        Returns:
            True se a operação foi bem-sucedida, False caso contrário
        """
        try:
            if self.memory_system is None:
                return False
            
            return self.memory_system.update_nina_personality(channel_id, personality)
        except Exception as e:
            logger.error(f"Erro ao atualizar personalidade do canal {channel_id}: {e}")
            return False
    
    def get_interactions(self, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Obtém a lista de interações recentes.
        
        Args:
            limit: Número máximo de interações a retornar
            offset: Número de interações a pular
            
        Returns:
            Lista de interações
        """
        try:
            if self.memory_system is None:
                return []
            
            # Obter interações de todos os canais
            # Em uma implementação real, seria necessário um método específico para isso
            # Aqui estamos simulando com base nas interações dos canais mais ativos
            
            statistics = self.memory_system.get_statistics()
            top_channels = statistics.get("top_channels", [])
            
            all_interactions = []
            for channel_info in top_channels[:5]:  # Limitar a 5 canais para não sobrecarregar
                channel_id = channel_info.get("channel_id")
                if channel_id:
                    channel_interactions = self.memory_system.memory_manager.db.get_channel_interactions(channel_id, 10)
                    all_interactions.extend(channel_interactions)
            
            # Ordenar por timestamp (mais recente primeiro)
            all_interactions.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            
            # Aplicar paginação
            paginated_interactions = all_interactions[offset:offset+limit]
            
            return paginated_interactions
        except Exception as e:
            logger.error(f"Erro ao obter interações: {e}")
            return []
    
    def get_interaction(self, interaction_id: int) -> Dict[str, Any]:
        """
        Obtém detalhes de uma interação.
        
        Args:
            interaction_id: ID da interação
            
        Returns:
            Dicionário com informações da interação
        """
        try:
            if self.memory_system is None:
                return {}
            
            # Em uma implementação real, seria necessário um método específico para isso
            # Aqui estamos simulando com uma busca nas interações recentes
            
            interactions = self.get_interactions(limit=100)
            for interaction in interactions:
                if interaction.get("interaction_id") == interaction_id:
                    return interaction
            
            return {}
        except Exception as e:
            logger.error(f"Erro ao obter interação {interaction_id}: {e}")
            return {}
    
    def delete_interaction(self, interaction_id: int) -> bool:
        """
        Remove uma interação.
        
        Args:
            interaction_id: ID da interação
            
        Returns:
            True se a operação foi bem-sucedida, False caso contrário
        """
        try:
            if self.memory_system is None:
                return False
            
            # Em uma implementação real, seria necessário um método específico para isso
            # Aqui estamos retornando False pois não temos acesso direto à função de remoção
            
            logger.warning(f"Remoção de interação {interaction_id} não implementada")
            return False
        except Exception as e:
            logger.error(f"Erro ao remover interação {interaction_id}: {e}")
            return False
    
    def search_interactions(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Busca interações por conteúdo.
        
        Args:
            query: Termo de busca
            limit: Número máximo de resultados
            
        Returns:
            Lista de interações
        """
        try:
            if self.memory_system is None:
                return []
            
            # Em uma implementação real, seria necessário um método específico para isso
            # Aqui estamos simulando com uma busca simples nas interações recentes
            
            interactions = self.get_interactions(limit=100)
            results = []
            
            for interaction in interactions:
                content = interaction.get("content_summary", "").lower()
                if query.lower() in content:
                    results.append(interaction)
                    if len(results) >= limit:
                        break
            
            return results
        except Exception as e:
            logger.error(f"Erro ao buscar interações: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Obtém estatísticas gerais do sistema de memória.
        
        Returns:
            Dicionário com estatísticas
        """
        try:
            if self.memory_system is None:
                return {}
            
            return self.memory_system.get_statistics()
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {e}")
            return {}
