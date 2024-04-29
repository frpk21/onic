var config = {
	"requireArcGISLogin": false, // Does the user need to log in to ArcGIS Online or ArcGIS Server?
	"tokenUrl": 'https://www.arcgis.com/sharing/generateToken', // ArcGIS token generation URL

	"title": "Geovisor SMT",
	"start": {
		// "maxZoom": 16,
		"center": [3.66873,-68.100403],
		"zoom": 6,
		"attributionControl": true,
		"zoomControl": false
	},
	"about": {
		"title": "Geovisor SMT",
		"contents": "<p>El Geovisor del SMT es una herramienta que permite consultar información espacial a través de diferentes capas temáticas...</p>"
	},
	"controls": {
		"zoom": {
			"position": "topleft",

		},
		"leafletGeocoder": {
			//https://github.com/perliedman/leaflet-control-geocoder
			"collapsed": true,
			"position": "topleft",
			"placeholder": "Buscador",
			"type": "OpenStreetMap", // OpenStreetMap, Google, ArcGIS
			//"suffix": "Australia", // optional keyword to append to every search
			//"key": "AIzaS....sbW_E", // when using the Google geocoder, include your Google Maps API key (https://developers.google.com/maps/documentation/geocoding/start#get-a-key)
		},
		"TOC": {
			//https://leafletjs.com/reference-1.0.2.html#control-layers-option
			"collapsed": false,
			"uncategorisedLabel": "Capas SMT-WEB",
			"position": "topright",
			"toggleAll": false
		},
		// "history": {
		// 	"position": "bottomleft"
		// },
		// "bookmarks": {
		// 	"position": "bottomright",
		// 	"places": [
		// 		{
		// 		"latlng": [
		// 			40.7916, -73.9924
		// 		],
		// 		"zoom": 12,
		// 		"name": "Manhattan",
		// 		"id": "a148fa354ba3",
		// 		"editable": true,
		// 		"removable": true
		// 		}
		// 	]
		// }
	},

	"activeTool": "",//"queryWidget", // options are identify/coordinates/filterWidget
	"basemaps": ['esriGray', 'OpenStreetMap', 'esriDarkGray', 'esriStreets', 'Aerial'],
	"bing_key": "Ap0QEleyAZPWg1gNS8jfe6ZGRV9mD0-AulMN3hxsfVOKRVrJj25GffRBKr-rrTER",
	"mapboxKey": "enter your MapBox key",
	// "defaultIcon": {
	// 	"imagePath": "https://leafletjs.com/examples/custom-icons/",
	// 	"iconUrl": "leaf-green.png",
	// 	"shadowUrl": "leaf-shadow.png",
	// 	"iconSize":     [38, 95],
	// 		"shadowSize":   [50, 64],
	// 		"iconAnchor":   [22, 94],
	// 		"shadowAnchor": [4, 62],
	// 		"popupAnchor":  [-3, -76]
	// },
	"tocCategories": [
		{
			"name": "Capas GeoJSON",
			"layers": []
			//"layers": ["theatres", "museums", "us_density"]
		},
		{
			"name": "Capas ArcGIS",
			//"layers" : ["cities", "counties", "railways", "us_states"]
			//"layers" : ["counties", "railways", "us_states"]
			"layers": []
		},
		{
			"name": "Capas WMS/WFS",
			//"layers": ["resguardos", "comunidades", "US_population", "countries"],
			//"layers": ["resguardos", "comunidades", "departamentos"],
			"layers": [],
			"exclusive": false
		}
	],
	"projections": [
		{4269: '+proj=longlat +ellps=GRS80 +datum=NAD83 +no_defs '},
		{4686: '+proj=longlat +ellps=GRS80 +no_defs +type=crs '}
	],
	"highlightStyle": {
		"weight": 1,
		"opacity": 1,
		"color": '#E31A1C',//'white',
		//"dashArray": '3',
		"fillOpacity": 0.5,
		"fillColor": '#E31A1C',
		"stroke": true
	},
	"layers": [
		// {
		// 	"id": "comunidades",
		// 	"name": "Comunidades (WFS)",
		// 	"type": "WFS",
		// 	"EPSG": 4686,
		// 	"cluster": true,
		// 	"showCoverageOnHover": false,
		// 	"removeOutsideVisibleBounds": true,
		// 	"url": "http://localhost:8080/geoserver/wfs",
		// 	"typeName": "isaa:Comunidades",
		// 	"visible": false,
		// 	"popup": true,
		// 	"tooltipField": "comunidad",
		// 	"outFields": [
		// 		{"name": "cod_depto", "alias": "Código Departamento"},
		// 		{"name": "nom_dep", "alias": "Departamento"},
		// 		{"name": "cod_mpio", "alias": "Código Municipio"},
		// 		{"name": "nom_mpio", "alias": "Municipio"},
		// 		{"name": "comunidad", "alias": "Comunidad"},
		// 		{"name": "nom_ri", "alias": "Resguardo"},
		// 		{"name": "viviendas", "alias": "N° de Viviendas", "type": "numeric"},
		// 		{"name": "familias", "alias": "N° de Familias", "type": "numeric"},
		// 		{"name": "personas", "alias": "N° de Personas", "type": "numeric"},
		// 		{"name": "etnia_1", "alias": "Pueblo"},
		// 		{"name": "org_nal", "alias": "Organización Nacional"},
		// 		{"name": "org_regnal", "alias": "Organización Regional"},				
		// 		{"name": "macro", "alias": "Macro"},								
		// 	],
		// 	"queryWidget": {
		// 		"queries" : [
		// 			{"name": "cod_depto", "alias": "Código Departamento", "defaultOperator": "contains"},
		// 			{"name": "nom_dep", "alias": "Departamento", "defaultOperator": "contains"},
		// 			{"name": "cod_mpio", "alias": "Código Municipio", "defaultOperator": "contains"},
		// 			{"name": "nom_mpio", "alias": "Municipio", "defaultOperator": "contains"},
		// 			{"name": "comunidad", "alias": "Nombre Comunidad", "defaultOperator": "contains"},
		// 			{"name": "nom_ri", "alias": "Nombre Resguardo", "defaultOperator": "contains"},
		// 			//{"name": "viviendas", "alias": "N° de Viviendas", "type": "numeric"},
		// 			{"name": "familias", "alias": "N° de Familias", "type": "numeric", "defaultOperator": "<"},
		// 			{"name": "personas", "alias": "N° de Personas", "type": "numeric", "defaultOperator": "<"},
		// 			{"name": "etnia_1", "alias": "Nombre Pueblo", "defaultOperator": "contains"},
		// 			{"name": "org_nal", "alias": "Organización Nacional", "defaultOperator": "contains"},
		// 			{"name": "org_regnal", "alias": "Organización Regional", "defaultOperator": "contains"},				
		// 			{"name": "macro", "alias": "Macro", "defaultOperator": "contains"},								
		// 			// {"name": "capital", "alias": "Capital", "type": "boolean"}
		// 		],
		// 		"outFields": [
		// 			{"name": "cod_depto", "alias": "Cód Dpto"},
		// 			{"name": "nom_dep", "alias": "Dpto"},
		// 			{"name": "cod_mpio", "alias": "Cód Mpio"},
		// 			{"name": "nom_mpio", "alias": "Mpio"},
		// 			{"name": "comunidad", "alias": "Comunidad"},
		// 			{"name": "nom_ri", "alias": "Resguardo"},
		// 			{"name": "viviendas", "alias": "Viviendas", "type": "numeric"},
		// 			{"name": "familias", "alias": "Familias", "type": "numeric"},
		// 			{"name": "personas", "alias": "Personas", "type": "numeric"},
		// 			{"name": "etnia_1", "alias": "Pueblo"},
		// 			{"name": "org_nal", "alias": "Org Nal"},
		// 			{"name": "org_regnal", "alias": "Org Regnal"},				
		// 			{"name": "macro", "alias": "Macro"},								
		// 		]
		// 	},
		// 	//   "filters": [
		// 	// 	  {"name": "cod_depto", "alias": "Departamento"},
		// 	// 	  {"name": "viviendas", "alias": "N° de Viviendas", "type": "numeric"}
		// 	//   ],
		// 	//"style": {
		// 	//	"stroke": true,
		// 	//	"fillColor": "#00FFFF",
		// 	//	"fillOpacity": 0.5,
		// 	//	"radius": 10,
		// 	//	"weight": 0.5,
		// 	//	"opacity": 1,
		// 	//	"color": '#727272'
		// 	//}
		// },		
		// {
		// 	"id": "resguardos",
		// 	"name": "Resguardos (WFS)",
		// 	"type": "WFS",
		// 	'EPSG': 4686,
		// 	"url": "https://smt-test.onic.org.co/geoserver/wfs?",
		// 	//"url": "http://localhost:8080/geoserver/wfs",
		// 	"typeName": "geonode:my_smt_cmp_resguardos_ambito_onic_v1",
		// 	//"typeName": "isaa:Resguardos",
		// 	"visible": false,
		// 	"popup": true,
		// 	"showCoverageOnHover": false,
		// 	"removeOutsideVisibleBounds": false,
		// 	"tooltipField": "territorio",
		// 	"geomField": "geom",
		// 	"outFields": [
		// 		{"name": "territorio", "alias": "Resguardo"},
		// 		{"name": "dpto_cnmbr", "alias": "Departamento"},
		// 		{"name": "mpio_cnmbr", "alias": "Municipio"},
		// 		{"name": "area_pg_ha", "alias": "Área (ha)", "thousands": true}
		// 	],
		// 		"queryWidget": {
		// 		"queries" : [
		// 			{"name": "dpto_cnmbr", "alias": "Departamento"},
		// 			{"name": "mpio_cnmbr", "alias": "Municipio"},

		// 			// {"name": "capital", "alias": "Capital", "type": "boolean"}
		// 		],
		// 		"outFields": [
		// 			{"name": "territorio", "alias": "Resguardo"},
		// 			{"name": "dpto_cnmbr", "alias": "Departamento"},
		// 			{"name": "mpio_cnmbr", "alias": "Municipio"},
		// 			{"name": "area_pg_ha", "alias": "Área (ha)"}
		// 		]
		// 	}			
		// },

		// {
		// 	"id": "resguardos",
		// 	"name": "Resguardos (WFS)",
		// 	"type": "WFS",
		// 	"EPSG": 4686,
		// 	"showCoverageOnHover": false,
		// 	"removeOutsideVisibleBounds": false,
		// 	"url": "http://localhost:8080/geoserver/wfs",
		// 	"typeName": "isaa:Resguardos_actualizados_ONIC",
		// 	"visible": false,
		// 	"popup": true,
		// 	"showOnTop" : true,
		// 	"tooltipField": "NOMBRE",
		// 	"geomField": "geom",
		// 	"outFields": [
		// 		{"name": "NOMBRE", "alias": "Resguardo"},
		// 		{"name": "CODIGO_DAN", "alias": "Código DANE"},
		// 		{"name": "ONIC_pueblo", "alias": "Pueblo"},
		// 		{"name": "ONIC_macro", "alias": "Macro"},
		// 		{"name": "ONIC_org_nal", "alias": "Organización Nacional"},
		// 		{"name": "ONIC_org_regnal", "alias": "Organización Regional"},
		// 		{"name": "ONIC_dpto_cnmbr", "alias": "Departamento"},
		// 		{"name": "ONIC_dpto_ccdgo", "alias": "Código Departamento"},
		// 		{"name": "ONIC_mpio_cnmbr", "alias": "Municipio"},
		// 		{"name": "ONIC_mpio_cdpmp", "alias": "Código Municipio"},
		// 		{"name": "ONIC_Area_Rgdo", "alias": "Área (ha)"}
		// 	],
		// 		"queryWidget": {
		// 		"queries" : [
		// 			{"name": "NOMBRE", "alias": "Nombre Resguardo", "defaultOperator": "contains"},
		// 			{"name": "CODIGO_DAN", "alias": "Código DANE", "defaultOperator": "contains"},
		// 			{"name": "ONIC_pueblo", "alias": "Nombre Pueblo", "defaultOperator": "contains"},
		// 			{"name": "ONIC_macro", "alias": "Macro", "defaultOperator": "contains"},
		// 			{"name": "ONIC_org_nal", "alias": "Organización Nacional", "defaultOperator": "contains"},
		// 			{"name": "ONIC_org_regnal", "alias": "Organización Regional", "defaultOperator": "contains"},
		// 			{"name": "ONIC_dpto_cnmbr", "alias": "Departamento", "defaultOperator": "contains"},
		// 			{"name": "ONIC_dpto_ccdgo", "alias": "Código Departamento", "defaultOperator": "contains"},
		// 			{"name": "ONIC_mpio_cnmbr", "alias": "Municipio", "defaultOperator": "contains"},
		// 			{"name": "ONIC_mpio_cdpmp", "alias": "Código Municipio", "defaultOperator": "contains"},
		// 			{"name": "ONIC_Area_Rgdo", "alias": "Área (ha)", "type": "numeric", "defaultOperator": "<"}
		// 		],
		// 		"outFields": [
		// 			{"name": "NOMBRE", "alias": "Resguardo"},
		// 			{"name": "CODIGO_DAN", "alias": "Cód DANE"},
		// 			{"name": "ONIC_pueblo", "alias": "Pueblo"},
		// 			{"name": "ONIC_macro", "alias": "Macro"},
		// 			{"name": "ONIC_org_nal", "alias": "Org Nal"},
		// 			{"name": "ONIC_org_regnal", "alias": "Org Regnal"},
		// 			{"name": "ONIC_dpto_cnmbr", "alias": "Dpto"},
		// 			{"name": "ONIC_dpto_ccdgo", "alias": "Cód Dpto"},
		// 			{"name": "ONIC_mpio_cnmbr", "alias": "Mpio"},
		// 			{"name": "ONIC_mpio_cdpmp", "alias": "Cód Mpio"},
		// 			{"name": "ONIC_Area_Rgdo", "alias": "Área (ha)", "type": "numeric"}
		// 		]
		// 	},
		// 	"style": {
		// 		//"color": "#005E14",
		// 		//"fillColor": "#005E14",
		// 		"fillOpacity": 0.5,
		// 		"weight": 1
		// 	}									
		// },		
		
		// {
		// 	"id": "departamentos",
		// 	"name": "Departamentos (WFS)",
		// 	"type": "WFS",
		// 	"EPSG": 4686,
		// 	"url": "http://localhost:8080/geoserver/wfs?",
		// 	//"url": "http://localhost:8080/geoserver/wfs",
		// 	"typeName": "isaa:Departamentos",
		// 	//"typeName": "isaa:Resguardos",
		// 	"visible": false,
		// 	"popup": true,
		// 	"showCoverageOnHover": false,
		// 	"removeOutsideVisibleBounds": false,
		// 	"tooltipField": "nombre_dep",
		// 	"geomField": "geom",
		// 	"outFields": [
		// 		{"name": "codigo_dep", "alias": "Código"},
		// 		{"name": "nombre_dep", "alias": "Departamento"},
		// 		{"name": "numero_res", "alias": "N° de Resguardos"}
		// 	],
		// 		"queryWidget": {
		// 		"queries" : [
		// 			{"name": "nombre_dep", "alias": "Departamento", "defaultOperator": "contains"},
		// 			{"name": "numero_res", "alias": "N° de Resguardos", "type": "numeric", "defaultOperator": "<"},

		// 			// {"name": "capital", "alias": "Capital", "type": "boolean"}
		// 		],
		// 		"outFields": [
		// 			{"name": "codigo_dep", "alias": "Código"},
		// 			{"name": "nombre_dep", "alias": "Departamento"},
		// 			{"name": "numero_res", "alias": "Resguardos"}
		// 		]
		// 	},
		// 	// "filters": [
		// 	// 	{"name": "nombre_dep", "alias": "Departamento"},
		// 	// 	{"name": "numero_res", "alias": "Resguardos", "type": "numeric"},
		// 	// ],			
		// 	"style": {
		// 		"color": "#c53e42",
		// 		"fillColor": "#c53e42",
		// 		"fillOpacity": 0.5,
		// 		"weight": 1,
		
		// 	},		
		// },
	]
}
