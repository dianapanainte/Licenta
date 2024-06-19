var select = document.getElementById("player1");
var newOptions = [];

newOptions.forEach(function (optionText) {
    var option = document.createElement("option");
    option.text = option.value = optionText;
    select.appendChild(option);
});

$(document).ready(function () {
    $('.chosen-select').chosen({
        placeholder_text_single: 'Search for an option',
        no_results_text: 'No results found'
    });
});

// --------------------------------------------PLAYER 2 DROPDOWN--------------------------------------------

var select2 = document.getElementById("player2");
var newOptions2 = [];

newOptions2.forEach(function (optionText) {
    var option = document.createElement("option");
    option.text = option.value = optionText;
    select2.appendChild(option);
});


// ---------------------------------------- SHOW FUTURE TOURNAMENTS ----------------------------------------
document.addEventListener('DOMContentLoaded', function () {
    const showFutureTournamentsLink = document.getElementById('showFutureTournaments');
    const containerRight = document.querySelector('.container-right');
    const futureTournaments = document.querySelector('.future-tournaments');

    showFutureTournamentsLink.addEventListener('click', function (event) {
        event.preventDefault();
        containerRight.style.display = 'none';
        futureTournaments.style.display = 'flex';
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const showFutureTournamentsLink = document.getElementById('showPastTournaments');
    const containerRight = document.querySelector('.container-right');
    const futureTournaments = document.querySelector('.future-tournaments');

    showFutureTournamentsLink.addEventListener('click', function (event) {
        event.preventDefault();
        containerRight.style.display = 'flex';
        futureTournaments.style.display = 'none';
    });
});