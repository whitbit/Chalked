
$(document).ready(gets_coordinates);


function gets_coordinates(evt) {

  $.get('/user-map.json', map_climbs);

}



var locations = []


function map_climbs(results) {
  
  var coordinates = results['coordinates'];

  for(var key in coordinates) {
    locations.push(coordinates[key]);
  }

  initMap();

}


function initMap() {

  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 3,
    center: locations[0]
  });

  // var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

  var markers = locations.map(function(location, i) {
    return new google.maps.Marker({
      position: location,
      // label: labels[i % labels.length]
    });
  });

  // Add a marker clusterer to manage the markers.
  var markerCluster = new MarkerClusterer(map, markers,
      {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
}
