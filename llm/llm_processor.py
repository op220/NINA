"""
Módulo para gerenciamento de contexto e conversas com o LLM.
Parte do projeto Nina IA para processamento de linguagem natural.
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

from .ollama_client import OllamaClient

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ConversationManager:
    """
    Gerenciador de contexto e conversas para o LLM.
    """
    
    def __init__(self, 
                 model: str = "mistral",
                 max_history: int = 10,
                 conversation_file: Optional[str] = None):
        """
        Inicializa o gerenciador de conversas.
        
        Args:
            model: Nome do modelo a ser usado
            max_history: Número máximo de mensagens no histórico
            conversation_file: Arquivo para salvar o histórico de conversas
        """
        self.model = model
        self.max_history = max_history
        self.conversation_file = conversation_file
        self.history = []
        
        logger.info(f"Inicializando gerenciador de conversas para o modelo {model}")
        
        # Carregar histórico se o arquivo existir
        if conversation_file and os.path.exists(conversation_file):
            try:
                with open(conversation_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
                logger.info(f"Histórico carregado com {len(self.history)} mensagens")
            except Exception as e:
                logger.error(f"Erro ao carregar histórico: {e}")
                self.history = []
    
    def add_message(self, role: str, content: str) -> None:
        """
        Adiciona uma mensagem ao histórico.
        
        Args:
            role: Papel do emissor ('user', 'assistant', 'system')
            content: Conteúdo da mensagem
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        self.history.append(message)
        
        # Limitar o tamanho do histórico
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        
        # Salvar histórico se o arquivo estiver definido
        if self.conversation_file:
            try:
                with open(self.conversation_file, 'w', encoding='utf-8') as f:
                    json.dump(self.history, f, ensure_ascii=False, indent=2)
            except Exception as e:
                logger.error(f"Erro ao salvar histórico: {e}")
    
    def get_conversation_messages(self) -> List[Dict[str, str]]:
        """
        Obtém as mensagens formatadas para envio ao LLM.
        
        Returns:
            Lista de mensagens no formato esperado pelo Ollama
        """
        # Converter formato interno para formato Ollama
        messages = []
        for msg in self.history:
            if msg["role"] != "system":  # Mensagens de sistema são tratadas separadamente
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        return messages
    
    def get_system_message(self) -> Optional[str]:
        """
        Obtém a mensagem de sistema mais recente.
        
        Returns:
            Conteúdo da mensagem de sistema ou None
        """
        for msg in reversed(self.history):
            if msg["role"] == "system":
                return msg["content"]
        return None
    
    def clear_history(self) -> None:
        """
        Limpa o histórico de conversas.
        """
        self.history = []
        
        # Remover arquivo de histórico se existir
        if self.conversation_file and os.path.exists(self.conversation_file):
            try:
                os.remove(self.conversation_file)
                logger.info("Histórico removido")
            except Exception as e:
                logger.error(f"Erro ao remover arquivo de histórico: {e}")


class LLMProcessor:
    """
    Processador de linguagem natural usando Ollama.
    """
    
    def __init__(self, 
                 model: str = "mistral",
                 base_url: str = "http://localhost:11434",
                 max_history: int = 10,
                 conversation_file: Optional[str] = None,
                 temperature: float = 0.7,
                 max_tokens: int = 500):
        """
        Inicializa o processador LLM.
        
        Args:
            model: Nome do modelo a ser usado
            base_url: URL base da API Ollama
            max_history: Número máximo de mensagens no histórico
            conversation_file: Arquivo para salvar o histórico de conversas
            temperature: Temperatura para geração (0.0 a 1.0)
            max_tokens: Número máximo de tokens a serem gerados
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        logger.info(f"Inicializando processador LLM com modelo {model}")
        
        # Inicializar componentes
        self.client = OllamaClient(base_url=base_url, model=model)
        self.conversation = ConversationManager(
            model=model,
            max_history=max_history,
            conversation_file=conversation_file
        )
    
    def set_personality(self, personality: str) -> None:
        """
        Define a personalidade do assistente através de uma mensagem de sistema.
        
        Args:
            personality: Descrição da personalidade
        """
        self.conversation.add_message("system", personality)
        logger.info("Personalidade definida")
    
    def process_input(self, 
                      user_input: str, 
                      temperature: Optional[float] = None,
                      max_tokens: Optional[int] = None) -> str:
        """
        Processa uma entrada do usuário e gera uma resposta.
        
        Args:
            user_input: Texto de entrada do usuário
            temperature: Temperatura para geração (None = usar padrão)
            max_tokens: Número máximo de tokens (None = usar padrão)
            
        Returns:
            Resposta gerada pelo modelo
        """
        # Adicionar mensagem do usuário ao histórico
        self.conversation.add_message("user", user_input)
        
        # Obter mensagens formatadas para o Ollama
        messages = self.conversation.get_conversation_messages()
        system_message = self.conversation.get_system_message()
        
        # Definir parâmetros
        temp = temperature if temperature is not None else self.temperature
        tokens = max_tokens if max_tokens is not None else self.max_tokens
        
        try:
            # Enviar para o modelo
            response = self.client.chat(
                messages=messages,
                system_prompt=system_message,
                temperature=temp,
                max_tokens=tokens
            )
            
            # Extrair resposta
            assistant_response = response.get("message", {}).get("content", "")
            
            # Adicionar resposta ao histórico
            self.conversation.add_message("assistant", assistant_response)
            
            return assistant_response
            
        except Exception as e:
            logger.error(f"Erro ao processar entrada: {e}")
            error_message = f"Desculpe, ocorreu um erro ao processar sua mensagem: {e}"
            self.conversation.add_message("assistant", error_message)
            return error_message
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """
        Obtém a lista de modelos disponíveis.
        
        Returns:
            Lista de modelos disponíveis
        """
        return self.client.list_models()
    
    def change_model(self, new_model: str) -> bool:
        """
        Muda o modelo usado pelo processador.
        
        Args:
            new_model: Nome do novo modelo
            
        Returns:
            True se a mudança for bem-sucedida
        """
        try:
            self.model = new_model
            self.client.model = new_model
            logger.info(f"Modelo alterado para {new_model}")
            return True
        except Exception as e:
            logger.error(f"Erro ao mudar modelo: {e}")
            return False
    
    def clear_conversation(self) -> None:
        """
        Limpa o histórico de conversas.
        """
        self.conversation.clear_history()


if __name__ == "__main__":
    # Exemplo de uso
    processor = LLMProcessor(model="mistral")
    
    # Definir personalidade
    processor.set_personality(
        "Você é Nina, uma assistente de IA amigável e prestativa. "
        "Você responde de forma clara e concisa, com um toque de simpatia."
    )
    
    # Processar algumas entradas
    response1 = processor.process_input("Olá, como você está?")
    print(f"Resposta 1: {response1}")
    
    response2 = processor.process_input("Pode me explicar o que é inteligência artificial?")
    print(f"Resposta 2: {response2}")
