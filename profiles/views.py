from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from post.models import Post, LikePost
from .models import Profile
from django.shortcuts import redirect

users = User.objects.all()

@login_required(login_url='login')
def profile_request(request):
    user_object = User.objects.get(email=request.user.email)
    user_profile = Profile.objects.get(user=user_object)

    return render(request, "profile.html", {"user_object": user_object, "user_profile": user_profile})

@login_required(login_url='login')
def profiledetail_request(request, slug):
    profile_slug = Profile.objects.get(slug=slug)
    user_slug = User.objects.get(id=profile_slug.user_id)
    post_slug = Post.objects.filter(user=user_slug.username)
    liked_post = LikePost.objects.filter(username=user_slug.username)
    post_ids = [like.post_id for like in liked_post]
    post_liked = Post.objects.filter(id__in=post_ids)

    context = {
        "profiledetail": profile_slug,
        "posts": post_slug,
        "postliked": post_liked,
        "users": users
    }
    return render(request, "profile_detail.html", context)


@login_required(login_url='login')
def settings_request(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('profileImage_name') is None:
            job = request.POST['job_name']
            location = request.POST['location_name']

            user_profile.job = job
            user_profile.location = location
            user_profile.save()

        if request.FILES.get('profileImage_name') is not None:
            image = request.FILES.get('profileImage_name')
            job = request.POST['job_name']
            location = request.POST['location_name']

            user_profile.profile_img = image
            user_profile.job = job
            user_profile.location = location
            user_profile.save()

        return redirect('profile')

    return render(request, 'settings.html', {"profile": user_profile})