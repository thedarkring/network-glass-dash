var getDevice = function (pk) {
    $.ajax({
        type: 'post',
        dataType: 'html',
        data: {
            // Attach CSRF token to POST, because we are not using a form  
            csrfmiddlewaretoken: $('#csrf').attr('value'),
            pk: pk,
            action: $('#action').val(),
            commands: $('#commands').val(),

        },
        success: function (html) {
            $(`#device-${pk}-tbody`).html(html);
            console.log(html)
            $(`#${pk}`).dataTable({
                searching: false,
                ordering:  true,
                paging: false,
                info: false,
        });
        }
    });
};
$('table').each(function () {
    table_pk = $(this).attr('id');
    getDevice(table_pk)
});