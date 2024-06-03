const profile = {
    'avatar_url': 'https://picsum.photos/200/300',
    'name': '王小明',
    'gender': '男',
    'birthday': '1990年1月1日',
    'bio': '你好，我是王小明。我是一名軟體工程師，專注於前端和後端開發。我喜歡閱讀和旅遊。',
    'website_name': 'blog',
    'website_href': '#',
    'articles': 120,
    'likes': 3500,
    'comments': 890
}

const articles = [
    {
        'title': '如何成為一名前端開發者',
        'time': '2024-04-01',
        'href': '#'
    },
    {
        'title': '後端開發的最佳實踐',
        'time': '2024-03-15',
        'href': '#'
    },
    {
        'title': '全端開發介紹',
        'time': '2024-03-01',
        'href': '#'
    }
]

function renderProfile() {
    const avatar = document.getElementById('avatar');
    const info = document.getElementById('personal-info');
    const stats = document.getElementById('stats-row');

    // avatar.innerHTML = `<img id="avatar-image" src="${profile.avatar_url}" alt="頭像">`;
    
    // info.innerHTML += `<h2>姓名：${profile.name}</h2>`;
    // info.innerHTML += `<p><strong>性別：</strong>${profile.gender}</p>`;
    // info.innerHTML += `<p><strong>生日：</strong>${profile.birthday}</p>`;
    // info.innerHTML += `<p><strong>自我介紹：</strong>${profile.bio}</p>`;
    // info.innerHTML += `<p><p><strong>個人網站：</strong><a href="${profile.website_href}">${profile.website_name}</a></p></p>`

    // stats.innerHTML += `<td>${profile.articles}</td>`;
    // stats.innerHTML += `<td>${profile.likes}</td>`;
    // stats.innerHTML += `<td>${profile.comments}</td>`;
}

function renderArticlesList() {
    // const articlesList = document.getElementById('articles-list');
    // for (let i = 0; i < articles.length; i++) {
    //     articleContent = `<li><a href="${articles[i].href}">${articles[i].title}</a> - ${articles[i].time}</li>`
    //     articlesList.innerHTML += articleContent;
    // }
}

renderProfile();
renderArticlesList();
