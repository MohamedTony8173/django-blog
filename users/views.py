from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import LoginForm, RegistrationForm

User = get_user_model()


def send_email_user(request, user):
    subject = "active e_mail"
    body = render_to_string(
        "users/registration/email_active.html",
        {
            "user": user,
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.id)),
            "token": default_token_generator.make_token(user),
        },
    )
    user_email = EmailMessage(
        subject=subject, body=body, from_email=settings.FROM_EMAIL, to=[user.email]
    )
    user_email.send()
    return user_email


def user_register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_email_user(request, user)
            messages.success(request, "Please Check Your E_mail")
            return redirect("blogs:home")
    else:
        form = RegistrationForm(request.POST)
    context = {"form": form}

    return render(request, "users/register.html", context)


def user_active_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(force_str(uidb64))
        user = User.objects.get(id=uid)
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Successfully Activate")
            return redirect("blogs:home")
    except:
        return HttpResponse("wrong activate")


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("blogs:home")
            else:
                messages.error(request, "Credential information wrong")
                return redirect(request.path_info)
    else:
        form = LoginForm()
    context = {"form": form}
    return render(request, "users/login.html", context)


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("blogs:home")
