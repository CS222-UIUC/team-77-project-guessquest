"""
URL configuration for guessquest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from games import views

urlpatterns = [
    path('', views.sign_in, name='sign_in'),
    path('temperature/<int:player_id>/', views.start_game, name='start_temp'),
    path('games/', views.game_selection, name='game_selection'),
    path('spotify/<int:player_id>/', views.spotify_game, name='start_spotify'),
]
