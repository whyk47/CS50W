from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import User, Bid, Listing, Comment, Category
from .util import *

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_active=True),
        "page": "Active Listings"
    })

def categories(request):
    if request.method == "POST":
        category = Category.objects.get(category=request.POST["category"])
        return render(request, "auctions/index.html", {
        "listings": category.listings.filter(is_active=True),
        "page": category.category
        })
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

def listing(request, id):
    listing = Listing.objects.get(id=id)
    if request.method == "POST":
        keys = request.POST.keys()
        for key in keys:
            match key:
                case "close":
                    listing.is_active = False
                    listing.save(update_fields=["is_active"])
                case "bid":
                    if (float(request.POST["bid"]) >= listing.min_bid()):
                        bid = Bid(bidder=request.user, price=request.POST["bid"])
                        bid.save()
                        old_bid = listing.highest_bid
                        listing.highest_bid = bid
                        listing.num_bids += 1
                        listing.save(update_fields=["highest_bid", "num_bids"])
                        if old_bid:
                            old_bid.delete()
                case "watch":
                    listing.watchers.add(request.user)
                case "unwatch":
                    listing.watchers.remove(request.user)
                case "comment":
                    comment = Comment(listing=listing, commenter=request.user, content=request.POST["comment"])
                    comment.save()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "user": request.user,
        "categories": listing.categories.all(),
        "curr_price": listing.curr_price(),
        "min_bid": listing.min_bid(),
        "watched": request.user.is_authenticated and request.user.watched.filter(id=listing.id).exists(),
        "comments": listing.comments.all()
    })

@login_required
def create(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data["seller"] = request.user
            categories = data.pop("categories")
            listing = Listing(**data)
            listing.save()
            listing.categories.set(categories)
            return HttpResponseRedirect(reverse("auctions:index"))
        return render(request, "auctions/create.html", {
            "form": form,
            "message": "Invalid Form",
            "categories": Category.objects.all()
        })

    return render(request, "auctions/create.html", {
        "form": NewListingForm(),
        "categories": Category.objects.all()
    })

@login_required
def watchlist(request):
    return render(request, "auctions/index.html", {
        "listings": request.user.watched.all(),
        "page": "Watchlist"
    })

@login_required
def my_listings(request):
    return render(request, "auctions/index.html", {
        "listings": request.user.listings.all(),
        "page": "My Listings"
    })

