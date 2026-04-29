from .blogdb_init import *
from .blogdb_insert import blog_reader, blog_list_insert, blog_tags_insert
from .blogdb_get import blog_list_get_all_names

import sqlite3
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Tuple, Union, Literal, Dict, Any

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
        blog_tags_insert(a_blog, db_path=db_path)
        logger.info(f"insert blog {a_blog.name} success")
        logger.info(f"insert blog tags {a_blog.name} success")

    logger.info(f"blog sync finished")
    
    check_result, check_set = blog_list_check(blog_dir, db_path)
    logger.info(f"blog list check result: {check_result}, check set: {check_set}")

# ==========================================
# Blog List
# ==========================================

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


def blog_list_check_ghost(
    blog_dir: Union[str, Path],
    *,
    db_path: Union[str, Path],
    ) -> Tuple[Literal["checked", 'warning', "error"], set]:

    '''ghost is the blog that is not in the blog dir but in the database'''

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

    '''outsync is the blog that is in the blog dir but not in the database'''

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
# Tags
# ==========================================

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
        blog_tags_insert(a_blog, db_path=db_path)
