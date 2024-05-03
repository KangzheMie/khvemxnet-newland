document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme');
    const savedHighlight = localStorage.getItem('highlight');
    if (savedTheme) {
        switchTheme(savedTheme, false); // 应用保存的主题
    }
    if (savedHighlight) {
        switchHighlight(savedHighlight, false); // 应用保存的主题
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