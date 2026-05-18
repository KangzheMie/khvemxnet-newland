import blogDatabaseLib as blogdb
from pathlib import Path
import json

config_file = Path(__file__).parent / "config.json"
with config_file.open("r", encoding="utf-8") as f:
    try:
        config_data = json.load(f)
    except json.JSONDecodeError as e:
        import sys
        print(f"[Error] Invalid JSON in config file: {e}", file=sys.stderr)
        raise ValueError(f"Invalid JSON in config file: {e}")
        
log_path = Path(config_data.get("log_path")).resolve()
blog_db_path = Path(config_data.get("db_path")).resolve()
blog_path = Path(config_data.get("blog_path")).resolve()

def blog_server_init():
    # creat log file
    blogdb.logger_init(log_level='INFO', log_path=log_path)
    blogdb.logger.info(f'log ready at {log_path}')

    if not blog_db_path.exists():
        blogdb.blogdb_init(db_path=blog_db_path)
        blogdb.logger.info(f"DB created at {blog_db_path}")

    blogdb.logger.info(f"DB ready at {blog_db_path}")
    blogdb.logger.info('blog_server_init finished')

def blog_sync():
    blogdb.blog_sync(blog_path, db_path=blog_db_path)

def main():
    blog_server_init()
    blog_sync()

if __name__ == '__main__':
    main()
