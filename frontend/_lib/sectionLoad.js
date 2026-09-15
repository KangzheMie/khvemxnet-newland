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

const sectionText = document.querySelector('#content #section-text');
const blogListLinks = document.querySelectorAll('#header nav a');

// ======================= MAIN ======================= //
function main() {
    console.log("Welcome to Newland Ciallo～(∠・ω<)⌒★");
    
    blogListLinks.forEach(link => {
        link.addEventListener('click', event => {
            const targetPath = link.getAttribute('href');

            if (targetPath) {
                console.log("Navigating to:", targetPath);
                event.preventDefault();
                navigate(targetPath);
            } else {
                console.error('Link does not have a valid href:', link);
            }
        });
    });

    navigate('/');
}

main();

// ======================= NAVIGATE ======================= //

async function navigate(path) {
    console.log(`Navigating to: ${path}`);
    let PageContent = '';
    let BlogList = '';

    if (path.startsWith('/blogs/category/') || path === '/blogs') {
        BlogList = await getBlogList(path);
        loadBlogList(BlogList);
    } else if (path === '/') {
        PageContent = await getLocalPage(CONFIG.BASE_URL + '/_pages/home.md');
        loadLocalPage(PageContent);
    } else if (path === '/about') {
        PageContent = await getLocalPage(CONFIG.BASE_URL + '/_pages/about.md');
        loadLocalPage(PageContent);
    } else {
        console.error('Invalid path:', path);
        sectionText.innerHTML = `<p style="color:red;">Invalid path: ${path}</p>`;
    }
}

// ======================= BIND ======================= //
function bindBlogLinks() {
    const links = document.querySelectorAll('.blog-list-item a');
    links.forEach(link => {
        link.addEventListener('click', async event => {
            event.preventDefault(); 
            const blogId = link.getAttribute('data-blog-id'); 
            if (!blogId) {
                console.error('Blog ID not found for link:', link);
                return;
            }
            console.log("Clicked blog ID:", blogId);
            
            let blogContent = await getBlogContent(`/blogs/content/${blogId}`);
            loadBlogContent(blogContent);
        });
    });
}

// ======================= GET CONTENT ======================= //

async function getLocalPage(filePath) {
    sectionText.innerHTML = '<p>Loading...</p>';
    console.log(`get local page from: ${filePath}`);

    try {
        const response = await fetch(filePath);
        if (!response.ok) throw new Error('Page not found (404)');
        console.log(`success for getting local page: ${filePath}`);

        return await response.text();
    } catch (error) {
        console.error('Loading failed:', error);
        sectionText.innerHTML = `<p style="color:red;">Loading failed: ${error.message}</p>`;
    }
}

async function getBlogList(apiPath){
    sectionText.innerHTML = '<p>Loading...</p>';
    const fullUrl = CONFIG.API_BASE_URL + apiPath;

    console.log(`get blog list from: ${fullUrl}`);

    try {
        const response = await fetch(fullUrl);
        if (!response.ok) throw new Error('Blog list not found (404)');
        console.log(`success for getting blog list: ${fullUrl}`);

        const blogList = await response.json();
        return blogList.data;
    } catch (error) {
        console.error('Loading blog list failed:', error);
        sectionText.innerHTML = `<p style="color:red;">Loading blog list failed: ${error.message}</p>`;
    }
}

async function getBlogContent(apiPath) {
    sectionText.innerHTML = '<p>Loading...</p>';
    const fullUrl = CONFIG.API_BASE_URL + apiPath;

    console.log(`Loading blog content from: ${fullUrl}`);

    try {
        const response = await fetch(fullUrl);
        if (!response.ok) throw new Error('Blog content not found (404)');
        console.log(`success for getting blog content: ${fullUrl}`);

        const blogContent = await response.json();
        return blogContent.data;
    } catch (error) {
        console.error('Loading blog content failed:', error);
        sectionText.innerHTML = `<p style="color:red;">Loading blog content failed: ${error.message}</p>`;
    }
}

// ======================= LOAD CONTENT ======================= //
function loadLocalPage(data) {
    sectionText.innerHTML = marked.parse(data);
}

function loadBlogList(data) {
    const blogArray = data;

    // operate on each element of the array [{}, {}, {}]
    const htmlList = blogArray.map(blog => {
        return `
            <li class="blog-list-item"> --
                <a href="#" data-blog-id="${blog.id}" class="blog-link">
                ${blog.name}</a>
            </li>
        `;
    });
    const finalHtml = `<div class="blog-list"><ul>${htmlList.join('')}</ul></div>`;

    sectionText.innerHTML = finalHtml;

    bindBlogLinks();
}

function loadBlogContent(data) {
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

    let html = marked.parse(dataWithoutMath);

    mathBlocks.forEach((math, index) => {
        html = html.replace(`@@MATH-${index}@@`, () => math); // replace placeholder with mathBlocks
    });
    
    sectionText.innerHTML = html; 

    // ======================= RENDER ======================= //
    renderMath(sectionText);
    renderCode();
}

// ======================= FUNCTION ======================= //
function renderCode() {
    if (typeof hljs !== 'undefined') {
        hljs.highlightAll();
    }
}
function renderMath(data){
    renderMathInElement(data, {delimiters: CONFIG.MATH_DELIMITERS});
}