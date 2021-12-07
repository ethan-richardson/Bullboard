let map;

function createMarker(){
	return 0;
}

function initMap() {
  const myLatlng = {
    lat: 42.98160187253904,
    lng: -78.81162667649288
  };
  map = new google.maps.Map(document.getElementById("map"), {
    center: myLatlng,
    zoom: 13,
  });

  let infoWindow = new google.maps.InfoWindow({
    content: "Click the map to place a marker",
    position: myLatlng,
  });
  infoWindow.open(map);
  const iconBase =
    "https://developers.google.com/maps/documentation/javascript/examples/full/images/";
  const icons = {
    parking: {
      icon: iconBase + "parking_lot_maps.png",
    },
    library: {
      icon: iconBase + "library_maps.png",
    },
    info: {
      icon: iconBase + "info-i_maps.png",
    },
  };

  const features = [{
    position: new google.maps.LatLng(43.000729099643095, -78.78952228733044),
  }, 
  ];
	
  map.addListener("click", (mapsMouseEvent) => {
    // Create a new InfoWindow.
    infoWindow.close();
    infoWindow = new google.maps.InfoWindow({
      position: mapsMouseEvent.latLng,
    });
    // console.log(mapsMouseEvent.latLng);
    infoWindow.setContent(
      JSON.stringify(mapsMouseEvent.latLng.toJSON(), null, 2)
    );
    infoWindow.open(map);
  });

  // Create markers.
  for (let i = 0; i < features.length; i++) {
    const marker = new google.maps.Marker({
    position: features[i].position,
    map,
    });
  }
}
