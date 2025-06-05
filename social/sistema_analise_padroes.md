# Sistema de Análise de Padrões de Conversas

## Arquitetura do Sistema

### Componentes Principais
1. **Processador de Transcrições**: Carrega e prepara as transcrições diarizadas
2. **Analisador de Sentimentos**: Avalia o tom emocional das mensagens
3. **Extrator de Tópicos**: Identifica temas recorrentes nas conversas
4. **Analisador de Estilo**: Detecta padrões de fala, vocabulário e formalidade
5. **Analisador de Clima**: Determina o clima geral da conversa (humorado, sério, técnico, etc.)
6. **Gerador de Insights**: Consolida análises em insights acionáveis para personalidade

### Fluxo de Dados
1. Transcrições diarizadas são carregadas do sistema de diarização
2. Texto é processado para análise de sentimentos, tópicos e estilo
3. Padrões são identificados e quantificados
4. Insights são gerados e armazenados para uso pelo sistema de personalidade
5. Resultados são organizados por falante, canal e sessão

## Implementação

### Processador de Transcrições
```python
import os
import json
import logging
from datetime import datetime
from collections import defaultdict
import re

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("conversation_analysis.log")
    ]
)
logger = logging.getLogger("TranscriptionProcessor")

class TranscriptionProcessor:
    def __init__(self, base_dir="./data/transcriptions"):
        """
        Inicializa o processador de transcrições.
        
        Args:
            base_dir: Diretório base para transcrições
        """
        self.base_dir = base_dir
        logger.info(f"Inicializando processador de transcrições. Diretório base: {base_dir}")
    
    def load_transcription_file(self, file_path):
        """
        Carrega um arquivo de transcrição.
        
        Args:
            file_path: Caminho para o arquivo de transcrição (JSON)
            
        Returns:
            Dicionário com dados da transcrição
        """
        if not os.path.exists(file_path):
            logger.error(f"Arquivo de transcrição não encontrado: {file_path}")
            return None
        
        try:
            logger.info(f"Carregando arquivo de transcrição: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return data
            
        except Exception as e:
            logger.error(f"Erro ao carregar arquivo de transcrição: {e}")
            return None
    
    def load_session_transcription(self, session_dir):
        """
        Carrega transcrições de uma sessão completa.
        
        Args:
            session_dir: Diretório da sessão
            
        Returns:
            Dicionário com dados da sessão
        """
        try:
            logger.info(f"Carregando transcrições da sessão: {session_dir}")
            
            # Procurar arquivo de transcrição da sessão
            session_json = os.path.join(session_dir, "session_transcription.json")
            
            if os.path.exists(session_json):
                return self.load_transcription_file(session_json)
            
            # Se não encontrar arquivo consolidado, procurar arquivos individuais
            transcription_files = []
            for file in os.listdir(session_dir):
                if file.endswith("_diarized_transcription.json"):
                    transcription_files.append(os.path.join(session_dir, file))
            
            if not transcription_files:
                logger.warning(f"Nenhum arquivo de transcrição encontrado em: {session_dir}")
                return None
            
            # Carregar e consolidar arquivos
            session_data = {
                "session_dir": session_dir,
                "processed_at": datetime.now().isoformat(),
                "files": {}
            }
            
            for file_path in transcription_files:
                file_data = self.load_transcription_file(file_path)
                if file_data:
                    session_data["files"][os.path.basename(file_path)] = file_data
            
            return session_data
            
        except Exception as e:
            logger.error(f"Erro ao carregar transcrições da sessão: {e}")
            return None
    
    def extract_speaker_utterances(self, transcription_data):
        """
        Extrai falas por falante de uma transcrição.
        
        Args:
            transcription_data: Dados de transcrição
            
        Returns:
            Dicionário com falas por falante
        """
        try:
            speaker_utterances = defaultdict(list)
            
            # Verificar se é um arquivo individual ou sessão
            if "files" in transcription_data:
                # Processar cada arquivo na sessão
                for file_name, file_data in transcription_data["files"].items():
                    if "segments" in file_data:
                        for segment in file_data["segments"]:
                            if "speaker" in segment and "text" in segment:
                                speaker_utterances[segment["speaker"]].append({
                                    "text": segment["text"],
                                    "start": segment.get("start", 0),
                                    "end": segment.get("end", 0),
                                    "file": file_name
                                })
            elif "segments" in transcription_data:
                # Processar arquivo individual
                for segment in transcription_data["segments"]:
                    if "speaker" in segment and "text" in segment:
                        speaker_utterances[segment["speaker"]].append({
                            "text": segment["text"],
                            "start": segment.get("start", 0),
                            "end": segment.get("end", 0)
                        })
            
            # Ordenar falas por tempo
            for speaker in speaker_utterances:
                speaker_utterances[speaker].sort(key=lambda x: x.get("start", 0))
            
            return dict(speaker_utterances)
            
        except Exception as e:
            logger.error(f"Erro ao extrair falas por falante: {e}")
            return {}
    
    def extract_conversation_text(self, transcription_data):
        """
        Extrai texto completo da conversa em ordem cronológica.
        
        Args:
            transcription_data: Dados de transcrição
            
        Returns:
            Lista de segmentos de texto em ordem cronológica
        """
        try:
            segments = []
            
            # Verificar se é um arquivo individual ou sessão
            if "files" in transcription_data:
                # Processar cada arquivo na sessão
                for file_name, file_data in transcription_data["files"].items():
                    if "segments" in file_data:
                        for segment in file_data["segments"]:
                            if "text" in segment:
                                segments.append({
                                    "text": segment["text"],
                                    "speaker": segment.get("speaker", "unknown"),
                                    "start": segment.get("start", 0),
                                    "end": segment.get("end", 0),
                                    "file": file_name
                                })
            elif "segments" in transcription_data:
                # Processar arquivo individual
                for segment in transcription_data["segments"]:
                    if "text" in segment:
                        segments.append({
                            "text": segment["text"],
                            "speaker": segment.get("speaker", "unknown"),
                            "start": segment.get("start", 0),
                            "end": segment.get("end", 0)
                        })
            
            # Ordenar segmentos por tempo
            segments.sort(key=lambda x: x.get("start", 0))
            
            return segments
            
        except Exception as e:
            logger.error(f"Erro ao extrair texto da conversa: {e}")
            return []
    
    def clean_text(self, text):
        """
        Limpa e normaliza texto para análise.
        
        Args:
            text: Texto a ser limpo
            
        Returns:
            Texto limpo e normalizado
        """
        if not text:
            return ""
        
        try:
            # Converter para minúsculas
            text = text.lower()
            
            # Remover caracteres especiais, mantendo pontuação básica
            text = re.sub(r'[^\w\s.,!?;:\-]', '', text)
            
            # Normalizar espaços
            text = re.sub(r'\s+', ' ', text).strip()
            
            return text
            
        except Exception as e:
            logger.error(f"Erro ao limpar texto: {e}")
            return text
    
    def preprocess_transcription(self, transcription_data):
        """
        Pré-processa transcrição para análise.
        
        Args:
            transcription_data: Dados de transcrição
            
        Returns:
            Dicionário com dados pré-processados
        """
        try:
            # Extrair falas por falante
            speaker_utterances = self.extract_speaker_utterances(transcription_data)
            
            # Extrair conversa completa
            conversation = self.extract_conversation_text(transcription_data)
            
            # Limpar e normalizar textos
            cleaned_utterances = {}
            for speaker, utterances in speaker_utterances.items():
                cleaned_utterances[speaker] = [
                    {**u, "cleaned_text": self.clean_text(u["text"])}
                    for u in utterances
                ]
            
            cleaned_conversation = [
                {**s, "cleaned_text": self.clean_text(s["text"])}
                for s in conversation
            ]
            
            # Consolidar em um único objeto
            processed_data = {
                "speaker_utterances": cleaned_utterances,
                "conversation": cleaned_conversation,
                "metadata": {
                    "num_speakers": len(cleaned_utterances),
                    "num_utterances": sum(len(u) for u in cleaned_utterances.values()),
                    "processed_at": datetime.now().isoformat()
                }
            }
            
            return processed_data
            
        except Exception as e:
            logger.error(f"Erro ao pré-processar transcrição: {e}")
            return None
```

### Analisador de Sentimentos
```python
import os
import json
import logging
import numpy as np
from textblob import TextBlob
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("sentiment_analysis.log")
    ]
)
logger = logging.getLogger("SentimentAnalyzer")

class SentimentAnalyzer:
    def __init__(self, method="textblob", language="pt", use_transformers=False, model_name=None):
        """
        Inicializa o analisador de sentimentos.
        
        Args:
            method: Método de análise ('textblob', 'vader', 'transformers')
            language: Código do idioma
            use_transformers: Se deve usar modelos transformers
            model_name: Nome do modelo transformers (se aplicável)
        """
        self.method = method
        self.language = language
        self.use_transformers = use_transformers
        
        logger.info(f"Inicializando analisador de sentimentos. Método: {method}, Idioma: {language}")
        
        try:
            # Inicializar analisador conforme método escolhido
            if method == "textblob":
                # Baixar recursos necessários para TextBlob
                try:
                    nltk.download('punkt', quiet=True)
                except:
                    logger.warning("Não foi possível baixar recursos NLTK. TextBlob pode não funcionar corretamente.")
            
            elif method == "vader":
                # Baixar recursos necessários para VADER
                try:
                    nltk.download('vader_lexicon', quiet=True)
                    self.vader = SentimentIntensityAnalyzer()
                except:
                    logger.warning("Não foi possível baixar recursos VADER. Alternando para TextBlob.")
                    self.method = "textblob"
            
            elif method == "transformers" and use_transformers:
                # Carregar modelo transformers
                if model_name is None:
                    if language == "pt":
                        model_name = "neuralmind/bert-base-portuguese-cased"
                    else:
                        model_name = "distilbert-base-uncased-finetuned-sst-2-english"
                
                logger.info(f"Carregando modelo transformers: {model_name}")
                self.sentiment_pipeline = pipeline(
                    "sentiment-analysis",
                    model=model_name,
                    tokenizer=model_name
                )
            else:
                logger.warning(f"Método {method} não reconhecido. Usando TextBlob como fallback.")
                self.method = "textblob"
                
            logger.info("Analisador de sentimentos inicializado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao inicializar analisador de sentimentos: {e}")
            logger.warning("Usando TextBlob como fallback")
            self.method = "textblob"
    
    def analyze_text(self, text):
        """
        Analisa o sentimento de um texto.
        
        Args:
            text: Texto a ser analisado
            
        Returns:
            Dicionário com resultados da análise
        """
        if not text:
            return {"polarity": 0, "subjectivity": 0, "sentiment": "neutral", "confidence": 0}
        
        try:
            if self.method == "textblob":
                return self._analyze_with_textblob(text)
            elif self.method == "vader":
                return self._analyze_with_vader(text)
            elif self.method == "transformers" and hasattr(self, 'sentiment_pipeline'):
                return self._analyze_with_transformers(text)
            else:
                # Fallback para TextBlob
                return self._analyze_with_textblob(text)
                
        except Exception as e:
            logger.error(f"Erro ao analisar sentimento: {e}")
            return {"polarity": 0, "subjectivity": 0, "sentiment": "neutral", "confidence": 0}
    
    def _analyze_with_textblob(self, text):
        """Analisa sentimento usando TextBlob"""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Determinar sentimento
        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        # Calcular confiança
        confidence = abs(polarity) if sentiment != "neutral" else 0
        
        return {
            "polarity": polarity,
            "subjectivity": subjectivity,
            "sentiment": sentiment,
            "confidence": confidence
        }
    
    def _analyze_with_vader(self, text):
        """An
(Content truncated due to size limit. Use line ranges to read in chunks)