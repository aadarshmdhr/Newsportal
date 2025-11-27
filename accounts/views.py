from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views import View
from .forms import RegistertionForm

# Create your views here.

class RegisterView(View):
    def get(self, request):
        form = RegistertionForm()
        return render(request, "registration/register.html", {"form:" form})
    
    def post(self, request):
        form = RegistertionForm(request.POST)
        if form.is_valid():
            user = form.save()

            #Optional: Log the user in immideiately after registration
            #logion(request, user)

            #Redirect to login page after successful registration
            return redirect("accounts:login")
        return render(request, "registration/register.html", {"form": form})