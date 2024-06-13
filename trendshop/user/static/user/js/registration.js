    $(document).ready(function() {

        $('#id_user_types').on('change', function() {
            if ($(this).val() == 'buyer') {
                $('#signup-button').show();

            }
            else if ($(this).val() == 'seller') {
                $('#gst-field').show();
                $('#gst-label').show();
                $('#signup-button').show();

            }
        });
    });