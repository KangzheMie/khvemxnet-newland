document.addEventListener('DOMContentLoaded', (event) => {
    // 解析URL参数获取'page'值
    const urlParams = new URLSearchParams(window.location.search);
    const page = urlParams.get('page');
    const blog = urlParams.get('blog');

    // 根据'page'参数的值来动态加载相应的HTML内容
    if (page) {
        const contentPath = `/pages/${page}.md`;
        checkFileExistenceAndLoad(contentPath);
    } else if (blog) {
        const contentPath = `/blogs/${blog}.md`;
        checkFileExistenceAndLoad(contentPath);
    }
    else {
        checkFileExistenceAndLoad('./pages/ciallo.md');
    }
});

// 检查文件是否存在并加载内容
function checkFileExistenceAndLoad(path) {
    fetch(path)
    .then(response => {
        if (response.ok) {
            loadMarkdownFile(path);
        } else {
            console.warn(`File not found: ${path}. Loading default content.`);
            loadMarkdownFile('./pages/blank.md');
        }
    })
    .catch(error => {
        console.error(`Error fetching file: ${error}. Loading default content.`);
        loadMarkdownFile('./pages/blank.md');
    });
}

// 加载markdown文件
function loadMarkdownFile(MarkdownFileName){
    fetch(MarkdownFileName)
    .then(response => response.text())
    .then(text => {
        // 移除YAML头部
        const yamlEnd = text.indexOf('---', 3);
        if (yamlEnd !== -1) {
            text = text.substring(yamlEnd + 3); 
        }

        // 在页面上显示渲染后的HTML
        // 重载所有的<em> 输出为 _ ，因为在渲染数学公式的时候，傻逼 marked 无法处理很多的下标符号。
        // 例如 {A}_1 B_{i+1} 输出为{A}<em>1 B</em>{i+1}
        // 重载 em 渲染器解决问题
        const renderer = {
            em({ tokens }) {
                const text = this.parser.parseInline(tokens);
                return `_${text}_`;
            }
        };
        
        marked.use({renderer});

        const markedHtml = marked.parse(text);
        const section = document.getElementById('section-text');
        section.innerHTML = markedHtml;

        // 所有对于文本部分的渲染都给爷放到这里 //

            // 使用KaTeX渲染页面上的所有数学公式
            renderMathInElement(section, {
                delimiters: [
                    {left: "$$", right: "$$", display: true},  // 用于显示模式的数学公式
                    {left: "$", right: "$"  , display: false}, // 用于行内模式的数学公式
                ]
            });

            // 使用highlight渲染页面上所有的<pre><code>
            document.querySelectorAll('pre code').forEach((el) => {
                hljs.highlightElement(el);
            });
    })
    .catch(error => console.error('Error loading the Markdown file: ', error));
}
