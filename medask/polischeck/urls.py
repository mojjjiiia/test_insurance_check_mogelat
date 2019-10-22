from django.urls import path
from .views import PolisCheckView

app_name = 'polischeck'

urlpatterns = [
    path('polischeck/', PolisCheckView.as_view()),
    ]
