from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from pw_safe import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token

# Create your views here.
def frontpage(request):
    return render(request, 'core/index.html')


def signup(request):
    if request.method =='POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']


        if User.objects.filter(username=username):
            messages.error(request, 'Username already exists.')
            return redirect('frontpage')
        
        if User.objects.filter(email=email):
            messages.error(request, 'Email already used.')
            return redirect('frontpage')

        if len(username) < 6:
            messages.error(request, 'Username must have at least 6 characters.')
            return redirect('frontpage')

        if password1 != password2:
            messages.error(request, "The passwords didn't match")
            return redirect('frontpage')

        user = User.objects.create_user(username, email, password1)
        user.first_name = fname
        user.last_name = lname
        user.is_active = False

        user.save()

        messages.success(request, "Your account has been created. We have sent you a confirmation email!")

        # Email
        # subject = 'Welcome to PW Manager!'
        # message = f'Hello {username}!\nWelcome to our site!\nBut before being able to use all of our features,' \
        # 'we need to have your email confirmed first. Click in the link below to activate your account: {}\n\n' \
        #     'Thank you so much for choosing our services!'
        # from_email = settings.EMAIL_HOST_USER
        # to_list = [user.email]
        # send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email address confirmation

        current_site = get_current_site(request)
        email_subject = "Confirm your email! - PW Manager"
        message2 = render_to_string('core/email_confirmation.html', {
            'name': user.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })
        email = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
        email.fail_silently = True
        email.send()

        return redirect('/login')


    return render(request, 'core/signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            print('sim')
            return render(request, 'core/index.html', {'fname': user.first_name})
        
        else:
            messages.error(request, 'Wrong credentials.')
            print('não')
            return redirect('frontpage')

    return render(request, 'core/login.html')

@login_required(login_url='/login')
def logout(request):
    auth_logout(request)
    messages.success(request, 'Logged out.')
    return redirect('frontpage')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        return redirect('frontpage')
    
    else:
        return render(request, 'activation_failed.html')
