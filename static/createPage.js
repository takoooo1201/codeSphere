// Initialize an empty array to store posts and drafts
let posts = [];
let drafts = [];



document.getElementById('postForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const title = document.getElementById('title').value;
    const content = document.getElementById('content').value;
    const summary = document.getElementById('summary').value;
    
    if (title && content) {
        const newPost = {
            title: title,
            summary: summary,
            content: marked.parse(content)
        };

        posts.push(newPost);
        document.getElementById('title').value = '';
        document.getElementById('summary').value = '';
        document.getElementById('content').value = '';

        // Save the posts array to localStorage
        //localStorage.setItem('posts', JSON.stringify(posts));

        console.log("Posts:", posts);
    }
});

document.getElementById('saveDraftBtn').addEventListener('click', function() {
    const title = document.getElementById('title').value;
    const summary = document.getElementById('summary').value;
    const content = document.getElementById('content').value;
    
    
    if (title && content) {
        const newDraft = {
            title: title,
            summary: summary,
            content: content // No markdown parsing for drafts
        };

        drafts.push(newDraft);
        document.getElementById('title').value = '';
        document.getElementById('summary').value = '';
        document.getElementById('content').value = '';

        console.log("Drafts:", drafts);
    }
});


