
# Create your views here.
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from .models import User,PRODUCT_TYPE,PRODUCT,COMMENTS

import json

def index(request):
    page_obj = {}
    all_ptypes = PRODUCT_TYPE.objects.all()

    all_product = PRODUCT.objects.all()

    page_obj = {
        "ptypes":all_ptypes,
        "all_product":all_product
    }
    return render(request, "home.html", page_obj )

def profile(request):
    print("here")
    return render(request, "profile.html",{})
    
def addproduct(request):
    if request.method == "POST":
        proimage = request.FILES["proimage"]
        proname = request.POST["proname"]
        promodel = request.POST["promodel"]
        protype = request.POST["protype"]
        probatlife = request.POST["probatlife"]
        proqrating = request.POST["proqrating"]
        proprating = request.POST["proprating"]
        prodesc = request.POST["prodesc"]

        type_obj = PRODUCT_TYPE.objects.filter(title=protype).first()
        
        pro_obj = PRODUCT.objects.create(
            creator=request.user,
            pimage = proimage,
            name=proname,
            pmodel=promodel,
            pbattery=probatlife if probatlife != "" else 0,
            p_rating=proprating if proprating != "" else 0,
            q_rating=proqrating if proqrating != "" else 0,
            ptype=type_obj,
            o_review=prodesc if prodesc != '' else 'NA'
        )

        pro_obj.save()
        
        if pro_obj.id is None:
            messages.error(request,"Error while saving product review")
        else:                
            messages.success(request,"Review added successfully")

    page_obj = {}
    all_ptypes = PRODUCT_TYPE.objects.all()

    page_obj = {
        "ptypes":all_ptypes,
        "messages":messages
    }
    return render(request, "addproduct.html",page_obj)

def showproduct(request, proid):
    if request.method == "POST":
        pro_obj = PRODUCT.objects.get(id=proid)
        _comment = request.POST["mycomment"]

        c_obj  = COMMENTS.objects.create(
            cmt_by= request.user,
            pro_cmt= pro_obj,
            cmt_desc= _comment
        )

    page_obj={}
    pro_obj = PRODUCT.objects.get(id=proid)

    all_ptypes = PRODUCT_TYPE.objects.all()

    cmt_obj = COMMENTS.objects.filter(pro_cmt=pro_obj)

    page_obj = {
        "ptypes":all_ptypes,
        "show_product":pro_obj,
        "comments_list":cmt_obj
    }
    return render(request, "showproduct.html", page_obj)

def login(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html",{})


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["cpassword"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        new_user = {}
        try:
            new_user = User.objects.create_user(email, email, password)
            new_user.first_name = name
            new_user.save()
        except IntegrityError:
            # user.delete()
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        auth_login(request, new_user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html",{})

def productunlike(request):
    if request.method == 'POST':
        _proid = request.POST.get("proid")

        pro_obj = PRODUCT.objects.get(id=_proid) 

        if request.user in pro_obj.liked.all():
            pro_obj.liked.remove(request.user)

        if request.user in pro_obj.unliked.all():
            pro_obj.unliked.remove(request.user)
        else:
            pro_obj.unliked.add(request.user)

    return index(request)

def productlike(request):
    if request.method == 'POST':
        _proid = request.POST.get("proid")

        pro_obj = PRODUCT.objects.get(id=_proid) 

        if request.user in pro_obj.unliked.all():
            pro_obj.unliked.remove(request.user)

        if request.user in pro_obj.liked.all():
            pro_obj.liked.remove(request.user)
        else:
            pro_obj.liked.add(request.user)

    return index(request)