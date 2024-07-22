from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Package
from .forms import PackageForm

class PackageListView(ListView):
    model = Package
    template_name = 'packages/package_list.html'
    context_object_name = 'packages'

class PackageCreateView(UserPassesTestMixin, CreateView):
    model = Package
    form_class = PackageForm
    template_name = 'packages/add_package.html'
    success_url = reverse_lazy('package_list')

    def test_func(self):
        return self.request.user.is_superuser

