from multiprocessing import context
import json
import re
import django
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from users.models import Drive, Vehicle
from .forms import UserRegistrationForm, VehicleCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from map.models import Trip,UserBookPlace,DriverTransportPassenger
from django.db.models import Q

from notifications.models import DriverNotification,UserNotification

from datetime import date
# Create your views here.


@login_required(login_url='login')
def index(request):


    template_name = 'user/index.html'
    context = {}

    return render(request, template_name,context)


def signin(request):

    template_name = 'user/login.html'
    context = {}
    context['year'] = date.today().year

    if request.user.is_authenticated:
        return redirect('user:user_index')

    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        print(username,password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user:user_index')
        else:
            messages.add_message(request, messages.WARNING,'Email of password incorrect!')


    return render(request, template_name,context)

def register(request):

    template_name = 'user/register.html'
    context = {}

    form = UserRegistrationForm
    context['form'] = UserRegistrationForm
    context['year'] = date.today().year

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)

        if form.is_valid():
            user = form.save()
            user.save()
            username = form.cleaned_data['email']
            # password = form.cleaned_data['password1']
            # user = authenticate(request,username=username,password=password)
            # login(request,user)
            messages.add_message(request, messages.SUCCESS,f'Hello {username} your account has beeen created successfully!')
            return redirect('login')

        else:
            context['form'] = form


    return render(request, template_name,context)

@login_required(login_url='login')
def signout(request):
    logout(request)
    return redirect('/')


def about(request):
    
    template_name = 'about.html'
    context = {}
    
    return render(request, template_name,context)


@login_required
def profile(request):

    template_name='user/profile.html'
    context = {}

    User = get_user_model()

    user = User.objects.get(id=request.user.id)

    trip = Trip.objects.filter(user=request.user)

    context['number_of_trips'] = len(trip)
    context['trip'] = trip

    context['user'] = user

    book = UserBookPlace.objects.filter(user=request.user)
    context['number_of_bookplace_ordered'] = len(book)
    context['book_place'] = book

    bookAccepted = DriverTransportPassenger.objects.filter(Q(booked__user=request.user) & Q(accept='accept'))
    bookRefuse = DriverTransportPassenger.objects.filter(Q(booked__user=request.user) & Q(accept='refuse'))

    context['bookAccepted'] = bookAccepted
    context['bookRefuse'] = bookRefuse
    context['numBookRefuse'] = len(bookRefuse)
    context['numBookAccepted'] = len(bookAccepted)

    form = UserRegistrationForm(instance=user)

    context['form'] = form


    return render(request,template_name,context)


@login_required
def deleteAccount(request):

    if request.method == 'POST':
        User = get_user_model()
        user = User.objects.get(id=request.user.id)
        user.delete()
        return HttpResponse(json.dumps({'deleted':True}),content_type='application/json')
        # return HttpResponse(json.dumps({'deleted':False}),content_type='application/json')
    else:
        return HttpResponse(json.dumps({'error':'Method not allow'}),content_type='application/json')


@login_required
# @csrf_exempt
def updateUserInfo(request):
    
    if request.method == 'POST':
        User = get_user_model()
        error_username,error_phone = False,False
        
        duplicate_name = User.objects.filter(Q(username=request.POST['username']) & ~Q(id=request.user.id))

        if duplicate_name.exists():
            error_username = True
            print('duplicates ',duplicate_name)
        duplicate_phone = User.objects.filter(Q(phone=request.POST['phone']) & ~Q(id=request.user.id))
        if duplicate_phone.exists():
            error_phone = True
            print(duplicate_phone)
        print(error_phone,error_username)
        if error_phone == True and  error_username == True:
            return HttpResponse(json.dumps({'updated':False,'errors':['Username already taken!','phone number already exists!']}),content_type='application/json')
        if error_phone == True and error_username == False:
            return HttpResponse(json.dumps({'updated':False,'errors':['phone number already exists!']}),content_type='application/json')
        if error_username == True and error_phone == False:
            return HttpResponse(json.dumps({'updated':False,'errors':['Username already taken!']}),content_type='application/json')
        if error_phone == False and error_username == False:
            user = User.objects.get(id=request.user.id)
            user.username = request.POST['username'];
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.sex = request.POST['sex']
            user.country = request.POST['country']
            user.phone = request.POST['phone']
            user.save()
            return HttpResponse(json.dumps({'updated':True}),content_type='application/json')

    return HttpResponse(json.dumps({'error':'Method Not Allow'}),content_type='application/json')




@login_required
def gotoSettings(request):

    template_name = 'user/settings.html'
    context = {}
    User = get_user_model()

    user = User.objects.get(id=request.user.id)

    trip = Trip.objects.filter(user=request.user)

    context['number_of_trips'] = len(trip)
    context['trip'] = trip

    context['user'] = user

    book = UserBookPlace.objects.filter(user=request.user)
    context['number_of_bookplace_ordered'] = len(book)
    context['book_place'] = book

    bookAccepted = DriverTransportPassenger.objects.filter(Q(booked__user=request.user) & Q(accept='accept'))
    bookRefuse = DriverTransportPassenger.objects.filter(Q(booked__user=request.user) & Q(accept='refuse'))

    context['bookAccepted'] = bookAccepted
    context['bookRefuse'] = bookRefuse
    context['numBookRefuse'] = len(bookRefuse)
    context['numBookAccepted'] = len(bookAccepted)

    form = UserRegistrationForm(instance=user)

    veh = Vehicle.objects.filter(user=request.user)
    context['vehicles'] = veh
    context['form'] = form
    context['veh_creation_form'] = VehicleCreationForm

    # drv = Drive.objects.filter()

    psg = DriverTransportPassenger.objects.filter(Q(vehicle__in=veh) & Q(accept='accept'))
    context['passengers_transported'] = psg

    return render(request,template_name,context)



@login_required
def verify_password(request):
    if request.method == 'POST':
        print(request)
        print(request.POST.get('password'))
        password = request.POST.get('password')
        User = get_user_model()
        user = User.objects.get(id=request.user.id)
        print(check_password(password,user.password))
        if check_password(password,user.password):
            return HttpResponse(json.dumps({'verify':True}),content_type='application/json')
            # return JsonResponse({'vefify':True})
        # return JsonResponse({'vefify':False})
        return HttpResponse(json.dumps({'verify':False}),content_type='application/json')


@login_required
def user_placedbook(request):

    template_name = 'user/bookedPlace.html'

    context = {}

    userbook = UserBookPlace.objects.filter(user=request.user)
    usertransport = DriverTransportPassenger.objects.filter(Q(booked__in=userbook) & Q(accept='accept'))
    userrefusetransport = DriverTransportPassenger.objects.filter(Q(booked__in=userbook) & Q(accept='refuse'))

    context['userbookplace'] = userbook
    context['usertransport'] = usertransport
    context['userrefusetransport'] = userrefusetransport
    return render(request, template_name,context)


@login_required
def update_user_password(request):

    if request.method == 'POST':
        User = get_user_model()
        user = User.objects.get(id=request.user.id)
        new_password = request.POST.get('password')
        user.set_password(new_password)
        user.save()
        user = authenticate(request, username=user.email, password=new_password)
        if user is not None:
            login(request, user)
        return HttpResponse(json.dumps({'updated':True}),content_type='application/json')
    return HttpResponse(json.dumps({'error':'method not allow'}),content_type='application/json')
    

    
@login_required
def update_vehicle(request):
    pass


@login_required
def create_vehicle(request):

    if request.method == 'POST':
        print(request.POST)

        veh = Vehicle.objects.filter(driver_plate_number=request.POST['driver_plate_number'])
        if not veh.exists():
            veh = Vehicle.objects.create(
                user=request.user,
                driver_plate_number=request.POST['driver_plate_number'],
                car_color=request.POST['car_color'],
                max_place=request.POST['max_place'],
                car_type=request.POST['car_type'],
                car_brand = request.POST['car_brand'],
                )
            
            return HttpResponse(json.dumps({'created':True}),content_type='application/json')
        else:
            return HttpResponse(json.dumps({'created':False,'error':'A Car With This Plate Number Already Exists!'}),content_type='application/json')
    else:
        return HttpResponse(json.dumps({'error':'Method not allow'}),content_type='application/json')


def checkIfEmailExists(request):

    if request.method == 'POST':
        User = get_user_model()
        if User.objects.filter(email=request.POST.get('email')).exists():
            return HttpResponse(json.dumps({'exist':True}),content_type='application/json')
        return HttpResponse(json.dumps({'exist':False}),content_type='application/json')
    return HttpResponse(json.dumps({'error':'Method not allow'}),content_type='application/json')

def checkIfUserNameExists(request):
    
    if request.method == 'POST':
        User = get_user_model()
        if User.objects.filter(username=request.POST.get('username')).exists():
            return HttpResponse(json.dumps({'exist':True}),content_type='application/json')
        return HttpResponse(json.dumps({'exist':False}),content_type='application/json')
    return HttpResponse(json.dumps({'error':'Method not allow'}),content_type='application/json')


def createUser(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            form.save()
        user = authenticate(username=request.POST['email'],password=request.POST['password1'])
        if user is not None:
            login(request, user)
        return HttpResponse(json.dumps({'created':True}),content_type='application/json')
    return HttpResponse(json.dumps({'error':'Method not allow'}),content_type='application/json')
    