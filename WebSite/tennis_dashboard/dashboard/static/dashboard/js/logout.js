document.getElementById('logoutLink').addEventListener('click', function (event) {
    event.preventDefault();  // Prevent the default action
    document.getElementById('logoutForm').submit();  // Submit the hidden form
    console.log('logoutForm submitted');
});
console.log('logout.js loaded');