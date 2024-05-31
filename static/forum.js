const posts = [
    {
        'title': '如何學習Python？',
        'author': '123',
        'content': '我是一個初學者，希望了解如何開始學習Python。有哪些資源可以推薦？'
    },
    {
        'title': '最近的科技新聞',
        'author': '456',
        'content': '有誰關注了最近的科技新聞？AI的最新應用有哪些值得注意的？'
    },
    {
        'title': '最近的科技新聞',
        'author': '456',
        'content': '有誰關注了最近的科技新聞？AI的最新應用有哪些值得注意的？'
    },
    {
        'title': '最近的科技新聞',
        'author': '456',
        'content': '有誰關注了最近的科技新聞？AI的最新應用有哪些值得注意的？'
    },
    {
        'title': '最近的科技新聞',
        'author': '456',
        'content': '有誰關注了最近的科技新聞？AI的最新應用有哪些值得注意的？'
    }
]

function renderPosts() {
    const postsContainer = document.getElementById('posts');

    for (let i = 0; i < posts.length; i++) {
        let post = '';

        post += '<div class="post">';
        post += `<h3>${posts[i].title}</h3>`;
        post += `<p>${posts[i].content}</p>`;
        post += `<div class="post-author"><span>— ${posts[i].author}</span></div></div>`;

        postsContainer.innerHTML += post;
    }
}

renderPosts();
