import unittest
import os
import sys
import json
import sqlite3
from datetime import datetime

# Adicionar o diretório raiz ao path para importar outros módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar módulos a serem testados
from memory.memory_integrator import NinaMemoryIntegrator
from memory.memory_adapter import NinaMemoryAdapter
from memory.memory_orchestrator import MemoryOrchestrator

class TestMemorySystem(unittest.TestCase):
    """
    Testes para o sistema de memória de longo prazo da Nina IA.
    """
    
    def setUp(self):
        """
        Configuração para cada teste.
        """
        # Usar banco de dados em memória para testes
        self.test_db_path = ":memory:"
        self.test_profiles_dir = "test_profiles"
        
        # Criar diretório de perfis para testes se não existir
        if not os.path.exists(self.test_profiles_dir):
            os.makedirs(self.test_profiles_dir)
            
        # Criar perfil padrão para testes
        self.default_profile = {
            "formality_level": 50,
            "humor_level": 50,
            "technicality_level": 50,
            "response_speed": "médio",
            "verbosity": "médio"
        }
        
        with open(os.path.join(self.test_profiles_dir, "default_profile.json"), "w") as f:
            json.dump(self.default_profile, f)
            
        # Inicializar integrador de memória
        self.memory_integrator = NinaMemoryIntegrator(
            memory_db_path=self.test_db_path,
            profiles_dir=self.test_profiles_dir
        )
        
        # Configuração de teste
        self.test_config = {
            "enabled": True,
            "memory_db_path": self.test_db_path,
            "profiles_dir": self.test_profiles_dir,
            "max_context_interactions": 5,
            "backup_dir": "test_backups",
            "auto_backup": False
        }
        
        # Inicializar adaptador de memória
        self.memory_adapter = NinaMemoryAdapter(
            memory_integrator=self.memory_integrator,
            config_path=None
        )
        self.memory_adapter.config = self.test_config
        
        # Dados de teste
        self.test_user_id = "test_user_123"
        self.test_channel_id = "test_channel_456"
        self.test_message = "Esta é uma mensagem de teste para verificar o funcionamento do sistema de memória."
        
    def tearDown(self):
        """
        Limpeza após cada teste.
        """
        # Remover arquivos de teste
        if os.path.exists(os.path.join(self.test_profiles_dir, "default_profile.json")):
            os.remove(os.path.join(self.test_profiles_dir, "default_profile.json"))
            
        # Remover diretório de perfis de teste
        if os.path.exists(self.test_profiles_dir):
            try:
                os.rmdir(self.test_profiles_dir)
            except OSError:
                # Diretório não está vazio, ignorar
                pass
                
        # Remover diretório de backups de teste
        if os.path.exists("test_backups"):
            try:
                os.rmdir("test_backups")
            except OSError:
                # Diretório não está vazio, ignorar
                pass
    
    def test_memory_integrator_initialization(self):
        """
        Testar inicialização do integrador de memória.
        """
        self.assertIsNotNone(self.memory_integrator)
        self.assertIsNotNone(self.memory_integrator.memory_manager)
        self.assertIsNotNone(self.memory_integrator.personality_manager)
        
    def test_memory_adapter_initialization(self):
        """
        Testar inicialização do adaptador de memória.
        """
        self.assertIsNotNone(self.memory_adapter)
        self.assertTrue(self.memory_adapter.is_enabled())
        self.assertEqual(self.memory_adapter.config["memory_db_path"], self.test_db_path)
        
    def test_process_input(self):
        """
        Testar processamento de entrada.
        """
        # Processar mensagem
        result = self.memory_integrator.process_input(
            text=self.test_message,
            user_id=self.test_user_id,
            channel_id=self.test_channel_id
        )
        
        # Verificar resultado
        self.assertIsNotNone(result)
        self.assertIn("interaction_id", result)
        self.assertIn("analysis", result)
        self.assertIn("user_profile", result)
        self.assertIn("channel_profile", result)
        
        # Verificar se a interação foi armazenada
        interaction_id = result["interaction_id"]
        interaction = self.memory_integrator.memory_manager.get_interaction(interaction_id)
        self.assertIsNotNone(interaction)
        self.assertEqual(interaction["content"], self.test_message)
        self.assertEqual(interaction["user_id"], self.test_user_id)
        self.assertEqual(interaction["channel_id"], self.test_channel_id)
        
    def test_get_context_for_response(self):
        """
        Testar obtenção de contexto para resposta.
        """
        # Processar mensagem primeiro
        self.memory_integrator.process_input(
            text=self.test_message,
            user_id=self.test_user_id,
            channel_id=self.test_channel_id
        )
        
        # Obter contexto para resposta
        context = self.memory_integrator.get_context_for_response(
            user_id=self.test_user_id,
            channel_id=self.test_channel_id
        )
        
        # Verificar contexto
        self.assertIsNotNone(context)
        self.assertIn("user_profile", context)
        self.assertIn("channel_profile", context)
        self.assertIn("personality", context)
        self.assertIn("recent_interactions", context)
        self.assertIn("timestamp", context)
        
        # Verificar perfil do usuário
        user_profile = context["user_profile"]
        self.assertEqual(user_profile["user_id"], self.test_user_id)
        
        # Verificar perfil do canal
        channel_profile = context["channel_profile"]
        self.assertEqual(channel_profile["channel_id"], self.test_channel_id)
        
        # Verificar personalidade
        personality = context["personality"]
        self.assertIsNotNone(personality)
        self.assertIn("formality_level", personality)
        self.assertIn("humor_level", personality)
        self.assertIn("technicality_level", personality)
        self.assertIn("response_speed", personality)
        self.assertIn("verbosity", personality)
        
        # Verificar interações recentes
        recent_interactions = context["recent_interactions"]
        self.assertIsInstance(recent_interactions, list)
        self.assertGreaterEqual(len(recent_interactions), 1)
        
    def test_adapt_personality(self):
        """
        Testar adaptação de personalidade.
        """
        # Processar algumas mensagens para ter dados para adaptação
        for i in range(3):
            self.memory_integrator.process_input(
                text=f"Mensagem de teste {i+1}",
                user_id=self.test_user_id,
                channel_id=self.test_channel_id
            )
            
        # Adaptar personalidade
        personality = self.memory_integrator.adapt_personality(self.test_channel_id)
        
        # Verificar personalidade adaptada
        self.assertIsNotNone(personality)
        self.assertIn("formality_level", personality)
        self.assertIn("humor_level", personality)
        self.assertIn("technicality_level", personality)
        self.assertIn("response_speed", personality)
        self.assertIn("verbosity", personality)
        
    def test_update_after_response(self):
        """
        Testar atualização após resposta.
        """
        # Processar mensagem
        self.memory_integrator.process_input(
            text=self.test_message,
            user_id=self.test_user_id,
            channel_id=self.test_channel_id
        )
        
        # Resposta da Nina
        response_text = "Esta é uma resposta de teste da Nina."
        
        # Atualizar após resposta
        self.memory_integrator.update_after_response(
            response_text=response_text,
            user_id=self.test_user_id,
            channel_id=self.test_channel_id
        )
        
        # Verificar se a resposta foi armazenada
        interactions = self.memory_integrator.memory_manager.get_channel_interactions(self.test_channel_id)
        self.assertGreaterEqual(len(interactions), 2)  # Mensagem original + resposta
        
        # Encontrar a resposta da Nina
        nina_responses = [i for i in interactions if i.get("is_nina_response", False)]
        self.assertGreaterEqual(len(nina_responses), 1)
        self.assertEqual(nina_responses[0]["content"], response_text)
        self.assertEqual(nina_responses[0]["user_id"], "nina")
        self.assertEqual(nina_responses[0]["target_user_id"], self.test_user_id)
        
    def test_memory_adapter_process_input(self):
        """
        Testar processamento de entrada através do adaptador.
        """
        # Processar mensagem
        result = self.memory_adapter.process_input(
            text=self.test_message,
            user_id=self.test_user_id,
            channel_id=self.test_channel_id
        )
        
        # Verificar resultado
        self.assertIsNotNone(result)
        self.assertIn("interaction_id", result)
        self.assertIn("analysis", result)
        self.assertIn("user_profile", result)
        self.assertIn("channel_profile", result)
        
    def test_memory_adapter_enrich_context(self):
        """
        Testar enriquecimento de contexto através do adaptador.
        """
        # Processar mensagem primeiro
        self.memory_adapter.process_input(
            text=self.test_message,
            user_id=self.test_user_id,
            channel_id=self.test_channel_id
        )
        
        # Contexto original
        original_context = {
            "input": self.test_message,
            "session_id": "test_session_789"
        }
        
        # Enriquecer contexto
        enriched_context = self.memory_adapter.enrich_context(
            context=original_context,
            user_id=self.test_user_id,
            channel_id=self.test_channel_id
        )
        
        # Verificar contexto enriquecido
        self.assertIsNotNone(enriched_context)
        self.assertIn("input", enriched_context)
        self.assertIn("session_id", enriched_context)
        self.assertIn("memory", enriched_context)
        self.assertIn("personality", enriched_context)
        
        # Verificar informações de memória
        memory = enriched_context["memory"]
        self.assertIn("user_profile", memory)
        self.assertIn("channel_profile", memory)
        self.assertIn("personality", memory)
        self.assertIn("recent_interactions", memory)
        
    def test_orchestrator_initialization(self):
        """
        Testar inicialização do orquestrador de memória.
        """
        # Criar orquestrador
        orchestrator = MemoryOrchestrator()
        
        # Verificar inicialização
        self.assertIsNotNone(orchestrator)
        self.assertIsNotNone(orchestrator.config)
        
        # Verificar se está habilitado
        if orchestrator.memory_adapter is not None:
            self.assertTrue(orchestrator.is_enabled())
            
    def test_orchestrator_process_message(self):
        """
        Testar processamento de mensagem através do orquestrador.
        """
        # Criar orquestrador com configuração de teste
        orchestrator = MemoryOrchestrator()
        orchestrator.config = self.test_config
        orchestrator.memory_adapter = self.memory_adapter
        
        # Mensagem de teste
        message = {
            "text": self.test_message,
            "user_id": self.test_user_id,
            "channel_id": self.test_channel_id,
            "metadata": {
                "timestamp": datetime.now().isoformat()
            }
        }
        
        # Processar mensagem
        enriched_message = orchestrator.process_message(message)
        
        # Verificar mensagem enriquecida
        self.assertIsNotNone(enriched_message)
        self.assertIn("text", enriched_message)
        self.assertIn("user_id", enriched_message)
        self.assertIn("channel_id", enriched_message)
        self.assertIn("metadata", enriched_message)
        self.assertIn("memory_data", enriched_message)
        
        # Verificar dados de memória
        memory_data = enriched_message["memory_data"]
        self.assertIn("interaction_id", memory_data)
        self.assertIn("analysis", memory_data)
        self.assertIn("user_profile", memory_data)
        self.assertIn("channel_profile", memory_data)
        
    def test_orchestrator_enrich_context(self):
        """
        Testar enriquecimento de contexto através do orquestrador.
        """
        # Criar orquestrador com configuração de teste
        orchestrator = MemoryOrchestrator()
        orchestrator.config = self.test_config
        orchestrator.memory_adapter = self.memory_adapter
        
        # Processar mensagem primeiro
        message = {
            "text": self.test_message,
            "user_id": self.test_user_id,
            "channel_id": self.test_channel_id,
            "metadata": {
                "timestamp": datetime.now().isoformat()
            }
        }
        orchestrator.process_message(message)
        
        # Contexto original
        original_context = {
            "input": self.test_message,
            "session_id": "test_session_789"
        }
        
        # Enriquecer contexto
        enriched_context = orchestrator.enrich_context(original_context, message)
        
        # Verificar contexto enriquecido
        self.assertIsNotNone(enriched_context)
        self.assertIn("input", enriched_context)
        self.assertIn("session_id", enriched_context)
        self.assertIn("memory", enriched_context)
        self.assertIn("personality", enriched_context)
        
    def test_orchestrator_format_memory_for_llm(self):
        """
        Testar formatação de memória para LLM através do orquestrador.
        """
        # Criar orquestrador com configuração de teste
        orchestrator = MemoryOrchestrator()
        orchestrator.config = self.test_config
        
        # Dados de memória de teste
        memory_data = {
            "user_profile": {
                "username": "Usuário Teste",
                "topics": {
                    "programação": 10,
                    "inteligência artificial": 8,
                    "jogos": 5
                },
                "emotions": {
                    "neutro": 15,
                    "entusiasmo": 7,
                    "curiosidade": 5
                },
                "expressions": ["interessante", "como funciona", "muito bom"]
            },
            "channel_profile": {
                "channel_name": "Canal Teste",
                "topics": {
                    "tecnologia": 20,
                    "programação": 15,
                    "inteligência artificial": 10
                },
                "tone": "técnico"
            },
            "personality": {
                "formality_level": 70,
                "humor_level": 40,
                "technicality_level": 80,
                "response_speed": "médio",
                "verbosity": "detalhado"
            },
            "recent_interactions": [
                {
                    "user_id": "user123",
                    "content": "Como funciona o sistema de memória?"
                },
                {
                    "user_id": "nina",
                    "content": "O sistema de memória funciona armazenando informações sobre usuários e canais."
                },
                {
                    "user_id": "user123",
                    "content": "Qual é a importância do sistema de memória?"
                }
            ]
        }
        
        # Formatar memória para LLM
        formatted_memory = orchestrator.format_memory_for_llm(memory_data)
        
        # Verificar formatação
        self.assertIsNotNone(formatted_memory)
        self.assertIsInstance(formatted_memory, str)
        self.assertIn("Usuário Teste", formatted_memory)
        self.assertIn("programação", formatted_memory)
        self.assertIn("inteligência artificial", formatted_memory)
        self.assertIn("Como funciona o sistema de memória?", formatted_memory)
        
    def test_orchestrator_update_after_response(self):
        """
        Testar atualização após resposta através do orquestrador.
        """
        # Criar orquestrador com configuração de teste
        orchestrator = MemoryOrchestrator()
        orchestrator.config = self.test_config
        orchestrator.memory_adapter = self.memory_adapter
        
        # Processar mensagem primeiro
        message = {
            "text": self.test_message,
            "user_id": self.test_user_id,
            "channel_id": self.test_channel_id,
            "metadata": {
                "timestamp": datetime.now().isoformat()
            }
        }
        orchestrator.process_message(message)
        
        # Resposta da Nina
        response_text = "Esta é uma resposta de teste da Nina."
        
        # Atualizar após resposta
        orchestrator.update_after_response(response_text, message)
        
        # Verificar se a resposta foi armazenada
        interactions = self.memory_integrator.memory_manager.get_channel_interactions(self.test_channel_id)
        self.assertGreaterEqual(len(interactions), 2)  # Mensagem original + resposta
        
        # Encontrar a resposta da Nina
        nina_responses = [i for i in interactions if i.get("is_nina_response", False)]
        self.assertGreaterEqual(len(nina_responses), 1)
        self.assertEqual(nina_responses[0]["content"], response_text)
        self.assertEqual(nina_responses[0]["user_id"], "nina")
        self.assertEqual(nina_responses[0]["target_user_id"], self.test_user_id)
