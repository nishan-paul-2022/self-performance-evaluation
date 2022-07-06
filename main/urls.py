from django.urls import path
from main import views

urlpatterns = []

urlvsview = {
    '': 'views_index',
    'index': 'views_index',
    'main': 'views_main',
    'main_undergraduate_details': 'views_main_undergraduate_details',
    'main_undergraduate_summary': 'views_main_undergraduate_summary',
    'main_analysis': 'views_main_analysis',
}

for key, value in urlvsview.items():
    pattern = path(key, getattr(views, value), name=value)
    urlpatterns.append(pattern)
