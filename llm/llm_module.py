"""
Módulo principal para LLM (Language Model) do projeto Nina IA.
Integra o processamento de linguagem natural com personalização.
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Union

from .ollama_client import OllamaClient
from .llm_processor import LLMProcessor

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LLMModule:
    """
    Módulo principal para processamento de linguagem natural.
    """
    
    def __init__(self,
                 model: str = "mistral",
                 base_url: str = "http://localhost:11434",
                 personality_file: Optional[str] = None,
                 conversation_dir: Optional[str] = None,
                 temperature: float = 0.7,
                 max_tokens: int = 500):
        """
        Inicializa o módulo LLM.
        
        Args:
            model: Nome do modelo a ser usado
            base_url: URL base da API Ollama
            personality_file: Arquivo com definição de personalidade
            conversation_dir: Diretório para armazenar conversas
            temperature: Temperatura para geração (0.0 a 1.0)
            max_tokens: Número máximo de tokens a serem gerados
        """
        self.model = model
        self.base_url = base_url
        self.personality_file = personality_file
        self.conversation_dir = conversation_dir
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.personality = {}
        
        # Criar diretório de conversas se não existir
        if conversation_dir and not os.path.exists(conversation_dir):
            os.makedirs(conversation_dir)
            logger.info(f"Diretório de conversas criado: {conversation_dir}")
        
        # Definir arquivo de conversas
        conversation_file = None
        if conversation_dir:
            conversation_file = os.path.join(conversation_dir, f"conversation_{model}.json")
        
        # Inicializar processador LLM
        self.processor = LLMProcessor(
            model=model,
            base_url=base_url,
            conversation_file=conversation_file,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # Carregar personalidade se o arquivo existir
        if personality_file and os.path.exists(personality_file):
            self.load_personality(personality_file)
    
    def load_personality(self, personality_file: str) -> bool:
        """
        Carrega a personalidade a partir de um arquivo JSON.
        
        Args:
            personality_file: Caminho para o arquivo de personalidade
            
        Returns:
            True se a personalidade foi carregada com sucesso
        """
        try:
            with open(personality_file, 'r', encoding='utf-8') as f:
                self.personality = json.load(f)
            
            # Aplicar personalidade ao processador
            self._apply_personality()
            
            logger.info(f"Personalidade carregada: {self.personality.get('name', 'Sem nome')}")
            return True
        except Exception as e:
            logger.error(f"Erro ao carregar personalidade: {e}")
            return False
    
    def _apply_personality(self) -> None:
        """
        Aplica a personalidade carregada ao processador LLM.
        """
        if not self.personality:
            logger.warning("Nenhuma personalidade definida")
            return
        
        # Construir prompt de sistema com base na personalidade
        system_prompt = self._build_system_prompt()
        
        # Definir personalidade no processador
        self.processor.set_personality(system_prompt)
    
    def _build_system_prompt(self) -> str:
        """
        Constrói o prompt de sistema com base na personalidade.
        
        Returns:
            Prompt de sistema formatado
        """
        name = self.personality.get("name", "Assistente")
        speech_style = self.personality.get("speech_style", "formal")
        preferences = self.personality.get("preferences", [])
        mood = self.personality.get("mood", "neutro")
        
        # Construir descrição de preferências
        prefs_text = ""
        if preferences:
            prefs_text = "Você gosta de falar sobre " + ", ".join(preferences) + ". "
        
        # Construir descrição de estilo de fala
        style_text = ""
        if speech_style == "formal":
            style_text = "Você fala de maneira formal e educada. "
        elif speech_style == "casual":
            style_text = "Você fala de maneira casual e descontraída. "
        elif speech_style == "amigável":
            style_text = "Você fala de maneira amigável e calorosa. "
        elif speech_style == "técnico":
            style_text = "Você fala de maneira técnica e precisa. "
        
        # Construir descrição de humor
        mood_text = ""
        if mood == "alegre":
            mood_text = "Seu humor atual é alegre e otimista. "
        elif mood == "sério":
            mood_text = "Seu humor atual é sério e focado. "
        elif mood == "neutro":
            mood_text = "Seu humor atual é neutro e equilibrado. "
        elif mood == "reflexivo":
            mood_text = "Seu humor atual é reflexivo e contemplativo. "
        
        # Montar prompt completo
        system_prompt = (
            f"Você é {name}, uma assistente de inteligência artificial. "
            f"{style_text}"
            f"{mood_text}"
            f"{prefs_text}"
            "Você responde de forma clara e concisa, mantendo seu estilo de fala e personalidade. "
            "Você é útil, respeitosa e não julga as perguntas do usuário. "
            "Você evita respostas muito longas e se concentra no que é mais relevante."
        )
        
        return system_prompt
    
    def set_personality_attribute(self, attribute: str, value: Any) -> None:
        """
        Define um atributo específico da personalidade.
        
        Args:
            attribute: Nome do atributo ('name', 'speech_style', 'mood', etc.)
            value: Valor do atributo
        """
        self.personality[attribute] = value
        
        # Atualizar personalidade no processador
        self._apply_personality()
        
        # Salvar personalidade se o arquivo estiver definido
        if self.personality_file:
            try:
                with open(self.personality_file, 'w', encoding='utf-8') as f:
                    json.dump(self.personality, f, ensure_ascii=False, indent=2)
                logger.info(f"Personalidade atualizada: {attribute} = {value}")
            except Exception as e:
                logger.error(f"Erro ao salvar personalidade: {e}")
    
    def process_text(self, text: str) -> str:
        """
        Processa um texto e gera uma resposta.
        
        Args:
            text: Texto de entrada
            
        Returns:
            Resposta gerada pelo modelo
        """
        return self.processor.process_input(text, temperature=self.temperature, max_tokens=self.max_tokens)
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """
        Obtém a lista de modelos disponíveis.
        
        Returns:
            Lista de modelos disponíveis
        """
        return self.processor.get_available_models()
    
    def change_model(self, new_model: str) -> bool:
        """
        Muda o modelo usado pelo módulo.
        
        Args:
            new_model: Nome do novo modelo
            
        Returns:
            True se a mudança for bem-sucedida
        """
        result = self.processor.change_model(new_model)
        if result:
            self.model = new_model
            
            # Atualizar arquivo de conversas
            if self.conversation_dir:
                conversation_file = os.path.join(self.conversation_dir, f"conversation_{new_model}.json")
                self.processor.conversation.conversation_file = conversation_file
            
            # Reaplicar personalidade
            self._apply_personality()
        
        return result
    
    def clear_conversation(self) -> None:
        """
        Limpa o histórico de conversas.
        """
        self.processor.clear_conversation()


if __name__ == "__main__":
    # Exemplo de uso
    import tempfile
    
    # Criar arquivo de personalidade temporário
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        personality = {
            "name": "Nina",
            "speech_style": "amigável",
            "preferences": ["tecnologia", "música", "filmes"],
            "mood": "alegre"
        }
        json.dump(personality, f, ensure_ascii=False, indent=2)
        personality_file = f.name
    
    # Criar diretório temporário para conversas
    conversation_dir = tempfile.mkdtemp()
    
    try:
        # Inicializar módulo LLM
        llm = LLMModule(
            model="mistral",
            personality_file=personality_file,
            conversation_dir=conversation_dir
        )
        
        # Processar algumas entradas
        response1 = llm.process_text("Olá, como você está?")
        print(f"Resposta 1: {response1}")
        
        # Mudar humor
        llm.set_personality_attribute("mood", "reflexivo")
        
        response2 = llm.process_text("Pode me falar sobre tecnologia?")
        print(f"Resposta 2: {response2}")
        
    finally:
        # Limpar arquivos temporários
        if os.path.exists(personality_file):
            os.unlink(personality_file)
