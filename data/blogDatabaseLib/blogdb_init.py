import logging
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Tuple, Union, Literal, Dict, Any
import sqlite3

@dataclass
class Blog:
    id: int = 0
    name: str = ""
    hash: str = ""
    category: str = ""
    create_time: str = ""
    summary: str = ""
    tags: list[str] = None
    content: str = ""
    
    @classmethod
    def new(
        self,
        *,
        id: int = 0,
        name: str,
        hash: str,
        category: str,
        summary: str,
        content: str,
        create_time: Optional[str] = None,
        tags: list[str] = None,
    ) -> "Blog":
        return self(
            id=id,
            name=name,
            hash=hash,
            category=category,
            create_time=create_time,
            summary=summary,
            tags=tags,
            content=content,
        )


logger = logging.getLogger(__name__)
def logger_init(log_level: str, log_path: Union[str, Path]) -> None:
    # convert the path to Path object
    log_path = Path(log_path)
    # check if the path exists
    if not log_path.parent.exists():
        raise FileNotFoundError(f"log path not exists: {log_path.parent}")

    logging.basicConfig(
        # the level order is DEBUG < INFO < WARNING < ERROR < CRITICAL
        level=log_level,
        format="[%(asctime)s][%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True, # Ensure this config overrides any existing default logging config
        handlers=[
            # print log to console
            logging.StreamHandler(),
            logging.FileHandler(log_path, mode="a", encoding="utf-8"),
        ]
    )
    logger.info(f"log init success: {log_path}")


def blogdb_init(db_path: Union[str, Path]) -> None:
    # convert the path to Path object
    db_path = Path(db_path)
    # check if the path exists
    if not db_path.parent.exists():
        logger.error(f"blog db path not exists: {db_path.parent}")
        raise FileNotFoundError(f"blog db path not exists: {db_path.parent}")

    if db_path.exists():
        logger.warning(f"blog db file already exists: {db_path}")
        return

    # connect to the database
    conn = sqlite3.connect(db_path)
    # basic database settings
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")

    # blog database settings
    # the AUTOINCREMENT keyword ensures that the id column is always unique and increases by 1
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS blog_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            hash TEXT NOT NULL,
            category TEXT NOT NULL,
            create_time TEXT NOT NULL,
            summary TEXT NOT NULL,
            tags TEXT NOT NULL,
            content TEXT NOT NULL
        );
        """
    )

    # tag database settings (Many-to-Many mapping table)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS blog_tags (
            blog_name TEXT NOT NULL,
            tag_name TEXT NOT NULL,
            PRIMARY KEY (blog_name, tag_name),
            FOREIGN KEY (blog_name) REFERENCES blog_list(name) ON DELETE CASCADE
        );
        """
    )
    # create index for faster reverse lookup (tag -> blogs) 
    conn.execute("CREATE INDEX IF NOT EXISTS idx_tag_name ON blog_tags(tag_name);")

    try:
        conn.commit()
        logger.info(f"blog db init success: {db_path}")

    except sqlite3.Error as e:
        logger.error(f"blog db init failed: {e}", exc_info=True)
        conn.rollback()
        raise e
    finally:
        conn.close()