from django.urls import path
from .views import PackageListView, PackageCreateView, Landing

urlpatterns = [
    path('', PackageListView.as_view(), name='package_list'),
    path('add/', PackageCreateView.as_view(), name='add_package'),
    path('landing', Landing.as_view() , name='landing_page' )
]
