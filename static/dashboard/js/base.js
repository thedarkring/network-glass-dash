var instant_search = $('meta[name=instant_search]').attr("content");
var limit = $('meta[name=device_limit]').attr("content");
var checked_boxes = 0
var Search = function () {
    search_val = $('#search_field').val()
    var search_fn = $.fn.dataTable
        .tables({ 
            visible: true, 
            api: true 
        })
        .search(search_val).draw();
        $.when(search_fn).done(function () { 
            $( ".custom-checkbox:hidden input" ).prop( "checked", false );
            bulkMenu();
        });
};
var errorBulk = function () {
    console.log('Too many')
    $('#SitesDropdownMenuLink').prop('disabled', true);
    $('#SitesDropdownMenuLink').html(`Bulk Action (<font color="red">${checked_boxes}</font>/${limit})`);
};
var bulkMenu = function () {
    checked_boxes = $('input[type="checkbox"]:checked').length
    if (checked_boxes == 0) {
        $('#bulk-menu').css('visibility', 'hidden');
    } else {
        $('#bulk-menu').css('visibility', 'visible');
        $('#select-all').html('<i>select none</i>')
    };
    if (checked_boxes > limit) {
        errorBulk();
    } else {
        $('#SitesDropdownMenuLink').prop('disabled', false);
        $('#SitesDropdownMenuLink').html(`Bulk Action (${checked_boxes}/${limit})`);
    };
};
$( document ).ready(function() {
    $('.submit-nav-button').click(function () {
        action = $(this).data('action');
        single_pk = $(this).data('pk');
        if (single_pk) {
            $( ".device-checkbox" ).prop( "checked", false );
            $( `#bulk${single_pk}` ).prop( "checked", true );
        }
        var update_action = $('#action').val(action)
        console.log(`Submit nav clicked with action=${action}, clicking submit button`)
        if (action == 'get_command') {
            $('#commandExecutorModal').modal('toggle');
            command_handlers();
        } else {
            $.when(update_action).done(function () {
                $("#submit-button").trigger("click");
            });
        };
    });
    $('.device-checkbox').on("change", function () {
        bulkMenu();
    })
    $('#search').on('click', function () {
        Search();
    });
    $('#search_field').on('keyup', function (e) {
        if (e.which === 13 || instant_search == 'True'){
            Search();
        }
    });
    $('#select-all').on('click', function () { 
        if ($(this).html() == '<i>select all</i>') {
            $('.device-checkbox').each(function() {
                if ($(this).is(':visible')) {
                        $(this).prop('checked', true)
                } else {
                    $(this).prop('checked', false)
                };
            });
            bulkMenu();
        } else {
            $('.device-checkbox').prop('checked', false)
            $(this).html('<i>select all</i>')
            $('#bulk-menu').css('visibility', 'hidden');
        };
    })
});
var commands = []
var command_handlers = function() {
    $('#add-command').on('click', function () {
        command_input = $('#command-input').val()
        $('#command-input').val('')
        if (command_input != '') {
            $('#command-queue').show()
            $('#execute').prop('disabled', false);
            $('#command-chain').append(`<li class="list-group-item py-1 command disabled" value="${command_input}">${command_input}</li>`)
        } else {
            $('#command-input').attr("placeholder", "Invalid Command!");
        };
    })
    $('#execute').on('click', function () {
        console.log('Command loop started')
        $('.command').each(function (i) {
            command = $(this).attr("value");
            commands[i] = command;
            console.log(`Read command "${command}" position ${i} in array`)
        });
        console.log('Command loop completed')
        var add_to_form = function () {
            console.log(`Converting "commands" object to string`)
            commands_json = JSON.stringify(commands)
            $('#commands').val(commands_json);
            $('#action').val('get_command');
            console.log(`Finished updating "commands" and "action" fields`)
        };
        add_to_form();
        $('#commandExecutorModal').modal('toggle');
        $.when(add_to_form).done(function () {
            console.log(`Handler function complete, clicking submit`)
            $("#submit-button").trigger("click");
        });
    })
};
$('.submit-button').on('click', function () {
    var checks = $('input[type="checkbox"]:checked').map(function () {
        return $(this).val();
    }).get()
    console.log(checks);
    return values;
})

