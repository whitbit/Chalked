function showStates(results) {
    //shows list of states
    
    var states = results.states;

    $.each(states, function(index, state) {
        $('#state').append('<option value=' + state + '>' + state + '</option>');
    });
}

function getStates(evt) {
    //loads list of states

    $.get('/search.json', showStates);
}

//shows all states in database in select form
getStates();

function showAreas(results) {
    //shows areas by state

    var areas = results.areas;

    $('#area').empty();
    // $('#route').empty();

    $.each(areas, function(index, area) {
        $('#area').append('<option value=' + area + '>' + area + '</option>');
    });
}



function getAreas(evt) {

    evt.preventDefault();

    var formInputs = {
        'state': $('select#state option:checked').text()
    };

    $.get('/search.json', formInputs, showAreas);
}


$('#state').on('change', getAreas);

$('#area').on('change', getRoutes);


function getRoutes(evt) {

    evt.preventDefault();

    var formInputs = {
        'area': $('select#area option:checked').text()
    };


    $.get('/search.json', formInputs, showRoutes);
}


function showRoutes(results) {

    var routes = results.routes;

    $('#route').empty();

    $.each(routes, function(index, route) {
         $('#route').append('<option value=' + route[2] + '>' + route[0] + ' ' + route[1] + '</option>');
    });

}


function submits_climb(evt) {

    evt.preventDefault();

    var formInputs = {
        'route_id': $('select#route option:checked').val(),
        'notes': $('#notes').val(),
        'complete': $( "input[type=checkbox][name=complete]:checked" ).val(),
        'rating': $('#rating').val(),
        // 'date': $('#date').val(),
        'photo': $('#photo').val()
    };


    $.post('/log-climb.json', formInputs, logs_climb);
}

function logs_climb(results) {
    alert('logged')
}


$('#log-climb').on('submit', submits_climb);



//displays user logged climbs
function display_logs(evt) {
    $.get('/user-info.json', get_logs);
}

function get_logs(results) {
    
    var log_entries = results.review_info;

    for(var log in log_entries){

        
        var table_row = log_entries[log];

        var html = ''

        for(var i = 0; i < table_row.length; i++) {
            html += '<td>' + table_row[i] + '</td>';
        }

        $('#user_logs').append('<tr>' + html + '</tr>');

    }

}
display_logs()