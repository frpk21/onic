// Enter your custom JavaScript code here

function beforeMapLoads(){
	console.log("Before map loads function");

	// // This function is called before the map loads, and is useful for manipulating the config object, eg
	// // to add a new custom layer.

	// Continue to load the map
	loadMap();

}

function afterMapLoads(){
	// This function is run after the map has loaded. It gives access to bootleaf.map, bootleaf.TOCcontrol, etc

	console.log("After map loads function");
	afterMapLoads
	$("#loader").hide();

	// Check to see whether the Gray basemap is chosen, and the user has zoomed in too far. In this case,
	// switch to the Streets basemap
	bootleaf.map.on("zoomend", function(evt){
		if (bootleaf.currentBasemap === 'Gray'){
			if (evt.target._zoom >= 17) {
				setBasemap({"type": 'esri', "id": 'Streets'});
				$.growl.warning({ title: "Basemap change", message: "The grayscale basemap is not available at this scale"});
			}
		}
	});

	// Detect the coordinates of the address returned by the geocoder. This can be used elsewhere as required
	bootleaf.leafletGeocoder.on("markgeocode", function(evt){
		console.log("Coordinates: ", evt.geocode.center.lat, ", ", evt.geocode.center.lng);
	});
}
