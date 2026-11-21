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

def read_blog(blog_path: Union[str, Path]) -> "Blog":
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


def insert_blog(
    blog: Blog,
    *,  # parameters after this must be passed by keyword, like db_path=xxx
    db_path: Union[str, Path],
    ) -> Tuple[Literal["inserted", "updated", "unchanged", "error"], str]:

    db_path = Path(db_path)
    # excluded is the values in the ON CONFLICT clause
    # if blog's name is already in the database, it will trigger the conflict clause
    # in the conflict clause, update the contents
    sql = (
        "INSERT INTO BLOG_LIST (blog_id, name, hash, category, create_time, summary, content) "
        "VALUES (?, ?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(name) DO UPDATE SET hash = excluded.hash, category = excluded.category, "
        "create_time = excluded.create_time, summary = excluded.summary, "
        "content = excluded.content"
    )
    conn = sqlite3.connect(db_path)

    try:
        logger.debug(f"try to insert blog list: name={blog.name}, hash={blog.hash}")
        row = conn.execute("SELECT hash FROM BLOG_LIST WHERE name = ?", (blog.name,)).fetchone()

        # the file hash covers the whole file, so an equal hash means nothing to write
        if row is not None and row[0] == blog.hash:
            logger.debug(f"blog list unchanged: name={blog.name}")
            return "unchanged", f"{blog.name}"

        conn.execute(sql, (
            blog_id_from_name(blog.name), blog.name, blog.hash,
            blog.category, blog.create_time, blog.summary, blog.content,
        ))
        conn.commit()

        if row is not None:
            logger.info(f"update blog list success: name={blog.name}")
            return "updated", f"{blog.name}"

        logger.info(f"insert blog list success: name={blog.name}, blog_id={blog_id_from_name(blog.name)}")
        return "inserted", f"{blog.name}"

    except sqlite3.Error as e:
        logger.error(f"insert blog list failed: name={blog.name}, error={e}", exc_info=True)
        conn.rollback()
        return "error", str(e)
    finally:
        conn.close()


def insert_tags(
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
        conn.execute("DELETE FROM BLOG_TAGS WHERE blog_name = ?", (blog.name,))
        
        if blog.tags:
            logger.debug(f"insert blog tags: blog_name={blog.name}, tags={blog.tags}")
            insert_data = [(blog.name, tag) for tag in blog.tags]
            conn.executemany("INSERT INTO BLOG_TAGS (blog_name, tag_name) VALUES (?, ?)", insert_data)
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