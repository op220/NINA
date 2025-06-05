import unittest
import os
import sys
import json
import requests
from unittest.mock import patch, MagicMock

# Adicionar o diretório raiz ao path para importar outros módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar módulos a serem testados
from web.backend.api import app
from fastapi.testclient import TestClient

class TestWebAPI(unittest.TestCase):
    """
    Testes para a API web do sistema de memória da Nina IA.
    """
    
    def setUp(self):
        """
        Configuração para cada teste.
        """
        # Criar cliente de teste para a API FastAPI
        self.client = TestClient(app)
        
        # Mock para o sistema de memória
        self.mock_memory_integrator = MagicMock()
        self.mock_memory_adapter = MagicMock()
        
        # Configurar mocks para retornar dados de teste
        self.setup_memory_mocks()
        
        # Patch para a função de dependência get_memory_system
        self.patcher = patch('web.backend.api.get_memory_system', return_value={
            'integrator': self.mock_memory_integrator,
            'adapter': self.mock_memory_adapter
        })
        self.mock_get_memory_system = self.patcher.start()
        
    def tearDown(self):
        """
        Limpeza após cada teste.
        """
        # Parar o patch
        self.patcher.stop()
        
    def setup_memory_mocks(self):
        """
        Configurar mocks para retornar dados de teste.
        """
        # Mock para get_all_users
        self.mock_memory_integrator.memory_manager.get_all_users.return_value = [
            {
                'user_id': 'user123',
                'username': 'Usuário Teste 1',
                'first_seen': '2025-04-01T10:00:00',
                'last_seen': '2025-04-24T15:30:00',
                'interaction_count': 42
            },
            {
                'user_id': 'user456',
                'username': 'Usuário Teste 2',
                'first_seen': '2025-04-05T14:20:00',
                'last_seen': '2025-04-23T18:45:00',
                'interaction_count': 27
            }
        ]
        
        # Mock para get_user_memories
        self.mock_memory_integrator.get_user_memories.return_value = {
            'profile': {
                'user_id': 'user123',
                'username': 'Usuário Teste 1',
                'first_seen': '2025-04-01T10:00:00',
                'last_seen': '2025-04-24T15:30:00',
                'interaction_count': 42,
                'notes': 'Usuário interessado em tecnologia'
            },
            'interactions': [
                {
                    'id': 'int123',
                    'user_id': 'user123',
                    'channel_id': 'channel456',
                    'content': 'Olá, como funciona o sistema de memória?',
                    'timestamp': '2025-04-24T15:30:00',
                    'sentiment': 'neutro'
                }
            ],
            'topics': {
                'tecnologia': 15,
                'programação': 10,
                'inteligência artificial': 8
            },
            'emotions': {
                'neutro': 20,
                'curiosidade': 12,
                'entusiasmo': 10
            },
            'expressions': ['interessante', 'como funciona', 'muito bom']
        }
        
        # Mock para get_user_profile
        self.mock_memory_integrator.memory_manager.get_user_profile.return_value = {
            'user_id': 'user123',
            'username': 'Usuário Teste 1',
            'first_seen': '2025-04-01T10:00:00',
            'last_seen': '2025-04-24T15:30:00',
            'interaction_count': 42,
            'notes': 'Usuário interessado em tecnologia'
        }
        
        # Mock para get_all_channels
        self.mock_memory_integrator.memory_manager.get_all_channels.return_value = [
            {
                'channel_id': 'channel456',
                'channel_name': 'Canal Teste 1',
                'type': 'texto',
                'created_at': '2025-03-15T08:00:00',
                'last_activity': '2025-04-24T16:45:00',
                'message_count': 156,
                'user_count': 12
            },
            {
                'channel_id': 'channel789',
                'channel_name': 'Canal Teste 2',
                'type': 'voz',
                'created_at': '2025-03-20T09:30:00',
                'last_activity': '2025-04-23T19:15:00',
                'message_count': 98,
                'user_count': 8
            }
        ]
        
        # Mock para get_channel_memories
        self.mock_memory_integrator.get_channel_memories.return_value = {
            'profile': {
                'channel_id': 'channel456',
                'channel_name': 'Canal Teste 1',
                'type': 'texto',
                'created_at': '2025-03-15T08:00:00',
                'last_activity': '2025-04-24T16:45:00',
                'message_count': 156,
                'user_count': 12,
                'description': 'Canal para discussões sobre tecnologia'
            },
            'interactions': [
                {
                    'id': 'int123',
                    'user_id': 'user123',
                    'channel_id': 'channel456',
                    'content': 'Olá, como funciona o sistema de memória?',
                    'timestamp': '2025-04-24T15:30:00',
                    'sentiment': 'neutro'
                }
            ],
            'topics': {
                'tecnologia': 45,
                'programação': 30,
                'inteligência artificial': 25
            },
            'users': {
                'user123': {
                    'username': 'Usuário Teste 1',
                    'interaction_count': 42,
                    'last_seen': '2025-04-24T15:30:00'
                },
                'user456': {
                    'username': 'Usuário Teste 2',
                    'interaction_count': 27,
                    'last_seen': '2025-04-23T18:45:00'
                }
            },
            'personality': {
                'formality_level': 60,
                'humor_level': 40,
                'technicality_level': 70,
                'response_speed': 'médio',
                'verbosity': 'detalhado'
            }
        }
        
        # Mock para get_channel_profile
        self.mock_memory_integrator.memory_manager.get_channel_profile.return_value = {
            'channel_id': 'channel456',
            'channel_name': 'Canal Teste 1',
            'type': 'texto',
            'created_at': '2025-03-15T08:00:00',
            'last_activity': '2025-04-24T16:45:00',
            'message_count': 156,
            'user_count': 12,
            'description': 'Canal para discussões sobre tecnologia'
        }
        
        # Mock para get_channel_personality
        self.mock_memory_integrator.personality_manager.get_channel_personality.return_value = {
            'formality_level': 60,
            'humor_level': 40,
            'technicality_level': 70,
            'response_speed': 'médio',
            'verbosity': 'detalhado'
        }
        
        # Mock para get_recent_interactions
        self.mock_memory_integrator.memory_manager.get_recent_interactions.return_value = [
            {
                'id': 'int123',
                'user_id': 'user123',
                'channel_id': 'channel456',
                'content': 'Olá, como funciona o sistema de memória?',
                'timestamp': '2025-04-24T15:30:00',
                'sentiment': 'neutro'
            },
            {
                'id': 'int124',
                'user_id': 'nina',
                'channel_id': 'channel456',
                'content': 'O sistema de memória funciona armazenando informações sobre usuários e canais.',
                'timestamp': '2025-04-24T15:30:30',
                'sentiment': 'neutro',
                'is_nina_response': True,
                'target_user_id': 'user123'
            }
        ]
        
        # Mock para get_system_statistics
        self.mock_memory_integrator.memory_manager.get_system_statistics.return_value = {
            'user_count': 25,
            'channel_count': 10,
            'interaction_count': 1250,
            'memory_size_mb': 5.2,
            'uptime_days': 30
        }
        
        # Mock para get_user_topics
        self.mock_memory_integrator.memory_manager.get_user_topics.return_value = {
            'tecnologia': 15,
            'programação': 10,
            'inteligência artificial': 8
        }
        
        # Mock para get_user_emotions
        self.mock_memory_integrator.memory_manager.get_user_emotions.return_value = {
            'neutro': 20,
            'curiosidade': 12,
            'entusiasmo': 10
        }
        
        # Mock para get_user_expressions
        self.mock_memory_integrator.memory_manager.get_user_expressions.return_value = [
            'interessante', 'como funciona', 'muito bom'
        ]
        
        # Mock para get_channel_topics
        self.mock_memory_integrator.memory_manager.get_channel_topics.return_value = {
            'tecnologia': 45,
            'programação': 30,
            'inteligência artificial': 25
        }
        
        # Mock para get_channel_users
        self.mock_memory_integrator.memory_manager.get_channel_users.return_value = {
            'user123': {
                'username': 'Usuário Teste 1',
                'interaction_count': 42,
                'last_seen': '2025-04-24T15:30:00'
            },
            'user456': {
                'username': 'Usuário Teste 2',
                'interaction_count': 27,
                'last_seen': '2025-04-23T18:45:00'
            }
        }
        
        # Mock para clear_user_memory
        self.mock_memory_integrator.clear_user_memory.return_value = True
        
        # Mock para clear_channel_memory
        self.mock_memory_integrator.clear_channel_memory.return_value = True
        
        # Mock para config
        self.mock_memory_adapter.config = {
            'enabled': True,
            'memory_db_path': 'memory.db',
            'profiles_dir': 'data/profiles',
            'max_context_interactions': 10,
            'backup_dir': 'backups',
            'auto_backup': True,
            'auto_backup_interval': 24
        }
        
        # Mock para create_backup
        self.mock_memory_adapter.create_backup.return_value = 'backups/memory_backup_20250425_114200.db'
        
    def test_get_status(self):
        """
        Testar endpoint de status.
        """
        response = self.client.get('/api/status')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('status', data['data'])
        self.assertEqual(data['data']['status'], 'online')
        
    def test_get_users(self):
        """
        Testar endpoint para obter usuários.
        """
        response = self.client.get('/api/users')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        self.assertIsInstance(data['data'], list)
        self.assertEqual(len(data['data']), 2)
        self.assertEqual(data['data'][0]['user_id'], 'user123')
        
    def test_get_user(self):
        """
        Testar endpoint para obter detalhes de um usuário.
        """
        response = self.client.get('/api/users/user123')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        self.assertIn('profile', data['data'])
        self.assertEqual(data['data']['profile']['user_id'], 'user123')
        
    def test_update_user(self):
        """
        Testar endpoint para atualizar perfil de usuário.
        """
        user_data = {
            'user_id': 'user123',
            'username': 'Usuário Atualizado',
            'notes': 'Notas atualizadas'
        }
        response = self.client.put('/api/users/user123', json=user_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        
        # Verificar se o método de atualização foi chamado
        self.mock_memory_integrator.memory_manager.update_user_profile.assert_called_once()
        
    def test_clear_user_memory(self):
        """
        Testar endpoint para limpar memória de um usuário.
        """
        response = self.client.delete('/api/users/user123')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        
        # Verificar se o método de limpeza foi chamado
        self.mock_memory_integrator.clear_user_memory.assert_called_once_with('user123')
        
    def test_get_channels(self):
        """
        Testar endpoint para obter canais.
        """
        response = self.client.get('/api/channels')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        self.assertIsInstance(data['data'], list)
        self.assertEqual(len(data['data']), 2)
        self.assertEqual(data['data'][0]['channel_id'], 'channel456')
        
    def test_get_channel(self):
        """
        Testar endpoint para obter detalhes de um canal.
        """
        response = self.client.get('/api/channels/channel456')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        self.assertIn('profile', data['data'])
        self.assertEqual(data['data']['profile']['channel_id'], 'channel456')
        
    def test_update_channel_personality(self):
        """
        Testar endpoint para atualizar personalidade de um canal.
        """
        personality_data = {
            'formality_level': 70,
            'humor_level': 50,
            'technicality_level': 60,
            'response_speed': 'rápido',
            'verbosity': 'conciso'
        }
        response = self.client.put('/api/channels/channel456/personality', json=personality_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        
        # Verificar se o método de atualização foi chamado
        self.mock_memory_integrator.personality_manager.save_channel_personality.assert_called_once()
        
    def test_clear_channel_memory(self):
        """
        Testar endpoint para limpar memória de um canal.
        """
        response = self.client.delete('/api/channels/channel456')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        
        # Verificar se o método de limpeza foi chamado
        self.mock_memory_integrator.clear_channel_memory.assert_called_once_with('channel456')
        
    def test_get_interactions(self):
        """
        Testar endpoint para obter interações.
        """
        response = self.client.get('/api/interactions')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        self.assertIsInstance(data['data'], list)
        
        # Testar com filtros
        response = self.client.get('/api/interactions?user_id=user123&channel_id=channel456')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        
    def test_get_system_statistics(self):
        """
        Testar endpoint para obter estatísticas do sistema.
        """
        response = self.client.get('/api/statistics/system')
        self.assertEqual(response.status_code, 200) # Corrigido: Método assertEqual completado
(Content truncated due to size limit. Use line ranges to read in chunks)