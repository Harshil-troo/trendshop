    $(document).ready(function() {
        $('#id_user_types').on('change', function() {
            if ($(this).val() == 'buyer') {
                $('#gst-field').hide();
            }
            else if ($(this).val() == 'seller') {
                $('#gst-field').show();
            }
        });
    });