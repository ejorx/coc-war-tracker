import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "wars.db")


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS war_participation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_tag TEXT NOT NULL,
                player_name TEXT NOT NULL,
                stars INTEGER DEFAULT 0,
                attacks INTEGER DEFAULT 0,
                war_end_time TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_player_tag ON war_participation(player_tag)
        """)
        self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_war_end_time ON war_participation(war_end_time)
        """)
        self.conn.commit()

    def war_already_registered(self, war_end_time: str) -> bool:
        row = self.conn.execute(
            "SELECT 1 FROM war_participation WHERE war_end_time = ? LIMIT 1",
            (war_end_time,)
        ).fetchone()
        return row is not None

    def upsert_participation(self, player_tag: str, player_name: str, stars: int, attacks: int, war_end_time: str):
        existing = self.conn.execute(
            "SELECT id FROM war_participation WHERE player_tag = ? AND war_end_time = ?",
            (player_tag, war_end_time)
        ).fetchone()
        if existing:
            self.conn.execute(
                """UPDATE war_participation SET player_name = ?, stars = ?, attacks = ?
                   WHERE player_tag = ? AND war_end_time = ?""",
                (player_name, stars, attacks, player_tag, war_end_time)
            )
        else:
            self.conn.execute(
                """INSERT INTO war_participation (player_tag, player_name, stars, attacks, war_end_time)
                   VALUES (?, ?, ?, ?, ?)""",
                (player_tag, player_name, stars, attacks, war_end_time)
            )
        self.conn.commit()

    def get_player_stats(self):
        rows = self.conn.execute("""
            SELECT
                player_name,
                player_tag,
                COUNT(*) as wars_played,
                SUM(stars) as total_stars,
                SUM(attacks) as total_attacks,
                ROUND(AVG(stars * 1.0), 2) as avg_stars
            FROM war_participation
            GROUP BY player_tag
            ORDER BY avg_stars DESC
        """).fetchall()
        return [dict(row) for row in rows]

    def get_recent_wars(self, limit=10):
        rows = self.conn.execute("""
            SELECT DISTINCT war_end_time
            FROM war_participation
            ORDER BY war_end_time DESC
            LIMIT ?
        """, (limit,)).fetchall()
        return [row["war_end_time"] for row in rows]

    def purge_old_records(self, max_age_days=90, max_rows=1000):
        self.conn.execute(
            "DELETE FROM war_participation WHERE created_at < datetime('now', ?)",
            (f'-{max_age_days} days',)
        )
        self.conn.execute("""
            DELETE FROM war_participation WHERE id NOT IN (
                SELECT id FROM war_participation ORDER BY created_at DESC LIMIT ?
            )
        """, (max_rows,))
        self.conn.commit()

    def close(self):
        self.conn.close()
