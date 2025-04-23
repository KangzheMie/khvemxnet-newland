// 获取用于显示内容的 HTML 元素
const contentElement = document.getElementById('section-text');

addEventListener('DOMContentLoaded', (event) => {
    // Strapi API 的 URL
    const strapiUrl = 'http://localhost:1337';
    const homepageApiUrl = `${strapiUrl}/api/homepage`;

    // Load homepage by default
    loadHomepageData(homepageApiUrl);

    // Add event listeners for menu navigation
    const navLinks = document.querySelectorAll('#menu-nav-li a');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const categoryId = link.dataset.categoryId;
            const page = link.dataset.page;

            // Clear previous content
            contentElement.innerHTML = '';

            if (categoryId) {
                // Load article list for category
                loadArticleList(categoryId);
            } else if (page) {
                // Load static page (e.g., home, about, friend, Anniv)
                if (page === 'home') {
                    loadHomepageData(homepageApiUrl);
                } else {
                    loadStaticPage(page);
                }
            }
        });
    });
});

function renderMarkdown(markdownString) {
    // 定义自定义渲染器，处理 <em> 标签，防止和公式中的下标冲突
    const renderer = {
        em({ tokens }) {
            const text = this.parser.parseInline(tokens);
            return `_${text}_`;
        }
    };
    
    marked.use({ renderer });

    try {
        // 解析 Markdown
        return marked.parse(markdownString || ''); // 确保传入非空字符串
    } catch (error) {
        console.error("Markdown 解析出错:", error);
        return `<p>Markdown 解析时发生错误。</p><pre>${markdownString}</pre>`;
    } finally {
        // 渲染数学公式
        setTimeout(() => {
            renderMathInElement(contentElement, {
                delimiters: [
                    { left: "$$", right: "$$", display: true },
                    { left: "$", right: "$", display: false },
                    { left: "\\(", right: "\\)", display: false },
                    { left: "\\[", right: "\\]", display: true }
                ]
            });
        }, 0);
        // 高亮代码
        hljs.highlightAll();
    }
}

function loadHomepageData(apiUrl) {
    contentElement.innerHTML = '<p class="loading">加载中...</p>';
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => {
                    throw new Error(`HTTP 错误! 状态码: ${response.status}\n响应体: ${text}`);
                });
            }
            return response.json();
        })
        .then(apiResponse => {
            const data = apiResponse.data;
            if (data && typeof data === 'object') {
                const content = data.Content;
                contentElement.innerHTML = renderMarkdown(content);
            } else {
                throw new Error('API 响应中缺少有效的 data 对象。');
            }
        })
        .catch(error => {
            console.error('加载主页数据时发生错误:', error);
            contentElement.innerHTML = `<p class="error">加载主页失败：${error.message}</p>`;
        });
}

function loadStaticPage(page) {
    contentElement.innerHTML = '<p class="loading">加载中...</p>';
    const apiUrl = `http://localhost:1337/api/${page}`;
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => {
                    throw new Error(`HTTP 错误! 状态码: ${response.status}\n响应体: ${text}`);
                });
            }
            return response.json();
        })
        .then(apiResponse => {
            const data = apiResponse.data;
            if (data && typeof data === 'object') {
                const content = data.Content;
                contentElement.innerHTML = renderMarkdown(content);
            } else {
                throw new Error('API 响应中缺少有效的 data 对象。');
            }
        })
        .catch(error => {
            console.error(`加载页面 ${page} 时发生错误:`, error);
            contentElement.innerHTML = `<p class="error">加载页面失败：${error.message}</p>`;
        });
}

function loadArticleList(categoryId) {
    contentElement.innerHTML = '<p class="loading">加载文章列表中...</p>';
    const apiUrl = `http://localhost:1337/api/articles?filters[categories][id]=${categoryId}&pagination[pageSize]=100&sort=id:asc`;
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => {
                    throw new Error(`HTTP 错误! 状态码: ${response.status}\n响应体: ${text}`);
                });
            }
            return response.json();
        })
        .then(apiResponse => {
            const data = apiResponse.data;
            if (data && data.length > 0) {
                let html = '<ul class="article-list">';
                data.forEach(article => {
                    html += `<li><a href="#" data-article-id="${article.id}">${article.Title}</a></li>`;
                });
                html += '</ul>';
                contentElement.innerHTML = html;

                // Add click event listeners for article links
                const articleLinks = contentElement.querySelectorAll('.article-list a');
                articleLinks.forEach(link => {
                    link.addEventListener('click', (e) => {
                        e.preventDefault();
                        const articleId = link.dataset.articleId;
                        loadArticleContent(articleId);
                    });
                });
            } else {
                contentElement.innerHTML = '<p class="error">该分类下没有文章。</p>';
            }
        })
        .catch(error => {
            console.error('加载文章列表时发生错误:', error);
            contentElement.innerHTML = `<p class="error">加载文章列表失败：${error.message}</p>`;
        });
}

function loadArticleContent(articleId) {
    contentElement.innerHTML = '<p class="loading">加载文章内容中...</p>';
    const apiUrl = `http://localhost:1337/api/articles?filters[id]=${articleId}`;
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => {
                    throw new Error(`HTTP 错误! 状态码: ${response.status}\n响应体: ${text}`);
                });
            }
            return response.json();
        })
        .then(apiResponse => {
            const data = apiResponse.data;
            if (data && data.length > 0) {
                const content = data[0].Content;
                contentElement.innerHTML = renderMarkdown(content);
            } else {
                contentElement.innerHTML = '<p class="error">文章内容未找到。</p>';
            }
        })
        .catch(error => {
            console.error('加载文章内容时发生错误:', error);
            contentElement.innerHTML = `<p class="error">加载文章内容失败：${error.message}</p>`;
        });
}