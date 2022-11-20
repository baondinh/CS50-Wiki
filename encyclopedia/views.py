from django.shortcuts import render
from django import forms
import markdown2
from . import util
import random

#Creates a form for "Search Encyclopedia"
class Search(forms.Form):
    query = forms.CharField(max_length=50)

#Creates a form for a new encyclopedia entry
class NewEntry(forms.Form):
    title = forms.CharField(label = "Title")
    body = forms.CharField(label = "Body ", widget=forms.Textarea())

#Creates a form to edit existing encyclopedia entries
class EditEntry(forms.Form):
    title = forms.CharField(label = "Edit Title")
    body = forms.CharField(label = "Edit Body ", widget=forms.Textarea())

#Main page of encyclopedia when user visits /wiki/
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), 
        "form": Search()
    })

#When user visits /wiki/TITLE, a page will render depending on TITLE inputted
#If TITLE does not exist as an encyclopedia entry, an error page will render instead
#python-markdown2 package was used to convert Markdown files to HTML
def title(request, title):
    content_check = util.get_entry(title)
    if content_check != None:
        return render(request, "encyclopedia/title.html", {
            "title": title, 
            "pagecontent": markdown2.markdown(content_check), 
            "form": Search() 
        })         
    if content_check == None: 
        #bug where code gets stuck when trying to use search bar
        return render(request, "encyclopedia/error.html", {
            "pagecontent": "Requested Page Not in Encyclopedia",
            "form": Search()
            })
      
#Logic for search requests in the encyclopedia
#Bug in code that causes program to get stuck in title function at content_check
#Have also tried to add an additional conditional title != "search" but does not work
#Can submit queries but all search requests end on the error page, even if page exists
def search(request): 
    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            query = form.cleaned_data.get("query")
            check = False
            for entry in util.list_entries():
                if query == entry:
                    content = util.get_entry(query)
                    check = True
            if check == True: 
                return render(request, "encyclopedia/title.html", {
                    "title": query, 
                    "pagecontent": markdown2.markdown(content),
                    "form": form
                })
            else: 
                substring_check = []
                for entry in util.list_entries():
                    if query in entry: 
                        substring_check.append(entry)
                if len(substring_check) == 0:
                    form = Search()
                    return render(request, "encyclopedia/error.html", {
                        "pagecontent": "Requested Page Not in Encyclopedia",
                        "form": form
                })
    if request.method == "GET":
        form = Search()
        return render(request, "encyclopedia/error.html", {
            "pagecontent": "What would you like to look up in the encyclopedia?",
            "form": form
        })

#User is able to create a new encyclopedia entry with Markdown
def newentry(request):
    form = Search()
    if request.method == "POST":
        newform = NewEntry(request.POST)
        if newform.is_valid():
            title = newform.cleaned_data.get("title")
            body = newform.cleaned_data.get("body")
            check = False
            for entry in util.list_entries(): 
                if title.lower() == entry.lower():
                    check = True
        if check == True: 
            return render(request, "encyclopedia/error.html", {
                "pagecontent": "Page Already in Encyclopedia",
                "form": form
            })        
        else: 
            util.save_entry(title, body)
            return render(request, "encyclopedia/title.html", {
                "title": title,
                "pagecontent": markdown2.markdown(util.get_entry(title)),
                "form": form
            })
    if request.method == "GET":
        return render(request, "encyclopedia/newentry.html", {
            "form": form,
            "newform": NewEntry()
        })

#User is able to edit existing encyclopedia entries with Markdown
def edit(request, title): 
    if request.method == "POST": 
        editentry = EditEntry(request.POST)
        if editentry.is_valid():
            title = editentry.cleaned_data.get("title")
            body = editentry.cleaned_data.get("body")
            util.save_entry(title, body)
            return render(request, "encyclopedia/title.html", {
                "title": title, 
                "pagecontent": markdown2.markdown(util.get_entry(title)), 
                "form": Search()
            })
    if request.method == "GET": 
        editentry = EditEntry({
            "title": title, 
            "body": util.get_entry(title)
        })
        return render(request, "encyclopedia/edit.html", { 
            "title": title,
            "editentry": editentry,
            "form": Search()
        })


#User is able to access a random encyclopedia page based on what entries are available
def randompage(request):
    form = Search()
    entries = util.list_entries()
    file = (random.choice(entries)).lower()
    title = file.removesuffix('.md')
    return render(request, "encyclopedia/title.html", {
        "title": title,
        "pagecontent": markdown2.markdown(util.get_entry(title)),
        "form": form
    })