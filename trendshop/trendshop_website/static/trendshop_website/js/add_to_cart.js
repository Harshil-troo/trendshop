$(document).ready(function() {
    $("#add-to-cart-button").on("click", function(event) {
        var form = $(this);

        for (key of document.cookie.split(';')) {
          if (key.includes("csrftoken"))  {
          // This is the csrftoken
          var csrfToken =  key.split("=")[1]

          }
        }
        $.ajax({
        type: "POST",
        url:this.getAttribute("data-link"),
        headers: {'X-CSRFToken': csrfToken },
        contentType: "application/json; charset=utf-8",
        data: null,
        success: function(response) {
        window.location.href = response.success_url;
        },
        error: function(response) {
            console.log(response);
        }
});
    })
});
