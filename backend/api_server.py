from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from typing import List, Dict, Any
import blogdb
import uvicorn

settings = blogdb.load_settings()
log_path = settings["log_path"]
blog_db_path = settings["db_path"]
backend_host = settings["backend_host"]
backend_port = settings["backend_port"]

# lifespan is a context manager that is used to execute code before and after the application starts and stops
# lifespan's execution order:
# 1. When the application starts, it first executes the code in the lifespan context manager,
#    until it encounters the yield statement. At this point, it passes control to the application.
# 2. The application runs, handling requests.
# 3. When the application shuts down, it returns to the lifespan context manager,
#    executes the code after the yield statement, and completes.
@asynccontextmanager
async def lifespan(app: FastAPI):

    # the code in the lifespan context manager can be synchronous or asynchronous
    # in the synchronous case: it will block the application startup until the initialization is complete
    # in the asynchronous case: it will not block the application startup, and can await other asynchronous operations, such as database connections
    
    try:
        blogdb.logger_init(log_level='INFO', log_path=log_path)
        blogdb.logger.info('api server start')

        if not blog_db_path.exists():
            raise FileNotFoundError("DB not found")

        blogdb.logger.info(f"DB ready at {blog_db_path}")

    except Exception as e:
        blogdb.logger.warning(f"DB init skipped or failed: {e}")

    yield

    blogdb.logger.info('api server stop')
    
app = FastAPI(title="NewLand Backend API", version="0.1.0", lifespan=lifespan)

# middleware is a feature of FastAPI that allows you to add extra logic to the request processing pipeline
# it can be used to add common functionality, such as logging, authentication, and CORS
# here, we add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins, tighten in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# =================== register routes =================== #
# routing is the process of mapping an input identifier to a specific path or function
# each route has a corresponding handler function, which is used to process requests for that route

# testing routes
# this route is used to test the API server, and return a simple JSON response
@app.get("/ping")
def ping() -> Dict[str, str]:
    return {"data": "Ciallo～(∠・ω<)⌒★"}

# blog list route
# this route is used to get a list of all blogs in the database
@app.get("/api/blogs")
def blog_list() -> Dict[str, List[Dict[str, Any]]]:
    data = blogdb.blog_list_get_all_names(db_path=blog_db_path)
    if not data:
        blogdb.logger.warning("No blogs found")
        raise HTTPException(status_code=404, detail="No blogs found")
    # using data wrapper, provide space for future extensions, can add other fields later
    # the first field faithfully reflects the content in the database, other extended fields can be added as needed
    # for example {"data": [...], "total_count": 100}
    return {"data": data}

# blog detail route
# this route is used to get the details of a blog, including its title, content, tags, and other metadata
@app.get("/api/blogs/{blog_id}")
def blog_detail(blog_id: int) -> Dict[str, Any]:
    data = blogdb.blog_list_get_by_id(blog_id, db_path=blog_db_path)
    if not data:
        blogdb.logger.warning(f"Blog not found: {blog_id}")
        raise HTTPException(status_code=404, detail="Blog not found")
    # use __dict__ to convert the object to a dictionary, which is more JSON-friendly
    return {"data": data.__dict__}

# blog list route by category
# this route is used to get a list of all blogs in the database, filtered by category
@app.get("/api/blogs/category/{category}")
def blog_list_by_category(category: str) -> Dict[str, List[Dict[str, Any]]]:
    data = blogdb.blog_list_get_by_category(category, db_path=blog_db_path)
    if not data:
        blogdb.logger.warning(f"No blogs found in category: {category}")
        raise HTTPException(status_code=404, detail=f"No blogs found in category: {category}")
    return {"data": data}

# blog content route
# this route is used to get the content of a blog
@app.get("/api/blogs/content/{blog_id}")
def blog_content(blog_id: int) -> Dict[str, str]:
    data = blogdb.blog_list_get_by_id(blog_id, db_path=blog_db_path)
    if not data:
        blogdb.logger.warning(f"Blog not found: {blog_id}")
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"data": data.content}

# blog tags route
# this route is used to get the tags of a blog
@app.get("/api/blogs/tags/{blog_id}")
def blog_tags(blog_id: int) -> Dict[str, List[Dict[str, str]]]:
    data = blogdb.blog_tags_get_by_id(blog_id, db_path=blog_db_path)
    if not data:
        blogdb.logger.warning(f"Blog tags not found: {blog_id}")
        raise HTTPException(status_code=404, detail="Blog tags not found")
    return {"data": data}

# tag list route
# this route is used to get a list of all tags and its count in the database
@app.get("/api/tags")
def tag_list() -> Dict[str, List[Dict[str, str]]]:
    data = blogdb.blog_tags_get_all(db_path=blog_db_path)
    if not data:
            blogdb.logger.warning("No tags found")
            raise HTTPException(status_code=404, detail="No tags found")
    return {"data": data}

if __name__ == "__main__":
    # run the API server using uvicorn
    print(f"fastapi doc: http://{backend_host}:{backend_port}/docs")
    uvicorn.run("api_server:app", host=backend_host, port=backend_port, reload=True)
