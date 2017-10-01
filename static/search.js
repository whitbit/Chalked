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

$(document).ready(getStates);



function showAreas(results) {
    //shows areas by state

    var areas = results.areas

    $.each(areas, function(index, area) {
        $('#area').append('<option value=' + area + '>' + area + '</option>');
    });
}



function getAreas(evt) {

    evt.preventDefault();

    $.get('/search.json', $('#state').serialize(), showAreas);
}


$('#state-form').on('submit', getAreas);

$('#area-form').on('submit', getRoutes);


function getRoutes(evt) {

    evt.preventDefault();

    var formInputs = {
        'area': $('select#area option:checked').text()
    };

    $.get('/search.json', formInputs, showRoutes);
}


function showRoutes(results) {


    var routes = results.routes

    $.each(routes, function(index, route) {
         $('#route').append('<option value=' + index + '>' + route + '</option>');
    });

}


function submits_climb(evt) {

    evt.preventDefault();

    var formInputs = {
        'route_id': $('select#route option:checked').val(),
        'notes': $('#notes').val(),
        'complete': $( "input[type=checkbox][name=complete]:checked" ).val()
    };

    console.log(formInputs)


    $.post('/log-climb.json', formInputs, logs_climb);
}

function logs_climb(results) {
    $('#submitted').innerHTML = '<p>success</p>' 
}


$('#log-climb').on('submit', submits_climb);


