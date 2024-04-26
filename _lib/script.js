document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme');
    const savedHighlight = localStorage.getItem('highlight');
    if (savedTheme) {
        switchTheme(savedTheme, false); // 应用保存的主题
    }
    if (savedHighlight) {
        switchHighlight(savedHighlight, false); // 应用保存的主题
    }

    // 解析URL参数获取'page'值
    const urlParams = new URLSearchParams(window.location.search);
    const page = urlParams.get('page');

    // 根据'page'参数的值来动态加载相应的HTML内容
    if (page) {
        const contentPath = `${page}`; // 构造内容文件的路径
        loadContent(contentPath);
    }else{
        loadContent('./mainPage.html'); // 加载默认内容
    }

    // 创建一个新的AJAX请求
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'counter.php'); // 指定请求的类型和URL
    xhr.onload = function() {
        if (xhr.status === 200) {
            // 请求成功，将返回的文本设置到div中
            document.getElementById('visitorCount').innerText = xhr.responseText;
        } else {
            // 出错时的处理
            document.getElementById('visitorCount').innerText = "???";
        }
    };
    xhr.send(); // 发送请求
});

function renderMath() {
    var mathElements = document.getElementsByClassName("math");
    var macros = {}; // 确保宏是一个对象，而不是数组
    for (var i = 0; i < mathElements.length; i++) {
        var texText = mathElements[i].firstChild;
        if (mathElements[i].tagName === "SPAN") {
            katex.render(texText.data, mathElements[i], {
                displayMode: mathElements[i].classList.contains('display'),
                throwOnError: false,
                macros: macros,
                fleqn: false
            });
        }
    }
}

function loadContent(contentUrl) {
    fetch(contentUrl).then(function(response) {
        return response.text();
    }).then(function(html) {
        document.getElementById('content').innerHTML = html;
        renderMath();
        // 使用pushState来更改URL，而不重新加载页面
        history.pushState({ path: contentUrl }, '', contentUrl);
    }).catch(function(err) {
        console.warn('Component failed to load', err);
    });
}

window.addEventListener('popstate', function(event) {
    // 检查event.state是否存在，如果存在，则加载对应的内容
    if(event.state && event.state.path) {
        loadContent(event.state.path);
    }
});


// 监听导航点击事件
document.body.addEventListener('click', function(event) {
    if (event.target.matches('nav .alink')) {
        event.preventDefault(); // 阻止链接默认行为
        const contentUrl = event.target.getAttribute('href') || './blank.html';
        loadContent(contentUrl);
    }
});

// 监听header a点击事件
document.body.addEventListener('click', function(event) {
    if (event.target.matches('header a')) {
        event.preventDefault(); // 阻止链接默认行为
        const contentUrl = event.target.getAttribute('href') || './blank.html';
        loadContent(contentUrl);
    }
});


// 监听timeline点击事件
document.body.addEventListener('click', function(event) {
    if (event.target.matches('.timeline a')) {
        event.preventDefault(); // 阻止链接默认行为
        const contentUrl = event.target.getAttribute('href') || './blank.html';
        loadContent(contentUrl);
    }
});

// 切换主题
function switchTheme(themeFileName, save = true) {
    // 更改主题
    var themeLink = document.getElementById('theme-css');
    if (themeLink) {
        themeLink.href = themeFileName;
    }
    // 如果需要，保存主题偏好到 localStorage
    if (save) {
        localStorage.setItem('theme', themeFileName);
    }
}

function switchHighlight(themeFileName, save = true) {
    // 更改主题
    var themeLink = document.getElementById('highlight-css');
    if (themeLink) {
        themeLink.href = themeFileName;
    }
    // 如果需要，保存主题偏好到 localStorage
    if (save) {
        localStorage.setItem('highlight', themeFileName);
    }
}
