/**
 * 🧭 NewLand2 轻量级路由器
 * 使用History API实现单页应用路由功能
 * 支持浏览器前进后退和URL分享
 */

class Router {
    constructor(contentLoader) {
        this.contentLoader = contentLoader;
        this.routes = new Map();
        this.currentRoute = null;
        this.init();
    }

    // 🚀 初始化路由器
    init() {
        this.setupRoutes();
        this.bindEvents();
        this.handleInitialRoute();
    }

    // 📋 设置路由规则
    setupRoutes() {
        // 主页路由
        this.routes.set('/', {
            handler: () => this.contentLoader.loadHomepage(),
            title: '主页 - NewLand2'
        });

        // 静态页面路由
        this.routes.set('/about', {
            handler: () => this.contentLoader.loadStaticPage('about'),
            title: '关于 - NewLand2'
        });

        this.routes.set('/friend', {
            handler: () => this.contentLoader.loadStaticPage('friend'),
            title: '友链 - NewLand2'
        });

        this.routes.set('/Anniv', {
            handler: () => this.contentLoader.loadStaticPage('Anniv'),
            title: '年鉴 - NewLand2'
        });

        this.routes.set('/contact', {
            handler: () => this.contentLoader.loadStaticPage('contact'),
            title: '联系 - NewLand2'
        });

        // 分类文章列表路由 /category/:id
        this.routes.set('/category', {
            handler: (params) => this.contentLoader.loadArticleList(params.id),
            title: '文章分类 - NewLand2',
            parameterized: true
        });

        // 文章详情路由 /article/:id
        this.routes.set('/article', {
            handler: (params) => this.contentLoader.loadArticleContent(params.id),
            title: '文章详情 - NewLand2',
            parameterized: true
        });
    }

    // 🔗 绑定事件
    bindEvents() {
        // 监听浏览器前进后退
        window.addEventListener('popstate', (e) => {
            if (e.state && e.state.route) {
                this.handleRoute(e.state.route, false); // 不推送到历史记录
            } else {
                this.handleInitialRoute();
            }
        });

        // 拦截所有链接点击
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a');
            if (link) {
                const href = link.getAttribute('href');
                console.log('🔗 链接点击:', href, '是否拦截:', this.shouldInterceptLink(link));
                
                if (this.shouldInterceptLink(link)) {
                    e.preventDefault();
                    console.log('🧭 路由导航到:', href);
                    this.navigate(href, true, link);
                }
            }
        });
    }

    // 🔍 判断是否应该拦截链接
    shouldInterceptLink(link) {
        const href = link.getAttribute('href');
        
        // 如果没有href属性，不拦截
        if (!href) {
            return false;
        }
        
        // 不拦截外部链接
        if (href.startsWith('http://') || href.startsWith('https://')) {
            return false;
        }
        
        // 不拦截邮件链接
        if (href.startsWith('mailto:')) {
            return false;
        }
        
        // 不拦截电话链接
        if (href.startsWith('tel:')) {
            return false;
        }
        
        // 不拦截锚点链接（页面内跳转）
        if (href.startsWith('#')) {
            return false;
        }
        
        // 忽略下载链接
        if (link.hasAttribute('download')) {
            return false;
        }

        // 不拦截带有target="_blank"的链接
        if (link.getAttribute('target') === '_blank') {
            return false;
        }
        
        // 拦截相对路径和绝对路径
        console.log('🔍 链接分析:', {
            href,
            hasDataAttributes: !!(link.dataset.categoryId || link.dataset.page),
            shouldIntercept: true
        });
        return true;
    }

    // 🧭 导航到指定路径
    navigate(path, pushState = true, linkElement = null) {
        let actualPath = path;
        
        // 如果提供了链接元素，检查data属性来确定实际路径
        if (linkElement) {
            const { categoryId, page } = linkElement.dataset;
            
            if (categoryId) {
                actualPath = `/category/${categoryId}`;
            } else if (page === 'home') {
                actualPath = '/';
            } else if (page) {
                actualPath = `/${page}`;
            }
            
            console.log('🔄 路径转换:', { original: path, actual: actualPath, data: { categoryId, page } });
        }
        
        this.handleRoute(actualPath, pushState);
    }

    // 🎯 处理路由
    async handleRoute(path, pushState = true) {
        console.log('🧭 处理路由:', path);
        
        try {
            const { route, params } = this.parseRoute(path);
            
            if (!route) {
                throw new Error(`路由未找到: ${path}`);
            }

            // 更新当前路由
            this.currentRoute = path;

            // 推送到浏览器历史记录
            if (pushState) {
                const state = { route: path };
                history.pushState(state, route.title, path);
                console.log('📝 更新URL:', path);
            }

            // 更新页面标题
            document.title = route.title;

            // 执行路由处理器
            await route.handler(params);

        } catch (error) {
            console.error('路由处理失败:', error);
            this.contentLoader.showError(`页面加载失败: ${error.message}`);
        }
    }

    // 🔍 解析路由
    parseRoute(path) {
        // 移除查询参数和哈希
        const cleanPath = path.split('?')[0].split('#')[0];
        
        // 直接匹配
        if (this.routes.has(cleanPath)) {
            return { route: this.routes.get(cleanPath), params: {} };
        }

        // 参数化路由匹配
        for (const [routePath, route] of this.routes.entries()) {
            if (route.parameterized) {
                const params = this.matchParameterizedRoute(routePath, cleanPath);
                if (params) {
                    return { route, params };
                }
            }
        }

        return { route: null, params: {} };
    }

    // 🎯 匹配参数化路由
    matchParameterizedRoute(routePath, actualPath) {
        // 对于/category和/article路由，检查是否匹配模式
        if (routePath === '/category' && actualPath.startsWith('/category/')) {
            const id = actualPath.split('/')[2];
            return id ? { id } : null;
        }
        
        if (routePath === '/article' && actualPath.startsWith('/article/')) {
            const id = actualPath.split('/')[2];
            return id ? { id } : null;
        }

        return null;
    }

    // 🏠 处理初始路由
    handleInitialRoute() {
        const currentPath = window.location.pathname;
        this.handleRoute(currentPath, false);
    }

    // 🔄 替换当前路由（不添加到历史记录）
    replace(path) {
        const { route } = this.parseRoute(path);
        if (route) {
            const state = { route: path };
            history.replaceState(state, route.title, path);
            document.title = route.title;
        }
    }

    // 📍 获取当前路由
    getCurrentRoute() {
        return this.currentRoute || window.location.pathname;
    }

    // 🔗 生成路由URL
    generateUrl(routeName, params = {}) {
        switch (routeName) {
            case 'home':
                return '/';
            case 'category':
                return `/category/${params.id}`;
            case 'article':
                return `/article/${params.id}`;
            case 'about':
                return '/about';
            case 'friend':
                return '/friend';
            case 'Anniv':
                return '/Anniv';
            case 'contact':
                return '/contact';
            default:
                return '/';
        }
    }
}

// 🌍 导出路由器
window.Router = Router;