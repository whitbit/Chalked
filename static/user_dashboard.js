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
    //upon new long, buble chart and logs tables update
    displayLogs()
    generatesChart()
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
    $.get('/user-info.json', function(results) {

        var completedEntries = results.completed;

        $('.items').empty()

        var completedLog = [];

        for(var log in completedEntries) {
            completedLog.push(completedEntries[log])
        }

        completedLog.sort().reverse()


        for(var i = 0; i < completedLog.length; i++) {
            var html = ''

            for(var j = 0; j < completedLog[i].length; j++)
                if (j === 0) {
                    html += '<td>' + moment(completedLog[i][j]).fromNow() + '</td>'
                } else {
                    html += '<td>' + completedLog[i][j] + '</td>';
                }
            $('#completedClimbs').append('<tr class="item">' + html + '</tr>');
        }


        var incompleteEntries = results.projects;

        var projectsLog = [];

        for(var log in incompleteEntries) {
            projectsLog.push(incompleteEntries[log])
        }

        projectsLog.sort().reverse()

        for(var i = 0; i < projectsLog.length; i++) {
            var html = ''

            for(var j = 0; j < projectsLog[i].length; j++)
                if (j === 0) {
                    html += '<td>' + moment(projectsLog[i][j]).fromNow() + '</td>'
                } else {
                    html += '<td>' + projectsLog[i][j] + '</td>';
                }
            $('#projects').append('<tr class="item">' + html + '</tr>');
        }
    });
}

displayLogs()


function displaysUserStatus() {
    $.get('/user-info.json', function(results) {
        points = results['user_points']


        $('#points').append('Total V-points: ', points)
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


function generatesChart() {
    $.get('/user-chart.json', function(data) {


        var myBubbleChart = new Chart(ctx, {
            type: 'bubble',
            data: data,
            options: {
                tooltips: {
                    callbacks: {
                        label: function(tooltipItem, data) {
                            var times = (data.datasets[tooltipItem.datasetIndex].data[0].r) / 23
                            return times + ' x ' + data.datasets[tooltipItem.datasetIndex].label
                        }
                    }
                },
                responsive: true,
                
                legend: {
                    display: false
                },
                
                title: {
                    display: true,
                    text: 'My 12 Month Progress'
                },
                
                scales: {
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: 'Difficulty (V-grade)'
                        },
                        ticks: {
                            min: 0,
                            max: 10,
                        }
                    }],
                    xAxes: [{
                        type: 'time',
                        time: {
                            unit: 'month',
                            min: moment().subtract(12, 'months'),
                            max: moment()
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'Month'
                        },
                    }]
                }
            }
        })
    })
}
generatesChart()


