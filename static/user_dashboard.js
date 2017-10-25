$('#myModal').appendTo("body") 

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

    $('#area').append('<option disable selected value> -- AREA -- </option>')
    
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

    $('#route').append('<option disable selected value> -- ROUTE -- </option>');

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
    $('#myModal').modal('hide');
    document.getElementById('log-climb').reset();
    displayLogs();
    generatesChart();
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

        $('tr').has('td').empty();

        var completedLog = [];

        for(var log in completedEntries) {
            completedLog.push(completedEntries[log])
        }

        completedLog.sort().reverse();


        for(var i = 0; i < completedLog.length; i++) {
            var html = ''

            for(var j = 0; j < completedLog[i].length; j++)
                if (j === 0) {
                    html += '<td>' + moment(completedLog[i][j]).fromNow() + '</td>';
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

        projectsLog.sort().reverse();

        for(var i = 0; i < projectsLog.length; i++) {
            var html = ''

            html += makeProjectLogRow(projectsLog[i]);
            
            html += '<td> <input type="checkbox" name="updated" value="true"> </td>';

            html += '<td> <input type="submit" value="update" class="' + projectsLog[i][7] + ' submitupdate"</td>';

            html += '<td> <button type="button" id="deleteLog" class="btn btn-default '+ projectsLog[i][7] +'">\
                    <span class="glyphicon glyphicon-remove-circle" area-hidden="true"</span></button></td>';

            $('#projects').append('<tr class="' + projectsLog[i][7] + ' item" >' + html + '</tr>');

        }
    });
}

displayLogs();


$('table').on('click', '#deleteLog', function() {
    var reviewId = ($(this).attr('class')).split(' ')[2]

    var formInputs = {
        'review_id': reviewId
    };

    $.post('/delete-log.json', formInputs, function() {
        displayLogs();
    });

})



$('table').on('click', '.submitupdate', updatesLog);


function updatesLog(evt) {

    evt.preventDefault();


    // debugger;
    var reviewId = ($(this).attr('class')).split(' ')[0]

    var tableData = $("table ." + reviewId + " td")
    var rating = tableData.eq(5).children().val()
    // console.log(rating)
    var notes = tableData.eq(6).children().val()
    // console.log(notes)
    var completed = $( "input[type=checkbox][name=updated]:checked" ).val()
    // console.log(completed)
    if(completed === undefined) {
        completed = false;
    }

    var formInputs = {
        'review_id': reviewId,
        'notes': notes,
        'complete': completed,
        'rating': rating,
        'date': moment(Date.now()).format('MM/DD/YYYY'),
    };

    console.log(formInputs)


    $.post('/update-log.json', formInputs, function() {
        displayLogs();
        generatesChart()
    });

}



function makeProjectLogRow(projectInfo) {
    var html = ''
    var originalNotes = projectInfo[5];


    for(var j = 0; j < projectInfo.length - 1; j++)
        if (j === 0) {
            html += '<td>' + moment(projectInfo[0]).fromNow() + '</td>'
        } else if (j === 5) {

            html += renderOldLogNotes(projectInfo[5])
        } else {
            html += '<td>' + projectInfo[j] + '</td>';
        }
    
    return html
}


function renderOldLogNotes(note) {
    var text = '';

    if(note === '') {
        text += '<td> <input type="text" class="projectNotes" placeholder="add notes...">'
    } else {
        text += '<td> <input type="text" class="projectNotes" value="' + note + '"">'
    }

    return text
}





function displaysUserStatus() {
    $.get('/user-info.json', function(results) {
        var points = results['user_points']
        var pointsAway;
        var badge;
        var animal;

        if(points > 50 && points < 100) {
            pointsAway = 100 - points;
            animal = 'monkey';
            badge = "<img src='/static/monkey.png'>";

        } else if (points > 100) {
            badge = "<img src='/static/goat.png'>";
            animal = 'mountain goat'
        } else {
            pointsAway = 50 - points;
            animal = 'gym rat'
            badge = "<img src='/static/rat.png'>";
        }


        
        $('#profile').append(badge);

        $('#animal').append(animal);

        $('#points').append('Total V-points: <b>' + points + '</b>');

        $('#next-badge').append('<i>' + pointsAway + ' pts away from your next badge! </i>')



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

        Chart.defaults.global.defaultFontFamily = "Open Sans";

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


