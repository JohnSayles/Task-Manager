import django
from django.shortcuts import render
from django.shortcuts import redirect
from django.db import transaction
from django.contrib.auth import authenticate, login
import random 
import string
import time
import uuid

django.setup()

# our database tables
from .models import User, Group, Page, Note 


def home(request):
    # (button) log in
    if(request.GET.get('mybtn')):
        username = request.GET.get('username')
        password = request.GET.get('password')
        if User.objects.filter(name=username, password = password).exists():
            #context = {"users": User.objects.order_by('name')}
            context = {"groups": Group.objects.filter(members__name__contains=username)}           
            return render(request, "mainpage.html", context)
        else:
            return render(request, "login.html")
    
    # Gets group data when button labelled "groupID" is pressed
    if(request.GET.get('getGroupData')):
        gID = request.GET.get('groupID')
        grp = Group.objects.get(id=gID)
        aID = grp.admin_id
        
        if Group.objects.filter(id=gID).exists():
            context = {"pages": Page.objects.filter(group_id__exact=gID),"groups": Group.objects.filter(admin_id__exact=aID)}
            return render(request, "mainpage.html", context)
        
    # Gets page data when button labelled "pageID" is pressed       
    if(request.GET.get('getPageData')):
        pID = request.GET.get('pageID')
        
        pObj = Page.objects.get(id=pID)
        adminID = pObj.group_id.admin_id
        
        if Page.objects.filter(id=pID).exists():
            context = {"notes":Note.objects.filter(page_id__exact=pID),
                       "pages":Page.objects.filter(group_id__exact=pObj.group_id),
                       "groups":Group.objects.filter(admin_id__exact=adminID)}
            return render(request, "mainpage.html", context)
    
    if(request.GET.get('subNote')):
        c = request.GET.get('noteContent')
        dueDate = request.GET.get('dateData')
        pageAppend = request.GET.get('pageAppend')
        
        currentPage = Page.objects.get(id=pageAppend)
        adminId = currentPage.group_id.admin_id
        
        with transaction.atomic(): # createuser
            newNote = [Note(content = c, page_id=Page.objects.get(id=pageAppend),due_date=dueDate)]
            Note.objects.bulk_create(newNote)
            context = {"pages":Page.objects.filter(group_id__exact=currentPage.group_id),
                       "notes":Note.objects.filter(page_id__exact=currentPage.id),
                       "groups":Group.objects.filter(admin_id=adminId)}
            return render(request, "mainpage.html", context)
    
    # (button) go to register account
    if(request.GET.get('regisbtn')):
        return redirect("/management/register")
    
    # (button) log out of main page
    if(request.GET.get('logoutbtn')):
        return render(request, "login.html")

    # default
    return render(request, "login.html")


def register(request):
    # when button clicked
    if(request.GET.get('mybtn')):
        name = request.GET.get('username')
        password = request.GET.get('password')
        email = request.GET.get('email')
        
        with transaction.atomic(): # createuser
            newUsers = [User(name=name,  email=email,password=password)]
            User.objects.bulk_create(newUsers)           
        return redirect("/management")   
    return render(request, "register.html")


