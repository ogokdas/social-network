from django.shortcuts import render
from .models import Category
from profiles.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required(login_url='login')
def categories(request, slug):
    username = request.user.username
    user = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user)
    data = {
        "profile__": user_profile,

        "kategoriler": Category.objects.get(slug=slug),

        # MantoToOne#
        # "filmler": Movie.objects.filter(category__slug=slug),

        # ManyToMany-1.Yöntem-
        # "filmler": Movie.objects.filter(categories__slug=slug),

        # ManyToMany-2.Yöntem - movie_set: Movie Modelinin ilk harfi küçük!!!!
        #"filmler": Category.objects.get(slug=slug).movie_set.filter(anasayfa=True),

        "posts": Category.objects.get(slug=slug).post.all(),
        "profile": Profile.objects.all()
    }
    return render(request, "category.html", data)