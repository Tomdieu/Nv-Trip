from django.shortcuts import render
from django.conf import settings

from django.views import generic
# Create your views here.


class LandingView(generic.TemplateView):

    template_name = "map/map.html"


def getDirections(request):

    # if request.method == 'POST':
    #     pass

    template_name = "map/find_direction.html"
    context = {'token': settings.ACCESS_TOKEN}

    return render(request, template_name, context)
