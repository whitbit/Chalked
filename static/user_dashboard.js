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

var files = [];
$('input[type=file]').on('change', prepareUpload);


function prepareUpload(event){
    files = event.target.files;
}



function submitsClimb(evt) {

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

    if(files.length > 0) {
        uploadsPhoto()
    }
}


function logsClimb(results) {
    displayLogs()
}


$('#log-climb').on('submit', submitsClimb);

function uploadsPhoto(evt) {
    $('#upload-button').text('Uploading...');

    var data = new FormData();

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



//displays user logged climbs
function displayLogs(evt) {
    $.get('/user-info.json', getLogs);
}

function getLogs(results) {
    
    var log_entries = results.review_info;

    $('#user_logs').empty()

    var logsArr = [];

    for(var log in log_entries) {
        logsArr.push(log_entries[log])
    }

    logsArr.sort().reverse()

    for(var i = 0; i < logsArr.length; i++) {
        var html = ''
        for(var j = 0; j < logsArr[i].length; j++)
            html += '<td>' + logsArr[i][j] + '</td>';
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



function convertMonth(num) {
    var months = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'Aug',
        9: 'Sept',
        10: 'Oct',
        11: 'Nov',
        12: 'Dec'
    }

    return months[num]
}


var ctx = document.getElementById('climbChart').getContext('2d')

$.get('/user-chart.json', function(data) {

    var myBubbleChart = new Chart(ctx, {
        type: 'bubble',
        data: data,
        options: {
            legend: {
                display: false
            },
            title: {
                display: true,
                text: '2017'
            },
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'V-Grade'
                    }
                }],
                xAxes: [{
                    ticks: {
                        callback: function(value, index, values) {
                            return convertMonth(parseInt(value));
                        }
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Month'
                    }
                }]
            }
        }
    })
})







