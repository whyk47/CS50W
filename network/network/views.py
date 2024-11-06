from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import json
from datetime import datetime
import pytz


from .util import *
from .models import *


def index(request):
    # make new post
    if request.method == "POST":
        content = request.POST["content"]
        post = Post(poster=request.user, content=content, timestamp=datetime.now(pytz.timezone('Asia/Singapore')))
        post.save()
    posts = Post.objects.all().order_by('-timestamp')
    return render(request, "network/index.html", {
        # display posts in rev chronological order
        "page": get_page(request, posts),
        "liked": get_liked(request)
    })

def edit(request, post_id):
    # edit post
    if request.method == "PUT":
        data = json.loads(request.body)
        post = Post.objects.get(pk=post_id)
        if data.get("textarea") is not None:
            post.content = data["textarea"]
        if data.get("like") is not None:
            post.likers.add(request.user)
        if data.get("unlike") is not None:
            post.likers.remove(request.user)
        post.save()
        return HttpResponse(status=204)
    else:
        assert False


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")

def profile(request, username):
    # Support following and unfollowing
    profile = User.objects.get(username=username)
    if request.method == "POST":
        keys = request.POST.keys()
        for key in keys:
            match key:
                case "follow":
                    profile.followers.add(request.user)
                case "unfollow":
                    profile.followers.remove(request.user)
    return render(request, "network/index.html", {
        "username": username,
        "profile": profile,
        "page": get_page(request, profile.posts.all().order_by("-timestamp")),
        "is_follower": profile.followers.filter(username=request.user.username).exists(),
        "liked": get_liked(request)
    })

def following(request):
    # get all posts from followed users, sorted in rev chronological order
    follows = request.user.following.all()
    posts = Post.objects.all().order_by("-timestamp")
    following_posts = [post for post in posts if post.poster in follows]
    return render(request, "network/index.html", {
        "page": get_page(request, following_posts),
        "liked": get_liked(request) 
    })