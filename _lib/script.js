document.addEventListener('DOMContentLoaded', function() {
    loadComponent('header', './module/header.html');
    loadComponent('navbar', './module/navbar.html');
    loadComponent('footer', './module/footer.html');
    loadContent('./module/mainPage.html'); // 加载默认内容
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

function loadComponent(componentId, componentUrl) {
    fetch(componentUrl).then(function(response) {
        return response.text();
    }).then(function(html) {
        document.getElementById(componentId).innerHTML = html;
    }).catch(function(err) {
        console.warn('Component failed to load', err);
    });
}

function loadContent(contentUrl) {
    fetch(contentUrl).then(function(response) {
        return response.text();
    }).then(function(html) {
        document.getElementById('content').innerHTML = html;
        renderMath();
    }).catch(function(err) {
        console.warn('Component failed to load', err);
    });
}

// 监听导航点击事件
document.body.addEventListener('click', function(event) {
    if (event.target.matches('nav .alink')) {
        event.preventDefault(); // 阻止链接默认行为
        const contentUrl = event.target.getAttribute('href') || './module/blank.html';
        loadContent(contentUrl);
    }
});

// 监听header a点击事件
document.body.addEventListener('click', function(event) {
    if (event.target.matches('header a')) {
        event.preventDefault(); // 阻止链接默认行为
        const contentUrl = event.target.getAttribute('href') || './module/blank.html';
        loadContent(contentUrl);
    }
});


// 监听timeline点击事件
document.body.addEventListener('click', function(event) {
    if (event.target.matches('.timeline a')) {
        event.preventDefault(); // 阻止链接默认行为
        const contentUrl = event.target.getAttribute('href') || './module/blank.html';
        loadContent(contentUrl);
    }
});

// 切换主题
// 在页面加载时检查并应用保存的主题
document.addEventListener('DOMContentLoaded', (event) => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        switchTheme(savedTheme, false); // 应用保存的主题，不重新保存到localStorage
    }
});

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
