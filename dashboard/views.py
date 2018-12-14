from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Product
from .models import Definition
from .models import Stack
from .models import Run

from collections import OrderedDict
from django.http import JsonResponse

# Include the `fusioncharts.py` file that contains functions to embed the charts.
# https://www.fusioncharts.com/charts/column-bar-charts/simple-column-chart

from django.shortcuts import render
from django.http import HttpResponse
from .fusioncharts import FusionCharts


def index(request):
    return JsonResponse({'Local':"Home", 'Dept':"MPQE"})


def home(request):
    return JsonResponse({'Page':"Home"})


def report(request):
    return JsonResponse({'Page':"Report"})

