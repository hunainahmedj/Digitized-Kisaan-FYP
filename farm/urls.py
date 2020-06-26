from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    home_view,
    FarmListView,
    FarmDetailView,
    FarmCreateView,
    FarmUpdateView,
    PictureCreateView,
    farm_search_view,
    add_coordinates_view,
    data_fetch_view,
    get_mask_view,
)

urlpatterns = [
    path('', home_view, name="home"),
    path('farm/create/', FarmCreateView.as_view(), name='farm-create'),
    path('farm/update/<int:pk>', FarmUpdateView.as_view(), name='farm-update'),
    path('farms/', FarmListView.as_view(), name='farm-list'),
    path('farm/<int:pk>/', FarmDetailView.as_view(), name='farm-detail'),
    path('farm/search/', farm_search_view, name='farm-search'),
    path('farm/data-upload/<int:pk>', PictureCreateView.as_view(), name='data-upload'),
    path('farm/data-control/', data_fetch_view, name='data-fetch'),
    path('farm/add-coordinates', add_coordinates_view, name='add-coordinates'),
    path('farm/get-masks/', get_mask_view, name='get-masks'),
]