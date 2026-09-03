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
        blog_insert_result = blog_list_insert(a_blog, db_path=db_path)
        tags_insert_result = blog_tags_insert(a_blog, db_path=db_path)
        logger.info(f"{blog_insert_result}")
        logger.info(f"{tags_insert_result}")

    logger.info(f"blog sync finished")
    
    check_result, _ = blog_list_check(blog_dir, db_path=db_path)
    logger.info(f"blog list check result: {check_result}")

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

    for file in blog_dir.rglob('*.md'):
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
        for file in blog_dir.rglob('*.md'):
            blog_set.add(file.stem)
        logger.debug(f"blog dir blog list: {blog_set}")

        blog_list = blog_list_get_all_names(db_path=db_path)
        database_set = set([row["name"] for row in blog_list])
        logger.debug(f"database blog list: {database_set}")
        ghost_set = database_set - blog_set or None

        if ghost_set is not None:
            logger.debug(f"have ghost blog list: {ghost_set}")
            return "warning", ghost_set
        else:
            logger.debug(f"have no ghost blog list")
            return "checked", set[Any]()

    except sqlite3.Error as e:
        logger.error(f"check ghost blog list failed: error={e}", exc_info=True)
        return "error", set[Any]()
    finally:
        conn.close()


def blog_list_check_outsync(
    blog_dir: Union[str, Path],
    *,
    db_path: Union[str, Path],
    ) -> Tuple[Literal["checked", "warning", "error"], set[Any]]:

    '''outsync is the blog that is in the blog dir but not in the database'''

    blog_dir = Path(blog_dir)
    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)

    try:
        logger.debug(f"try to check out of sync blog list")
        blog_set = set()
        for file in blog_dir.rglob('*.md'):
            blog_set.add(file.stem)

        blog_list = blog_list_get_all_names(db_path=db_path)
        database_set = set([row["name"] for row in blog_list])
        outsync_set = blog_set - database_set or None

        if outsync_set is not None:
            logger.debug(f"have out of sync blog list: {outsync_set}")
            return "warning", outsync_set
        else:
            logger.debug(f"have no out of sync blog list")
            return "checked", set[Any]()

    except sqlite3.Error as e:
        logger.error(f"check out of sync blog list failed: error={e}", exc_info=True)
        return "error", set[Any]()
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
            return "checked", set[Any]()
        else:
            logger.info(f"have ghost blog list: {ghost_set[1]} \n out of sync blog list: {outsync_set[1]}")
            return "warning", ghost_set[1] | outsync_set[1]

    except sqlite3.Error as e:
        logger.error(f"check blog list failed: error={e}", exc_info=True)
        return "error", set[Any]()
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

    for file in blog_dir.rglob('*.md'):
        a_blog = blog_reader(file)
        blog_tags_insert(a_blog, db_path=db_path)
