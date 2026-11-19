import blogDatabaseLib as blogdb
from pathlib import Path
import time

root_path = Path(__file__).parent.parent
config_path = root_path / "config.json"
config_data = blogdb.read_config(config_path)
        
blog_db_path = Path(config_data.get("db_path")).resolve()
blog_path = Path(config_data.get("blog_path")).resolve()
db_log_path = Path(config_data.get("db_log_dir") + f"blog_db_{time.strftime('%Y%m%d%H%M%S', time.localtime())}.log").resolve()

def blog_setup():
    # creat log file
    blogdb.logger_init(log_level='INFO', log_path=db_log_path)
    blogdb.logger.info(f'log ready at {db_log_path}')

    blogdb.blogdb_init(db_path=blog_db_path)
    blogdb.logger.info(f"DB ready at {blog_db_path}")
    blogdb.logger.info('blog_setup finished')

def sync_all():
    blogdb.sync_all(blog_path, db_path=blog_db_path)

def main():
    blog_setup()
    sync_all()

if __name__ == '__main__':
    main()
