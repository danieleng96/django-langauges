from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('<str:langstring>', views.input_parse_language, name = 'parse_lang'),
    path('input_phonemes/', views.input_phoneme_features, name = 'input_phonemes'),
    path('sync/', views.sync_audio_to_phonemes, name = 'sync'),

    # path('search/', views.search_phonemes, name = 'search_all'),
    path('cust_search/', views.custom_search_phonemes, name = 'search_all'),
    path('vac/', views.vac, name = 'vac'),
    path('geo/', views.try_geo_data, name = 'geo'),

    ]

