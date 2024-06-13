$(document).ready(function() {
    $("#increaseQuantity").on("click", function increaseQuantity(id) {
        event.preventDefault();
        $.ajax({
            url: "/increase-quantity/" + id,
            type: 'POST',
            dataType: 'json',

            success: function() {

            }
        })
    });
});
