from django.core.paginator import Paginator
from .models import *

def get_page(request, posts):
    paginator = Paginator(posts, 10)
    page_no = request.GET.get("page")
    page = paginator.get_page(page_no)
    return page

def get_liked(request):
    if request.user.is_authenticated:
        return [post.id for post in request.user.liked.all()]