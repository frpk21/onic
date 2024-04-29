// Enter your custom JavaScript code here

function beforeMapLoads(){
	console.log("Before map loads function");
	//var Layers = new Array();
	var paramsLayer = {
		"type": "WFS",
		"EPSG": 4686,
		"showCoverageOnHover": false,
		"removeOutsideVisibleBounds": false,
		"url": "http://localhost:8080/geoserver/wfs",
		"visible": false,	
		"popup": true,
		//"tooltipField": "comunidad",
		"geomField": "geom"			
	}

	$.ajax({
		type: 'GET',
		async: false,
		url: 'http://localhost:8080/geoserver/wms?request=getCapabilities',
		dataType: 'xml',//'json',
		success: function (xml, status, xhr) {
		  console.log("GetCapabilities success xml response ", xml);
		  var wmsUrl = 'http://localhost:8080/geoserver/ows?';
			$(xml).find('Layer').find('Layer').each(function() {
				var layerName = $(this).children('Name').text();
				var getUrl = wmsUrl+'service=wfs&version=1.1.0&request=DescribeFeatureType&typeName='+layerName+'&outputFormat=application/json';	
				$.ajax({
					//jsonpCallback: 'getJson',
					type: 'GET',
					url: getUrl,
					async: false,
					//dataType: 'jsonp',
					success: function (data, status, xhr) {
						var dataLayer = data.featureTypes[0];
						//console.log("data Info: ", data);

						dataLayer.properties.map(function(e) { 
							delete e.nillable;
							delete e.localType;
							delete e.maxOccurs;
							delete e.minOccurs;
							return e							
						});
						
						var dictLayer = {
							"id": dataLayer.typeName.toLowerCase(),
							"name": dataLayer.typeName,
							"type": paramsLayer.type,
							"EPSG": paramsLayer.EPSG,
							"showCoverageOnHover": paramsLayer.showCoverageOnHover,
							"removeOutsideVisibleBounds":paramsLayer.removeOutsideVisibleBounds,
							"url": paramsLayer.url,
							"typeName": layerName,
							"visible": paramsLayer.visible,
							"popup": paramsLayer.popup,
							"geomField": paramsLayer.geomField,
							"geometry": dataLayer.properties[0].type,
							"outFields": dataLayer.properties
						};
						//Layers.push(dictLayer);
						addLayerToTOC(dictLayer);
					},
					error: function (xhr, status, error) {
					  console.log(error);
					}
				});				
			});
			//console.log("Layers Info: ", Layers);
		},
		error: function(err){
			console.log("WMS GetCapabilities error with ", err);
			$.growl.warning({ message: "There was a problem fetching the Layers for " + err});
		}
	});	

	// // This function is called before the map loads, and is useful for manipulating the config object, eg
	// // to add a new custom layer.

	// // Create a layer which is based on a query string in the URL - this shows the US state based on the query
	// // value, eg bootleaf.html/?query=california
	// var statesConfig = {
	// 	"id": "us_states",
	// 	"name": "States",
	// 	"type": "agsDynamicLayer",
	// 	"url": "https://sampleserver1.arcgisonline.com/ArcGIS/rest/services/Demographics/ESRI_Census_USA/MapServer/",
	// 	"layers": [5],
	// 	"useCors": false,
	// 	"visible": true
	// }

	// var query = getURLParameter('query');
	// if(query) {
	// 	statesConfig.layerDefs = "5: STATE_NAME = '" + query + "'";
	// 	statesConfig.name += " (" + query + ")";
	// }

	// // Add this layer to the TOC and map.
	// config.layers.push(statesConfig);
	// for (i in config.tocCategories){
	// 	if (config.tocCategories[i]['name'] === 'ArcGIS Layers') {
	// 		config.tocCategories[i]['layers'].push(statesConfig.id);
	// 	}
	// }

	// // If there are any layers defined in the URL, add this layer to the list so it draws by default
	// if(bootleaf.layerParams.length > 0){
	// 	bootleaf.layerParams.push(statesConfig.id);
	// }

	// Continue to load the map
	loadMap();
}

function addLayerToTOC(Layer){
	if (Layer.geometry === "gml:Point"){
		Layer.cluster = true;
		delete Layer.geomField;
	}
	else if(Layer.geometry === "gml:MultiPolygon"){
		var randomColor = Math.floor(Math.random()*16777215).toString(16);
		Layer.style = {
			"color": "#" + randomColor,
			"fillColor": "#" + randomColor,
			"fillOpacity": 0.5,
			"weight": 1,
		}				
	}

	//delete Layer.geometry;
	Layer.outFields.shift();
	Layer.outFields.map(function(field) { 
		if (field.type === "xsd:int" || field.type === "xsd:number"){
			field.type = "numeric";
			field.defaultOperator = ">";
		}
		else if(field.type === "xsd:string"){
			delete field.type;
			field.defaultOperator = "contains";
		}		
		return field						
	});

	Layer.queryWidget = {
		"queries": Layer.outFields,
		"outFields": Layer.outFields,
	}

	if (Layer.name === "Comunidades" || Layer.name === "Departamentos" || Layer.name === "Resguardos_actualizados_ONIC"){
		config.layers.push(Layer);
	}

	console.log("Layer: ", Layer);
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

	configureQueryWidget();
}
