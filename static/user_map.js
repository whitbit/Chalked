
$(document).ready(gets_coordinates);



function gets_coordinates(evt) {
    $.get('/user-info.json', map_climbs);
}


function map_climbs(results) {

    var map = new google.maps.Map(document.getElementById('map'))

    var bounds = new google.maps.LatLngBounds();

    var places = results['map'];

    var infoWindows = [];

    var markers = [];

    var i = 0;

    for(var place in places) {

      var marker = new google.maps.Marker({
        position: places[place].coordinates,
        num: i
      });

      markers.push(marker);

      console.log(marker.position)

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
      date = data[0];
      name = data[1].toUpperCase();
      v_grade = data[2]
      state = data[3];
      area = data[4];
      img = data[5];
      url = data[6];
      lat = data[7];
      lng = data[8];

      // console.log(date)

      return '<h4>' + name + ' (V' + v_grade + ') </h4>' 
             + '<h5>' + date + '</h5>'
             + '<h5>(' + lat + ', ' + lng + ')</h5>'
             + '<h5>' + area + ', ' + state + '</h5>' 
             + '<a href=' + url + '> MORE INFO </a>'
             + '<img src=' + img + '>'

    }

  }

    map.fitBounds(bounds)

  // Add a marker clusterer to manage the markers.
  // var markerCluster = new MarkerClusterer(map, markers,
  //     {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
}



