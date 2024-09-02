from django.db import models


class OrderNews(models.IntegerChoices):
    CAROUSEL = 0, 'Carrusel'
    NEWS = 1, 'Noticia 1'
    UPDATES = 2, 'Novedades 2'
    BULLETINS = 3, 'Boletines 3'
    MEDIA_LIBRARY = 4, 'Mediateca 4'
    GENERAL = 5, 'General'


class LinkType(models.TextChoices):
    NONE = 'normal', 'Normal'
    BLANK = 'blank', 'Open in a new tab'
