
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

    var i = 0;

    for(var place in places) {
      var content = createContent(places[place].info_window);

      var infowindow = new google.maps.InfoWindow();
      infowindow.setContent(content)

      infoWindows.push(infowindow)
      
      var marker = new google.maps.Marker({
        position: places[place].coordinates,
        num: i
      });

      i += 1;

      bounds.extend(marker.position);

      marker.setMap(map);


    function addClick(marker) {
      marker.addListener('click', function() {
        infowindow.setContent(content);
        index = marker.num
        infoWindows[index].open(map, marker);
      })
    }
    addClick(marker)

    function createContent(data) {
      name = data[0].toUpperCase();
      v_grade = data[1]
      state = data[2];
      area = data[3];
      img = data[4];
      url = data[5];

      // console.log(date)

      return '<h4>' + name + ' (' + v_grade + ') </h4>' 
             + '<h5>' + area + ', ' + state + '</h5>' 
             + '<a href=' + url + '> More Info </a>'
             + '<img src=' + img + '>'

    }

  }

    map.fitBounds(bounds)

  // Add a marker clusterer to manage the markers.
  // var markerCluster = new MarkerClusterer(map, markers,
  //     {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
}



