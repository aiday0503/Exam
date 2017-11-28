from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib import messages

def index(request):
    # Giving value to session

    try:
        request.session['userid']
    except:
        request.session['userid'] = ""

    if request.session['userid']:
        return redirect('/dashboard')
        
    return render(request,'index.html')


def dashboard(request):
    context = {}

    if not request.session['userid']:
        messages.warning(request, "You must be logged in to see these friends")
        return redirect('/')

    else:
        
        loginuser = User.objects.get(id=request.session['userid'])
        travelers = Travel.objects.all()
        upload_traveler = []
        other_traveler = []
        wishtravels = GroupTravel.objects.all()

        for traveler in travelers:
            if traveler.uploader.id == loginuser.id:
                upload_traveler.append(traveler)
            else:
                other_traveler.append(traveler)
                
        travels = GroupTravel.objects.filter(traveler=loginuser.id)
        travel_list = []
        print loginuser.id
        for travel in travels:
            travel_list.append(travel.joiner)

        not_on_list = []
        for travel in other_traveler:
            if travel not in travel_list:
                not_on_list.append(travel)
        
        context = {
            'loginuser' : loginuser,
            'upload_traveler': upload_traveler,
            'other_traveler': not_on_list,
            'travels': travel_list,
        }

    return render(request,'dashboard.html', context)

def register(request):
    result = User.objects.basic_validator(request.POST)

    if result[0] == False:
        for tag, error in result[1].iteritems():
            messages.error(request,error, extra_tags=tag)
        return redirect('/')
    
    else:
        request.session['userid'] = result[1].id
        return redirect('/dashboard')


def login(request):
    result = User.objects.login_validator(request.POST)

    if result[0] == False:
        for tag, error in result[1].iteritems():
            messages.error(request,error, extra_tags=tag)
        return redirect('/')

    else:
        request.session['userid'] = result[1].id 
        return redirect('/dashboard')

def logout(request):
    request.session.clear()

    return redirect('/')

def wish_travels_create(request):
    
    return render(request,'wish_travels_create.html')


def wish_travels_add(request):
    result = Travel.objects.travel_validator(request.POST,request.session['userid'])

    if result[0] == False:
        for tag, error in result[1].iteritems():
            messages.error(request,error, extra_tags=tag)
        return redirect('/wish_travels/create')

    
    return redirect('/dashboard')

def add_travel(request, id): #This is travel id
    result = Travel.objects.add_travel(request.session['userid'],id)
    return redirect('/dashboard')

def show_travel(request, id): #This is travel id
    result = Travel.objects.get(id=id)
    travelers = User.objects.all()
    groupTravel = GroupTravel.objects.all()
    print result.plan
    context = {
            'travel' : result,
            'travelers' : travelers,
        }
    return render(request,'show_travel.html', context)


