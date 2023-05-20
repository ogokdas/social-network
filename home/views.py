from django.shortcuts import render
from category.models import Category
from post.models import Post, LikePost
from profiles.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required(login_url='login')
def home(request):
    # Like
    username = request.user.username
    if LikePost.objects.filter(username=username):
        likedPost_ = LikePost.objects.filter(username=username)
        likedPost = likedPost_.values_list('post_id', flat=True).distinct()
    else:
        likedPost = [999,998,997]

    global users, post_id
    if request.method == 'POST':
        like = request.POST.get('like')
        post_id = request.POST.get('post_id')

        if post_id:
            post = Post.objects.get(id=post_id)

            if like == '1' or '2' or '3':
                like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

                if like_filter is None:
                    new_like = LikePost.objects.create(post_id=post_id, username=username)
                    new_like.save()
                    post.no_of_likes = post.no_of_likes + 1
                    post.save()

                else:
                    if like_filter:
                        like_filter.delete()
                        post.no_of_likes = post.no_of_likes - 1
                        post.save()

    ##############
    # Profile
    # Search
    query = request.POST.get('profile_s', '')
    if query:
        user_results = User.objects.filter(first_name__istartswith=query)
    else:
        user_results = []

    profile_results = []
    for user in user_results:
        profile = Profile.objects.filter(user=user).first()
        if profile:
            profile_results.append(profile)
    ##############

    categories = Category.objects.all()
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    category_counts = {}
    for category in categories:
        count = category.post.count()
        category_counts[str(category.id)] = count

    users = User.objects.all()
    profiles_ = Profile.objects.all()

    data = {
        "kategoriler": categories,
        'category_counts': category_counts,
        "post": Post.objects.all(),
        "user_profile": user_profile,
        "profile_results": profile_results,
        "users": users,
        "likedPost": likedPost,
        "profiles_" : profiles_
    }
    return render(request, "index.html", data)