from django.urls import path
from .views import PolisView


app_name = 'polischeck'

urlpatterns = [
    path('polischeck/', PolisView.as_view()),
    ]
