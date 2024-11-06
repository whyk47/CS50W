from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Bids")
    price = models.DecimalField(decimal_places=2, max_digits=10)

class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return self.category

class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=128)
    img_url = models.CharField(max_length=2048, default=None, blank=True)
    starting_bid = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    highest_bid = models.OneToOneField(Bid, null=True, blank=True, default=None, on_delete=models.CASCADE, related_name="listings")
    num_bids = models.IntegerField(default=0)
    desc = models.CharField(max_length=1024)
    categories = models.ManyToManyField(Category, blank=True, default=None, related_name="listings")
    is_active = models.BooleanField(default=True)
    watchers = models.ManyToManyField(User, blank=True, null=True, default=None, related_name="watched")

    def min_bid(self):
        if self.highest_bid:
            return float(self.highest_bid.price) + 0.01
        return self.starting_bid
    
    def curr_price(self):
        if self.highest_bid:
            return self.highest_bid.price
        return self.starting_bid

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=512)


