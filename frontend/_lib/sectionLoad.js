// ======================= GLOBAL ======================= //
const CONFIG = {
    BASE_URL: window.location.origin,
    API_BASE_URL: window.location.origin + '/api',
    MATH_DELIMITERS: [
        { left: "$$", right: "$$", display: true },
        { left: "$", right: "$", display: false },
        { left: "\\(", right: "\\)", display: false },
        { left: "\\[", right: "\\]", display: true }
    ]
};

const SITE_TITLE = '新大陆发现部';
const sectionText = document.querySelector('#content #section-text');

// ======================= ROUTES ======================= //
const ROUTES = [
    { pattern: /^\/$/, render: renderHome },
    { pattern: /^\/about$/, render: renderAbout },
    { pattern: /^\/blogs$/, render: () => renderBlogList(null) },
    { pattern: /^\/blogs\/category\/([^/]+)$/, render: match => renderBlogList(safeDecode(match[1])) },
    { pattern: /^\/blogs\/(\d+)$/, render: match => renderBlog(match[1]) }
];

// ======================= MAIN ======================= //
function main() {
    console.log("Welcome to Newland Ciallo～(∠・ω<)⌒★");

    document.addEventListener('click', handleLinkClick);
    window.addEventListener('popstate', () => {
        navigate(window.location.pathname, { push: false });
    });

    navigate(window.location.pathname, { push: false, replace: true });
}

main();

function handleLinkClick(event) {
    if (event.defaultPrevented || event.button !== 0) return;
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    if (!(event.target instanceof Element)) return;

    const link = event.target.closest('a[href]');
    if (!link) return;

    const url = new URL(link.getAttribute('href'), window.location.origin);
    if (url.origin !== window.location.origin) return;
    if (url.pathname === window.location.pathname && url.hash === window.location.hash) return;

    event.preventDefault();
    navigate(url.pathname);
}

// ======================= NAVIGATE ======================= //
async function navigate(path, { push = true, replace = false } = {}) {
    const normalized = normalizePath(path);

    let matched = null;
    for (const route of ROUTES) {
        const match = route.pattern.exec(normalized);
        if (match) {
            matched = { route, match };
            break;
        }
    }

    if (!matched) {
        renderNotFound(normalized);
    } else {
        await matched.route.render(matched.match);
    }

    if (push) window.history.pushState({ path: normalized }, '', normalized);
    else if (replace) window.history.replaceState({ path: normalized }, '', normalized);
    window.scrollTo(0, 0);
}

function normalizePath(path) {
    const stripped = path.replace(/\/+$/, '');
    return stripped === '' ? '/' : stripped;
}

// ======================= RENDER PAGE ======================= //
async function renderHome() {
    const content = await getLocalPage('/_pages/home.md');
    if (content === null) return;

    document.title = SITE_TITLE;
    loadLocalPage(content);
}

async function renderAbout() {
    const content = await getLocalPage('/_pages/about.md');
    if (content === null) return;

    document.title = `关于 - ${SITE_TITLE}`;
    loadLocalPage(content);
}

async function renderBlogList(category) {
    const apiPath = category ? `/blogs/category/${encodeURIComponent(category)}` : '/blogs';
    const blogs = await getApiData(apiPath);
    if (blogs === null) return;

    document.title = category ? `${category} - ${SITE_TITLE}` : `文章 - ${SITE_TITLE}`;
    loadBlogList(blogs);
}

async function renderBlog(blogId) {
    const blog = await getApiData(`/blogs/${blogId}`);
    if (blog === null) return;

    document.title = `${blog.name} - ${SITE_TITLE}`;
    loadBlogContent(blog.name, blog.content);
}

function renderNotFound(path) {
    document.title = `未找到 - ${SITE_TITLE}`;
    sectionText.innerHTML = `<p style="color:red;">Invalid path: ${escapeHtml(path)}</p>`;
}

// ======================= GET CONTENT ======================= //
async function getLocalPage(filePath) {
    sectionText.innerHTML = '<p>Loading...</p>';
    const fullUrl = CONFIG.BASE_URL + filePath;
    console.log(`get local page from: ${fullUrl}`);

    try {
        const response = await fetch(fullUrl);
        if (!response.ok) throw new Error(`Page not found (${response.status})`);
        console.log(`success for getting local page: ${fullUrl}`);

        return await response.text();
    } catch (error) {
        console.error('Loading local page failed:', error);
        sectionText.innerHTML = `<p style="color:red;">Loading failed: ${escapeHtml(error.message)}</p>`;
        return null;
    }
}

async function getApiData(apiPath) {
    sectionText.innerHTML = '<p>Loading...</p>';
    const fullUrl = CONFIG.API_BASE_URL + apiPath;
    console.log(`get api data from: ${fullUrl}`);

    try {
        const response = await fetch(fullUrl);
        if (!response.ok) throw new Error(`Request failed (${response.status})`);
        console.log(`success for getting api data: ${fullUrl}`);

        const json = await response.json();
        return json.data;
    } catch (error) {
        console.error('Loading api data failed:', error);
        sectionText.innerHTML = `<p style="color:red;">Loading failed: ${escapeHtml(error.message)}</p>`;
        return null;
    }
}

// ======================= LOAD CONTENT ======================= //
function loadLocalPage(data) {
    sectionText.innerHTML = marked.parse(data);
    decorateImages();
}

function loadBlogList(blogs) {
    const htmlList = blogs.map(blog => {
        return `
            <li class="blog-list-item">
                <a href="/blogs/${blog.blog_id}" class="blog-link">${escapeHtml(blog.name)}</a>
            </li>
        `;
    });
    const finalHtml = `<div class="blog-list"><ul>${htmlList.join('')}</ul></div>`;

    sectionText.innerHTML = finalHtml;
}

function loadBlogContent(title, data) {
    const mathBlocks = [];

    let dataWithoutMath = 
            data.replace(/\$\$([\s\S]*?)\$\$/g, (match) => {
                mathBlocks.push(match); 
                return `@@MATH-${mathBlocks.length - 1}@@`; 
            }).replace(/\$([^\$\n]+?)\$/g, (match) => {
                mathBlocks.push(match); 
                return `@@MATH-${mathBlocks.length - 1}@@`;
            });

    dataWithoutMath = dataWithoutMath
        .replace(/!\[([^\]]*)\]\(([^)]+)\)/g, (match, p1, p2) => {
            return `![${p1}](${CONFIG.BASE_URL}/api/image/${p2})`;
        });


    let html_title = `<h1>${escapeHtml(title)}</h1>`;
    let html_data = marked.parse(dataWithoutMath);

    mathBlocks.forEach((math, index) => {
        html_data = html_data.replace(`@@MATH-${index}@@`, () => math); // replace placeholder with mathBlocks
    });
    
    sectionText.innerHTML = html_title + html_data; 
    decorateImages();

    // ======================= RENDER ======================= //
    renderMath(sectionText);
    renderCode();
}

// ======================= FUNCTION ======================= //
function decorateImages() {
    sectionText.querySelectorAll('img').forEach(img => {
        if (img.closest('figure') || img.closest('.friend-card')) return;

        const figure = document.createElement('figure');
        figure.className = 'blog-figure';

        img.replaceWith(figure);
        figure.append(img);

        if (img.alt) {
            const caption = document.createElement('figcaption');
            caption.textContent = img.alt;
            figure.append(caption);
        }
    });
}

function renderCode() {
    if (typeof hljs !== 'undefined') {
        hljs.highlightAll();
    }
}

function renderMath(data) {
    renderMathInElement(data, {delimiters: CONFIG.MATH_DELIMITERS});
}

function safeDecode(text) {
    try {
        return decodeURIComponent(text);
    } catch {
        return text;
    }
}

function escapeHtml(text) {
    return String(text).replace(/[&<>"']/g, char => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
    }[char]));
}
