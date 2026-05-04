from django.urls import path
from . import views  # Mana shu qator borligiga ishonch hosil qiling

urlpatterns = [
    path('', views.index, name='index'),
]