from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from user.forms import RegistrationForm


class SignUp(generic.CreateView):
    """
    Class-based view for Registration
    """
    form_class = RegistrationForm
    success_url = reverse_lazy('user:login')
    template_name = 'user/signup.html'
