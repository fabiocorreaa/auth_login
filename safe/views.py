from django.shortcuts import render, redirect
from .forms import PasswordForm
from django.contrib import messages
from .models import SecretWord
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.

@login_required(login_url='/login')
def create_password(request):
    form = PasswordForm()
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid:
            secret_word = make_password(request.POST['pass_word'])
            password = form.save(commit=False)
            print(password.pass_word)
            print(secret_word)
            password.pass_word = secret_word
            password.owner = request.user
            password.save()
            #print(form)
            return redirect('safe:list-password')
        else:
            messages.error(request, 'Something went wrong.')
            print(form)
            return redirect('safe:list-password')
    return render(request, 'safe/create.html', {"form": form})

@login_required(login_url='/login')
def password_list(request):
    pws = SecretWord.objects.filter(owner=request.user)
    return render(request, 'safe/main_page.html', {"list": pws})


def delete_password(request, id):
    try:
        password = SecretWord.objects.get(id=id)
        password.delete()
    except:
        print(password.id, password)
    return redirect('safe:list-password')


