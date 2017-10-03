
$(document).ready(gets_coordinates);



function gets_coordinates(evt) {
    $.get('/user-info.json', map_climbs);
}


function map_climbs(results) {

  
    var places = results['map'];

    var bounds = new google.maps.LatLngBounds();
    //sets bounds of where map is centered

  
    var map = new google.maps.Map(document.getElementById('map'))

    var infoWindows = [];

    var i = 0
    for(var place in places) {
      var content = places[place].info_window;

      var infowindow = new google.maps.InfoWindow();
      infowindow.setContent(content)

      infoWindows.push(infowindow)
      // append this window to array
      
      var marker = new google.maps.Marker({
        position: places[place].coordinates,
        num: i
      });

      i += 1

      bounds.extend(marker.position)

      marker.setMap(map)

  
      function addClick(marker) {
        marker.addListener('click', function() {
          infowindow.setContent(content);
          index = marker.num
          infoWindows[index].open(map, marker);
        })
      }
      addClick(marker)

    }

    map.fitBounds(bounds)

  // Add a marker clusterer to manage the markers.
  // var markerCluster = new MarkerClusterer(map, markers,
  //     {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
}

