document.getElementById('logoutLink').addEventListener('click', function (event) {
    event.preventDefault();
    document.getElementById('logoutForm').submit();
    console.log('logoutForm submitted');
});
console.log('logout.js loaded');