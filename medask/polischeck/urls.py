from django.urls import path, re_path
from .views import PolisView, SearchView


app_name = 'polischeck'

urlpatterns = [
    re_path(r'^polischeck/search\?\w.*', SearchView.as_view()),
    path('polischeck/', PolisView.as_view()),
    ]
