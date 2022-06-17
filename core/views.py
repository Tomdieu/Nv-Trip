
from django.shortcuts import render,redirect,reverse
from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import generic,View
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse

from django.conf import settings
import json
from django.core import serializers

from Service.map import MapServices
from Service import MapPoint,getDirectionsFromAddress
from Service.positionstack import forward
from map.models import UserBookPlace,Trip

from map.form import UserBookPlaceForm
from users.forms import VehicleCreationForm
from users.models import Vehicle,Drive

from Service import positionstack

from django.db.models import F,Q
from django.core import serializers
from django.http import HttpResponse


from notifications.models import DriverNotification

# Create your views here.

def driver_only(user):
    return user.user_type == 'DRIVER'

class LandingView(generic.TemplateView):
    template_name = 'index.html'


@login_required
@user_passes_test(driver_only,redirect_field_name='user:user_index')
def createVehicle(request):
    template_name = 'driver/create_vehicle.html'
    context = {}
    context['form'] = VehicleCreationForm()

    if request.method == 'POST':
        form = VehicleCreationForm(request.POST)
        if form.is_valid():
            veh = form.save(commit=False)
            veh.nbp = int(form.cleaned_data['max_place'])-1
            veh.lat = 0
            veh.lng = 0
            veh.user = request.user
            veh.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, 'your vehicle {} has been created successfully!'.format(veh))
            return redirect('user:user_index')

        context['form'] = form
        return render(request, template_name,context)

    return render(request, template_name,context)


# this functions enabel the user to dtermine the path between two places
class FindPath(LoginRequiredMixin,View):


    def post(self,request):
        template_name = 'path/path.html'
        origin = request.POST['origin']
        destination = request.POST['destination']
        profile = request.POST['profile']
        context = {}

        origin_data = forward(origin)
        lat1,lng1 = origin_data['data'][0]['latitude'],origin_data['data'][0]['longitude']
        point1 = MapPoint(lat=lat1,lng=lng1)
        destination_data = forward(destination)
        lat2,lng2 = destination_data['data'][0]['latitude'],destination_data['data'][0]['longitude']
        point2 = MapPoint(lat=lat2,lng=lng2)

        ms = MapServices()
        data = getDirectionsFromAddress(origin, destination,profile='mapbox/{}'.format(profile))[1]
        context = {'origin':'','destination':'','instructions':True,'mapbox_token':settings.MB_ACCESS_TOKEN,'ps_token':settings.PS_ACCESS_TOKEN}
        context['origin'] = origin
        context['destination'] = destination
        context['profile'] = profile
        context['origin_coordinates'] = json.dumps({'lat':lat1,'lng':lng1});
        context['destination_coordinates'] = json.dumps({'lat':lat2,'lng':lng2})
        context['mapbox_token']=settings.MB_ACCESS_TOKEN
        context['ps_token'] = settings.PS_ACCESS_TOKEN
        context['ok'] = True
        context['metho'] = 'POST'
        context['data'] = json.dumps(data)

        Trip.objects.create(user=request.user,
                            origin_name=origin,
                            origin_lat=lat1,
                            origin_lng = lng1,
                            destination_name=destination,
                            destination_lat=lat2,
                            destination_lng=lng2,
                            type_of_transport=profile.upper())


        return render(request, template_name,context)

        # except Exception as e:
        # 	errors = True
        # 	error = '<b>Could Not Connect To MapBox !</b> <br/> <small>Make sur your are connected to the internet</small>'
        # 	context = {'errors':errors,'origin':origin,'destination':destination,'instructions':True,'mapbox_token':settings.MB_ACCESS_TOKEN,'error':error}
        # 	return render(request, self.template_name,context)



    def get(self,request):
        template_name = 'path/path.html'

        context = {'origin':'','destination':'','instructions':False,'mapbox_token':settings.MB_ACCESS_TOKEN,'ps_token':settings.PS_ACCESS_TOKEN}
        context['origin_coordinates'] = 'null'
        context['destination_coordinates'] = 'null'
        context['ok'] = False
        context['data'] = 'null'
        context['method'] = 'GET'
        return render(request, template_name,context)


class BookPlace(LoginRequiredMixin,View):
    def post(self,request,*arg,**kwargs):
        form = UserBookPlaceForm(request.POST or None)
        if form.is_valid():
            org = request.POST.get('origin')
            dest = request.POST.get('destination')
            booked = form.save(commit=False)
            form.user= request.user
            booked.origin = org
            booked.destination = dest
            booked.user = request.user
            booked.save()
            print(booked)
            base_url = reverse('user:choose-driver')
            parameter = urlencode({'booked_id':booked.id})
            url = '{}?{}'.format(base_url,parameter)
            return redirect(url)

        template_name = 'path/choose.html'

        context = {'mapbox_token':settings.MB_ACCESS_TOKEN,'ps_token':settings.PS_ACCESS_TOKEN}
        context['form'] = form
        return render(request,template_name,context)

    def get(self,request,*args,**kwargs):
        template_name = 'path/choose.html'
        context = {'mapbox_token':settings.MB_ACCESS_TOKEN,'ps_token':settings.PS_ACCESS_TOKEN}
        forms = UserBookPlaceForm
        context['form'] = forms

        return render(request, template_name,context)

class SelectDriver(LoginRequiredMixin,View):

    def get(self,request,*args,**kwargs):

        print(*args,**kwargs)
        context = {'mapbox_token':settings.MB_ACCESS_TOKEN,'ps_token':settings.PS_ACCESS_TOKEN}

        booked_id = request.GET.get('booked_id')

        booked = UserBookPlace.objects.get(id=booked_id)
        context['booked'] = booked


        driver_to = Drive.objects.filter(Q(vehicle__status='online') & Q(origin=booked.origin) & Q(destination=booked.destination) & ~Q(vehicle__user=request.user))
        context['drivers_availabel'] = driver_to

        # origin = request.GET.get('origin')
        # destination = request.GET.get('destination')
        # price = request.GET.get('price')
        # payment_option = request.GET.get('payment_option')

        template_name = 'path/find-drivers.html'

        # context['origin'] = origin
        # context['destination'] = destination
        # context['price'] = price
        # context['payment_option'] = payment_option


        return render(request, template_name,context)


class SelectOriginDestination(LoginRequiredMixin,View):

    def get(self,request,*args,**kwargs):
        template_name = 'driver/choose.html'
        context ={'mapbox_token':settings.MB_ACCESS_TOKEN,'ps_token':settings.PS_ACCESS_TOKEN}
        veh = Vehicle.objects.filter(user=request.user)

        if veh.exists():
            context['vehicle'] = veh
            return render(request, template_name,context)

        else:
            messages.add_message(request, messages.WARNING, 'Sorry You must first create a vehicle! ')
            return redirect('user:user_index')

    def post(self,request,*args,**kwargs):
        context ={'mapbox_token':settings.MB_ACCESS_TOKEN,'ps_token':settings.PS_ACCESS_TOKEN}

        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        vehicle_id = request.POST.get('vehicle_id')

        if origin == '' and destination == '':
            template_name = 'driver/choose.html'
            context['error'] = 'You must enter your origin and your destination'
            return render(request, template_name,context)

        veh = Vehicle.objects.get(id=vehicle_id)
        template_name = 'driver/index.html'
        print(request.POST)
        # base_url = reverse('user:drive',)
        drive = Drive.objects.create(vehicle=veh,origin=origin,destination=destination)
        # para = {'origin':origin,'destination':destination,'vehicle_id':vehicle_id,'drive_id':drive.id}
        # para = {'drive_id':drive.id}
        # url_params = urlencode(para)
        # url = '{}?{}'.format(base_url,url_params)
        base_url = reverse('user:drive',kwargs={'drive_id':drive.id})
        return redirect(base_url)

@login_required
@user_passes_test(driver_only,redirect_field_name='user:user_index')
def driver(request,drive_id):
    template_name = 'driver/index.html'
    context = {'mapbox_token':settings.MB_ACCESS_TOKEN,'ps_token':settings.PS_ACCESS_TOKEN}

    context['driver_vehicles'] = Vehicle.objects.filter(user=request.user)

    try:
        drive_data = Drive.objects.get(id=drive_id)
    except:
        return redirect('user:driver-choose')
    context['drive'] = drive_data
    origin = drive_data.origin
    destination = drive_data.destination
    vehicle = Vehicle.objects.get(id=drive_data.vehicle_id)
    context['vehicle'] = vehicle
    context['notifications'] = DriverNotification.objects.filter(Q(vehicle=drive_data.vehicle) & Q(sender__origin=origin) & Q(sender__destination=destination)) 
    context['count'] = len(context['notifications'])
    try:
        origin = forward(drive_data.origin)
        destination = forward(drive_data.destination)
        context['origin'] = origin['data'][0]['label']
        context['origin_lat'] = origin['data'][0]['latitude']
        context['origin_lng'] = origin['data'][0]['longitude']
        context['destination'] = destination['data'][0]['label']
        context['destination_lat'] = destination['data'][0]['latitude']
        context['destination_lng'] = destination['data'][0]['longitude']


    except Exception as e:
        # origin = forward(drive_data.origin)
        # destination = forward(drive_data.destination)
        context['origin'] ='' #['data'][0]['label']
        context['origin_lat'] = 0 #['data'][0]['latitude']
        context['origin_lng'] =0 #['data'][0]['longitude']
        context['destination'] = ''#destination['data'][0]['label']
        context['destination_lat'] = 0 #destination['data'][0]['latitude']
        context['destination_lng'] = 0 #destination['data'][0]['longitude']
        context['error'] = e
        context['orgpos'] = {'lat':0,'lng':0}
        context['despos'] = {'lat':0,'lng':0}
        context['error'] = True
        # context['connect'] = 'You Must be connect to the internet'
    return render(request, template_name,context)


@login_required
@user_passes_test(driver_only,redirect_field_name='user:user_index')
def update_driver_drive(request,*args,**kwargs):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    print('ajax :',is_ajax)
    if is_ajax:
        # if request.method == 'POST':
        id = request.POST.get('id')
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        vehicle_id = request.POST.get('vehicle_id')
        dri = Drive.objects.get(id=id)
        dri.origin = origin
        dri.destination = destination
        dri.vehicle_id = vehicle_id
        dri.save()
        print(dri)
        return JsonResponse({'updated':True},safe=True)
        # return JsonResponse({'status': 'Invalid request'}, status=400,safe=True)
    # else:
    #     return JsonResponse({'error':'method not allow'})

@csrf_exempt
@login_required
@user_passes_test(driver_only,redirect_field_name='user:user_index')
def update_vehicle_place(request,*args,**kwargs):
    print(request)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    print('ajax :',is_ajax)

    if is_ajax:
        vehicle_id = request.POST.get('vehicle_id')
        method_type = request.POST.get('type')
        # print(request.POST)
        veh = Vehicle.objects.get(id=vehicle_id)
        if method_type == 'increase':
            if veh.nbp == veh.max_place:
                pass
            else:
                veh.nbp += 1 #F('nbp') + 1
        else:
            if veh.nbp == 1:
                pass
            else:
                veh.nbp -= 1 #F('nbp') - 1
        veh.save();
        out = serializers.serialize('json',[veh])
        x = json.loads(out)
        print(x)
        o = x[0]
        o['updated'] = True
        print(o)
        out = json.dumps(o)
        return HttpResponse(out,content_type='text/json')
    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle_id')
        method_type = request.POST.get('type')
        print(request.POST)
        veh = Vehicle.objects.get(id=vehicle_id)
        if method_type == 'increase':
            if veh.nbp == veh.max_place:
                pass
            else:
                veh.nbp = F('nbp') + 1
        else:
            if veh.nbp == 1:
                pass
            else:
                veh.nbp = F('nbp') - 1
        veh.save();
        out = serializers.serialize('json',[veh])
        x = json.loads(out)
        print(x)
        o = x[0]
        o['updated'] = True
        print(o)
        out = json.dumps(o)
        return HttpResponse(out,content_type='text/json')

class FindWeather(LoginRequiredMixin,View):

    def post(self,request,*args,**kwargs):
        context = {'mapbox_token':settings.MB_ACCESS_TOKEN,'ps_token':settings.PS_ACCESS_TOKEN}
        template_name = 'wheather/index.html'


        return render(request, template_name,context)

    def get(self,request,*args,**kwargs):

        template_name = 'wheather/index.html'
        context = {'mapbox_token':settings.MB_ACCESS_TOKEN,'ps_token':settings.PS_ACCESS_TOKEN}

        return render(request, template_name,context)