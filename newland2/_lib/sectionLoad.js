// 加载contentUrl中的文本内容到<div id="section">中
function loadSection(contentUrl) {
    fetch(contentUrl).then(function(response) {
        // 返回值作为下一个.then的Promise链参数
        return response.text();
    }).then(function(htmltext) {
        document.getElementById('section').innerHTML = htmltext;
        // 使用HTML5 History API的 pushState 方法更新浏览器的地址栏，同时不重新加载页面。
        history.pushState({ path: contentUrl }, '', contentUrl);
    }).catch(function(err) {
        console.warn('Component failed to load', err);
    });
}

// 当页面加载后根据url中带有的page参数加载html内容到<div id="section">中
document.addEventListener('DOMContentLoaded', function() {
// 解析URL参数获取'page'值
const urlParams = new URLSearchParams(window.location.search);
const page = urlParams.get('page');

// 根据'page'参数的值来动态加载相应的HTML内容
    if (page) {
        const contentPath = `${page}`; // 构造内容文件的路径
        loadSection(contentPath);
    }else{
        loadSection('./ciallo.html'); // 加载默认内容
    }
});

// 监听导航点击事件 阻止页面重新加载 仅加载html文本到<div id="section">中
document.body.addEventListener('click', function(event) {
    if (event.target.matches('#nav .alink')) {
        // 阻止链接默认行为
        // 链接默认跳转到指定链接并重新加载页面
        event.preventDefault();
        // 阻止并根据#nav .alink中的href参数确定需要加载内容的对象
        const contentUrl = event.target.getAttribute('href') || './blank.html';
        // 调用loadSection直接加载href指定内容中的html文本，而不需要重新加载整个网页
        loadSection(contentUrl);
    }
});