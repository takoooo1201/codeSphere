/*
// Initialize with some sample data for testing
let posts = [
    {title: '123', summary: 'test', content: '<p>123</p>\n'},
    {title: '456', summary: 'test', content: '<p>456</p>\n'}
];

// Render posts
const postsContainer = document.getElementById('posts-container');

posts.forEach((post, index) => {
    const postDiv = document.createElement('div');
    postDiv.className = 'post';
    postDiv.dataset.index = index; // Add a custom data attribute to identify posts

    const postTitle = document.createElement('h2');
    postTitle.className = 'post-title';
    postTitle.innerText = post.title;

    const postSummary = document.createElement('h3');
    postSummary.className = 'post-summary';
    postSummary.innerText = post.summary;

    postDiv.appendChild(postTitle);
    postDiv.appendChild(postSummary);

    postDiv.style.cursor = 'pointer'; // Make it look clickable

    postDiv.addEventListener('click', function() {
        // Save selected post to localStorage
        localStorage.setItem('selectedPost', JSON.stringify(post));
        window.location.href = 'postPage.html'; // Navigate to postPage
    });

    postsContainer.appendChild(postDiv);
});
*/
//

// Search function
function filterPosts() {
    const query = document.getElementById('search-bar').value.toLowerCase();
    const filteredPosts = posts.filter(post =>
        post.title.toLowerCase().includes(query) ||
        post.content.toLowerCase().includes(query)
    );
    renderPosts(filteredPosts);
}



// decode from here
// let posts = [
//     {title: '123', summary: 'test summary 1', tag: 'javascript', content: '<p>123</p>\n'},
//     {title: '456', summary: 'test summary 2', tag: 'html', content: '<p>456</p>\n'},
// ];

// // Function to render posts
// function renderPosts(filteredPosts) {
//     const postsContainer = document.getElementById('posts-container');
//     postsContainer.innerHTML = '';

//     filteredPosts.forEach((post, index) => {
//         const postDiv = document.createElement('div');
//         postDiv.className = 'post';
//         postDiv.dataset.index = index; // Add a custom data attribute to identify posts

//         const postTitle = document.createElement('h2');
//         postTitle.className = 'post-title';
//         postTitle.innerText = post.title;

//         const postSummary = document.createElement('h3');
//         postSummary.className = 'post-summary';
//         postSummary.innerText = post.summary;

//         const postTag = document.createElement('p');
//         postTag.className = 'post-tag';
//         postTag.innerText = `Tag: ${post.tag}`;

//         postDiv.appendChild(postTitle);
//         postDiv.appendChild(postSummary);
//         postDiv.appendChild(postTag);

//         postDiv.addEventListener('click', function() {
//             // Save selected post to localStorage
//             localStorage.setItem('selectedPost', JSON.stringify(post));
//             window.location.href = './../post/postPage.html'; // Navigate to postPage
//         });

//         postsContainer.appendChild(postDiv);
//     });
// }

// // Search function
// function filterPosts() {
//     const query = document.getElementById('search-bar').value.toLowerCase();
//     const filteredPosts = posts.filter(post =>
//         post.title.toLowerCase().includes(query) ||
//         post.summary.toLowerCase().includes(query) ||
//         post.tag.toLowerCase().includes(query)
//     );
//     renderPosts(filteredPosts);
// }

// // Initially render all posts
// renderPosts(posts);

