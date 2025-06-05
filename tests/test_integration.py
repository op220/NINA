import unittest
import os
import sys
import json
import time
from unittest.mock import patch, MagicMock

# Adicionar o diretório raiz ao path para importar outros módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestIntegration(unittest.TestCase):
    """
    Testes de integração para o sistema completo de memória de longo prazo e interface web da Nina IA.
    """
    
    def setUp(self):
        """
        Configuração para cada teste.
        """
        # Configurar variáveis de ambiente para testes
        os.environ["NINA_CONFIG_PATH"] = "test_config.json"
        os.environ["NINA_MEMORY_DB_PATH"] = ":memory:"
        os.environ["NINA_PROFILES_DIR"] = "test_profiles"
        os.environ["NINA_API_PORT"] = "8001"
        
        # Criar diretório de perfis para testes se não existir
        if not os.path.exists("test_profiles"):
            os.makedirs("test_profiles")
            
        # Criar perfil padrão para testes
        self.default_profile = {
            "formality_level": 50,
            "humor_level": 50,
            "technicality_level": 50,
            "response_speed": "médio",
            "verbosity": "médio"
        }
        
        with open(os.path.join("test_profiles", "default_profile.json"), "w") as f:
            json.dump(self.default_profile, f)
            
        # Criar configuração de teste
        self.test_config = {
            "enabled": True,
            "memory_db_path": ":memory:",
            "profiles_dir": "test_profiles",
            "max_context_interactions": 5,
            "backup_dir": "test_backups",
            "auto_backup": False
        }
        
        with open("test_config.json", "w") as f:
            json.dump(self.test_config, f)
            
        # Criar diretório de backups para testes se não existir
        if not os.path.exists("test_backups"):
            os.makedirs("test_backups")
            
        # Importar módulos a serem testados
        ffrom memory.memory_integrator   import MemoryIntegrator
        from memory.memory_adapter import NinaMemoryAdapter
        from memory.memory_orchestrator import MemoryOrchestrator
        from web.backend.api import app
        
        # Inicializar componentes para testes
        self.memory_integrator = NinaMemoryIntegrator(
            memory_db_path=":memory:",
            profiles_dir="test_profiles"
        )
        
        self.memory_adapter = NinaMemoryAdapter(
            memory_integrator=self.memory_integrator,
            config_path="test_config.json"
        )
        
        self.memory_orchestrator = MemoryOrchestrator()
        self.memory_orchestrator.config = self.test_config
        self.memory_orchestrator.memory_adapter = self.memory_adapter
        
        # Dados de teste
        self.test_user_id = "test_user_123"
        self.test_channel_id = "test_channel_456"
        self.test_message = "Esta é uma mensagem de teste para verificar o funcionamento do sistema de memória."
        
    def tearDown(self):
        """
        Limpeza após cada teste.
        """
        # Remover arquivos de teste
        if os.path.exists("test_config.json"):
            os.remove("test_config.json")
            
        if os.path.exists(os.path.join("test_profiles", "default_profile.json")):
            os.remove(os.path.join("test_profiles", "default_profile.json"))
            
        # Remover diretórios de teste
        if os.path.exists("test_profiles"):
            try:
                os.rmdir("test_profiles")
            except OSError:
                # Diretório não está vazio, ignorar
                pass
                
        if os.path.exists("test_backups"):
            try:
                os.rmdir("test_backups")
            except OSError:
                # Diretório não está vazio, ignorar
                pass
                
        # Limpar variáveis de ambiente
        for var in ["NINA_CONFIG_PATH", "NINA_MEMORY_DB_PATH", "NINA_PROFILES_DIR", "NINA_API_PORT"]:
            if var in os.environ:
                del os.environ[var]
    
    def test_end_to_end_flow(self):
        """
        Testar fluxo completo do sistema de memória e interface web.
        """
        # 1. Processar mensagem de entrada
        result = self.memory_integrator.process_input(
            text=self.test_message,
            user_id=self.test_user_id,
            channel_id=self.test_channel_id
        )
        
        # Verificar resultado do processamento
        self.assertIsNotNone(result)
        self.assertIn("interaction_id", result)
        interaction_id = result["interaction_id"]
        
        # 2. Obter contexto para resposta
        context = self.memory_integrator.get_context_for_response(
            user_id=self.test_user_id,
            channel_id=self.test_channel_id
        )
        
        # Verificar contexto
        self.assertIsNotNone(context)
        self.assertIn("user_profile", context)
        self.assertIn("channel_profile", context)
        self.assertIn("personality", context)
        
        # 3. Adaptar personalidade
        personality = self.memory_integrator.adapt_personality(self.test_channel_id)
        
        # Verificar personalidade adaptada
        self.assertIsNotNone(personality)
        self.assertIn("formality_level", personality)
        
        # 4. Simular resposta da Nina
        response_text = "Esta é uma resposta de teste da Nina."
        
        # 5. Atualizar após resposta
        self.memory_integrator.update_after_response(
            response_text=response_text,
            user_id=self.test_user_id,
            channel_id=self.test_channel_id
        )
        
        # 6. Verificar se a interação foi armazenada
        interaction = self.memory_integrator.memory_manager.get_interaction(interaction_id)
        self.assertIsNotNone(interaction)
        self.assertEqual(interaction["content"], self.test_message)
        
        # 7. Verificar se a resposta foi armazenada
        interactions = self.memory_integrator.memory_manager.get_channel_interactions(self.test_channel_id)
        self.assertGreaterEqual(len(interactions), 2)  # Mensagem original + resposta
        
        # 8. Testar fluxo através do orquestrador
        message = {
            "text": "Esta é outra mensagem de teste.",
            "user_id": self.test_user_id,
            "channel_id": self.test_channel_id,
            "metadata": {
                "timestamp": time.time()
            }
        }
        
        # Processar mensagem através do orquestrador
        enriched_message = self.memory_orchestrator.process_message(message)
        
        # Verificar mensagem enriquecida
        self.assertIsNotNone(enriched_message)
        self.assertIn("memory_data", enriched_message)
        
        # 9. Enriquecer contexto através do orquestrador
        original_context = {
            "input": message["text"],
            "session_id": "test_session_789"
        }
        
        enriched_context = self.memory_orchestrator.enrich_context(original_context, message)
        
        # Verificar contexto enriquecido
        self.assertIsNotNone(enriched_context)
        self.assertIn("memory", enriched_context)
        
        # 10. Formatar memória para LLM
        memory_text = self.memory_orchestrator.format_memory_for_llm(enriched_context["memory"])
        
        # Verificar texto de memória
        self.assertIsNotNone(memory_text)
        self.assertIsInstance(memory_text, str)
        self.assertIn("Informações do Usuário", memory_text)
        
    def test_memory_adapter_integration(self):
        """
        Testar integração do adaptador de memória com o sistema Nina IA.
        """
        # Simular contexto do LLM
        llm_context = {
            "input": self.test_message,
            "session_id": "test_session_789",
            "user": {
                "id": self.test_user_id,
                "name": "Usuário Teste"
            },
            "channel": {
                "id": self.test_channel_id,
                "name": "Canal Teste"
            }
        }
        
        # Enriquecer contexto com memória
        enriched_context = self.memory_adapter.enrich_context(
            context=llm_context,
            user_id=self.test_user_id,
            channel_id=self.test_channel_id
        )
        
        # Verificar contexto enriquecido
        self.assertIsNotNone(enriched_context)
        self.assertIn("memory", enriched_context)
        
        # Simular resposta do LLM
        llm_response = {
            "text": "Esta é uma resposta de teste do LLM.",
            "metadata": {
                "timestamp": time.time()
            }
        }
        
        # Atualizar memória após resposta
        self.memory_adapter.update_after_response(
            response_text=llm_response["text"],
            user_id=self.test_user_id,
            channel_id=self.test_channel_id
        )
        
        # Verificar se a resposta foi armazenada
        interactions = self.memory_integrator.memory_manager.get_user_interactions(self.test_user_id)
        self.assertGreaterEqual(len(interactions), 1)
        
    def test_memory_orchestrator_integration(self):
        """
        Testar integração do orquestrador de memória com o sistema Nina IA.
        """
        # Patch para simular o processador LLM
        with patch('core.memory_orchestrator.LLMProcessor') as mock_llm_processor:
            # Configurar mock para retornar resposta de teste
            mock_llm_instance = MagicMock()
            mock_llm_instance.process.return_value = {
                "text": "Esta é uma resposta de teste do LLM.",
                "metadata": {
                    "timestamp": time.time()
                }
            }
            mock_llm_processor.return_value = mock_llm_instance
            
            # Configurar orquestrador com mock
            self.memory_orchestrator.llm_processor = mock_llm_instance
            
            # Simular mensagem de entrada
            message = {
                "text": self.test_message,
                "user_id": self.test_user_id,
                "channel_id": self.test_channel_id,
                "metadata": {
                    "timestamp": time.time()
                }
            }
            
            # Processar mensagem através do orquestrador
            enriched_message = self.memory_orchestrator.process_message(message)
            
            # Verificar mensagem enriquecida
            self.assertIsNotNone(enriched_message)
            self.assertIn("memory_data", enriched_message)
            
            # Simular processamento de resposta
            response = self.memory_orchestrator.process_response(enriched_message)
            
            # Verificar resposta
            self.assertIsNotNone(response)
            self.assertIn("text", response)
            
            # Verificar se o LLM foi chamado com contexto enriquecido
            mock_llm_instance.process.assert_called_once()
            call_args = mock_llm_instance.process.call_args[0][0]
            self.assertIn("memory", call_args)
            
    def test_api_integration(self):
        """
        Testar integração da API com o sistema de memória.
        """
        from fastapi.testclient import TestClient
        from web.backend.api import app, get_memory_system
        
        # Patch para a função de dependência get_memory_system
        with patch('web.backend.api.get_memory_system', return_value={
            'integrator': self.memory_integrator,
            'adapter': self.memory_adapter
        }):
            # Criar cliente de teste para a API
            client = TestClient(app)
            
            # Testar endpoint de status
            response = client.get('/api/status')
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data['success'])
            
            # Processar mensagem para criar dados de teste
            self.memory_integrator.process_input(
                text=self.test_message,
                user_id=self.test_user_id,
                channel_id=self.test_channel_id
            )
            
            # Testar endpoint para obter usuários
            response = client.get('/api/users')
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data['success'])
            self.assertIn('data', data)
            
            # Testar endpoint para obter detalhes de um usuário
            response = client.get(f'/api/users/{self.test_user_id}')
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data['success'])
            self.assertIn('data', data)
            
            # Testar endpoint para obter canais
            response = client.get('/api/channels')
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data['success'])
            
            # Testar endpoint para obter detalhes de um canal
            response = client.get(f'/api/channels/{self.test_channel_id}')
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data['success'])
            
            # Testar endpoint para obter interações
            response = client.get('/api/interactions')
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data['success'])
            
            # Testar endpoint para obter estatísticas do sistema
            response = client.get('/api/statistics/system')
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data['success'])
            
            # Testar endpoint para obter configurações
            response = client.get('/api/settings')
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data['success'])
            
            # Testar endpoint para criar backup
            response = client.post('/api/backups')
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data['success'])

if __name__ == "__main__":
    unittest.main()
