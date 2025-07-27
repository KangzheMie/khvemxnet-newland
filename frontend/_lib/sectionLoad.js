/**
 * 🚀 NewLand2 内容加载器 - 简洁而有力的版本
 * 负责处理所有内容的动态加载和渲染
 */

// 📋 配置中心
const CONFIG = {
    // 智能检测API URL：支持开发环境和生产环境的自动切换
    STRAPI_URL: (() => {
        const hostname = window.location.hostname;
        const protocol = window.location.protocol;
        
        // 开发环境：localhost 或 127.0.0.1
        if (hostname === 'localhost' || hostname === '127.0.0.1') {
            return 'http://localhost:1337';
        }
        
        // 生产环境：使用当前域名的1337端口
        // 如果是通过nginx代理，也可以使用相对路径（空字符串）
        return `${protocol}//${hostname}:1337`;
    })(),
    PAGE_SIZE: 100,
    SORT_ORDER: 'PublishedDate:desc',
    CACHE_TTL: 5 * 60 * 1000, // 5分钟缓存
    MATH_DELIMITERS: [
        { left: "$$", right: "$$", display: true },
        { left: "$", right: "$", display: false },
        { left: "\\(", right: "\\)", display: false },
        { left: "\\[", right: "\\]", display: true }
    ]
};

// 🎯 主应用类
class ContentLoader {
    constructor() {
        this.sectionElement = document.getElementById('section-text');
        this.cache = new Map();
        this.api = new StrapiAPI(CONFIG.STRAPI_URL);
        this.renderer = new ContentRenderer();
        this.router = null; // 路由器将在初始化后设置
        this.init();
    }

    init() {
        // 不再直接加载主页，让路由器处理
        // 不再绑定导航事件，路由器会处理所有链接点击
        // 初始化路由器
        this.router = new Router(this);
    }

    // 🔗 设置路由器（用于路由器初始化后的双向绑定）
    setRouter(router) {
        this.router = router;
    }

    // 🧭 处理导航（已移除，路由器直接处理所有导航）

    // 🏠 加载主页
    async loadHomepage() {
        try {
            this.showLoading('加载主页中...');
            const data = await this.api.getHomepage();
            this.renderer.renderContent(data.Content);
        } catch (error) {
            this.showError(`加载主页失败：${error.message}`);
        }
    }

    // 📄 加载静态页面
    async loadStaticPage(page) {
        try {
            this.showLoading(`加载${page}页面中...`);
            const data = await this.api.getStaticPage(page);
            this.renderer.renderContent(data.Content);
        } catch (error) {
            this.showError(`加载页面失败：${error.message}`);
        }
    }

    // 📚 加载文章列表
    async loadArticleList(categoryId) {
        try {
            this.showLoading('加载文章列表中...');
            const articles = await this.api.getArticlesByCategory(categoryId);
            
            if (articles.length === 0) {
                this.showError('该分类下没有文章');
                return;
            }

            this.renderArticleList(articles);
        } catch (error) {
            this.showError(`加载文章列表失败：${error.message}`);
        }
    }

    // 📖 加载文章内容
    async loadArticleContent(articleId) {
        try {
            this.showLoading('加载文章内容中...');
            const article = await this.api.getArticleById(articleId);
            this.renderer.renderContent(article.Content);
        } catch (error) {
            this.showError(`加载文章失败：${error.message}`);
        }
    }

    // 🎨 渲染文章列表
    renderArticleList(articles) {
        const listHTML = articles.map(article => {
            const publishDate = article.PublishedDate 
                ? new Date(article.PublishedDate).toISOString().split('T')[0]
                : '暂无日期';
            
            // 使用路由URL
            const articleUrl = this.router ? this.router.generateUrl('article', { id: article.id }) : `#article-${article.id}`;
            
            return `
                <li class="article-item">
                    <a href="${articleUrl}" class="article-link">
                        <span class="article-date">${publishDate}</span>
                        <span class="article-title">${article.Title}</span>
                    </a>
                </li>
            `;
        }).join('');

        this.sectionElement.innerHTML = `<ul class="article-list">${listHTML}</ul>`;
        // 不再需要单独绑定文章事件，路由器会处理所有链接点击
    }

    // 🔗 绑定文章点击事件（已由路由器处理，保留此方法作为降级方案）
    bindArticleEvents() {
        // 如果没有路由器，使用传统方式处理文章链接
        if (!this.router) {
            this.sectionElement.querySelectorAll('.article-link').forEach(link => {
                link.addEventListener('click', async (e) => {
                    e.preventDefault();
                    const href = link.getAttribute('href');
                    const articleId = href.match(/article-(\d+)/) ? href.match(/article-(\d+)/)[1] : null;
                    if (articleId) {
                        await this.loadArticleContent(articleId);
                    }
                });
            });
        }
    }

    // ⏳ 显示加载状态
    showLoading(message = '加载中...') {
        this.sectionElement.innerHTML = `
            <div class="loading-container">
                <div class="loading-spinner"></div>
                <p class="loading">${message}</p>
            </div>
        `;
    }

    // ❌ 显示错误
    showError(message) {
        console.error(message);
        this.sectionElement.innerHTML = `<p class="error">${message}</p>`;
    }
}

// 🌐 Strapi API 客户端
class StrapiAPI {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
        this.cache = new Map();
    }

    // 🔄 通用请求方法
    async request(endpoint, cacheKey = null) {
        // 检查缓存
        if (cacheKey && this.cache.has(cacheKey)) {
            const cached = this.cache.get(cacheKey);
            if (Date.now() - cached.timestamp < CONFIG.CACHE_TTL) {
                return cached.data;
            }
        }

        const url = `${this.baseUrl}/api/${endpoint}`;
        
        try {
            const response = await fetch(url);
            
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP ${response.status}: ${response.statusText}\n${errorText}`);
            }

            const result = await response.json();
            const data = result.data;

            // 缓存结果
            if (cacheKey) {
                this.cache.set(cacheKey, {
                    data,
                    timestamp: Date.now()
                });
            }

            return data;
        } catch (error) {
            if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
                throw new Error('网络连接失败，请检查网络或服务器状态');
            }
            throw error;
        }
    }

    // 🏠 获取主页数据
    async getHomepage() {
        return await this.request('homepage', 'homepage');
    }

    // 📄 获取静态页面
    async getStaticPage(page) {
        return await this.request(page, `page_${page}`);
    }

    // 📚 根据分类获取文章
    async getArticlesByCategory(categoryId) {
        const endpoint = `articles?filters[categories][id]=${categoryId}&pagination[pageSize]=${CONFIG.PAGE_SIZE}&sort=${CONFIG.SORT_ORDER}&fields[0]=Title&fields[1]=PublishedDate`;
        return await this.request(endpoint, `articles_cat_${categoryId}`);
    }

    // 📖 根据ID获取文章
    async getArticleById(articleId) {
        const endpoint = `articles?filters[id]=${articleId}`;
        const articles = await this.request(endpoint, `article_${articleId}`);
        
        if (!articles || articles.length === 0) {
            throw new Error('文章未找到');
        }
        
        return articles[0];
    }
}

// 🎨 内容渲染器
class ContentRenderer {
    constructor() {
        this.setupMarkdownRenderer();
    }

    // ⚙️ 设置Markdown渲染器
    setupMarkdownRenderer() {
        const renderer = {
            em({ tokens }) {
                const text = this.parser.parseInline(tokens);
                return `_${text}_`;
            }
        };
        marked.use({ renderer });
    }

    // 🎯 渲染内容
    renderContent(markdownString) {
        try {
            const html = marked.parse(markdownString || '');
            document.getElementById('section-text').innerHTML = html;
            
            // 异步渲染数学公式和代码高亮
            requestAnimationFrame(() => {
                this.renderMath();
                this.highlightCode();
            });
        } catch (error) {
            console.error('Markdown渲染失败:', error);
            document.getElementById('section-text').innerHTML = `
                <p class="error">内容渲染失败</p>
                <details>
                    <summary>查看原始内容</summary>
                    <pre>${markdownString}</pre>
                </details>
            `;
        }
    }

    // 🧮 渲染数学公式
    renderMath() {
        if (typeof renderMathInElement !== 'undefined') {
            renderMathInElement(document.getElementById('section-text'), {
                delimiters: CONFIG.MATH_DELIMITERS
            });
        }
    }

    // 🎨 代码高亮
    highlightCode() {
        if (typeof hljs !== 'undefined') {
            hljs.highlightAll();
        }
    }
}

// 🚀 应用启动
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new ContentLoader();
    console.log('🎉 NewLand2 内容加载器已启动！');
});

// 🌍 全局导出（用于调试）
window.ContentLoader = { app, CONFIG };