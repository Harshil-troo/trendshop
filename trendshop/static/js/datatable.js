$(document).ready(function() {
    $('#datatable tfoot th').each(function() {
        var title = $(this).text();
        if (title == 'Actions') {
            $(this).html('<input type="text" placeholder="No Search Available" style="min-width: 100%" disabled/>');
        }
        else {
            $(this).html('<input type="text" placeholder="Search ' + title + '" style="min-width: 100%"/>');
        }
    });
    var table = $('#datatable').DataTable({
        searching: true,
        paging: true,
        pageLength: 9,
        lengthChange: true,
        responsive: true,
        autoWidth: true,
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
