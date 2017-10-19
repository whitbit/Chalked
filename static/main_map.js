
$(document).ready(gets_coordinates);



function gets_coordinates(evt) {
    $.get('/map.json', map_climbs);
}


function map_climbs(results) {


    var map = new google.maps.Map(document.getElementById('map'))

    var bounds = new google.maps.LatLngBounds();


    var infoWindows = [];

    var markers = [];

    var i = 0;

    for(var place in results) {

      route = results[place]

      var marker = new google.maps.Marker({
        position: route.coordinates,
        num: i
      });

      markers.push(marker);

      var infowindow = new google.maps.InfoWindow();

      var content = createContent(route.info_window);

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
      var name = data[0];
      var v_grade = data[1]
      var state = data[2];
      var area = data[3];
      var url = data[4];
      var lat = data[5];
      var lng = data[6];
      var image = data[7]


      return '<h4>' + name + ' (V' + v_grade + ') </h4>'
             + '<h5>(' + lat + ', ' + lng + ')</h5>'
             + '<h5>' + area + ', ' + state + '</h5>' 
             + '<a href=' + url + '> MORE INFO </a><br>'
             + '<img src=' + image + ' width="450px">'

    }


  }

    map.fitBounds(bounds)

  // Add a marker clusterer to manage the markers.
  var markerCluster = new MarkerClusterer(map, markers,
      {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
}



