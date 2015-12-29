requirejs(['helper/google_api', 'helper/jquery'], function(
    google_api, jquery
){
  console.log('Hello World')

  var map;
  //debugger;

  $(document).ready(function() {
    var mapOptions = {
      zoom: 12,
      center: {lat: 39.2946020, lng: -76.648824},
      mapTypeId: google.maps.MapTypeId.TERRAIN
    };

    map = new google.maps.Map(document.getElementById('map'), mapOptions);
    var script = document.createElement('script');
    script.src = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojsonp';
    document.getElementsByTagName('head')[0].appendChild(script);
  })
});