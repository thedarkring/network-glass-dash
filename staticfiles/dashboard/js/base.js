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
        checked_boxes = $('input[type="checkbox"]:checked').length
        if (checked_boxes == 0) {
            $('#bulk-menu').css('visibility', 'hidden');
        } else {
            $('#bulk-menu').css('visibility', 'visible');
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