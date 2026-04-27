// local environment check
const isLocal = window.location.hostname === 'localhost';

// default config
const CONFIG = {
    API_BASE_URL: isLocal ? 'http://127.0.0.1:8000/api' : 'https://newland.khvemx.work/api',
    BASE_URL: isLocal ? window.location.origin : 'https://newland.khvemx.work',
    MATH_DELIMITERS: [
        { left: "$$", right: "$$", display: true },
        { left: "$", right: "$", display: false },
        { left: "\\(", right: "\\)", display: false },
        { left: "\\[", right: "\\]", display: true }
    ]
};
// the container of the section text
const sectionText = document.querySelector('#content #section-text');
// Blog List Loading
const blogListLinks = document.querySelectorAll('#header nav a');
blogListLinks.forEach(link => {
    link.addEventListener('click', event => {
        const targetPath = link.getAttribute('href');

        if (targetPath && targetPath.startsWith('/')) {
            event.preventDefault(); // 阻止跳转
            navigate(targetPath);   // 召唤路由函数去干活！
        }
    });
});

navigate('/');

// Fuctions

function navigate(path) {
    if (path.startsWith('/blogs/category/') || path === '/blogs') {
        getBlogList(path);
    } else if (path === '/') {
        loadLocalPage(CONFIG.BASE_URL + '/_pages/home.md');
    } else if (path === '/about') {
        loadLocalPage(CONFIG.BASE_URL + '/_pages/about.md');
    } else {
        console.error('Invalid path:', path);
        sectionText.innerHTML = `<p style="color:red;">Invalid path: ${path}</p>`;
    }
}

function bindBlogLinks() {
    const links = document.querySelectorAll('.blog-list-item a');
    links.forEach(link => {
        link.addEventListener('click', event => {
            event.preventDefault(); 
            const blogId = link.getAttribute('data-blog-id'); 
            if (!blogId) {
                console.error('Blog ID not found for link:', link);
                return;
            }
            console.log("Clicked blog ID:", blogId);
            
            getBlogContent(`/blogs/content/${blogId}`);
        });
    });
}

function getBlogList(apiPath){
    sectionText.innerHTML = '<p>Loading blog list...</p>';
    const fullUrl = CONFIG.API_BASE_URL + apiPath;

    fetch(fullUrl)
        .then(response => response.json())
        .then(responseData => { 
            const blogArray = responseData.data;

            if (!blogArray || blogArray.length === 0) {
                sectionText.innerHTML = '<p>Currently no blog articles available.</p>';
                return;
            }

            // map is a method of Array
            const htmlList = blogArray.map(blog => {
                return `
                    <li class="blog-list-item"> --
                        <a href="#" data-blog-id="${blog.id}" class="blog-link">
                        ${blog.name}</a>
                    </li>
                `;
            });

            // union all htmlList
            const finalHtml = `<div class="blog-list"><ul>${htmlList.join('')}</ul></div>`;
            sectionText.innerHTML = finalHtml;
            bindBlogLinks();
        })
        .catch(error => {
            console.error('Loading blog list failed:', error);
            sectionText.innerHTML = `<p style="color:red;">Loading blog list failed: ${error.message}</p>`;
        });
}

function getBlogContent(apiPath) {
    sectionText.innerHTML = '<p>Loading blog content...</p>';
    const fullUrl = CONFIG.API_BASE_URL + apiPath;
    console.log(fullUrl);

    fetch(fullUrl)
        .then(response => response.json())
        .then(data => { 
            const mathBlocks = [];
            let dataWithoutMath = data.data;

            dataWithoutMath = dataWithoutMath.replace(/\$\$([\s\S]*?)\$\$/g, (match) => {
                mathBlocks.push(match); // find all mathBlocks in dataWithoutMath
                return `@@MATH-${mathBlocks.length - 1}@@`; // using placeholder to replace mathBlocks
            });
            dataWithoutMath = dataWithoutMath.replace(/\$([^\$\n]+?)\$/g, (match) => {
                mathBlocks.push(match); // find all inline mathBlocks in dataWithoutMath
                return `@@MATH-${mathBlocks.length - 1}@@`; // using placeholder to replace mathBlocks
            });

            let html = marked.parse(dataWithoutMath);
            mathBlocks.forEach((math, index) => {
                html = html.replace(`@@MATH-${index}@@`, () => math); // replace placeholder with mathBlocks
            });
            sectionText.innerHTML = html; 
            renderMathInElement(sectionText, {
                delimiters: CONFIG.MATH_DELIMITERS
            });
            highlightCode();
        })
        .catch(error => {
            console.error('Loading blog content failed:', error);
            sectionText.innerHTML = `<p style="color:red;">Loading blog content failed: ${error.message}</p>`;
        });
}

function loadLocalPage(filePath) {
    sectionText.innerHTML = '<p>Loading...</p>';
    console.log(filePath);
    
    fetch(filePath)
        .then(response => {
            if (!response.ok) throw new Error('Page not found (404)');
            return response.text();
        })
        .then(data => {
            sectionText.innerHTML = marked.parse(data);
        })
        .catch(error => {
            console.error('Loading failed:', error);
            sectionText.innerHTML = `<p style="color:red;">Loading failed: ${error.message}</p>`;
        });
}

function getNormalContent(apiPath) {
    sectionText.innerHTML = '<p>Loading normal content...</p>';
    const fullUrl = CONFIG.API_BASE_URL + apiPath;

    fetch(fullUrl)
        .then(response => response.text())
        .then(data => { 
            let html = marked.parse(data);
            sectionText.innerHTML = html; 
        })
        .catch(error => {
            console.error('Loading normal content failed:', error);
            sectionText.innerHTML = `<p style="color:red;">Loading normal content failed: ${error.message}</p>`;
        });
}

function highlightCode() {
    if (typeof hljs !== 'undefined') {
        hljs.highlightAll();
    }
}