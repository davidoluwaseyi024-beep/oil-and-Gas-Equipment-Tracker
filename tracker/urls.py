from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('',               views.dashboard,          name='dashboard'),
    path('equipment/',     views.equipment_list,     name='equipment_list'),
    path('equipment/add/', views.equipment_create,   name='equipment_create'),
    path('overdue/',       views.equipment_overdue,  name='equipment_overdue'),
    path('equipment/<int:pk>/',        views.equipment_detail, name='equipment_detail'),
    path('equipment/<int:pk>/edit/',   views.equipment_edit,   name='equipment_edit'),
    path('equipment/<int:pk>/delete/', views.equipment_delete, name='equipment_delete'),
]
