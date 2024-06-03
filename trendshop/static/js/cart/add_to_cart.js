$(document).ready(function() {
    $(".add-to-cart-form").on("submit", function(event) {
        event.preventDefault();
        var form = $(this);
        var formData = form.serializeArray();
        var cartItemQuantity = document.getElementById('cartItemQuantity');
        var cartItemQuantityValue = cartItemQuantity.innerHTML;
        $.ajax({
            url: form.attr("action"),
            method: "POST",
            dataType: "json",
            data: formData,
            }).done(function(mydata) {
                getToasterMessage(mydata.status, mydata.message);
                cartItemQuantityValue = parseInt(cartItemQuantityValue) + parseInt(formData[1]['value']);
                cartItemQuantity.innerHTML = cartItemQuantityValue;
                form[0].reset();
            });
    })
});
