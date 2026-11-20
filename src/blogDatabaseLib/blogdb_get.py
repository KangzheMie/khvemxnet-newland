from .blogdb_init import *

import sqlite3
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Tuple, Union, Literal, Dict, Any

def _get_tags_by_blog_name(conn: sqlite3.Connection, blog_name: str) -> list[str]:
    result = conn.execute(
        "SELECT tag_name FROM BLOG_TAGS WHERE blog_name = ?", (blog_name,)
    ).fetchall()
    return [row[0] for row in result]

def get_blog_by_name(
    blog_name: str,
    *,
    db_path: Union[str, Path],
    ) -> Optional[Blog]:

    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)

    try:
        logger.debug(f"try to get blog list by name: name={blog_name}")
        sql = "SELECT blog_id, hash, category, create_time, summary, content FROM BLOG_LIST WHERE name = ?"
        result = conn.execute(sql, (blog_name,)).fetchone()

        if result is not None:
            logger.debug(f"get blog list success: name={blog_name}")
            return Blog(
                blog_id=result[0],
                name=blog_name,
                hash=result[1],
                category=result[2],
                create_time=result[3],
                summary=result[4],
                tags=_get_tags_by_blog_name(conn, blog_name),
                content=result[5],
            )
        else:
            logger.warning(f"get blog list failed: name={blog_name}")
            return None

    except sqlite3.Error as e:
        logger.error(f"get blog list failed: name={blog_name}, error={e}", exc_info=True)
        return None
    finally:
        conn.close()


def get_blog_by_id(
    blog_id: int,
    *,
    db_path: Union[str, Path],
    ) -> Optional[Blog]:

    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)

    try:
        logger.debug(f"try to get blog list by id: blog_id={blog_id}")
        sql = "SELECT name, hash, category, create_time, summary, content FROM BLOG_LIST WHERE blog_id = ?"
        result = conn.execute(sql, (blog_id,)).fetchone()

        if result is not None:
            logger.debug(f"get blog list success: blog_id={blog_id}")
            return Blog(
                blog_id=blog_id,
                name=result[0],
                hash=result[1],
                category=result[2],
                create_time=result[3],
                summary=result[4],
                tags=_get_tags_by_blog_name(conn, result[0]),
                content=result[5],
            )
        else:
            logger.warning(f"get blog list failed: blog_id={blog_id}")
            return None

    except sqlite3.Error as e:
        logger.error(f"get blog list failed: blog_id={blog_id}, error={e}", exc_info=True)
        return None
    finally:
        conn.close()


def get_blogs_by_category(
    category: str,
    *,
    db_path: Union[str, Path],
    ) -> Optional[list]:

    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)

    try:
        logger.debug(f"try to get blog list by category: category={category}")
        sql = "SELECT blog_id, name FROM BLOG_LIST WHERE category = ? ORDER BY create_time DESC"
        result = conn.execute(sql, (category,)).fetchall()

        if result is not None:
            logger.debug(f"get blog list by category success: category={category}")
            return [{"blog_id": row[0], "name": row[1]} for row in result]
        else:
            logger.warning(f"get blog list by category failed: category={category}")
            return None
    except sqlite3.Error as e:
        logger.error(f"get blog list by category failed: category={category}, error={e}", exc_info=True)
        return None
    finally:
        conn.close()


def get_all_blogs(
    *,
    db_path: Union[str, Path],
    ) -> Optional[list[Dict[str, Any]]]:

    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)

    try:
        logger.debug(f"try to get all blog list names")
        sql = "SELECT blog_id, name FROM BLOG_LIST"
        result = conn.execute(sql).fetchall()

        if result is not None:
            logger.debug(f"get all blog list names success")
            return [{"blog_id": row[0], "name": row[1]} for row in result]
        else:
            logger.warning(f"get all blog list names failed")
            return set[Any]()

    except sqlite3.Error as e:
        logger.error(f"get all blog list names failed: error={e}", exc_info=True)
        return set[Any]()
    finally:
        conn.close()

def get_tags_by_blog_name(
    blog_name: str,
    *,
    db_path: Union[str, Path],
    ) -> list[str]:

    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)
    
    try:
        sql = "SELECT tag_name FROM BLOG_TAGS WHERE blog_name = ?"
        result = conn.execute(sql, (blog_name,)).fetchall()
        return [row[0] for row in result]

    except sqlite3.Error as e:
        logger.error(f"get blog tags failed: blog_name={blog_name}, error={e}", exc_info=True)
        return []
    finally:
        conn.close()

def get_blog_names_by_tag(
    tag_name: str,
    *,
    db_path: Union[str, Path],
    ) -> list[str]:

    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)
    
    try:
        sql = "SELECT blog_name FROM BLOG_TAGS WHERE tag_name = ?"
        result = conn.execute(sql, (tag_name,)).fetchall()
        return [row[0] for row in result]

    except sqlite3.Error as e:
        logger.error(f"get blog names failed: tag_name={tag_name}, error={e}", exc_info=True)
        return []
    finally:
        conn.close()


def get_tags_by_blog_id(
    blog_id: int,
    *,
    db_path: Union[str, Path],
    ) -> list[str]:

    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)

    try:
        sql = "SELECT tag_name FROM BLOG_TAGS WHERE blog_name = (SELECT name FROM BLOG_LIST WHERE blog_id = ?)"
        result = conn.execute(sql, (blog_id,)).fetchall()
        return [row[0] for row in result]

    except sqlite3.Error as e:
        logger.error(f"get blog tags failed: blog_id={blog_id}, error={e}", exc_info=True)
        return []
    finally:
        conn.close()


def get_all_tags(
    *,
    db_path: Union[str, Path],
    ) -> list[str]:
    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)
    
    try:
        sql = "SELECT DISTINCT tag_name, COUNT(*) FROM BLOG_TAGS GROUP BY tag_name ORDER BY COUNT(*) DESC"
        result = conn.execute(sql).fetchall()
        return [{"tag_name": row[0], "count": row[1]} for row in result]

    except sqlite3.Error as e:
        logger.error(f"get all tags failed: error={e}", exc_info=True)
        return []
    finally:
        conn.close()