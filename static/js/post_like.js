const handleLikeClick = (buttonId) => {
    console.log(buttonId);

    const likeButton = document.getElementById(buttonId);
    console.log(likeButton);
    const likeIcon = likeButton.querySelector("i");
    console.log(likeIcon);
    likeIcon.classList.replace("fa-heart-o", "fa-heart")

}