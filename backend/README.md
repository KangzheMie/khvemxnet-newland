# NewLand Backend

A small and simple api server based on python for NewLand project.

The only thing the backend to do, is read out the database and serve the api.

## Installation

### config the path

you should write a config.json file in the root folder, and set the following fields:

```json
// demo
{
    "log_path": "./api_server.log",
    "blog_path": "./blog",
    "db_path": "./blog.db",
    "backend_host": "127.0.0.1",
    "backend_port": 8000
}
```

### blog article format

the blog_path is the folder where your blog articles are stored. and each article should be a markdown file. and the head of each article should be yaml format:

```markdown
---
category: tech
create_time: 2026-01-01
summary: hello world!
tags:
  - tech
  - blog
---

# blog1

this is blog1 content.
```

if you want to change markdown keys, you should modify the `blogbd.py`.
and don't forget to modify the `api_server.py` as well.

### start the server

for windows:

```bash
./start.bat
```

for linux:

```bash
./start.sh
```

## api list

- '/api/ping' 
```python
	Dict[str, str]
	{"data": "ping"}
```

- '/api/blogs'
```python
	Dict[str, List[Dict[str, str]]]
	{"data": [{"id": "1","name": "blog1"}]}
```

- '/api/blogs/<id>'
```python
	Dict[str, Blog]
	{"data": 
    - {"id": "1",
    - "name": "blog1", 
    - "hash": "123456", 
    - "category": "tech", 
    - "create_time": "2026-01-01", 
    - "summary": "this is blog1", 
    - "tags": ["tech", "blog"], 
    - "content": "this is blog1 content"}}
```
  
- '/api/blogs/category/<category>'
```python
	Dict[str, List[Dict[str, str]]]
	{"data": [{"id": "1","name": "blog1"}]}
```

- '/api/blogs/content/<id>'
```python
	Dict[str, str]
	{"data": "this is blog1 content"}
```

- '/api/blogs/tags/<id>'
```python
	Dict[str, List[str]]
	{"data": ["tech", "blog"]}
```

- '/api/tags'
```python
	Dict[str, List[str]]
	{"data": ["tech", "blog"]}
```
