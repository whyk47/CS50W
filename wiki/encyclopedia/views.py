from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
from random import choice
import markdown2

from . import util

# Home page
def index(request):
    if request.method == "POST":
        return search(request)
    # List of links to entries
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# To display a page of an entry
def page(request, name):
    if request.method == "POST":
        return search(request)
    f = util.get_entry(name)
    if f: 
        pg = markdown2.markdown(f)
        return render(request, "encyclopedia/page.html", {
            "page": pg,
            "name": name
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "error": "Error: Page Not Found."
        })
    
# Search for page using searchbar
def search(request, query=None):
    # Submit query. Redirect to entry if exact match, else display search results
    if request.method == "POST":
        query = str(request.POST['q'])
        if util.get_entry(query):
            return HttpResponseRedirect(reverse("encyclopedia:page", kwargs={"name":query}))
        else:
            return HttpResponseRedirect(reverse("encyclopedia:search", kwargs={"query":query}))
    query = query.lower()
    results = [entry for entry in util.list_entries() if (query in entry.lower())]
    return render(request, "encyclopedia/search.html", {
        "entries": results
    })

# Allow user to create new page and saves as md file 
def new_page(request):
    if request.method == "POST":
        keys = request.POST.keys()
        for key in keys:
            match key:
                case 'title' | 'edit':
                    title = request.POST["title"]
                    content = request.POST["edit"]
                    if util.get_entry(title):
                        return render(request, "encyclopedia/error.html", {
                            "error": "Error: Page Already Exists."
                        })
                    util.save_entry(title, content)
                    return HttpResponseRedirect(reverse("encyclopedia:page", kwargs={
                        "name":title
                    }))
                case 'q':
                    return search(request)
                case _:
                    continue
    return render(request, "encyclopedia/edit.html", {
        "new_page": True,
        "content": ""
    })

# Allows user to edit page
def edit_page(request, name=None):
    if request.method == "POST":
        keys = request.POST.keys()
        for key in keys:
            match key:
                case 'content' | 'title':
                    title = request.POST["title"]
                    content = request.POST["edit"]
                    util.save_entry(title, content)
                    return HttpResponseRedirect(reverse("encyclopedia:page", kwargs={
                        "name": name
                    }))
                case 'q':
                    return search(request)
                case _:
                    continue
    return render(request, "encyclopedia/edit.html", {
        "new_page": False,
        "name": name,
        "content": util.get_entry(name)
    })

def rand_page(request):
    name = choice(util.list_entries())
    return HttpResponseRedirect(reverse("encyclopedia:page", kwargs={
        "name": name
    }))

