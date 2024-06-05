document.addEventListener('DOMContentLoaded', function() {
    // Get the post ID from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const postId = urlParams.get('id');

    // Fetch the post data from the server
    fetch(`/post/${postId}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const post = data.post;
                document.getElementById('post-title').innerText = post.title;
                document.getElementById('post-summary').innerText = post.summary;
                document.getElementById('post-content').innerHTML = post.content;

                // Initialize comments
                const commentsContainer = document.getElementById('comments-container');
                data.comments.forEach(comment => {
                    const commentDiv = document.createElement('div');
                    commentDiv.innerText = comment.content;
                    commentsContainer.appendChild(commentDiv);
                });
            } else {
                console.error('Error fetching post:', data.message);
            }
        })
        .catch(error => console.error('Error:', error));

    // Initialize the like count
    let likeCount = 0;
    document.getElementById('like-button').addEventListener('click', function() {
        fetch(`/like/${postId}`, { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    likeCount++;
                    document.getElementById('like-count').innerText = likeCount;
                } else {
                    console.error('Error liking post:', data.message);
                }
            })
            .catch(error => console.error('Error:', error));
    });

    // Add comment functionality
    document.getElementById('add-comment-button').addEventListener('click', function() {
        const commentText = document.getElementById('comment-input').value;
        if (commentText) {
            fetch(`/comment/${postId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ comment: commentText })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        const commentsContainer = document.getElementById('comments-container');
                        const commentDiv = document.createElement('div');
                        commentDiv.innerText = commentText;
                        commentsContainer.appendChild(commentDiv);
                        document.getElementById('comment-input').value = '';
                    } else {
                        console.error('Error adding comment:', data.message);
                    }
                })
                .catch(error => console.error('Error:', error));
        }
    });
});

// document.addEventListener('DOMContentLoaded', function() {
//     // Retrieve the selected post ID from localStorage
//     const postId = localStorage.getItem('selectedPostId');
//     console.log(postId)

//     // Fetch the post data from the server
//     fetch(`/post/${postId}`)
//         .then(response => response.json())
//         .then(data => {
//             if (data.status === 'success') {
//                 const post = data.post;
//                 document.getElementById('post-title').innerText = post.title;
//                 document.getElementById('post-summary').innerText = post.summary;
//                 document.getElementById('post-content').innerHTML = post.content;

//                 // Initialize comments
//                 const commentsContainer = document.getElementById('comments-container');
//                 data.comments.forEach(comment => {
//                     const commentDiv = document.createElement('div');
//                     commentDiv.innerText = comment.content;
//                     commentsContainer.appendChild(commentDiv);
//                 });
//             } else {
//                 console.error('Error fetching post:', data.message);
//             }
//         })
//         .catch(error => console.error('Error:', error));

//     // Initialize the like count
//     let likeCount = 0;
//     document.getElementById('like-button').addEventListener('click', function() {
//         fetch(`/like/${postId}`, { method: 'POST' })
//             .then(response => response.json())
//             .then(data => {
//                 if (data.status === 'success') {
//                     likeCount++;
//                     document.getElementById('like-count').innerText = likeCount;
//                 } else {
//                     console.error('Error liking post:', data.message);
//                 }
//             })
//             .catch(error => console.error('Error:', error));
//     });

//     // Add comment functionality
//     document.getElementById('add-comment-button').addEventListener('click', function() {
//         const commentText = document.getElementById('comment-input').value;
//         if (commentText) {
//             fetch(`/comment/${postId}`, {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 body: JSON.stringify({ comment: commentText })
//             })
//                 .then(response => response.json())
//                 .then(data => {
//                     if (data.status === 'success') {
//                         const commentsContainer = document.getElementById('comments-container');
//                         const commentDiv = document.createElement('div');
//                         commentDiv.innerText = commentText;
//                         commentsContainer.appendChild(commentDiv);
//                         document.getElementById('comment-input').value = '';
//                     } else {
//                         console.error('Error adding comment:', data.message);
//                     }
//                 })
//                 .catch(error => console.error('Error:', error));
//         }
//     });
// });


// // Retrieve the selected post data from localStorage
// const post = JSON.parse(localStorage.getItem('selectedPost'));

// // Set the post details in the DOM
// document.getElementById('post-title').innerText = post.title;
// document.getElementById('post-summary').innerText = post.summary;
// document.getElementById('post-content').innerHTML = post.content;

// // Initialize the like count
// let likeCount = 0;
// document.getElementById('like-button').addEventListener('click', function() {
//     likeCount++;
//     document.getElementById('like-count').innerText = likeCount;
// });

// // Initialize the comments
// const commentsContainer = document.getElementById('comments-container');
// const comments = [];

// // Add comment functionality
// document.getElementById('add-comment-button').addEventListener('click', function() {
//     const commentText = document.getElementById('comment-input').value;
//     if (commentText) {
//         comments.push(commentText);
//         document.getElementById('comment-input').value = '';
//         renderComments();
//     }
// });

// // Function to render comments
// function renderComments() {
//     commentsContainer.innerHTML = '';
//     comments.forEach(comment => {
//         const commentDiv = document.createElement('div');
//         commentDiv.innerText = comment;
//         commentsContainer.appendChild(commentDiv);
//     });
// }