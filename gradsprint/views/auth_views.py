from django.contrib.auth import login
from django.shortcuts import get_object_or_404, render, redirect 

from ..forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("gradsprint:dashboard")
    else: 
        form = RegisterForm()
        
    return render(request, "gradsprint/register.html", 
                  {"form": form}
            )