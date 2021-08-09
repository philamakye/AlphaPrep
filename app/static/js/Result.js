document.getElementById("reviewBtn").addEventListener('click', function() {
    document.querySelector(".answeredQs").style.display = "flex"
});
document.querySelector(".closeBtn").addEventListener('click', function() {
    document.querySelector(".answeredQs").style.display = "none"
})