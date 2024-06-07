function createNavbar(username) {
    navbarHtml = ''
    if (username == 'Guest') {
        navbarHtml = `
        <nav class="navbar">
            <div class="nav-left">
                <a href="/home">CodeSphere</a>
                <a href="/display">Posts</a>
                <a href="/forum">Forum</a>
                <a href="/yt">youtube extension</a>
                <a href="/eeclasslogin">eeclass extension</a>
            </div>
            <div class="nav-right">
                <a href="/profile">訪客</a>
                <a href="/entrance">Login</a>
                <a href="/register">Register</a>
            </div>
        </nav>
        `;
    }
    else {
        navbarHtml = `
            <nav class="navbar">
                <div class="nav-left">
                    <a href="/home">CodeSphere</a>
                    <a href="/display">Posts</a>
                    <a href="/forum">Forum</a>
                    <a href="/yt">youtube extension</a>
                    <a href="/eeclasslogin">eeclass extension</a>
                </div>
                <div class="nav-right">
                    <a href="/profile">${username}</a>
                    <a href="/logout">Logout</a>
                </div>
            </nav>
        `;
    }

//${username}
    // 选择一个元素来插入导航栏
    const headerElement = document.querySelector('body');
    headerElement.insertAdjacentHTML('beforebegin', navbarHtml);
}

// 当文档加载完成后，调用 createNavbar 函数
document.addEventListener('DOMContentLoaded', function() {
    createNavbar(window.username);
});
