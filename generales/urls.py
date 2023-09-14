from generales import views
from django.conf.urls import url



urlpatterns = [
    url(r'^$', views.HomeView, name='home'),

]
