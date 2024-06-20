document.addEventListener('DOMContentLoaded', function () {
    const openButtons = document.querySelectorAll('.btn-open-popover');
    const closeButtons = document.querySelectorAll('.btn-close-popover');

    openButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            $('.container-left').not($(this).closest('.container-left')).hide();

            const card = button.closest('.card');
            const popover = card.querySelector('.popover');
            popover.style.top = 120 + 'px';
            popover.classList.toggle('open');
            console.log("popover opened");
        });
    });

    closeButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            button.closest('.popover').classList.remove('open');
            $('.container-left').show();
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const openButtons = document.querySelectorAll('.btn-open-stats');
    const closeButtons = document.querySelectorAll('.btn-close-stats');

    openButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            $('.container-left').not($(this).closest('.container-left')).hide();

            const card = button.closest('.card');
            const popover = card.querySelector('.popover-stats');
            popover.style.top = 120 + 'px';
            popover.classList.toggle('open');
            console.log("popover-stats opened");
        });
    });

    closeButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            button.closest('.popover-stats').classList.remove('open');
            $('.container-left').show();
        });
    });
});


console.log("favourites.js loaded");
