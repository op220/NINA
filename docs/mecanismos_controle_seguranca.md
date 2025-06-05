# Mecanismos de Controle de Segurança para o Sistema de Personalidade Dinâmica

## Visão Geral

O sistema de personalidade dinâmica precisa de controles de segurança robustos para garantir que a evolução da personalidade da IA ocorra de forma segura, previsível e controlada. Este documento descreve os mecanismos de segurança implementados para proteger o sistema contra mudanças indesejadas, comportamentos inadequados e possíveis vulnerabilidades.

## Mecanismos de Segurança Implementados

### 1. Limites de Evolução

```python
import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Union

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("safety_limits.log")
    ]
)
logger = logging.getLogger("SafetyLimits")

class SafetyLimits:
    def __init__(self, config_path: str = "./config/safety_limits.json"):
        """
        Inicializa o sistema de limites de segurança.
        
        Args:
            config_path: Caminho para o arquivo de configuração
        """
        self.config_path = config_path
        self.config_dir = os.path.dirname(config_path)
        
        # Garantir que o diretório exista
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Carregar configurações
        self.config = self._load_config()
        
        logger.info("Sistema de limites de segurança inicializado")
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Carrega o arquivo de configuração.
        
        Returns:
            Dicionário com configurações
        """
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Configuração padrão
                config = {
                    "personality_traits": {
                        "formality_level": {
                            "min": 20,
                            "max": 80,
                            "max_change_per_session": 5
                        },
                        "humor_level": {
                            "min": 10,
                            "max": 70,
                            "max_change_per_session": 5
                        },
                        "empathy_level": {
                            "min": 50,
                            "max": 90,
                            "max_change_per_session": 5
                        },
                        "technicality_level": {
                            "min": 30,
                            "max": 80,
                            "max_change_per_session": 5
                        }
                    },
                    "vocabulary": {
                        "max_custom_words": 50,
                        "max_expressions": 20,
                        "max_new_words_per_session": 5
                    },
                    "topics": {
                        "max_favorite_topics": 15,
                        "max_knowledge_areas": 10,
                        "max_new_topics_per_session": 3
                    },
                    "evolution": {
                        "min_interactions_for_change": 10,
                        "min_confidence_for_change": 0.6,
                        "max_changes_per_day": 20
                    },
                    "forbidden_words": [],
                    "forbidden_topics": [],
                    "forbidden_expressions": []
                }
                
                # Salvar configuração padrão
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                
                return config
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {e}")
            return {
                "personality_traits": {
                    "formality_level": {"min": 20, "max": 80, "max_change_per_session": 5},
                    "humor_level": {"min": 10, "max": 70, "max_change_per_session": 5},
                    "empathy_level": {"min": 50, "max": 90, "max_change_per_session": 5},
                    "technicality_level": {"min": 30, "max": 80, "max_change_per_session": 5}
                }
            }
    
    def save_config(self) -> bool:
        """
        Salva o arquivo de configuração.
        
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Configuração salva: {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar configuração: {e}")
            return False
    
    def validate_trait_value(self, trait_name: str, value: int) -> int:
        """
        Valida o valor de um traço de personalidade.
        
        Args:
            trait_name: Nome do traço
            value: Valor a ser validado
            
        Returns:
            Valor validado
        """
        try:
            # Verificar se o traço existe
            if trait_name not in self.config["personality_traits"]:
                logger.warning(f"Traço não encontrado: {trait_name}")
                return value
            
            # Obter limites
            trait_config = self.config["personality_traits"][trait_name]
            min_value = trait_config.get("min", 0)
            max_value = trait_config.get("max", 100)
            
            # Validar valor
            if value < min_value:
                logger.warning(f"Valor abaixo do mínimo para {trait_name}: {value} < {min_value}")
                return min_value
            elif value > max_value:
                logger.warning(f"Valor acima do máximo para {trait_name}: {value} > {max_value}")
                return max_value
            else:
                return value
        except Exception as e:
            logger.error(f"Erro ao validar valor de traço: {e}")
            return value
    
    def validate_trait_change(self, trait_name: str, current_value: int, new_value: int) -> int:
        """
        Valida a mudança de um traço de personalidade.
        
        Args:
            trait_name: Nome do traço
            current_value: Valor atual
            new_value: Novo valor
            
        Returns:
            Valor validado
        """
        try:
            # Verificar se o traço existe
            if trait_name not in self.config["personality_traits"]:
                logger.warning(f"Traço não encontrado: {trait_name}")
                return new_value
            
            # Obter limite de mudança
            trait_config = self.config["personality_traits"][trait_name]
            max_change = trait_config.get("max_change_per_session", 5)
            
            # Calcular mudança
            change = abs(new_value - current_value)
            
            # Validar mudança
            if change > max_change:
                logger.warning(f"Mudança acima do máximo para {trait_name}: {change} > {max_change}")
                
                # Limitar mudança
                if new_value > current_value:
                    return current_value + max_change
                else:
                    return current_value - max_change
            else:
                return new_value
        except Exception as e:
            logger.error(f"Erro ao validar mudança de traço: {e}")
            return new_value
    
    def validate_vocabulary(self, words: List[str]) -> List[str]:
        """
        Valida uma lista de palavras.
        
        Args:
            words: Lista de palavras
            
        Returns:
            Lista de palavras validada
        """
        try:
            # Obter lista de palavras proibidas
            forbidden_words = self.config.get("forbidden_words", [])
            
            # Filtrar palavras proibidas
            filtered_words = [word for word in words if word.lower() not in forbidden_words]
            
            # Verificar se alguma palavra foi removida
            if len(filtered_words) < len(words):
                logger.warning(f"Palavras proibidas removidas: {len(words) - len(filtered_words)}")
            
            # Limitar número de palavras
            max_words = self.config["vocabulary"].get("max_custom_words", 50)
            if len(filtered_words) > max_words:
                logger.warning(f"Número de palavras excede o máximo: {len(filtered_words)} > {max_words}")
                filtered_words = filtered_words[:max_words]
            
            return filtered_words
        except Exception as e:
            logger.error(f"Erro ao validar vocabulário: {e}")
            return words
    
    def validate_expressions(self, expressions: List[str]) -> List[str]:
        """
        Valida uma lista de expressões.
        
        Args:
            expressions: Lista de expressões
            
        Returns:
            Lista de expressões validada
        """
        try:
            # Obter lista de expressões proibidas
            forbidden_expressions = self.config.get("forbidden_expressions", [])
            
            # Filtrar expressões proibidas
            filtered_expressions = []
            for expr in expressions:
                is_forbidden = False
                for forbidden in forbidden_expressions:
                    if forbidden.lower() in expr.lower():
                        is_forbidden = True
                        break
                
                if not is_forbidden:
                    filtered_expressions.append(expr)
            
            # Verificar se alguma expressão foi removida
            if len(filtered_expressions) < len(expressions):
                logger.warning(f"Expressões proibidas removidas: {len(expressions) - len(filtered_expressions)}")
            
            # Limitar número de expressões
            max_expressions = self.config["vocabulary"].get("max_expressions", 20)
            if len(filtered_expressions) > max_expressions:
                logger.warning(f"Número de expressões excede o máximo: {len(filtered_expressions)} > {max_expressions}")
                filtered_expressions = filtered_expressions[:max_expressions]
            
            return filtered_expressions
        except Exception as e:
            logger.error(f"Erro ao validar expressões: {e}")
            return expressions
    
    def validate_topics(self, topics: List[str]) -> List[str]:
        """
        Valida uma lista de tópicos.
        
        Args:
            topics: Lista de tópicos
            
        Returns:
            Lista de tópicos validada
        """
        try:
            # Obter lista de tópicos proibidos
            forbidden_topics = self.config.get("forbidden_topics", [])
            
            # Filtrar tópicos proibidos
            filtered_topics = []
            for topic in topics:
                is_forbidden = False
                for forbidden in forbidden_topics:
                    if forbidden.lower() in topic.lower():
                        is_forbidden = True
                        break
                
                if not is_forbidden:
                    filtered_topics.append(topic)
            
            # Verificar se algum tópico foi removido
            if len(filtered_topics) < len(topics):
                logger.warning(f"Tópicos proibidos removidos: {len(topics) - len(filtered_topics)}")
            
            # Limitar número de tópicos
            max_topics = self.config["topics"].get("max_favorite_topics", 15)
            if len(filtered_topics) > max_topics:
                logger.warning(f"Número de tópicos excede o máximo: {len(filtered_topics)} > {max_topics}")
                filtered_topics = filtered_topics[:max_topics]
            
            return filtered_topics
        except Exception as e:
            logger.error(f"Erro ao validar tópicos: {e}")
            return topics
    
    def validate_knowledge_areas(self, areas: List[str]) -> List[str]:
        """
        Valida uma lista de áreas de conhecimento.
        
        Args:
            areas: Lista de áreas
            
        Returns:
            Lista de áreas validada
        """
        try:
            # Obter lista de tópicos proibidos
            forbidden_topics = self.config.get("forbidden_topics", [])
            
            # Filtrar áreas proibidas
            filtered_areas = []
            for area in areas:
                is_forbidden = False
                for forbidden in forbidden_topics:
                    if forbidden.lower() in area.lower():
                        is_forbidden = True
                        break
                
                if not is_forbidden:
                    filtered_areas.append(area)
            
            # Verificar se alguma área foi removida
            if len(filtered_areas) < len(areas):
                logger.warning(f"Áreas proibidas removidas: {len(areas) - len(filtered_areas)}")
            
            # Limitar número de áreas
            max_areas = self.config["topics"].get("max_knowledge_areas", 10)
            if len(filtered_areas) > max_areas:
                logger.warning(f"Número de áreas excede o máximo: {len(filtered_areas)} > {max_areas}")
                filtered_areas = filtered_areas[:max_areas]
            
            return filtered_areas
        except Exception as e:
            logger.error(f"Erro ao validar áreas de conhecimento: {e}")
            return areas
    
    def add_forbidden_word(self, word: str) -> bool:
        """
        Adiciona uma palavra à lista de palavras proibidas.
        
        Args:
            word: Palavra a ser adicionada
            
        Returns:
            True se adicionou com sucesso, False caso contrário
        """
        try:
            # Garantir que a lista existe
            if "forbidden_words" not in self.config:
                self.config["forbidden_words"] = []
            
            # Verificar se a palavra já está na lista
            if word.lower() in [w.lower() for w in self.config["forbidden_words"]]:
                logger.info(f"Palavra já está na lista de proibidas: {word}")
                return True
            
            # Adicionar palavra
            self.config["forbidden_words"].append(word.lower())
            
            # Salvar configuração
            return self.save_config()
        except Exception as e:
            logger.error(f"Erro ao adicionar palavra proibida: {e}")
            return False
    
    def add_forbidden_topic(self, topic: str) -> bool:
        """
        Adiciona um tópico à lista de tópicos proibidos.
        
        Args:
            topic: Tópico a ser adicionado
            
        Returns:
            True se adicionou com sucesso, False caso contrário
        """
        try:
            # Garantir que a lista existe
            if "forbidden_topics" not in self.config:
                self.config["forbidden_topics"] = []
            
            # Verificar se o tópico já está na lista
            if topic.lower() in [t.lower() for t in self.config["forbidden_topics"]]:
                logger.info(f"Tópico já está na lista de proibidos: {topic}")
                return True
            
            # Adicionar tópico
            self.config["forbidden_topics"].append(topic.lower())
            
            # Salvar configuração
            return self.save_config()
        except Exception as e:
            logger.error(f"Erro ao adicionar tópico proibido: {e}")
            retu
(Content truncated due to size limit. Use line ranges to read in chunks)