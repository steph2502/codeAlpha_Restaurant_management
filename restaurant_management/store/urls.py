from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('place-order/', views.place_order, name='place_order'),
    path('make-reservation/', views.make_reservation, name='make_reservation'),
    path('process-order/<int:order_id>/', views.process_order, name='process_order'),
    path('manage-table/', views.manage_table, name='manage_table'),
    path('manage-inventory/', views.manage_inventory, name='manage_inventory'),
    path('report/', views.generate_report, name='report'),
]
