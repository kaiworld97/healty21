// const handleLikeClick = (buttonId) => {
//     console.log(buttonId);
//     const likeButton = document.getElementById(buttonId);
//     console.log(likeButton);
//     const likeIcon = likeButton.querySelector("i");
//     console.log(likeIcon);
//     likeIcon.classList.replace("fa-heart-o", "fa-heart")
// }

document.querySelector('.btnUpdate').addEventListener('click', e => {
    let content = document.querySelector('.comment_content');
    let btnSubmit = document.querySelector('.btnSubmit');
    let btnUpdate = document.querySelector('.btnUpdate');

    content.readOnly = false;

    btnSubmit.style.display = 'inline-block';
    btnUpdate.style.display = 'none';
})
