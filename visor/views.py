from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse_lazy

from django.views import generic

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from datetime import date

from django.shortcuts import render

from generales.models import Noticias, Comentario, Contacto, VideoSMT, Nosotros, Categoria, SubCategoria, Equipo, Podcast, Videos, Imagenes, Categoria_multimedia

from django.http import JsonResponse
from datetime import timedelta
import json 
import os
import folium
from folium.features import CustomIcon
from folium.plugins import Search,  MarkerCluster, FastMarkerCluster
from folium import plugins
#from geoserver.catalog import Catalog
from django.views import generic
from owslib.wms import WebMapService
from owslib.wfs import WebFeatureService
from owslib.fes import *
from owslib.etree import etree
import json
import geopandas as gpd
import requests
from pyproj import CRS
import geojson
import asyncio

def create_wfs(url):
    return WebFeatureService(url, version='2.0.0')

def get_data(wfs, layer):
    """
    Function that returns a GeoDataFrame or GeoJSON of data layer
    
    Args:
        wfs: A WFS/OWS service -> owslib.feature.wfs110.WebFeatureService_1_1_0 object
        layer: A layer name -> str
    
    Return:
        A GeoDataFrame or GeoJSON data layer -> DataFrame or Dict
    

    # Fetch data from WFS
    r = wfs.getfeature(typename=layer, outputFormat='json')
    
    # Get geometry layer
    json_ = json.loads(r.read())
    geom = json_['features'][0]['geometry']['type']

    if geom == 'Point':
        # Get GeoDataFrame layer
        data = get_gdf(layer)
    else:
        data = json_
        
    return data, geom

    """
    # Define parameters
    service = 'WFS'
    version = '2.0.0'
    request = 'GetFeature'
    outputFormat = 'json'

    # Specify parameters (read data in json format).
    params = dict(service=service,
                  version=version,
                  request=request,
                  typeName=layer,
                  outputFormat=outputFormat)

    # Fetch geojson data from WFS using requests
    r = requests.get(wfs, params=params)

    # Fetch data from WFS
    #r = wfs.getfeature(typename=layer, outputFormat='json')
    
   # Get geometry layer
    json_ = json.loads(r.content)
    geom = json_['features'][0]['geometry']['type']
    print("gggggggggggggggggggggggggggggg ----------------> ")
        
    return json_, geom

def get_gdf(layer):
    # Define parameters
    service = 'WFS'
    version = '2.0.0'
    request = 'GetFeature'
    outputFormat = 'json'
    wfs_url = 'https://smt-test.onic.org.co/geoserver/wfs?'

    # Specify parameters (read data in json format).
    params = dict(service=service,
                  version=version,
                  request=request,
                  typeName=layer,
                  outputFormat=outputFormat)

    # Fetch data from WFS using requests
    r = requests.get(wfs_url, params=params)

    # Create GeoDataFrame from geojson
    gdf = gpd.GeoDataFrame.from_features(geojson.loads(r.content))

    # Define crs
    gdf.crs = CRS.from_epsg(4686)
    return gdf

async def get_point_map(gjson, gdf, name_layer, catalogo):
    # Create a map instance
    mymap = folium.Map(
        location=[4.668730, -72.100403],
        zoom_start=12,
        tiles='cartodbpositron',
        #attributionControl = False,
        prefer_canvas=True)
    fields = list(gjson['features'][0]['properties'].keys())
    names = ""
    vakues_list = []
    for field in fields:
        names += '<b>' + field + '</b>' + ':{}<br>'
        innerlist = gdf[field].values.tolist()
        vakues_list.append(innerlist)
    lat = gdf["geometry"].apply(lambda geom: geom.x)
    lon = gdf["geometry"].apply(lambda geom: geom.y)
    marker_cluster = MarkerCluster(
        name=name_layer,
        overlay=True,
        control=False,
        icon_create_function=None
    )
    for k in range(len(lon)):
        values = [item[k] for item in vakues_list]
        location = lon[k], lat[k]
        marker = folium.Marker(location=location)
        popup = names.format(*values)
        folium.Popup(popup).add_to(marker)
        marker_cluster.add_child(marker)
    marker_cluster.add_to(mymap)
    mapdata = folium.GeoJson(
        gjson,
        name = name_layer,
        zoom_on_click=True,
        show=False
    ).add_to(mymap)
    layers = catalogo
    idx_layer = layers.index(name_layer)
    if idx_layer == 0:
        search_field = fields[2]  
    elif idx_layer == 1:
        search_field = fields[3]
    elif idx_layer == 2:
        search_field = fields[5]
    elif idx_layer == 3:
        search_field = fields[7]    
    else: 
        search_field = fields[0]
    controlsearch = Search(
        layer=mapdata,
        geom_type='Point',
        placeholder='Buscador capa ' + name_layer,
        cllapsed=False,
        search_label=search_field,    
    ).add_to(mymap)  
    folium.LayerControl().add_to(mymap)

    return mymap

def get_polygon_map(gjson, name_layer, catalogo):
    mymap = folium.Map(
        location=[4.668730, -72.100403],
        zoom_start=6,
        titles='cartodbpositron', attributionControl = False,
        prefer_canvas=True)
    print("poly:  1111111111111111111111111111111111111")
    mapdata = folium.GeoJson(
        gjson,
        name = name_layer,
        highlight_function=lambda x: {"fillOpacity": 0.8},
        zoom_on_click=True,
    ).add_to(mymap)
    print("poly:  222222222222222222222222222222222222")
    layers = catalogo
    idx_layer = layers.index(name_layer)
    folium.LayerControl().add_to(mymap)
    print("Poly: 3333333333333333333333333333333")
    return mymap

class ajax_updateCapas(generic.View):
    
    def get(self, request):
        capa = int(request.GET.get('capa', 0))
        layer_name = request.GET.get('nombre', '')
        wfs_url = 'https://smt-test.onic.org.co/geoserver/wfs?'
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        # Get data and geometry type layer
        gjson_data = get_data(wfs_url, layer_name)
        print(" 2222222222222222222222222222222222 ")
        geom_type = gjson_data  #['features'] #[0]['geometry']['type']
        print("3333333333333333333333333333333333 ")
        #capas
        wfs = create_wfs(wfs_url)
        layers_catalogue = wfs.contents
        print("44444444444444444444444444444444444444444444")
        catalogo=[]
        for i, item in enumerate(layers_catalogue):
            catalogo.append(item)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        if geom_type == 'Point':
            gdf = gpd.GeoDataFrame.from_features(gjson_data)
            gdf.crs = CRS.from_epsg(4686)
            print("Poooooooooooooooooooooooooooiiiiiiiiiiiiiiiiinnnnnnnnnnnnnnnnnnnnttttttttttttttttt")
            my_map = loop.run_until_complete(get_point_map(gjson_data, gdf, layer_name, catalogo))
        else:
            print("polyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
            my_map = loop.run_until_complete(get_polygon_map(gjson_data, layer_name, catalogo))
        print("ffffffffffff ***********************   ")
        map = my_map._repr_html_()

        return JsonResponse(
            {
                'content': {
                    'mapa': map
                }
            }
        )
class Visor(LoginRequiredMixin, generic.TemplateView):
    template_name='visor/visor.html'
    login_url='generales:login'

    def get(self, request, *args, **kwargs):
        categorias = Categoria.objects.all().order_by('id')
        subcategorias = SubCategoria.objects.all().order_by('id')
        lat = 4.668730
        lon = -72.100403
        logo_path = "static/base/image/favicon.png"
        m = folium.Map(location=[lat, lon], zoom_start=5, attributionControl = False)     
        m = m._repr_html_()
        wfs_url = 'https://smt-test.onic.org.co/geoserver/wfs?'
        wfs = create_wfs(wfs_url)
        layers_catalogue = wfs.contents
        catalogo=[]
        for i, item in enumerate(layers_catalogue):
            catalogo.append(item.replace('geonode:', '')) #[8:]
        context = super().get_context_data(**kwargs)
        context = {'mapa': m, 'l': len(layers_catalogue)}
        
        return self.render_to_response( 
            self.get_context_data(
                context=context,
                mapa=m,
                catalogo=catalogo,
                subcategorias = subcategorias,
                categorias = categorias,
                categorias_mul = Categoria_multimedia.objects.all().order_by('id'),
                modulos = SubCategoria.objects.filter(categoria__id=20).order_by('id')
            )
        )