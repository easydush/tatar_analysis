from django.urls import path

from core.views import check_view

app_name = 'core'
urlpatterns = [
    path('check/', check_view),
]
