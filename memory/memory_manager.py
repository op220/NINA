# memory_manager.py
# Módulo corrigido para gerenciar memória da Nina IA

import os
import json
import logging
import sqlite3
from typing import Dict, List, Any, Optional
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self, memory_dir: str = None):
        self.memory_dir = memory_dir or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data", "memory"
        )
        os.makedirs(self.memory_dir, exist_ok=True)
        self.db_path = os.path.join(self.memory_dir, "memory.db")
        self._init_database()
        logger.info(f"Gerenciador de memória inicializado: {self.db_path}")

    def _init_database(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS knowledge (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    fact TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    source TEXT,
                    confidence REAL,
                    metadata TEXT
                )
            ''')
            conn.commit()
        except Exception as e:
            logger.error(f"Erro ao inicializar banco de dados: {e}")
        finally:
            conn.close()

    def add_knowledge(self, topic: str, fact: str,
                      source: Optional[str] = None,
                      confidence: Optional[float] = 1.0,
                      metadata: Optional[Dict[str, Any]] = None) -> int:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            timestamp = datetime.now().isoformat()
            metadata_json = json.dumps(metadata) if metadata else None
            cursor.execute(
                "INSERT INTO knowledge (topic, fact, timestamp, source, confidence, metadata) VALUES (?, ?, ?, ?, ?, ?)",
                (topic, fact, timestamp, source, confidence, metadata_json)
            )
            knowledge_id = cursor.lastrowid
            conn.commit()
            return knowledge_id
        except Exception as e:
            logger.error(f"Erro ao adicionar conhecimento: {e}")
            return -1
        finally:
            conn.close()

    def get_knowledge_by_topic(self, topic: str) -> List[Dict[str, Any]]:
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM knowledge WHERE topic = ? ORDER BY confidence DESC",
                (topic,)
            )
            rows = cursor.fetchall()
            knowledge_list = []
            for row in rows:
                knowledge = dict(row)
                if knowledge["metadata"]:
                    knowledge["metadata"] = json.loads(knowledge["metadata"])
                knowledge_list.append(knowledge)
            return knowledge_list
        except sqlite3.Error as e:
            logger.error(f"Erro ao pesquisar conhecimento (SQLite): {e}")
            return []
        except Exception as e:
            logger.error(f"Erro inesperado ao pesquisar conhecimento: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    def search_knowledge(self, query: str) -> List[Dict[str, Any]]:
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            search_term = f"%{query}%"
            cursor.execute(
                "SELECT * FROM knowledge WHERE topic LIKE ? OR fact LIKE ? ORDER BY confidence DESC",
                (search_term, search_term)
            )
            rows = cursor.fetchall()
            knowledge_list = []
            for row in rows:
                knowledge = dict(row)
                if knowledge["metadata"]:
                    knowledge["metadata"] = json.loads(knowledge["metadata"])
                knowledge_list.append(knowledge)
            return knowledge_list
        except Exception as e:
            logger.error(f"Erro ao pesquisar conhecimentos: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    def generate_session_id(self) -> str:
        """Gera um ID único de sessão com timestamp."""
        return datetime.now().strftime("%Y%m%d%H%M%S%f")

    def store_user_info(self, key: str, data: dict):
        """
        Armazena dados do usuário ou da sessão em arquivo JSON.
        """
        try:
            path = os.path.join(self.memory_dir, f"{key}.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Dados armazenados com sucesso: {path}")
        except Exception as e:
            logger.error(f"Erro ao armazenar dados do usuário: {e}")
