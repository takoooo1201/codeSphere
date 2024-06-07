document.getElementById('postForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const title = document.getElementById('title').value;
    const content = document.getElementById('content').value;
    
    if (title && content) {
        fetch('/create_post', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: title,
                content: content,
                usrname: window.username
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Post published successfully!');
                window.location.href = '/display';
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }
});

document.getElementById('saveDraftBtn').addEventListener('click', function() {
    const title = document.getElementById('title').value;
    const content = document.getElementById('content').value;
    
    if (title && content) {
        const newDraft = {
            title: title,
            content: content // No markdown parsing for drafts
        };

        drafts.push(newDraft);
        document.getElementById('title').value = '';
        document.getElementById('content').value = '';

        console.log("Drafts:", drafts);
    }
});
// // Initialize an empty array to store posts and drafts
// let posts = [];
// let drafts = [];



// document.getElementById('postForm').addEventListener('submit', function(event) {
//     event.preventDefault();
    
//     const title = document.getElementById('title').value;
//     const content = document.getElementById('content').value;
//     // const summary = document.getElementById('summary').value;
    
//     if (title && content) {
//         const newPost = {
//             title: title,
//             // summary: summary,
//             content: marked.parse(content)
//         };

//         posts.push(newPost);
//         document.getElementById('title').value = '';
//         // document.getElementById('summary').value = '';
//         document.getElementById('content').value = '';

//         // Save the posts array to localStorage
//         //localStorage.setItem('posts', JSON.stringify(posts));

//         console.log("Posts:", posts);
//     }
// });

// document.getElementById('saveDraftBtn').addEventListener('click', function() {
//     const title = document.getElementById('title').value;
//     // const summary = document.getElementById('summary').value;
//     const content = document.getElementById('content').value;
    
    
//     if (title && content) {
//         const newDraft = {
//             title: title,
//             // summary: summary,
//             content: content // No markdown parsing for drafts
//         };

//         drafts.push(newDraft);
//         document.getElementById('title').value = '';
//         // document.getElementById('summary').value = '';
//         document.getElementById('content').value = '';

//         console.log("Drafts:", drafts);
//     }
// });


