from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid

def listing(request, id):
    listingData = Listing.objects.get(pk=id)
    isListingINWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.user.username
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingINWatchlist": isListingINWatchlist,
        "allComments": allComments,
        "isOwner": isOwner
    })

def closeAuction(request, id):
    listingData = Listing.objects.get(pk=id)
    listingData.active = False
    listingData.save()
    isOwner = request.user.username == listingData.user.username
    isListingINWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingINWatchlist": isListingINWatchlist,
        "allComments": allComments,
        "isOwner": isOwner,
        "update": True,
        "message": "Congratulations! Your auction is closed."
    })

def addBid(request, id):
    newBid = request.POST['newBid']
    listingData = Listing.objects.get(pk=id)
    isListingINWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.user.username
    if int(newBid) > listingData.price.bid:
        updateBid = Bid(user=request.user, bid=int(newBid))
        updateBid.save()
        listingData.price = updateBid
        listingData.save()
        return render(request, "auctions/listing.html", {
        "listing": listingData,
        "message": "Bid was updated successfully",
        "update": True,
        "isListingINWatchlist": isListingINWatchlist,
        "allComments": allComments,
        "isOwner": isOwner,
    })
    else:
        return render(request, "auctions/listing.html", {
        "listing": listingData,
        "message": "Bid updated failed",
        "update": False,
        "isListingINWatchlist": isListingINWatchlist,
        "allComments": allComments,
        "isOwner": isOwner,
    })

def addComment(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST['newComment']

    newComment = Comment(
        author=currentUser,
        listing=listingData,
        message=message
    )

    newComment.save()

    return HttpResponseRedirect(reverse("listing",args=(id, )))

def displayWatchlist(request):
    currentUser = request.user
    listings = currentUser.listingWatchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

def removeWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing",args=(id, )))

def addWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing",args=(id, )))

def index(request):
    activeListings = Listing.objects.filter(active=True)
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": activeListings,
        "categories": allCategories
    })

def displayCategories(request):
    if request.method == "POST":
        categoryFromForm = request.POST['category']
        category = Category.objects.get(categoryName=categoryFromForm)
        activeListings = Listing.objects.filter(active=True, category=category)
        allCategories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": activeListings,
            "categories": allCategories
        })

def createListing(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": allCategories
        })
    else:
        # Get the data from the form
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["image"]
        price = request.POST["price"]
        category = request.POST["category"]
        # Who is the user
        currentUser = request.user
        # Get  all content about the paticular category
        categoryData = Category.objects.get(categoryName=category)
        # Create a bid object
        bid = Bid(bid=int(price), user=currentUser)
        bid.save()
        # Create a new listing object
        newListing = Listing(
            title=title,
            description=description,
            image=image,
            price=bid,
            category=categoryData,
            user=currentUser
        )
        # Insert the object in our database
        newListing.save()
        # Redirect to index page
        return HttpResponseRedirect(reverse(index))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
