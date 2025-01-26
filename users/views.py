from django.shortcuts import render, redirect
from .forms import UserForm

# Create your views here.
def home(request):

    if request.method == 'POST':
        form: UserForm = UserForm(request.POST)
        if form.is_valid():
            request.session['form_data'] = form.cleaned_data
            return redirect('users:index')
    else:
        form = UserForm()

    context = {
        'form': form
    }

    return render(request, "users/base.html", context)

def index(request):
    return render(request, "users/index.html")