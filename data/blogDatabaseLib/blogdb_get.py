from .blogdb_init import *

import sqlite3
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Tuple, Union, Literal, Dict, Any

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