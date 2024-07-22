from django.urls import path
from .views import PackageListView, PackageCreateView

urlpatterns = [
    path('', PackageListView.as_view(), name='package_list'),
    path('add/', PackageCreateView.as_view(), name='add_package'),
]
