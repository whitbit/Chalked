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
         $('#route').append('<option value=' + route[2] + '>' + 'V' + route[0] + ' ' + route[1] + '</option>');
    });

}


function submitsClimb(evt) {
    console.log('hello friend')
    evt.preventDefault();

    var formInputs = {
        'route_id': $('select#route option:checked').val(),
        'notes': $('#notes').val(),
        'complete': $( "input[type=checkbox][name=complete]:checked" ).val(),
        'rating': $('#rating').val(),
        'date': $('#date').val(),
        'photo': $('#photo').val()
    };


    $.post('/log-climb.json', formInputs, logsClimb);

    $('#upload-button').text('Uploading...');

    var data = new FormData();
    console.log(data)
  
    $.each(files, function(key, value) {
        data.append('file', value);
    });


    $.ajax({
        url: '/upload.json',
        type: 'POST',
        data: data,
        dataType: 'json',
        processData: false,
        contentType: false,
        success: function(results, textStatus,  jqXHR) {
            if(typeof results.error === 'undefined') {
                $('#upload-button').text('Success!');
            } else {
                $('#upload-button').text('ERROR');
            }
        }
    });
}

function logsClimb(results) {
    $('#date').empty();
}


$('#log-climb').on('submit', submitsClimb);



//displays user logged climbs
function displayLogs(evt) {
    $.get('/user-info.json', getLogs);
}

function getLogs(results) {
    
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
displayLogs()


function displaysUserStatus() {
    $.get('/user-info.json', function(results) {
        points = results['user_points']


        $('#points').append('V-points: ', points)
    })
}



$(document).ready(displaysUserStatus);



var files;
$('input[type=file]').on('change', prepareUpload);


function prepareUpload(event){
    files = event.target.files;
}





