var config = {
	"requireArcGISLogin": false,
	"tokenUrl": 'https://www.arcgis.com/sharing/generateToken', 

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
			"position": "topleft"
		},
		"leafletGeocoder": {
			"collapsed": false,
			"position": "topleft",
			"placeholder": "Buscador",
			"type": "OpenStreetMap", 
		},
		"TOC": {
			"collapsed": false,
			"uncategorisedLabel": "Layers",
			"position": "topright",
			"toggleAll": false
		},
		// "history": {
		// 	"position": "bottomleft"
		// },
	},

	"activeTool": "queryWidget",
	"basemaps": ['esriGray', 'esriDarkGray', 'esriStreets', 'OpenStreetMap', 'Aerial'],
	"bing_key": "Ap0QEleyAZPWg1gNS8jfe6ZGRV9mD0-AulMN3hxsfVOKRVrJj25GffRBKr-rrTER",
	"tocCategories": [
		{
			"name": "Capas GeoJSON",
			"layers": []
		},
		{
			"name": "Capas ArcGIS",
			"layers": []
		},
		{
			"name": "Capas WMS/WFS",
			"layers": ["resguardos", "comunidades", "departamentos"],
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
		"fillOpacity": 0.5,
		"fillColor": '#E31A1C',
		"stroke": true
	},
	"layers": [
		{
			"id": "comunidades",
			"name": "Comunidades (WFS)",
			"type": "WFS",
			'EPSG': 4686,
			"cluster": true,
			"showCoverageOnHover": false,
			"removeOutsideVisibleBounds": true,
			"url": "http://localhost:8080/geoserver/wfs",
			"typeName": "isaa:Comunidades",
			"visible": false,
			"popup": true,
			//"tooltipField": "comun_cnmbr",
			"outFields": [
				{"name": "cod_depto", "alias": "Código Departamento"},
				{"name": "nom_dep", "alias": "Departamento"},
				{"name": "cod_mpio", "alias": "Código Municipio"},
				{"name": "nom_mpio", "alias": "Municipio"},
				{"name": "comunidad", "alias": "Comunidad"},
				{"name": "nom_ri", "alias": "Resguardo"},
				{"name": "viviendas", "alias": "N° de Viviendas"},
				{"name": "familias", "alias": "N° de Familias"},
				{"name": "personas", "alias": "N° de Personas"},
				{"name": "etnia_1", "alias": "Pueblo"},
				{"name": "org_nal", "alias": "Organización Nacional"},
				{"name": "org_regnal", "alias": "Organización Regional"},				
				{"name": "macro", "alias": "Macro"},								
			],
				"queryWidget": {
					"queries" : [
						{"name": "cod_depto", "alias": "Código Departamento"},
						{"name": "nom_dep", "alias": "Departamento"},
						{"name": "cod_mpio", "alias": "Código Municipio"},
						{"name": "nom_mpio", "alias": "Municipio"},
						{"name": "comunidad", "alias": "Nombre Comunidad"},
						{"name": "nom_ri", "alias": "Nombre Resguardo"},
						{"name": "viviendas", "alias": "N° de Viviendas", "type": "numeric"},
						{"name": "familias", "alias": "N° de Familias", "type": "numeric"},
						{"name": "personas", "alias": "N° de Personas", "type": "numeric"},
						{"name": "etnia_1", "alias": "Nombre Pueblo"},
						{"name": "org_nal", "alias": "Organización Nacional"},
						{"name": "org_regnal", "alias": "Organización Regional"},				
						{"name": "macro", "alias": "Macro"},								
					],
					"outFields": [
						{"name": "cod_depto", "alias": "Cód Dpto"},
						{"name": "nom_dep", "alias": "Dpto"},
						{"name": "cod_mpio", "alias": "Cód Mpio"},
						{"name": "nom_mpio", "alias": "Mpio"},
						{"name": "comunidad", "alias": "Comunidad"},
						{"name": "nom_ri", "alias": "Resguardo"},
						{"name": "viviendas", "alias": "Viviendas", "type": "numeric"},
						{"name": "familias", "alias": "Familias", "type": "numeric"},
						{"name": "personas", "alias": "Personas", "type": "numeric"},
						{"name": "etnia_1", "alias": "Pueblo"},
						{"name": "org_nal", "alias": "Org Nal"},
						{"name": "org_regnal", "alias": "Org Regnal"},				
						{"name": "macro", "alias": "Macro"},								
					]
				},
		},		
		{
			"id": "resguardos",
			"name": "Resguardos (WFS)",
			"type": "WFS",
			'EPSG': 4686,
			"url": "http://localhost:8080/geoserver/wfs",
			"typeName": "isaa:Resguardos_actualizados_ONIC",
			"visible": false,
			"popup": true,
			"showCoverageOnHover": false,
			"removeOutsideVisibleBounds": false,
			//"tooltipField": "resguardo",
			"geomField": "geom",
			"outFields": [
				{"name": "NOMBRE", "alias": "Resguardo"},
				{"name": "CODIGO_DAN", "alias": "Código DANE"},
				{"name": "ONIC_pueblo", "alias": "Pueblo"},
				{"name": "ONIC_macro", "alias": "Macro"},
				{"name": "ONIC_org_nal", "alias": "Organización Nacional"},
				{"name": "ONIC_org_regnal", "alias": "Organización Regional"},
				{"name": "ONIC_dpto_cnmbr", "alias": "Departamento"},
				{"name": "ONIC_dpto_ccdgo", "alias": "Código Departamento"},
				{"name": "ONIC_mpio_cnmbr", "alias": "Municipio"},
				{"name": "ONIC_mpio_cdpmp", "alias": "Código Municipio"},
				{"name": "ONIC_Area_Rgdo", "alias": "Área (ha)"}
			],
				"queryWidget": {
				"queries" : [
					{"name": "NOMBRE", "alias": "Nombre Resguardo"},
					{"name": "CODIGO_DAN", "alias": "Código DANE"},
					{"name": "ONIC_pueblo", "alias": "Nombre Pueblo"},
					{"name": "ONIC_macro", "alias": "Macro"},
					{"name": "ONIC_org_nal", "alias": "Organización Nacional"},
					{"name": "ONIC_org_regnal", "alias": "Organización Regional"},
					{"name": "ONIC_dpto_cnmbr", "alias": "Departamento"},
					{"name": "ONIC_dpto_ccdgo", "alias": "Código Departamento"},
					{"name": "ONIC_mpio_cnmbr", "alias": "Municipio"},
					{"name": "ONIC_mpio_cdpmp", "alias": "Código Municipio"},
					{"name": "ONIC_Area_Rgdo", "alias": "Área (ha)", "type": "numeric"}
				],
				"outFields": [
					{"name": "NOMBRE", "alias": "Resguardo"},
					{"name": "CODIGO_DAN", "alias": "Cód DANE"},
					{"name": "ONIC_pueblo", "alias": "Pueblo"},
					{"name": "ONIC_macro", "alias": "Macro"},
					{"name": "ONIC_org_nal", "alias": "Org Nal"},
					{"name": "ONIC_org_regnal", "alias": "Org Regnal"},
					{"name": "ONIC_dpto_cnmbr", "alias": "Dpto"},
					{"name": "ONIC_dpto_ccdgo", "alias": "Cód Dpto"},
					{"name": "ONIC_mpio_cnmbr", "alias": "Mpio"},
					{"name": "ONIC_mpio_cdpmp", "alias": "Cód Mpio"},
					{"name": "ONIC_Area_Rgdo", "alias": "Área (ha)", "type": "numeric"}
				]
			},
			"style": {
				//"color": "#005E14",
				//"fillColor": "#005E14",
				"fillOpacity": 0.5,
				"weight": 1
			}									
		},		
		
		{
			"id": "departamentos",
			"name": "Departamentos (WFS)",
			"type": "WFS",
			'EPSG': 4686,
			"url": "http://localhost:8080/geoserver/wfs?",
			"typeName": "isaa:Departamentos",
			"visible": false,
			"popup": true,
			"showCoverageOnHover": false,
			"removeOutsideVisibleBounds": false,
			//"tooltipField": "nombre_dep",
			"geomField": "geom",
			"outFields": [
				{"name": "codigo_dep", "alias": "Código"},
				{"name": "nombre_dep", "alias": "Departamento"},
				{"name": "numero_res", "alias": "N° de Resguardos"}
			],
				"queryWidget": {
				"queries" : [
					{"name": "nombre_dep", "alias": "Departamento"},
					{"name": "numero_res", "alias": "N° de Resguardos", "type": "numeric"},
				],
				"outFields": [
					{"name": "codigo_dep", "alias": "Código"},
					{"name": "nombre_dep", "alias": "Departamento"},
					{"name": "numero_res", "alias": "Resguardos"}
				]
			},
			"style": {
				"color": "#c53e42",
				"fillColor": "#c53e42",
				"fillOpacity": 0.5,
				"weight": 1,
		
			},		
		},
	]
}
