from django.urls import re_path
from .views import PolisCheckView, SearchView


app_name = 'polischeck'

urlpatterns = [
    re_path(r'^polischeck/search\?\w.*', SearchView.as_view()),
    re_path(r'^polischeck\?.*', PolisCheckView.as_view()),
    ]
