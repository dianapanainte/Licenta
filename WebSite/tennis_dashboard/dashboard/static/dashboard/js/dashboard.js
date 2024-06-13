var select = document.getElementById("player1");
var newOptions = ["Toyota", "Ford", "Honda", "BMW", "Audi", "Mercedes", "Tesla", "Ford", "Honda", "BMW", "Audi", "Mercedes", "Tesla", "Ford", "Honda", "BMW", "Audi", "Mercedes", "Tesla", "Ford", "Honda", "BMW", "Audi", "Mercedes", "Tesla", "Ford", "Honda", "BMW", "Audi", "Mercedes", "Tesla"];

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
var newOptions2 = ["Toyota", "Ford", "Honda", "BMW", "Audi", "Mercedes", "Tesla"];

newOptions2.forEach(function (optionText) {
    var option = document.createElement("option");
    option.text = option.value = optionText;
    select2.appendChild(option);
});