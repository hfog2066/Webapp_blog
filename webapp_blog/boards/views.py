from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.views.generic import ListView

from .models import Users
from .forms import ContactForm, LoginForm
# Create your views here.

def index(request):
    loginform = LoginForm(request.POST)
    if request.method == 'POST':
        if loginform.is_valid():
            data = loginform.cleaned_data
            username = data.get("username")
            password = data.get("password")
            access = authenticate(username = username, password = password)
            if access is not None:
                login(request, access)
                return HttpResponseRedirect(reverse('blog:home'))
            else:
                return HttpResponse("Incorrect Username or Password")

    return render(request, 'blog/index.html', {"form": loginform})



class HomeView(ListView):
    model = Users
    template_name = "blog/home.html"


def contact(request):
    #Inserta los datos del formulario en la db
    pub_date = timezone.now()
    contactform = ContactForm(request.POST)
    if request.method == 'POST':
        if contactform.is_valid():
            data = contactform.cleaned_data
            #print(data)
            db_register = Users(
                fullname = data.get("fullname"),
                email = data.get("email"),
                message = data.get("message"),
                pub_date = pub_date )
            db_register.save()
            return HttpResponseRedirect(reverse('blog:home'))
    else:
        return render(request, 'blog/contact.html', {'form':contactform})