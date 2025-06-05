"""
Módulo de análise de padrões para o sistema de memória de longo prazo da Nina IA.
Implementa funcionalidades para análise de sentimentos, extração de tópicos e detecção de padrões.
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pattern_analyzer.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("PatternAnalyzer")

class PatternAnalyzer:
    """
    Classe para análise de padrões em mensagens e interações.
    """
    
    def __init__(self):
        """
        Inicializa o analisador de padrões.
        """
        # Palavras-chave para tópicos comuns
        self.topic_keywords = {
            "jogos": ["jogo", "jogar", "game", "gaming", "console", "playstation", "xbox", "nintendo", "steam"],
            "tecnologia": ["tech", "tecnologia", "computador", "pc", "programação", "código", "software", "hardware"],
            "música": ["música", "canção", "banda", "artista", "álbum", "spotify", "playlist", "tocar"],
            "filmes": ["filme", "cinema", "assistir", "netflix", "série", "episódio", "temporada", "ator", "atriz"],
            "animes": ["anime", "manga", "otaku", "japonês", "episódio", "personagem", "naruto", "one piece"],
            "esportes": ["esporte", "futebol", "basquete", "vôlei", "time", "jogo", "campeonato", "copa"],
            "comida": ["comida", "comer", "restaurante", "receita", "prato", "culinária", "cozinhar", "delicioso"],
            "política": ["política", "governo", "presidente", "eleição", "partido", "congresso", "lei", "votar"],
            "educação": ["escola", "faculdade", "universidade", "estudar", "professor", "aluno", "curso", "aula"],
            "trabalho": ["trabalho", "emprego", "empresa", "chefe", "colega", "escritório", "reunião", "projeto"]
        }
        
        # Palavras-chave para emoções
        self.emotion_keywords = {
            "feliz": ["feliz", "alegre", "contente", "animado", "empolgado", "divertido", "ótimo", "excelente", "maravilhoso", "incrível", "😊", "😄", "😁", "🙂", "😀"],
            "triste": ["triste", "chateado", "deprimido", "desanimado", "melancólico", "infeliz", "péssimo", "terrível", "😢", "😭", "😔", "😞", "😥"],
            "bravo": ["bravo", "irritado", "furioso", "nervoso", "chateado", "frustrado", "raiva", "ódio", "😠", "😡", "🤬", "😤", "😒"],
            "neutro": ["ok", "normal", "tanto faz", "talvez", "pode ser", "mais ou menos", "médio", "moderado", "😐", "😶", "🙄"]
        }
        
        # Expressões comuns
        self.common_expressions = [
            r"nossa senhora",
            r"caramba meu",
            r"meu deus",
            r"pelo amor",
            r"na moral",
            r"fala sério",
            r"com certeza",
            r"tipo assim",
            r"sabe como é",
            r"então né",
            r"pois é",
            r"tá ligado",
            r"vamos combinar",
            r"sei lá",
            r"enfim",
            r"basicamente"
        ]
        
        logger.info("Analisador de padrões inicializado")
    
    def analyze_message(self, content: str) -> Dict[str, Any]:
        """
        Analisa uma mensagem para extrair informações relevantes.
        
        Args:
            content: Conteúdo da mensagem
            
        Returns:
            Dicionário com resultados da análise
        """
        try:
            # Converter para minúsculas
            text = content.lower()
            
            # Analisar sentimento
            sentiment = self.analyze_sentiment(text)
            
            # Extrair tópicos
            topics = self.extract_topics(text)
            
            # Detectar expressões
            expressions = self.detect_expressions(text)
            
            # Calcular estatísticas básicas
            word_count = len(text.split())
            char_count = len(text)
            
            return {
                "sentiment": sentiment,
                "topics": topics,
                "expressions": expressions,
                "word_count": word_count,
                "char_count": char_count
            }
        except Exception as e:
            logger.error(f"Erro ao analisar mensagem: {e}")
            return {
                "sentiment": 0.0,
                "topics": [],
                "expressions": [],
                "word_count": 0,
                "char_count": 0
            }
    
    def analyze_sentiment(self, text: str) -> float:
        """
        Analisa o sentimento de um texto.
        
        Args:
            text: Texto a ser analisado
            
        Returns:
            Pontuação de sentimento (-1.0 a 1.0)
        """
        try:
            # Implementação simples baseada em palavras-chave
            # Em uma implementação real, usaríamos um modelo de ML
            
            score = 0.0
            word_count = 0
            
            # Contar ocorrências de palavras-chave de emoções
            for emotion, keywords in self.emotion_keywords.items():
                for keyword in keywords:
                    count = text.count(keyword)
                    if count > 0:
                        if emotion == "feliz":
                            score += count * 0.5
                        elif emotion == "triste":
                            score -= count * 0.3
                        elif emotion == "bravo":
                            score -= count * 0.5
                        word_count += count
            
            # Normalizar score
            if word_count > 0:
                score = max(-1.0, min(1.0, score / word_count))
            
            return score
        except Exception as e:
            logger.error(f"Erro ao analisar sentimento: {e}")
            return 0.0
    
    def extract_topics(self, text: str) -> List[str]:
        """
        Extrai tópicos de um texto.
        
        Args:
            text: Texto a ser analisado
            
        Returns:
            Lista de tópicos identificados
        """
        try:
            topics = []
            
            # Verificar ocorrências de palavras-chave de tópicos
            for topic, keywords in self.topic_keywords.items():
                for keyword in keywords:
                    if keyword in text:
                        if topic not in topics:
                            topics.append(topic)
                        break
            
            return topics
        except Exception as e:
            logger.error(f"Erro ao extrair tópicos: {e}")
            return []
    
    def detect_expressions(self, text: str) -> List[str]:
        """
        Detecta expressões comuns em um texto.
        
        Args:
            text: Texto a ser analisado
            
        Returns:
            Lista de expressões identificadas
        """
        try:
            expressions = []
            
            # Verificar ocorrências de expressões comuns
            for expression_pattern in self.common_expressions:
                matches = re.findall(expression_pattern, text)
                if matches:
                    for match in matches:
                        if match not in expressions:
                            expressions.append(match)
            
            return expressions
        except Exception as e:
            logger.error(f"Erro ao detectar expressões: {e}")
            return []
    
    def analyze_user_pattern(self, messages: List[str]) -> Dict[str, Any]:
        """
        Analisa padrões de comunicação de um usuário com base em várias mensagens.
        
        Args:
            messages: Lista de mensagens do usuário
            
        Returns:
            Dicionário com resultados da análise
        """
        try:
            if not messages:
                return {}
            
            # Analisar cada mensagem
            analyses = [self.analyze_message(msg) for msg in messages]
            
            # Calcular média de sentimento
            sentiment_scores = [a["sentiment"] for a in analyses]
            avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
            
            # Agregar tópicos
            all_topics = []
            for a in analyses:
                all_topics.extend(a["topics"])
            
            # Contar ocorrências de tópicos
            topic_counts = {}
            for topic in all_topics:
                if topic in topic_counts:
                    topic_counts[topic] += 1
                else:
                    topic_counts[topic] = 1
            
            # Ordenar tópicos por contagem
            sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
            top_topics = [t[0] for t in sorted_topics[:5]]
            
            # Agregar expressões
            all_expressions = []
            for a in analyses:
                all_expressions.extend(a["expressions"])
            
            # Contar ocorrências de expressões
            expression_counts = {}
            for expr in all_expressions:
                if expr in expression_counts:
                    expression_counts[expr] += 1
                else:
                    expression_counts[expr] = 1
            
            # Ordenar expressões por contagem
            sorted_expressions = sorted(expression_counts.items(), key=lambda x: x[1], reverse=True)
            top_expressions = [e[0] for e in sorted_expressions[:5]]
            
            # Calcular tamanho médio de mensagem
            word_counts = [a["word_count"] for a in analyses]
            avg_word_count = sum(word_counts) / len(word_counts)
            
            char_counts = [a["char_count"] for a in analyses]
            avg_char_count = sum(char_counts) / len(char_counts)
            
            return {
                "average_sentiment": avg_sentiment,
                "top_topics": top_topics,
                "top_expressions": top_expressions,
                "average_word_count": avg_word_count,
                "average_char_count": avg_char_count,
                "message_count": len(messages)
            }
        except Exception as e:
            logger.error(f"Erro ao analisar padrão de usuário: {e}")
            return {}
    
    def analyze_channel_pattern(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analisa padrões de comunicação em um canal com base em várias mensagens.
        
        Args:
            messages: Lista de mensagens do canal, cada uma com "user_id" e "content"
            
        Returns:
            Dicionário com resultados da análise
        """
        try:
            if not messages:
                return {}
            
            # Analisar cada mensagem
            analyses = [self.analyze_message(msg["content"]) for msg in messages]
            
            # Calcular média de sentimento
            sentiment_scores = [a["sentiment"] for a in analyses]
            avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
            
            # Agregar tópicos
            all_topics = []
            for a in analyses:
                all_topics.extend(a["topics"])
            
            # Contar ocorrências de tópicos
            topic_counts = {}
            for topic in all_topics:
                if topic in topic_counts:
                    topic_counts[topic] += 1
                else:
                    topic_counts[topic] = 1
            
            # Ordenar tópicos por contagem
            sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
            top_topics = [t[0] for t in sorted_topics[:5]]
            
            # Contar mensagens por usuário
            user_message_counts = {}
            for msg in messages:
                user_id = msg["user_id"]
                if user_id in user_message_counts:
                    user_message_counts[user_id] += 1
                else:
                    user_message_counts[user_id] = 1
            
            # Ordenar usuários por contagem de mensagens
            sorted_users = sorted(user_message_counts.items(), key=lambda x: x[1], reverse=True)
            top_users = [u[0] for u in sorted_users[:5]]
            
            # Calcular tamanho médio de mensagem
            word_counts = [a["word_count"] for a in analyses]
            avg_word_count = sum(word_counts) / len(word_counts)
            
            char_counts = [a["char_count"] for a in analyses]
            avg_char_count = sum(char_counts) / len(char_counts)
            
            # Determinar tom predominante
            if avg_sentiment >= 0.3:
                predominant_tone = "informal"
            elif avg_sentiment >= -0.3:
                predominant_tone = "neutro"
            else:
                predominant_tone = "formal"
            
            return {
                "average_sentiment": avg_sentiment,
                "predominant_tone": predominant_tone,
                "top_topics": top_topics,
                "top_users": top_users,
                "average_word_count": avg_word_count,
                "average_char_count": avg_char_count,
                "message_count": len(messages),
                "user_count": len(user_message_counts)
            }
        except Exception as e:
            logger.error(f"Erro ao analisar padrão de canal: {e}")
            return {}
    
    def detect_user_personality(self, messages: List[str]) -> Dict[str, Any]:
        """
        Detecta traços de personalidade de um usuário com base em suas mensagens.
        
        Args:
            messages: Lista de mensagens do usuário
            
        Returns:
            Dicionário com traços de personalidade
        """
        try:
            if not messages:
                return {}
            
            # Analisar padrão geral
            pattern = self.analyze_user_pattern(messages)
            
            # Calcular traços de personalidade
            
            # Formalidade (0-100)
            # Baseado no sentimento médio e tamanho das mensagens
            avg_sentiment = pattern.get("average_sentiment", 0.0)
            avg_word_count = pattern.get("average_word_count", 0)
            
            formality = 50  # Valor padrão
            
            # Sentimento mais negativo tende a ser mais formal
            formality -= avg_sentiment * 20
            
            # Mensagens mais longas tendem a ser mais formais
            if avg_word_count > 20:
                formality += 10
            elif avg_word_count > 10:
                formality += 5
            
            # Humor (0-100)
            # Baseado no sentimento médio
            humor = 50 + (avg_sentiment * 50)
            
            # Tecnicidade (0-100)
            # Baseado nos tópicos
            technicality = 50  # Valor padrão
            technical_topics = ["tecnologia", "educação", "política", "trabalho"]
            
            top_topics = pattern.get("top_topics", [])
            for topic in top_topics:
                if topic in technical_topics:
                    technicality += 10
            
            # Limitar valores
            formality = max(0, min(100, formality))
            humor = max(0, min(100, humor))
            technicality = max(0, min(100, technicality))
            
            return {
                "formality_level": int(formality),
                "humor_level": int(humor),
                "technicality_level": int(technicality)
            }
        except Exception as e:
            logger.error(f"Erro ao detectar personalidade do usuário: {e}")
            return {
                "formality_level": 50,
                "humor_level": 50,
                "technicality_level": 50
            } # Adicionado fechamento da chave

(Content truncated due to size limit. Use line ranges to read in chunks)