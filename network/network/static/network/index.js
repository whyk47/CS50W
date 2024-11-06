document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.post').forEach(post => {
        try {
            var liked = post.querySelector('#liked').innerHTML === 'true';
            const id = parseInt(post.querySelector('#id').innerHTML);
            if (liked) {
                post.querySelector(`#like_${id}`).style.display = 'none';
                post.querySelector(`#unlike_${id}`).style.display = 'block';
            } else {
                post.querySelector(`#like_${id}`).style.display = 'block';
                post.querySelector(`#unlike_${id}`).style.display = 'none';
            }
        } catch(err) {} 
    });
    try {
        document.querySelectorAll('.edit').forEach(button => button.addEventListener('click', e => edit_post(parseInt(e.target.value))));
        document.querySelectorAll('.save').forEach(button => button.addEventListener('click', e => update_post(parseInt(e.target.value))));
    } catch(err) {}
    try {
        document.querySelectorAll('.like').forEach(button => button.addEventListener('click', e => like(parseInt(e.currentTarget.value))));
        document.querySelectorAll('.unlike').forEach(button => button.addEventListener('click', e => unlike(parseInt(e.currentTarget.value))));
    } catch(err) {}
});

// like post
function like(post_id) {
    console.log(post_id);
    document.querySelector(`#like_${post_id}`).style.display = 'none';
    document.querySelector(`#unlike_${post_id}`).style.display = 'block';
    document.querySelector(`#numlikes_${post_id}`).innerHTML++;
    fetch(`${post_id}`, {
        headers: {
            'X-CSRFTOKEN': document.querySelector("#csrf_token").innerHTML,
        },
        method: 'PUT',
        body: JSON.stringify({
            like: true
        })
    });
    return false;
}

// unlike post
function unlike(post_id) {
    console.log(post_id);
    document.querySelector(`#like_${post_id}`).style.display = 'block';
    document.querySelector(`#unlike_${post_id}`).style.display = 'none';
    document.querySelector(`#numlikes_${post_id}`).innerHTML--;
    fetch(`${post_id}`, {
        headers: {
            'X-CSRFTOKEN': document.querySelector("#csrf_token").innerHTML,
        },
        method: 'PUT',
        body: JSON.stringify({
            unlike: true
        })
    });
    return false;
}

// open textarea for edits
function edit_post(post_id) {
    document.querySelector(`#edit-view-${post_id}`).style.display = 'block';
    document.querySelector(`#content-view-${post_id}`).style.display = 'none';
    return false;
}

// update post according to edits
function update_post(post_id) {
    textarea = document.querySelector(`#textarea_${post_id}`);
    content = document.querySelector(`#content_${post_id}`);
    content.innerHTML = textarea.value;
    document.querySelector(`#edit-view-${post_id}`).style.display = 'none';
    document.querySelector(`#content-view-${post_id}`).style.display = 'block';
    console.log(textarea.value)
    fetch(`${post_id}`, {
        headers: {
            'X-CSRFTOKEN': document.querySelector("#csrf_token").innerHTML,
        },
        method: 'PUT',
        body: JSON.stringify({
            textarea: textarea.value
        })
    });
    return false;
}