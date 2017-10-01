

function getStates() {

    $.get('/search-states.json', function(results) {
        states = results.states
        
        for(var i = 0; i < states.length; i++) {
            $('#state').append('<option value=' + states[i] + '>' + states[i] + '</option>')
        }  
    })
}


$(document).ready(getStates)

$('#state').on('submit', getStateInfo)

function getStateInfo(evt) {
    evt.preventDefault()

    var formInputs = {
        'state': $('#state').val()
    }

    var url = $(this).attr('action');

    $.get(url, formInputs, getAreas)
}


// $('#state').click(function(evt) {
//     evt.preventDefault();
//     var url = $(this).attr('action')
//     console.log(url)
//     $.get(url, getAreas)
// })


function getAreas(results) {

    console.log('RESULTS', results)
    areas = results.areas

    for(var i = 0; i < areas.length; i++) {
        $('#route').append('<option value=' + areas[i] + '>' + areas[i] + '</option>')
    }
}


