
$(document).ready(gets_coordinates);



function gets_coordinates(evt) {
    $.get('/user-info.json', map_climbs);
}


function map_climbs(results) {

    var map = new google.maps.Map(document.getElementById('map'), {
      styles: [{"elementType":"geometry","stylers":[{"hue":"#ff4400"},{"saturation":-68},{"lightness":-4},{"gamma":0.72}]},{"featureType":"road","elementType":"labels.icon"},{"featureType":"landscape.man_made","elementType":"geometry","stylers":[{"hue":"#0077ff"},{"gamma":3.1}]},{"featureType":"water","stylers":[{"hue":"#00ccff"},{"gamma":0.44},{"saturation":-33}]},{"featureType":"poi.park","stylers":[{"hue":"#44ff00"},{"saturation":-23}]},{"featureType":"water","elementType":"labels.text.fill","stylers":[{"hue":"#007fff"},{"gamma":0.77},{"saturation":65},{"lightness":99}]},{"featureType":"water","elementType":"labels.text.stroke","stylers":[{"gamma":0.11},{"weight":5.6},{"saturation":99},{"hue":"#0091ff"},{"lightness":-86}]},{"featureType":"transit.line","elementType":"geometry","stylers":[{"lightness":-48},{"hue":"#ff5e00"},{"gamma":1.2},{"saturation":-23}]},{"featureType":"transit","elementType":"labels.text.stroke","stylers":[{"saturation":-64},{"hue":"#ff9100"},{"lightness":16},{"gamma":0.47},{"weight":2.7}]}]
    })

    var bounds = new google.maps.LatLngBounds();

    var places = results['map'];

    var infoWindows = [];

    var markers = [];

    var i = 0;

    // consider making some noise on coordinates to prevent stacking

    for(var place in places) {

      //adds noise to coordinates to prevent inadvertenant overlaying 
      places[place].coordinates['lat'] = places[place].coordinates['lat'] + Math.random() * 0.001

      var marker = new google.maps.Marker({
        position: places[place].coordinates,
        num: i
      });

      markers.push(marker);

      var infowindow = new google.maps.InfoWindow();

      var content = createContent(places[place].info_window);

      infowindow.setContent(content)

      infoWindows.push(infowindow)
      
      i += 1;

      bounds.extend(marker.position);

      marker.setMap(map);


    function addClick(marker) {
      marker.addListener('click', function() {
        infowindow.setContent(content);
        
        index = marker.num;

        infoWindows.map(function(info_window) {
          info_window.close()
        });

        infoWindows[index].open(map, marker);
      })
    }
    addClick(marker)


    function createContent(data) {
      var date = data[0];
      var name = data[1].toUpperCase();
      var v_grade = data[2]
      var state = data[3];
      var area = data[4];
      var url = data[6];
      var lat = data[7];
      var lng = data[8];

      if(data[5] === '') {
        var img = '';
      } else {
        var img = '/uploads/' + data[5]
      }

      return '<h4>' + name + ' (V' + v_grade + ') </h4>' 
             + '<h5>' + date + '</h5>'
             + '<h5>(' + lat + ', ' + lng + ')</h5>'
             + '<h5>' + area + ', ' + state + '</h5>' 
             + '<a href=' + url + '> MORE INFO </a><br>'
             + '<img src="' + img + '"" width="450px">'

    }

  }

    map.fitBounds(bounds)

  // Add a marker clusterer to manage the markers.
  var markerCluster = new MarkerClusterer(map, markers,
      {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
}



