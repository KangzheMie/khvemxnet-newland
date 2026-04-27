import blogdb

def main():
    settings = blogdb.load_settings()
    blog_path = settings["blog_path"]
    blog_db_path = settings["db_path"]

    blogdb.blogdb_init(db_path=blog_db_path)
    print("DB initialized")
    blogdb.blogdb_sync(blog_path=blog_path)
    print("Blog synchronized")

if __name__ == "__main__":
    main()