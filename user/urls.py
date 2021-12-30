from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from user.views import SignUp

app_name = 'user'
urlpatterns = [

    path('register/', SignUp.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')

]