// Author: Jonathan Armoza
// Created: November 4, 2021
// Purpose: JS for the query demo

// Event listeners

$("#dataset-checkall").click(function () {
    $(".dataset-checkbox").prop('checked', $(this).prop('checked'));
});