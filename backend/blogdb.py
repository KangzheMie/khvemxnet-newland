import logging
import sqlite3
import hashlib
import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Tuple, Union, Literal, Dict, Any
import json
import sys

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

def load_settings(config_file: Path = None) -> Dict[str, Any]:
    if config_file is None:
        config_file = Path(__file__).parent / "config.json"
    config_data = {}
    
    if not config_file.exists():
        print(f"[Error] Configuration file not found: {config_file}", file=sys.stderr)
        raise FileNotFoundError(f"Configuration file not found: {config_file}")
        
    with config_file.open("r", encoding="utf-8") as f:
        try:
            config_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"[Error] Invalid JSON in config file: {e}", file=sys.stderr)
            raise ValueError(f"Invalid JSON in config file: {e}")
            
    # resolve is used to convert relative relative paths to absolute paths
    log_path = (config_file.parent / config_data.get("log_path")).resolve()
    blog_path = (config_file.parent / config_data.get("blog_path")).resolve()
    db_path = (config_file.parent / config_data.get("db_path")).resolve()
    backend_host = config_data.get("backend_host")
    backend_port = int(config_data.get("backend_port"))
    
    return {"log_path": log_path, "blog_path": str(blog_path), "db_path": str(db_path), "backend_host": backend_host, "backend_port": backend_port}


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


def file_hash(blog_Path: Union[str, Path],
              algo: str = "sha256",
              chunk_size: int = 1024 * 1024,
    ) -> str:
    # convert the path to Path object
    blog_Path = Path(blog_Path)
    if not blog_Path.is_file():
        raise FileNotFoundError(f"Not a file: {blog_Path}")

    h = hashlib.new(algo)
    with blog_Path.open("rb") as f:
        # read the file in binary mode and update by chunk
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def blog_reader(blog_path: Union[str, Path]) -> "Blog":
    # convert the path to Path object
    blog_path = Path(blog_path)
    if not blog_path.is_file():
        logger.error(f"Not a file: {blog_path}")
        raise FileNotFoundError(f"Not a file: {blog_path}")

    with blog_path.open("r", encoding="utf-8") as f:
        content = f.read()

    if content.startswith('---'):
        parts = content.split('---', 2)
        yaml_dict = yaml.safe_load(parts[1].strip()) or {}
        markdown_text = parts[2].strip()
        return Blog.new(
            name=str(blog_path.stem), # filename without extension
            hash=file_hash(blog_path),
            category=yaml_dict.get("category", ""),
            summary=yaml_dict.get("summary", ""),
            content=markdown_text,
            create_time=yaml_dict.get("create_time", ""),
            tags=yaml_dict.get("tags", None) or [],
        )


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


def blog_sync(
    blog_dir: Union[str, Path],
    *,
    db_path: Union[str, Path],
    ) -> None:

    blog_dir = Path(blog_dir)
    db_path = Path(db_path)
    # check if the path exists
    if not blog_dir.exists():
        logger.error(f"blog dir not exists: {blog_dir}")
        raise FileNotFoundError(f"blog dir not exists: {blog_dir}")

    for file in blog_dir.rglob('*.md'): 
        a_blog = blog_reader(file)
        blog_list_insert(a_blog, db_path=db_path)
        blog_tags_update(a_blog, db_path=db_path)

# ==========================================
# Blog List Database Operations
# ==========================================

def blog_list_insert(
    blog: Blog,
    *,  # parameters after this must be passed by keyword, like db_path=xxx
    db_path: Union[str, Path],
    ) -> Tuple[Literal["inserted", "updated", "error"], str]:

    db_path = Path(db_path)
    # excluded is the values in the ON CONFLICT clause
    sql = (
        "INSERT INTO blog_list (name, hash, category, create_time, summary, tags, content) "
        "VALUES (?, ?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(name) DO UPDATE SET hash = excluded.hash, category = excluded.category, "
        "create_time = excluded.create_time, summary = excluded.summary, "
        "tags = excluded.tags, content = excluded.content"
    )
    conn = sqlite3.connect(db_path)

    try:
        logger.debug(f"try to insert blog list: name={blog.name}, hash={blog.hash}")
        cur = conn.execute(sql, (blog.name, blog.hash, blog.category, blog.create_time, blog.summary, str(blog.tags), blog.content))
        conn.commit()

        # if data is inserted, lastrowid is the id of the inserted row
        if cur.lastrowid > 0:
            logger.info(f"insert blog list success: name={blog.name}, id={cur.lastrowid}")
            return "inserted", f"{blog.name} id= {cur.lastrowid}"
        else:
            logger.debug(f"update blog list success: name={blog.name}")
            return "updated", f"{blog.name}"

    except sqlite3.Error as e:
        logger.error(f"insert blog list failed: name={blog.name}, error={e}", exc_info=True)
        conn.rollback()
        return "error", str(e)
    finally:
        conn.close()


def blog_list_sync(
    blog_dir: Union[str, Path],
    *,
    db_path: Union[str, Path],
    ) -> None:

    blog_dir = Path(blog_dir)
    db_path = Path(db_path)
    # check if the path exists
    if not blog_dir.exists():
        logger.error(f"blog dir not exists: {blog_dir}")
        raise FileNotFoundError(f"blog dir not exists: {blog_dir}")

    for file in blog_dir.glob('*.md'):
        a_blog = blog_reader(file)
        blog_list_insert(a_blog, db_path=db_path)


def blog_list_get_by_name(
    blog_name: str,
    *,
    db_path: Union[str, Path],
    ) -> Optional[Blog]:

    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)

    try:
        logger.debug(f"try to get blog list by name: name={blog_name}")
        sql = "SELECT id, hash, category, create_time, summary, tags, content FROM blog_list WHERE name = ?"
        result = conn.execute(sql, (blog_name,)).fetchone()

        if result is not None:
            logger.debug(f"get blog list success: name={blog_name}")
            return Blog(
                id=result[0],
                name=blog_name,
                hash=result[1],
                category=result[2],
                create_time=result[3],
                summary=result[4],
                tags=result[5],
                content=result[6],
            )
        else:
            logger.warning(f"get blog list failed: name={blog_name}")
            return None

    except sqlite3.Error as e:
        logger.error(f"get blog list failed: name={blog_name}, error={e}", exc_info=True)
        return None
    finally:
        conn.close()


def blog_list_get_by_id(
    blog_id: int,
    *,
    db_path: Union[str, Path],
    ) -> Optional[Blog]:

    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)

    try:
        logger.debug(f"try to get blog list by id: id={blog_id}")
        sql = "SELECT name, hash, category, create_time, summary, tags, content FROM blog_list WHERE id = ?"
        result = conn.execute(sql, (blog_id,)).fetchone()

        if result is not None:
            logger.debug(f"get blog list success: id={blog_id}")
            return Blog(
                id=blog_id,
                name=result[0],
                hash=result[1],
                category=result[2],
                create_time=result[3],
                summary=result[4],
                tags=result[5],
                content=result[6],
            )
        else:
            logger.warning(f"get blog list failed: id={blog_id}")
            return None

    except sqlite3.Error as e:
        logger.error(f"get blog list failed: id={blog_id}, error={e}", exc_info=True)
        return None
    finally:
        conn.close()


def blog_list_get_by_category(
    category: str,
    *,
    db_path: Union[str, Path],
    ) -> Optional[list]:

    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)

    try:
        logger.debug(f"try to get blog list by category: category={category}")
        sql = "SELECT id, name FROM blog_list WHERE category = ? ORDER BY create_time DESC"
        result = conn.execute(sql, (category,)).fetchall()

        if result is not None:
            logger.debug(f"get blog list by category success: category={category}")
            return [{"id": row[0], "name": row[1]} for row in result]
        else:
            logger.warning(f"get blog list by category failed: category={category}")
            return None
    except sqlite3.Error as e:
        logger.error(f"get blog list by category failed: category={category}, error={e}", exc_info=True)
        return None
    finally:
        conn.close()


def blog_list_get_all_names(
    *,
    db_path: Union[str, Path],
    ) -> Optional[list]:

    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)

    try:
        logger.debug(f"try to get all blog list names")
        sql = "SELECT id, name FROM blog_list"
        result = conn.execute(sql).fetchall()

        if result is not None:
            logger.debug(f"get all blog list names success")
            return [{"id": row[0], "name": row[1]} for row in result]
        else:
            logger.warning(f"get all blog list names failed")
            return None

    except sqlite3.Error as e:
        logger.error(f"get all blog list names failed: error={e}", exc_info=True)
        return None
    finally:
        conn.close()


def blog_list_del_by_name(
    blog_name: str,
    *,
    db_path: Union[str, Path],
    ) -> Tuple[Literal["deleted", "error"], str]:

    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)

    try:
        logger.warning(f"try to delete blog list by name: name={blog_name}")
        sql = "DELETE FROM blog_list WHERE name = ?"
        cur = conn.execute(sql, (blog_name,))
        conn.commit()

        if cur.rowcount > 0:
            logger.info(f"delete blog list success: name={blog_name}")
            return "deleted", f"{blog_name}"
        else:
            logger.warning(f"delete blog list failed: name={blog_name}")
            return "error", f"blog name not found: {blog_name}"

    except sqlite3.Error as e:
        logger.error(f"delete blog list failed: name={blog_name}, error={e}", exc_info=True)
        conn.rollback()
        return "error", str(e)
    finally:
        conn.close()


def blog_list_del_all(
    *,
    db_path: Union[str, Path],
    ) -> Tuple[Literal["deleted", "error"], str]:

    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)

    try:
        logger.warning(f"try to delete all blog list")
        sql = "DELETE FROM blog_list"
        cur = conn.execute(sql)
        conn.commit()

        if cur.rowcount > 0:
            logger.info(f"delete all blog list success, deleted {cur.rowcount} rows")
            return "deleted", f"deleted {cur.rowcount} rows"
        else:
            logger.warning(f"delete all blog list failed, no rows deleted")
            return "error", f"no rows deleted"

    except sqlite3.Error as e:
        logger.error(f"delete all blog list failed: error={e}", exc_info=True)
        conn.rollback()
        return "error", str(e)
    finally:
        conn.close()


def blog_list_check_ghost(
    blog_dir: Union[str, Path],
    *,
    db_path: Union[str, Path],
    ) -> Tuple[Literal["checked", 'warning', "error"], set]:

    blog_dir = Path(blog_dir)
    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)

    try:
        logger.debug(f"try to check ghost blog list")
        blog_set = set()
        for file in blog_dir.glob('*.md'):
            blog_set.add(file.stem)
        database_set = set(blog_list_get_all_names(db_path=db_path))
        ghost_set = database_set - blog_set or None

        if ghost_set is not None:
            logger.info(f"have ghost blog list: {ghost_set}")
            return "warning", ghost_set
        else:
            logger.info(f"have no ghost blog list")
            return "checked", set()

    except sqlite3.Error as e:
        logger.error(f"check ghost blog list failed: error={e}", exc_info=True)
        return "error", set()
    finally:
        conn.close()


def blog_list_check_outsync(
    blog_dir: Union[str, Path],
    *,
    db_path: Union[str, Path],
    ) -> Tuple[Literal["checked", "warning", "error"], set]:

    blog_dir = Path(blog_dir)
    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)

    try:
        logger.debug(f"try to check out of sync blog list")
        blog_set = set()
        for file in blog_dir.glob('*.md'):
            blog_set.add(file.stem)
        database_set = set(blog_list_get_all_names(db_path=db_path))
        outsync_set = blog_set - database_set or None

        if outsync_set is not None:
            logger.info(f"have out of sync blog list: {outsync_set}")
            return "warning", outsync_set
        else:
            logger.info(f"have no out of sync blog list")
            return "checked", set()

    except sqlite3.Error as e:
        logger.error(f"check out of sync blog list failed: error={e}", exc_info=True)
        return "error", set()
    finally:
        conn.close()


def blog_list_check(
    blog_dir: Union[str, Path],
    *,
    db_path: Union[str, Path],
    ) -> Tuple[Literal["checked", "warning", "error"], set]:

    blog_dir = Path(blog_dir)
    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)

    try:
        logger.debug(f"try to check blog list")
        ghost_set = blog_list_check_ghost(blog_dir=blog_dir, db_path=db_path)
        outsync_set = blog_list_check_outsync(blog_dir=blog_dir, db_path=db_path)

        if ghost_set[0] == "checked" and outsync_set[0] == "checked":
            logger.info(f"have no ghost blog list and out of sync blog list")
            return "checked", set()
        else:
            logger.info(f"have ghost blog list: {ghost_set[1]} \n out of sync blog list: {outsync_set[1]}")
            return "warning", ghost_set[1] | outsync_set[1]

    except sqlite3.Error as e:
        logger.error(f"check blog list failed: error={e}", exc_info=True)
        return "error", set()
    finally:
        conn.close()


# ==========================================
# Tags Database Operations
# ==========================================

def blog_tags_update(
    blog: Blog,
    *,
    db_path: Union[str, Path],
    ) -> Tuple[Literal["updated", "error"], str]:

    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)
    
    try:
        # transaction make sure the update success or fail at the same time
        conn.execute("BEGIN TRANSACTION;")
        # delete all tags of the blog then reflesh the tags
        conn.execute("DELETE FROM blog_tags WHERE blog_name = ?", (blog.name,))
        
        if blog.tags:
            logger.debug(f"update blog tags: blog_name={blog.name}, tags={blog.tags}")
            insert_data = [(blog.name, tag) for tag in blog.tags]
            conn.executemany("INSERT INTO blog_tags (blog_name, tag_name) VALUES (?, ?)", insert_data)
        else:
            logger.debug(f"blog {blog.name} have no tags")
        conn.commit()
        logger.debug(f"update blog tags success: blog_name={blog.name}, tags={blog.tags}")
        return "updated", f"Tags updated for blog {blog.name}"    

    except sqlite3.Error as e:
        conn.rollback()
        logger.error(f"update blog tags failed: blog_name={blog.name}, error={e}", exc_info=True)
        return "error", str(e)
    finally:
        conn.close()


def blog_tags_sync(
    blog_dir: Union[str, Path],
    *,
    db_path: Union[str, Path],
    ) -> None:

    blog_dir = Path(blog_dir)
    db_path = Path(db_path)
    # check if the path exists
    if not blog_dir.exists():
        logger.error(f"blog dir not exists: {blog_dir}")
        raise FileNotFoundError(f"blog dir not exists: {blog_dir}")

    for file in blog_dir.glob(pattern='*.md'):
        a_blog = blog_reader(file)
        blog_tags_update(a_blog, db_path=db_path)


def blog_tags_get_by_name(
    blog_name: str,
    *,
    db_path: Union[str, Path],
    ) -> list[str]:

    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)
    
    try:
        sql = "SELECT tag_name FROM blog_tags WHERE blog_name = ?"
        result = conn.execute(sql, (blog_name,)).fetchall()
        return [row[0] for row in result]

    except sqlite3.Error as e:
        logger.error(f"get blog tags failed: blog_name={blog_name}, error={e}", exc_info=True)
        return []
    finally:
        conn.close()

def blog_name_get_by_tag(
    tag_name: str,
    *,
    db_path: Union[str, Path],
    ) -> list[str]:

    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)
    
    try:
        sql = "SELECT blog_name FROM blog_tags WHERE tag_name = ?"
        result = conn.execute(sql, (tag_name,)).fetchall()
        return [row[0] for row in result]

    except sqlite3.Error as e:
        logger.error(f"get blog names failed: tag_name={tag_name}, error={e}", exc_info=True)
        return []
    finally:
        conn.close()


def blog_tags_get_by_id(
    blog_id: int,
    *,
    db_path: Union[str, Path],
    ) -> list[str]:

    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)

    try:
        sql = "SELECT tag_name FROM blog_tags WHERE blog_name = (SELECT name FROM blog_list WHERE id = ?)"
        result = conn.execute(sql, (blog_id,)).fetchall()
        return [row[0] for row in result]

    except sqlite3.Error as e:
        logger.error(f"get blog tags failed: blog_id={blog_id}, error={e}", exc_info=True)
        return []
    finally:
        conn.close()


def blog_tags_get_all(
    *,
    db_path: Union[str, Path],
    ) -> list[str]:
    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)
    
    try:
        sql = "SELECT DISTINCT tag_name, COUNT(*) FROM blog_tags GROUP BY tag_name ORDER BY COUNT(*) DESC"
        result = conn.execute(sql).fetchall()
        return [{"tag_name": row[0], "count": row[1]} for row in result]

    except sqlite3.Error as e:
        logger.error(f"get all tags failed: error={e}", exc_info=True)
        return []
    finally:
        conn.close()