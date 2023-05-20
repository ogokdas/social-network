from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from profiles.models import Profile
from django.shortcuts import redirect

users = User.objects.all()


def check_user_not_authenticated(user):
    return not user.is_authenticated


def login_request(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "login.html", {
                "error": "username or password is not valid"
            })

    return render(request, "login.html")


@user_passes_test(check_user_not_authenticated, login_url='home')
def register_request(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        name = request.POST["name"]
        surname = request.POST["surname"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]

        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(request, "register.html", {"error": "Username kullanılıyor"})
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, "register.html", {"error": "Email kullanılıyor"})
                else:
                    user = User.objects.create_user(username=username, email=email, first_name=name, last_name=surname,
                                                    password=password)
                    user.save()

                    # log user in and redirect to settings page
                    user_login = auth.authenticate(username=username, password=password)
                    auth.login(request, user_login)

                    # create a Profile object for the new user
                    user_model = User.objects.get(username=username)
                    new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                    new_profile.save()

                    return redirect("settings")
        else:
            return render(request, "register.html", {"error": "Parola eşleşmiyor"})

    return render(request, "register.html")


def logout_request(request):
    logout(request)
    return redirect("home")
