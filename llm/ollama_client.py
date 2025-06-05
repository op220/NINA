"""
Módulo para comunicação com o Ollama para processamento de linguagem natural.
Parte do projeto Nina IA para processamento de texto e geração de respostas.
"""

import os
import json
import logging
import requests
from typing import Dict, List, Optional, Any, Union

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OllamaClient:
    """
    Cliente para comunicação com o Ollama API.
    """
    
    def __init__(self, 
                 base_url: str = "http://localhost:11434",
                 model: str = "mistral",
                 timeout: int = 60):
        """
        Inicializa o cliente Ollama.
        
        Args:
            base_url: URL base da API Ollama
            model: Nome do modelo a ser usado
            timeout: Timeout para requisições em segundos
        """
        self.base_url = base_url
        self.model = model
        self.timeout = timeout
        self.api_generate = f"{base_url}/api/generate"
        self.api_chat = f"{base_url}/api/chat"
        self.api_models = f"{base_url}/api/tags"
        
        logger.info(f"Inicializando cliente Ollama para o modelo {model}")
        
        # Verificar conexão com o servidor
        try:
            self.check_connection()
            logger.info("Conexão com Ollama estabelecida com sucesso")
        except Exception as e:
            logger.error(f"Erro ao conectar com Ollama: {e}")
            logger.error("Certifique-se de que o servidor Ollama está em execução")
    
    def check_connection(self) -> bool:
        """
        Verifica a conexão com o servidor Ollama.
        
        Returns:
            True se a conexão for bem-sucedida
        """
        try:
            response = requests.get(f"{self.base_url}/api/version", timeout=self.timeout)
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Erro ao verificar conexão com Ollama: {e}")
            raise ConnectionError(f"Não foi possível conectar ao servidor Ollama: {e}")
    
    def list_models(self) -> List[Dict[str, Any]]:
        """
        Lista os modelos disponíveis no servidor Ollama.
        
        Returns:
            Lista de modelos disponíveis
        """
        try:
            response = requests.get(self.api_models, timeout=self.timeout)
            response.raise_for_status()
            return response.json().get("models", [])
        except Exception as e:
            logger.error(f"Erro ao listar modelos: {e}")
            return []
    
    def generate(self, 
                 prompt: str, 
                 system_prompt: Optional[str] = None,
                 temperature: float = 0.7,
                 top_p: float = 0.9,
                 top_k: int = 40,
                 max_tokens: int = 500,
                 stop_sequences: Optional[List[str]] = None) -> str:
        """
        Gera texto a partir de um prompt usando o modelo.
        
        Args:
            prompt: Texto de entrada para o modelo
            system_prompt: Prompt de sistema para definir comportamento do modelo
            temperature: Temperatura para geração (0.0 a 1.0)
            top_p: Valor de top-p para amostragem
            top_k: Valor de top-k para amostragem
            max_tokens: Número máximo de tokens a serem gerados
            stop_sequences: Lista de sequências para parar a geração
            
        Returns:
            Texto gerado pelo modelo
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "num_predict": max_tokens,
            "stream": False
        }
        
        if system_prompt:
            payload["system"] = system_prompt
            
        if stop_sequences:
            payload["stop"] = stop_sequences
        
        try:
            logger.info(f"Enviando prompt para o modelo {self.model}")
            response = requests.post(self.api_generate, json=payload, timeout=self.timeout)
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            logger.error(f"Erro na geração de texto: {e}")
            return f"Erro na geração de texto: {e}"
    
    def chat(self, 
             messages: List[Dict[str, str]],
             system_prompt: Optional[str] = None,
             temperature: float = 0.7,
             top_p: float = 0.9,
             top_k: int = 40,
             max_tokens: int = 500,
             stop_sequences: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Realiza uma conversa com o modelo.
        
        Args:
            messages: Lista de mensagens no formato [{"role": "user", "content": "Olá"}, ...]
            system_prompt: Prompt de sistema para definir comportamento do modelo
            temperature: Temperatura para geração (0.0 a 1.0)
            top_p: Valor de top-p para amostragem
            top_k: Valor de top-k para amostragem
            max_tokens: Número máximo de tokens a serem gerados
            stop_sequences: Lista de sequências para parar a geração
            
        Returns:
            Resposta do modelo com informações adicionais
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "num_predict": max_tokens,
            "stream": False
        }
        
        if system_prompt:
            payload["system"] = system_prompt
            
        if stop_sequences:
            payload["stop"] = stop_sequences
        
        try:
            logger.info(f"Enviando conversa para o modelo {self.model}")
            response = requests.post(self.api_chat, json=payload, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Erro na conversa: {e}")
            return {"message": {"content": f"Erro na conversa: {e}"}}
    
    def pull_model(self, model_name: Optional[str] = None) -> bool:
        """
        Baixa um modelo do Ollama.
        
        Args:
            model_name: Nome do modelo a ser baixado (None = usar o modelo atual)
            
        Returns:
            True se o download for bem-sucedido
        """
        model = model_name or self.model
        
        try:
            logger.info(f"Baixando modelo {model}")
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": model},
                timeout=None  # Sem timeout para downloads
            )
            response.raise_for_status()
            logger.info(f"Modelo {model} baixado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao baixar modelo {model}: {e}")
            return False


if __name__ == "__main__":
    # Exemplo de uso
    client = OllamaClient(model="mistral")
    
    # Listar modelos disponíveis
    models = client.list_models()
    print(f"Modelos disponíveis: {json.dumps(models, indent=2)}")
    
    # Gerar texto
    response = client.generate(
        prompt="Explique o que é inteligência artificial em poucas palavras.",
        system_prompt="Você é um assistente útil e conciso."
    )
    print(f"Resposta: {response}")
    
    # Conversa
    chat_response = client.chat(
        messages=[
            {"role": "user", "content": "Olá, como você está?"}
        ],
        system_prompt="Você é um assistente amigável chamado Nina."
    )
    print(f"Resposta da conversa: {chat_response.get('message', {}).get('content', '')}")
