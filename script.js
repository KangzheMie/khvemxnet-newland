document.addEventListener("DOMContentLoaded", function () {
    var sections = document.querySelectorAll("section");
    var navLinks = document.querySelectorAll("nav a");

    var logContent = document.getElementById("logContent");
    var pagination = document.getElementById("pagination");

    var logsPerPage = 5; // 每页显示的日志条目数
    var currentPage = 1;

    // 隐藏除第一个文章区域之外的所有区域
    for (var i = 1; i < sections.length; i++) {
        sections[i].style.display = "none";
    }

    // 为每个链接添加点击事件监听器
    navLinks.forEach(function (link, index) {
        link.addEventListener("click", function (event) {
            sections.forEach(function (section) {
                section.style.display = "none";
            });
            sections[index].style.display = "block";
        });
    });

    // 加载日志内容
    function loadLogs() {
        fetch('./logs/log.txt')
            .then(response => response.text())
            .then(data => {
                displayLogs(data);
            })
            .catch(error => console.error('Error loading logs:', error));
    }

    // 显示日志内容
    function displayLogs(logText) {
        var logs = logText.split('##');
        logs.shift(); // 移除第一个空元素，因为日志以##开头

        var totalPages = Math.ceil(logs.length / logsPerPage);

        // 根据当前页码和每页显示的日志条目数计算起始和结束索引
        var startIndex = (currentPage - 1) * logsPerPage;
        var endIndex = startIndex + logsPerPage;

        // 获取当前页的日志条目
        var currentLogs = logs.slice(startIndex, endIndex);

        // 将日志内容显示在页面上
        logContent.innerHTML = currentLogs.map(log => formatLogEntry(log)).join('');

        // 显示页码
        displayPagination(totalPages);
    }

    // 格式化日志条目，加粗时间
    function formatLogEntry(log) {
        var lines = log.trim().split('\n');
        var formattedTime = lines.shift().replace(/(\d{4}-\d{2}-\d{2})/, '<strong>$1</strong>'); // 加粗时间

        return `<div class="log-entry"><p>${formattedTime}</p><p>${lines.join('<br>')}</p></div>`;
    }

    // 显示分页
    function displayPagination(totalPages) {
        pagination.innerHTML = '';

        // 添加第一页链接
        pagination.innerHTML += `<a href="#" onclick="changePage(1)">第一页</a> | `;

        // 添加中间页码链接
        for (var i = 1; i <= totalPages; i++) {
            pagination.innerHTML += `<a href="#" onclick="changePage(${i})">${i}</a> | `;
        }

        // 添加最后一页链接
        pagination.innerHTML += `<a href="#" onclick="changePage(${totalPages})">最后一页</a>`;
    }

    // 切换页码
    window.changePage = function (page) {
        currentPage = page;
        loadLogs();
    };

    // 初始化加载日志
    loadLogs();
});