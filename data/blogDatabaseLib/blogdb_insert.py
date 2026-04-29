from .blogdb_init import *

import sqlite3
import hashlib
import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Tuple, Union, Literal, Dict, Any

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


def blog_tags_insert(
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
            logger.debug(f"insert blog tags: blog_name={blog.name}, tags={blog.tags}")
            insert_data = [(blog.name, tag) for tag in blog.tags]
            conn.executemany("INSERT INTO blog_tags (blog_name, tag_name) VALUES (?, ?)", insert_data)
        else:
            logger.debug(f"blog {blog.name} have no tags")
        conn.commit()
        logger.debug(f"insert blog tags success: blog_name={blog.name}, tags={blog.tags}")
        return "updated", f"Tags updated for blog {blog.name}"    

    except sqlite3.Error as e:
        conn.rollback()
        logger.error(f"delete or insert blog tags failed: blog_name={blog.name}, error={e}", exc_info=True)
        return "error", str(e)
    finally:
        conn.close()