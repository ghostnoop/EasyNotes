// push_btn

$(document).ready(function () {
    $( "#cke_38" ).remove();
    $('#push_btn').click(function () {

        var d = $('#form_push').serializeArray();
        var value = CKEDITOR.instances['id_note_text'].getData();

        $.ajax({
            url: '/ajax',
            data: {
                'd': d,
                'rich': value
            },
            dataType: 'json',
            success: function (data) {
                if (data.is_taken) {
                    var pathname = window.location.pathname;
                    if (pathname === '/board/') {
                        location.reload()
                    }
                } else {
                    // $('.toast').toast(option)
                    $('.bd-example-modal-sm').modal('show').delay(500).modal('hide');

                    setTimeout(function () {
                        $('.bd-example-modal-sm').modal('hide');
                    }, 5000);
                    //    alert not full data
                }
            }

        });
    });
    $('#exampleModal').on('show.bs.modal', function (event) {
            var button = $(event.relatedTarget);
            var recipient = button.data('whatever');
            var modal = $(this);
            modal.find('.modal-title').text('New message to ' + recipient);
            modal.find('.modal-body input').val(recipient)
        })
});


