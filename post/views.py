from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Post, LikePost
from profiles.models import Profile
from category.models import Category
from django.shortcuts import redirect

users = User.objects.all()

@login_required(login_url='login')
def post_request(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    category_ = Category.objects.all()
    data = {
        "user_profile": user_profile,
        "category" : category_
    }
    user = request.user.username

    if request.method == "POST":
        if request.FILES.get('image') is not None:
            image = request.FILES.get('image')
            caption = request.POST['Title']
            content = request.POST['message']
            category = request.POST.getlist('select[]')
            if Post.objects.filter(caption=caption).exists():
                return render(request, "post.html", {"error": "Bu başlık kullanılmış, değiştirin"})
            else:
                new_post = Post.objects.create(user=user, image=image, caption=caption, content=content)
                for c in category:
                    new_post.categories.add(c)
                new_post.save()
        if request.FILES.get('image') is None:
            caption = request.POST['Title']
            content = request.POST['message']
            category = request.POST.getlist('select[]')
            if Post.objects.filter(caption=caption).exists():
                return render(request, "post.html", {"error": "Bu başlık kullanılmış, değiştirin"})
            else:
                new_post = Post.objects.create(user=user, caption=caption, content=content)
                for c in category:
                    new_post.categories.add(c)
                new_post.save()

        return redirect("home")
    return render(request, "post.html", data)

@login_required(login_url='login')
def post_details(request, slug):
    post = Post.objects.get(slug=slug)
    profile = Profile.objects.get(user=User.objects.get(username=post.user))
    user_ = request.user
    profile_user = Profile.objects.get(user=user_)
    data = {
        "post": Post.objects.get(slug=slug),
        "profile_s": profile,
        "profile_user": profile_user
    }
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        is_delete = request.POST.get("delete")
        try:
            post = Post.objects.get(id=post_id)
            if is_delete == "True":
                post.delete()
                return redirect("home")
        except Post.DoesNotExist:
            # post_id değerine sahip bir Post nesnesi bulunamadı
            pass

    return render(request, "details.html", data)