// JavaScript

$(document).ready(function() {
    $('.button').each(function(){
        var attrib_id = $(this).attr('id');
        var entry_nbr = $(this).attr('entry_nbr');
        var star_nbr = $(this).attr('star_nbr');
        var gEBI_attrib_id = document.getElementById(attrib_id);
        var gEBI_star_1 = document.getElementById("button_"+entry_nbr+"_1");
        var gEBI_star_2 = document.getElementById("button_"+entry_nbr+"_2");
        var gEBI_star_3 = document.getElementById("button_"+entry_nbr+"_3");
        var gEBI_star_4 = document.getElementById("button_"+entry_nbr+"_4");
        var gEBI_star_5 = document.getElementById("button_"+entry_nbr+"_5");
        var gEBI_avg_rating = document.getElementById("avg_rating_"+entry_nbr);

        $(this).click(function(){
            // $('#'+toggle_div_id).toggle();
            // If star 1, turn star 1 gold and 2/3/4/5 gray
            if (star_nbr == 1) {
                // gEBI_star_1.style.color = "gold";
                gEBI_star_1.style.color = "gold"; gEBI_star_1.innerHTML = "★";
                gEBI_star_2.style.color = "gray"; gEBI_star_2.innerHTML = "☆";
                gEBI_star_3.style.color = "gray"; gEBI_star_3.innerHTML = "☆";
                gEBI_star_4.style.color = "gray"; gEBI_star_4.innerHTML = "☆";
                gEBI_star_5.style.color = "gray"; gEBI_star_5.innerHTML = "☆";
                gEBI_avg_rating.style.color = "gray";
            }
            // If star 2, turn star 1/2 gold and 3/4/5 gray
            if (star_nbr == 2) {
                gEBI_star_1.style.color = "gold"; gEBI_star_1.innerHTML = "★";
                gEBI_star_2.style.color = "gold"; gEBI_star_2.innerHTML = "★";
                gEBI_star_3.style.color = "gray"; gEBI_star_3.innerHTML = "☆";
                gEBI_star_4.style.color = "gray"; gEBI_star_4.innerHTML = "☆";
                gEBI_star_5.style.color = "gray"; gEBI_star_5.innerHTML = "☆";
                gEBI_avg_rating.style.color = "gray";
            }
            // If star 3, turn star 1/2/3 gold and 4/5 gray
            if (star_nbr == 3) {
                gEBI_star_1.style.color = "gold"; gEBI_star_1.innerHTML = "★";
                gEBI_star_2.style.color = "gold"; gEBI_star_2.innerHTML = "★";
                gEBI_star_3.style.color = "gold"; gEBI_star_3.innerHTML = "★";
                gEBI_star_4.style.color = "gray"; gEBI_star_4.innerHTML = "☆";
                gEBI_star_5.style.color = "gray"; gEBI_star_5.innerHTML = "☆";
                gEBI_avg_rating.style.color = "gray";
            }
            // If star 4, turn star 1/2/3/4 gold and 5 gray
            if (star_nbr == 4) {
                gEBI_star_1.style.color = "gold"; gEBI_star_1.innerHTML = "★";
                gEBI_star_2.style.color = "gold"; gEBI_star_2.innerHTML = "★";
                gEBI_star_3.style.color = "gold"; gEBI_star_3.innerHTML = "★";
                gEBI_star_4.style.color = "gold"; gEBI_star_4.innerHTML = "★";
                gEBI_star_5.style.color = "gray"; gEBI_star_5.innerHTML = "☆";
                gEBI_avg_rating.style.color = "gray";
            }
            // If star 5, turn star 1/2/3/4/5 gold
            if (star_nbr == 5) {
                gEBI_star_1.style.color = "gold"; gEBI_star_1.innerHTML = "★";
                gEBI_star_2.style.color = "gold"; gEBI_star_2.innerHTML = "★";
                gEBI_star_3.style.color = "gold"; gEBI_star_3.innerHTML = "★";
                gEBI_star_4.style.color = "gold"; gEBI_star_4.innerHTML = "★";
                gEBI_star_5.style.color = "gold"; gEBI_star_5.innerHTML = "★";
                gEBI_avg_rating.style.color = "gray";
            }
            // Clear stars (turn back to gray)
            if (attrib_id == "button_"+entry_nbr+"_clear") {
                gEBI_star_1.style.color = "gray"; gEBI_star_1.innerHTML = "☆";
                gEBI_star_2.style.color = "gray"; gEBI_star_2.innerHTML = "☆";
                gEBI_star_3.style.color = "gray"; gEBI_star_3.innerHTML = "☆";
                gEBI_star_4.style.color = "gray"; gEBI_star_4.innerHTML = "☆";
                gEBI_star_5.style.color = "gray"; gEBI_star_5.innerHTML = "☆";
                gEBI_avg_rating.style.color = "white";
            }
        });
        // ^ maybe can streamline further

        // Hover: To change color to gold when hover over
        $(this).hover(function(){
            if (gEBI_attrib_id.style.color == "gold") {
                gEBI_attrib_id.style.color = "gold"
            } else {
                gEBI_attrib_id.style.color = "goldenrod";
            }
        },
        // Unhover: Then to revert color to gray when uncover
        function(){
            if (gEBI_attrib_id.style.color == "gold") {
                gEBI_attrib_id.style.color = "gold";
            } else {
                gEBI_attrib_id.style.color = "gray";
            }
        });
    });
});
