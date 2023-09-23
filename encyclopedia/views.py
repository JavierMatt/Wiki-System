from django.shortcuts import render

from . import util
import markdown
import random
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,title):
    html_content = ConvertToHTml(title)
    if html_content == None:
        return render(request,"encyclopedia/eror.html",{
            "message" : "This entry does not exist"
        })
    else:
        return render(request,"encyclopedia/entry.html",{
            "title" : title,
            "content": html_content
        })


def ConvertToHTml(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)
    
def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = ConvertToHTml(entry_search)
        if html_content is not None:
            return render(request,"encyclopedia/entry.html",{
            "title" : entry_search,
            "content": html_content
        })
        else:
            allEntries = util.list_entries()
            recomendation = []
            for entry in allEntries:
                if entry_search.lower() in entry.lower():
                    recomendation.append(entry)
            return render(request,"encyclopedia/search.html",{
                "recomendation":recomendation
            })
 
def newpage(request):
    if request.method == "GET":
        return render(request,"encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request,"encyclopedia/eror.html",{
                "message": "Entry Page already exists"
            })
        else:
            util.save_entry(title,content)
            html_content = ConvertToHTml(title)
            return render(request,"encyclopedia/entry.html",{
                "title": title,
                "content" : html_content,
            })
            
def edit(request):
    if request.method =="POST":
        title= request.POST["entry_title"]
        content = util.get_entry(title)
        return render(request,"encyclopedia/edit.html",{
            "title" :title,
            "content":content,
        })
def save_edit(request):
    if request.method =="POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title,content)
        html_content = ConvertToHTml(title)
        return render(request,"encyclopedia/entry.html",{
            "title" : title,
            "content": html_content
        })
def rand(request):
    allentries = util.list_entries()
    rand_entry = random.choice(allentries)
    html_content = ConvertToHTml(rand_entry)
    return render(request,"encyclopedia/entry.html",{
        "title" : rand_entry,
        "content": html_content
    })