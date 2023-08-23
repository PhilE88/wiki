from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


import markdown2

from . import util

# The Random Page functionality is in layout.html

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, article):
    # html = markdown2.markdown_path(f"./entries/{article}.md")
    allEntries = util.list_entries()
    mdFile = util.get_entry(article)
    if mdFile is None:
        return render(request, "encyclopedia/error.html", {
            "article": article,
            "entries": allEntries
        })    

    return render(request, "encyclopedia/article.html", {
        "article": article,
        "mdFile": markdown2.markdown(mdFile),
        "entries": allEntries
    })

def search(request):
    query = request.GET
    searchVal = query.get('q')
    allEntries = util.list_entries()
    if searchVal in allEntries:
        return article(request, searchVal)
    return render(request, "encyclopedia/search.html", {
       "searchVal": searchVal,
       "allEntries": allEntries
    })

def newEntry(request):
    allEntries = util.list_entries()
    if request.method == "POST":
        postDict = request.POST
        title = postDict.get('title')
        content = postDict.get('entryTxt')
        for entry in allEntries:
            if title.lower() == entry.lower():
                error = True
                errorMsg = "An article with that title already exists."
                return render(request, "encyclopedia/newEntry.html", {
                    "error": error,
                    "errorMsg": errorMsg
                })
        util.save_entry(title, content)
        return article(request, title)

    return render(request, "encyclopedia/newEntry.html")

def edit(request, entry):
    mdFile = util.get_entry(entry)
    if mdFile is None:
        return render(request, "encyclopedia/error.html", {
            "article": entry
        })
    
    if request.method == "POST":
        postDict = request.POST
        # title = postDict.get('title')
        content = postDict.get('entryTxt')
        util.save_entry(entry, content)
        return article(request, entry)
    
    return render(request, "encyclopedia/edit.html", {
        "entry": entry,
        "mdFile": mdFile
    })