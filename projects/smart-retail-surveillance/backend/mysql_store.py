"""MySQL persistence for Smart Retail detection events."""
from __future__ import annotations

import os
from pathlib import Path

import mysql.connector
from mysql.connector import pooling


class MySQLStore:
    def __init__(self) -> None:
        self.config = {
            "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
            "port": int(os.getenv("MYSQL_PORT", "3306")),
            "user": os.getenv("MYSQL_USER", "smart_retail"),
            "password": os.getenv("MYSQL_PASSWORD", "smart_retail"),
            "database": os.getenv("MYSQL_DATABASE", "smart_retail"),
        }
        self.pool = pooling.MySQLConnectionPool(
            pool_name="smart_retail_pool",
            pool_size=int(os.getenv("MYSQL_POOL_SIZE", "5")),
            **self.config,
        )

    def connection(self):
        return self.pool.get_connection()

    def initialize(self, schema_path: Path) -> None:
        connection = mysql.connector.connect(
            host=self.config["host"],
            port=self.config["port"],
            user=self.config["user"],
            password=self.config["password"],
        )
        try:
            cursor = connection.cursor()
            statements = [s.strip() for s in schema_path.read_text(encoding="utf-8").split(";") if s.strip()]
            for statement in statements:
                cursor.execute(statement)
            connection.commit()
        finally:
            connection.close()

    def insert_events(self, events: list[dict[str, str]]) -> int:
        if not events:
            return 0
        connection = self.connection()
        try:
            cursor = connection.cursor()
            sql = """INSERT INTO detection_events
                (event_timestamp, class_name, confidence, x1, y1, x2, y2)
                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            rows = []
            for event in events:
                rows.append((
                    event.get("timestamp"), event.get("class"), float(event.get("confidence", 0)),
                    event.get("x1") or None, event.get("y1") or None,
                    event.get("x2") or None, event.get("y2") or None,
                ))
            cursor.executemany(sql, rows)
            connection.commit()
            return cursor.rowcount
        finally:
            connection.close()

    def fetch_events(self, limit: int = 1000) -> list[dict[str, str]]:
        connection = self.connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""SELECT event_timestamp, class_name, confidence, x1, y1, x2, y2
                FROM detection_events ORDER BY id DESC LIMIT %s""", (limit,))
            rows = cursor.fetchall()
            return [{
                "timestamp": row["event_timestamp"].isoformat() if row["event_timestamp"] else None,
                "class": row["class_name"], "confidence": float(row["confidence"]),
                "x1": row["x1"], "y1": row["y1"], "x2": row["x2"], "y2": row["y2"],
            } for row in rows]
        finally:
            connection.close()

    def close(self) -> None:
        self.pool = None
