function createNavbar(username) {
    const navbarHtml = `
        <nav class="navbar">
            <div class="nav-left">
                <a href="./../home/homePage.html">CodeSphere</a>
                <a href="./../profile-detailed/profile.html">Profile</a>
                <a href="./../display-post/displayPage.html">Posts</a>
                <a href="./../forum/forum.html">Forum</a>
            </div>
            <div class="nav-right">
                <a href="/profile">${username}</a>
                <a href="./../entrance/entrancePage.html">Login</a>
                <a href="./../register/registerPage.html">Register</a>
            </div>
        </nav>
    `;

    // 选择一个元素来插入导航栏
    const headerElement = document.querySelector('body');
    headerElement.insertAdjacentHTML('beforebegin', navbarHtml);
}

// 当文档加载完成后，调用 createNavbar 函数
document.addEventListener('DOMContentLoaded', function() {
    createNavbar(window.username);
});

// function createNavbar() {
//     const navbarHtml = `
//         <nav class="navbar">
//             <div class="nav-left">
//                 <a href="./../home/homePage.html">CodeSphere</a>
//                 <a href="./../profile-detailed/profile.html">Profile</a>
//                 <a href="./../display-post/displayPage.html">Posts</a>
//                 <a href="./../forum/forum.html">Forum</a>
//             </div>
//             <div class="nav-right">
//                 <a href="./../entrance/entrancePage.html">Login</a>
//                 <a href="./../register/registerPage.html">Register</a>
//             </div>
//         </nav>
//     `;

//     // 选择一个元素来插入导航栏
//     const headerElement = document.querySelector('body');
//     headerElement.insertAdjacentHTML('beforebegin', navbarHtml);
// }

// // 当文档加载完成后，调用 createNavbar 函数
// document.addEventListener('DOMContentLoaded', createNavbar);
