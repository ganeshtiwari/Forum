from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm


# Create your views here.
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            user.set_password(password1)
            user.save()

            user = authenticate(username=username, password=password1)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('board:home')
    else:
        form = SignUpForm(None)
    return render(request, 'signup.html', {'form': form})

