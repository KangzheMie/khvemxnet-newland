document.addEventListener("DOMContentLoaded", function () {
    var sections = document.querySelectorAll("section");
    var navLinks = document.querySelectorAll("nav a");
    var subMenuLinks = document.querySelectorAll(".submenu a");

    var logsPerPage = 1; // 每页显示的日志条目数
    var currentPage = 1;
    var totalPages = 0; // 初始化 totalPages

    var initialLogFile = 'log1.txt'; // 举例，您需要根据实际情况来设置这个值
    var currentLogFile = initialLogFile; // 初始化为初始日志文件

    // 在全局声明 logContent 和 pagination
    var logContent;
    var pagination;

    // 隐藏除第一个文章区域之外的所有区域
    for (var i = 1; i < sections.length; i++) {
        sections[i].style.display = "none";
    }

    // 为每个链接添加点击事件监听器
    navLinks.forEach(function (link) {
        link.addEventListener("click", function (event) {
            event.preventDefault();

            var targetSection = link.getAttribute("href").slice(1);

            sections.forEach(function (section) {
                if (section.id === targetSection) {
                    section.style.display = "block";
                    // 在这里获取 logContent 和 pagination 元素
                    logContent = section.querySelector('.logContent-' + targetSection);
                    pagination = section.querySelector('.pagination-' + targetSection);
                } else {
                    section.style.display = "none";
                }
            });
        });
    });

    subMenuLinks.forEach(function (link) {
        link.addEventListener("click", function (event) {
            event.preventDefault();

            var targetSection = link.getAttribute("href").slice(1);
            var logFile = link.getAttribute("data-logfile");

            sections.forEach(function (section) {
                if (section.id === targetSection) {
                    section.style.display = "block";

                    // 在这里获取 logContent 和 pagination 元素
                    logContent = section.querySelector('.logContent-' + targetSection);
                    pagination = section.querySelector('.pagination-' + targetSection);

                    if (logFile) {
                        loadLogs(logFile); // 加载相应的日志文件
                    }

                    currentLogFile = logFile; // 更新当前日志文件变量
                    currentPage = 1;

                } else {
                    section.style.display = "none";
                }
            });
        });
    });

    function loadLogs(logFile) {
        fetch(`./logs/${logFile}`)
            .then(response => response.text())
            .then(data => {
                displayLogs(data);
                displayPagination(totalPages); // 移到这里
            })
            .catch(error => console.error('Error loading logs:', error));
    }

    // 显示日志内容
    function displayLogs(logText) {
        var logs = logText.split('##');
        logs.shift(); // 移除第一个空元素，因为日志以##开头

        totalPages = Math.ceil(logs.length / logsPerPage); // 将 totalPages 定义为全局变量

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

    // 切换页码
    function changePage(page) {
        currentPage = page;
        loadLogs(currentLogFile); // 直接调用 loadLogs
    };

    // 显示分页
    function displayPagination(totalPages) {
        pagination.innerHTML = ''; // 清空前一次的内容
    
        // 添加第一页链接
        createPageLink('第一页', 1);
    
        // 添加中间页码链接
        for (var i = 1; i <= totalPages; i++) {
            createPageLink(i, i);
        }
    
        // 添加最后一页链接
        createPageLink('最后一页', totalPages);
    }

    function createPageLink(text, pageNumber) {
        var pageLink = document.createElement('a');
        pageLink.href = '#';
        pageLink.textContent = text;
        pageLink.addEventListener('click', function () {
            changePage(pageNumber);
        });
        pagination.appendChild(pageLink);
    
        var separator = document.createTextNode(' | ');
        pagination.appendChild(separator);
    }

    // 初始化加载日志
    loadLogs(initialLogFile);
});
