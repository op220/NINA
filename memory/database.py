"""
Módulo de banco de dados para o sistema de memória de longo prazo da Nina IA.
Implementa a estrutura do banco de dados SQLite e funções para manipulação dos dados.
"""

import os
import json
import sqlite3
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("memory_database.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("MemoryDatabase")

class MemoryDatabase:
    """
    Classe para gerenciar o banco de dados do sistema de memória de longo prazo.
    """
    
    def __init__(self, db_path: str = "memory.db", json_dir: str = "memory_data"):
        """
        Inicializa o banco de dados.
        
        Args:
            db_path: Caminho para o arquivo do banco de dados SQLite
            json_dir: Diretório para armazenar os arquivos JSON
        """
        self.db_path = db_path
        self.json_dir = json_dir
        
        # Criar diretório para arquivos JSON se não existir
        os.makedirs(self.json_dir, exist_ok=True)
        
        # Inicializar banco de dados
        self._init_database()
        
        logger.info(f"Banco de dados inicializado: {db_path}")
    
    def _init_database(self) -> None:
        """
        Inicializa a estrutura do banco de dados.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Criar tabelas
            cursor.executescript("""
                -- Tabela de Usuários
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    username TEXT,
                    first_seen TIMESTAMP,
                    last_seen TIMESTAMP,
                    interaction_count INTEGER DEFAULT 0,
                    voice_participation_count INTEGER DEFAULT 0,
                    metadata_path TEXT  -- Caminho para o arquivo JSON com dados adicionais
                );

                -- Tabela de Canais
                CREATE TABLE IF NOT EXISTS channels (
                    channel_id TEXT PRIMARY KEY,
                    guild_id TEXT,
                    channel_name TEXT,
                    channel_type TEXT,
                    first_activity TIMESTAMP,
                    last_activity TIMESTAMP,
                    message_count INTEGER DEFAULT 0,
                    metadata_path TEXT,  -- Caminho para o arquivo JSON com dados adicionais
                    FOREIGN KEY (guild_id) REFERENCES guilds(guild_id)
                );

                -- Tabela de Servidores (Guilds)
                CREATE TABLE IF NOT EXISTS guilds (
                    guild_id TEXT PRIMARY KEY,
                    guild_name TEXT,
                    first_activity TIMESTAMP,
                    last_activity TIMESTAMP,
                    metadata_path TEXT  -- Caminho para o arquivo JSON com dados adicionais
                );

                -- Tabela de Interações
                CREATE TABLE IF NOT EXISTS interactions (
                    interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    channel_id TEXT,
                    timestamp TIMESTAMP,
                    interaction_type TEXT,
                    content_summary TEXT,
                    sentiment_score REAL,
                    topics TEXT,  -- Tópicos separados por vírgula ou JSON serializado
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (channel_id) REFERENCES channels(channel_id)
                );

                -- Tabela de Relações Usuário-Canal
                CREATE TABLE IF NOT EXISTS user_channel_stats (
                    user_id TEXT,
                    channel_id TEXT,
                    message_count INTEGER DEFAULT 0,
                    last_interaction TIMESTAMP,
                    participation_score REAL DEFAULT 0.0,
                    PRIMARY KEY (user_id, channel_id),
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (channel_id) REFERENCES channels(channel_id)
                );

                -- Tabela de Palavras Frequentes por Usuário
                CREATE TABLE IF NOT EXISTS user_frequent_words (
                    user_id TEXT,
                    word TEXT,
                    count INTEGER DEFAULT 0,
                    last_used TIMESTAMP,
                    PRIMARY KEY (user_id, word),
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                );

                -- Tabela de Tópicos por Usuário
                CREATE TABLE IF NOT EXISTS user_topics (
                    user_id TEXT,
                    topic TEXT,
                    relevance_score REAL DEFAULT 0.0,
                    last_discussed TIMESTAMP,
                    PRIMARY KEY (user_id, topic),
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                );

                -- Tabela de Tópicos por Canal
                CREATE TABLE IF NOT EXISTS channel_topics (
                    channel_id TEXT,
                    topic TEXT,
                    relevance_score REAL DEFAULT 0.0,
                    last_discussed TIMESTAMP,
                    PRIMARY KEY (channel_id, topic),
                    FOREIGN KEY (channel_id) REFERENCES channels(channel_id)
                );
                
                -- Criar índices para melhorar desempenho
                CREATE INDEX IF NOT EXISTS idx_interactions_user_id ON interactions(user_id);
                CREATE INDEX IF NOT EXISTS idx_interactions_channel_id ON interactions(channel_id);
                CREATE INDEX IF NOT EXISTS idx_interactions_timestamp ON interactions(timestamp);
                CREATE INDEX IF NOT EXISTS idx_user_topics_topic ON user_topics(topic);
                CREATE INDEX IF NOT EXISTS idx_channel_topics_topic ON channel_topics(topic);
            """)
            
            conn.commit()
            conn.close()
            
            logger.info("Estrutura do banco de dados criada com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar banco de dados: {e}")
            raise
    
    def _get_connection(self) -> sqlite3.Connection:
        """
        Obtém uma conexão com o banco de dados.
        
        Returns:
            Conexão com o banco de dados
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Para acessar colunas pelo nome
            return conn
        except Exception as e:
            logger.error(f"Erro ao conectar ao banco de dados: {e}")
            raise
    
    def _save_json(self, data: Dict[str, Any], filename: str) -> str:
        """
        Salva dados em um arquivo JSON.
        
        Args:
            data: Dados a serem salvos
            filename: Nome do arquivo
            
        Returns:
            Caminho completo para o arquivo JSON
        """
        try:
            filepath = os.path.join(self.json_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return filepath
        except Exception as e:
            logger.error(f"Erro ao salvar arquivo JSON {filename}: {e}")
            raise
    
    def _load_json(self, filepath: str) -> Dict[str, Any]:
        """
        Carrega dados de um arquivo JSON.
        
        Args:
            filepath: Caminho para o arquivo JSON
            
        Returns:
            Dados carregados do arquivo
        """
        try:
            if not os.path.exists(filepath):
                logger.warning(f"Arquivo JSON não encontrado: {filepath}")
                return {}
            
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erro ao carregar arquivo JSON {filepath}: {e}")
            return {}
    
    def add_or_update_user(self, user_id: str, username: str) -> bool:
        """
        Adiciona ou atualiza um usuário no banco de dados.
        
        Args:
            user_id: ID do usuário
            username: Nome do usuário
            
        Returns:
            True se a operação foi bem-sucedida, False caso contrário
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Verificar se o usuário já existe
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            user = cursor.fetchone()
            
            current_time = datetime.now().isoformat()
            
            if user:
                # Atualizar usuário existente
                cursor.execute("""
                    UPDATE users 
                    SET username = ?, last_seen = ?
                    WHERE user_id = ?
                """, (username, current_time, user_id))
            else:
                # Criar novo usuário
                metadata_path = self._create_user_metadata(user_id, username)
                
                cursor.execute("""
                    INSERT INTO users 
                    (user_id, username, first_seen, last_seen, interaction_count, voice_participation_count, metadata_path)
                    VALUES (?, ?, ?, ?, 0, 0, ?)
                """, (user_id, username, current_time, current_time, metadata_path))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Usuário {username} ({user_id}) {'atualizado' if user else 'adicionado'}")
            return True
        except Exception as e:
            logger.error(f"Erro ao adicionar/atualizar usuário {user_id}: {e}")
            return False
    
    def _create_user_metadata(self, user_id: str, username: str) -> str:
        """
        Cria o arquivo de metadados para um novo usuário.
        
        Args:
            user_id: ID do usuário
            username: Nome do usuário
            
        Returns:
            Caminho para o arquivo de metadados
        """
        current_time = datetime.now().isoformat()
        
        metadata = {
            "user_id": user_id,
            "username": username,
            "frequent_expressions": [],
            "emotions": {
                "predominant": "neutro",
                "distribution": {
                    "feliz": 0.0,
                    "neutro": 1.0,
                    "bravo": 0.0,
                    "triste": 0.0
                },
                "last_updated": current_time
            },
            "topics": [],
            "voice_activity": {
                "total_time": 0,
                "average_session": 0,
                "last_session": None,
                "preferred_channels": []
            },
            "interaction_patterns": {
                "active_hours": [],
                "active_days": [],
                "response_rate": 0.0,
                "average_message_length": 0
            }
        }
        
        filename = f"user_{user_id}.json"
        filepath = self._save_json(metadata, filename)
        
        return filepath
    
    def add_or_update_channel(self, channel_id: str, guild_id: str, channel_name: str, channel_type: str) -> bool:
        """
        Adiciona ou atualiza um canal no banco de dados.
        
        Args:
            channel_id: ID do canal
            guild_id: ID do servidor
            channel_name: Nome do canal
            channel_type: Tipo do canal
            
        Returns:
            True se a operação foi bem-sucedida, False caso contrário
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Verificar se o canal já existe
            cursor.execute("SELECT * FROM channels WHERE channel_id = ?", (channel_id,))
            channel = cursor.fetchone()
            
            current_time = datetime.now().isoformat()
            
            if channel:
                # Atualizar canal existente
                cursor.execute("""
                    UPDATE channels 
                    SET channel_name = ?, channel_type = ?, last_activity = ?
                    WHERE channel_id = ?
                """, (channel_name, channel_type, current_time, channel_id))
            else:
                # Verificar se o servidor existe, se não, criar
                cursor.execute("SELECT * FROM guilds WHERE guild_id = ?", (guild_id,))
                guild = cursor.fetchone()
                
                if not guild:
                    cursor.execute("""
                        INSERT INTO guilds 
                        (guild_id, guild_name, first_activity, last_activity, metadata_path)
                        VALUES (?, ?, ?, ?, ?)
                    """, (guild_id, "Unknown Guild", current_time, current_time, ""))
                
                # Criar novo canal
                metadata_path = self._create_channel_metadata(channel_id, guild_id, channel_name)
                
                cursor.execute("""
                    INSERT INTO channels 
                    (channel_id, guild_id, channel_name, channel_type, first_activity, last_activity, message_count, metadata_path)
                    VALUES (?, ?, ?, ?, ?, ?, 0, ?)
                """, (channel_id, guild_id, channel_name, channel_type, current_time, current_time, metadata_path))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Canal {channel_name} ({channel_id}) {'atualizado' if channel else 'adicionado'}")
            return True
        except Exception as e:
            logger.error(f"Erro ao adicionar/atualizar canal {channel_id}: {e}")
            return False
    
    def _create_channel_metadata(self, channel_id: str, guild_id: str, channel_name: str) -> str:
        """
        Cria o arquivo de metadados para um novo canal.
        
        Args:
            channel_id: ID do canal
            guild_id: ID do servidor
            channel_name: Nome do canal
            
        Returns:
            Caminho para o arquivo de metadados
        """
        current_time = datetime.now().isoformat()
        
        metadata = {
            "channel_id": channel_id,
            "guild_id": guild_id,
            "name": channel_name,
            "tone": {
                "predominant": "neutro",
                "distribution": {
                    "informal": 0.33,
                    "neutro": 0.34,
                    "formal": 0.33
                },
                "last_updated": current_time
            },
            "recurring_themes": [],
            "activity_patterns": {
                "peak_hours": [],
                "peak_days": [],
                "messages_per_day": 0,
                "average_participants": 0
            },
            "nina_personality": {
                "formality_level": 50,
                "humor_level": 50,
                "technicality_level": 50,
                "response_speed": "médio",
                "verbosity": "médio",
                "last_updated": current_time
            },
            "active_users": []
        }
        
        filename = f"channel_{channel_id}.json"
        filepath = self._save_json(metadata, filename)
        
        return filepath
    
    def add_interaction(self, user_id: str, channel_id: str, interaction_type: str, 
                       content_summary: str, sentiment_score: float, topics: List[str]) -> int:
        """
        Adiciona uma nova interação ao banco de dados.
        
        Args:
            user_id: ID do usuário
            channel_id: ID do canal

(Content truncated due to size limit. Use line ranges to read in chunks)