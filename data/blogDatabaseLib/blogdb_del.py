from .blogdb_init import *

import sqlite3
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Tuple, Union, Literal, Dict, Any

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