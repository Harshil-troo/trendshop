function getResponseForSignup() {
    getToasterMessage("success", "Signed Up Successfully");
    setTimeout(function() {
    $("#signup").submit();
    }, 1000);
}

function getResponseForLogin() {
    getToasterMessage("success", "Logged In Successfully");
    setTimeout(function() {
    $("#login").submit();
    }, 1000);
}

function getResponseForProfileUpdate() {
    getToasterMessage("success", "Profile Updated Successfully");
    setTimeout(function() {
    $("#updateProfile").submit();
    }, 1000);
}

function getResponseForAddressUpdate() {
    getToasterMessage("success", "Address Updated Successfully");
    setTimeout(function() {
    $("#updateAddress").submit();
    }, 1000);
}

$(document).ready(function() {
    $('#datatable tfoot th').each(function() {
        var title = $(this).text();
        if (title == 'User Profile') {
            $(this).html('<input type="text" placeholder="No Search Available" style="min-width: 100%" disabled/>');
        }
        else {
            $(this).html('<input type="text" placeholder="Search ' + title + '" style="min-width: 100%"/>');
        }
    });
    var table = $('#datatable').DataTable({
        searching: true,
        paging: true,
        pageLength: 7,
        lengthChange: true,
        responsive: true,
        autoWidth: true,
        scrollCollapse: true,
        columnDefs: [{
            targets: 'actions',
            orderable: false
        }],
        initComplete: function() {
            this.api()
                .columns()
                .every(function() {
                    var that = this;
                    $('input', this.footer()).on('keyup change clear', function() {
                        if (that.search() !== this.value) {
                            that.search(this.value).draw();
                        }
                    });
                });
        },
    });
    $('#search').keyup(function() {
        table.search($(this).val()).draw();
    })
});
