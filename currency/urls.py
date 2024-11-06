from django.urls import path
from .views import CurrentUSDView

urlpatterns = [
    path('get-current-usd/', CurrentUSDView.as_view(), name='get_current_usd'),
]
