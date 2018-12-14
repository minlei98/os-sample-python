# Create your report views here.
from django.shortcuts import render
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
import json
import pprint
import random
from datetime import datetime, timedelta
import pytz


def product_stack_chart(request):
    
    GET = False
    context_dict = {}
    rid=''

    if request.META['REQUEST_METHOD'] == 'GET':
        #rname = request.session.get('rname', '')
        #rtype = request.session.get('rtype', '')
        #rstate = request.session.get('rstate', '')
        
        print ('GET')
        rname = request.GET.get('rname', '')
        rtype = request.GET.get('rtype', '')
        rstate = request.GET.get('rstate', '')
        rid = request.GET.get('rid', '')
        stime = request.GET.get('stime', '')
        etime = request.GET.get('etime', '')
        GET = True

    if request.META['REQUEST_METHOD'] == 'POST':
        print ('POST')
        rname = request.POST.get('rname', '')
        rtype = request.POST.get('rtype', '')
        rstate = request.POST.get('rstate', '')
        stime = request.POST.get('stime', '')
        etime = request.POST.get('etime', '')
        GET = False
        
        
    if stime == "":
        myDate = datetime.now() + timedelta(days=-7)
        stime =  myDate.strftime("%Y-%m-%d")
        
    if etime == "":
        myDate = datetime.now()
        etime =  myDate.strftime("%Y-%m-%d")


        
    print(rname,rtype,rstate, stime, etime)

    # set session info    
    request.session['rname'] = rname
    request.session['rtype'] = rtype
    request.session['rstate'] = rstate
    request.session['stime'] = stime
    request.session['etime'] = etime
        
        
    # set selection for template
    context_dict['rname'] = rname
    context_dict['rtype'] = rtype
    context_dict['rstate'] = rstate
    context_dict['stime'] = stime
    context_dict['etime'] = etime
    
    context_dict['readystate'] = ['DEVELOPMENT','PRODUCTION']
    context_dict['readytype'] = ['INTEROP','CSS','SYSTEM']


    # query for product stacks
    ps_queryset = []
    ps_queryset = Stack.objects.all().order_by('-id')
    for qs in ps_queryset:
        print (qs.name, list(qs.products.all()))
        qs.productlist = list(qs.products.all())

    product3d = FusionCharts("doughnut3d", "ex2", "800", "600", "chart-2", "json", '')
    
    if ps_queryset:
        
        if rname:
            
            # Chart data is passed to the `dataSource` parameter, like a dictionary in the form of key-value pairs.
            dataSource = OrderedDict()
        
            # The `chartConfig` dict contains key-value pairs of data for chart attribute
            chartConfig = OrderedDict()
            chartConfig["caption"] = "Multi Product Stack"
            chartConfig["subCaption"] = "Products"
            chartConfig["numberSuffix"] = ""
            chartConfig["theme"] = "fusion"
        
            # The `chartData` dict contains key-value pairs of data
            chartData = OrderedDict()
            if rname:
              pschart_queryset = ps_queryset.filter(name = rname).distinct()
            
            prodlist = list(pschart_queryset[0].products.all())
            
            for p in prodlist:
                chartData[str(p)] = 1
        
            dataSource["chart"] = chartConfig
            dataSource["data"] = []
        
            for key, value in chartData.items():
                data = {}
                data["label"] = key
                data['tooltext'] = "Products in the Test Stack"
                data["value"] = value
                dataSource["data"].append(data)
                
            product3d = FusionCharts("doughnut3d", "ex2", "800", "600", "chart-2", "json", dataSource)
        
        
    return render(request, 'ui/product_stack_chart.html', {'productstacktable':  ps_queryset,'productstackchart': product3d.render(), "data": context_dict })
        
        


def index(request):
    return JsonResponse({'Local':"Home", 'Dept':"MPQE"})


def home(request):
    return JsonResponse({'Page':"Home"})


def report(request):
    return JsonResponse({'Page':"Report"})


    jdata = """{
          "chart": {
            "caption": "Title",
            "yaxisname": "",
            "xaxisname": "Jenkins Builds",
            "subcaption": "Test Results",
            "flatscrollbars": "0",
            "scrollheight": "12",
            "numvisibleplot": "7",
            "plottooltext": "<b>$dataValue</b> $seriesName in build $label",
            "theme": "fusion"
          },
          "categories": [ ],
          "dataset": [ ]
        }"""

def p1(request):
    chartObj = FusionCharts(
    'multilevelpie',
    'ex1',
    '600',
    '400',
    'chart-1',
    'json',
    
    
    
    
    
    """{
      "chart": {
        "caption": "Product Stacks",
        "subcaption": "",
        "showplotborder": "1",
        "plotfillalpha": "60",
        "hoverfillcolor": "#CCCCCC",
        "numberprefix": "$",
        "plottooltext": "Sales of <b>$label</b> was <b>$$valueK</b>, which was $percentValue of parent category",
        "theme": "fusion"
      },
      "category": [
                     {
                      "label": "Product Stacks",
                      "tooltext": "Please hover over a sub-category to see details",
                      "color": "#ffffff",
                      "value": "150",
                      "category": [
                                       {
                                        "label": "Stack1",
                                        "color": "#f8bd19",
                                        "value": "100",
                                        "category": [
                                                        {
                                                          "label": "Breads",
                                                          "color": "#f8bd19",
                                                          "value": "25"
                                                        },
                                                        {
                                                          "label": "Juice",
                                                          "color": "#f8bd19",
                                                          "value": "25"
                                                        },
                                                        {
                                                          "label": "Noodles",
                                                          "color": "#f8bd19",
                                                          "value": "25"
                                                        },
                                                        {
                                                          "label": "Seafood",
                                                          "color": "#f8bd19",
                                                          "value": "25"
                                                        }
                                                    ]
                                        }
                                   ]
                        }
                 ]
        }""")
    
    
    return render(request, 'ui/chart1.html', {'output1': chartObj.render() })

def pie_chart1(request):
    
    GET = False
    context_dict = {}
    rid=''

    if request.META['REQUEST_METHOD'] == 'GET':
        #rname = request.session.get('rname', '')
        #rtype = request.session.get('rtype', '')
        #rstate = request.session.get('rstate', '')
        
        print ('GET')
        rname = request.GET.get('rname', '')
        rtype = request.GET.get('rtype', '')
        rstate = request.GET.get('rstate', '')
        rid = request.GET.get('rid', '')
        stime = request.GET.get('stime', '')
        etime = request.GET.get('etime', '')
        GET = True

    if request.META['REQUEST_METHOD'] == 'POST':
        print ('POST')
        rname = request.POST.get('rname', '')
        rtype = request.POST.get('rtype', '')
        rstate = request.POST.get('rstate', '')
        stime = request.POST.get('stime', '')
        etime = request.POST.get('etime', '')
        GET = False
        
        
    if stime == "":
        myDate = datetime.now() + timedelta(days=-7)
        stime =  myDate.strftime("%Y-%m-%d")
        
    if etime == "":
        myDate = datetime.now()
        etime =  myDate.strftime("%Y-%m-%d")


        
    print(rname,rtype,rstate, stime, etime)

    # set session info    
    request.session['rname'] = rname
    request.session['rtype'] = rtype
    request.session['rstate'] = rstate
    request.session['stime'] = stime
    request.session['etime'] = etime
        
        
    # set selection for template
    context_dict['rname'] = rname
    context_dict['rtype'] = rtype
    context_dict['rstate'] = rstate
    context_dict['stime'] = stime
    context_dict['etime'] = etime
    
    context_dict['readystate'] = ['DEVELOPMENT','PRODUCTION']
    context_dict['readytype'] = ['INTEROP','CSS','SYSTEM']




    
    
    # query for solutions
    squeryset = []
    if rname is not '':
        squeryset = Definition.objects.all().order_by('-id')
        if rid is not '':
            squeryset = squeryset.filter(id = rid).distinct()
        squeryset = squeryset.filter(name = rname).distinct()
    print ('Definition>>>>>>>>>>>>>>>>>>>>>>>>>>',len(squeryset))        
    
    # query for runs
    rqueryset = []
    if rname is not '':
        rqueryset = Run.objects.all().order_by('-id')
        rqueryset = rqueryset.filter(run_status = 'COMPLETE').distinct()
        rqueryset = rqueryset.filter(definition__name = rname).distinct()
        
        local = pytz.timezone ("America/New_York")        
        if stime:
            stime = '%s 00:00:00' % stime
            format_str = "%Y-%m-%d %H:%M:%S"
            naive = datetime.strptime (stime, format_str)
            local_dt = local.localize(naive, is_dst=None)
            run_start_obj= local_dt.astimezone(pytz.utc)            
            rqueryset = rqueryset.filter(run_start__date__gte=run_start_obj)
                
        if etime:
            etime = '%s 23:59:59' % etime
            format_str = '%Y-%m-%d %H:%M:%S'
            naive = datetime.strptime (etime, format_str)
            local_dt = local.localize(naive, is_dst=None)
            run_end_obj= local_dt.astimezone(pytz.utc)
            rqueryset = rqueryset.filter(run_stop__date__lte=run_end_obj)
            
        print(rname,rtype,rstate)            
        print( stime, etime)
        print(str(run_start_obj), str(run_end_obj))
        
        
        if rtype is not '':
            rqueryset = rqueryset.filter(definition__test_type = rtype).distinct()
            
        if rstate is not '':
            rqueryset = rqueryset.filter(definition__ready_state = rstate).distinct()
            
    print ('Runs>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',len(rqueryset))
        
   
    l = []
    a = []
    p = []
    f = []
    s = []

    if len(squeryset) == 1:
    
        for r in rqueryset:
            
            #print (r.id, r.test_info)
            
            # (Att: 1 , Pass: 1 , Fail: 0 , Skip: 0)
            apfs = r.test_info
            
            if apfs.startswith("(Att:"):
                apfs = apfs.replace ('(', '')
                apfs = apfs.replace (')', '')
                apfs = apfs.replace (' ', '')
                apfs = apfs.replace ('Att:', '')
                apfs = apfs.replace ('Pass:', '')
                apfs = apfs.replace ('Fail:', '')
                apfs = apfs.replace ('Skip:', '')
                apfslist =  apfs.split(',')
                
                # label
                d1 = {"label": 'j%s (%s)'  % (r.id, r.run_start)}
                l.append(d1.copy())
                
                # attempts
                d2 = {"value":"%s" % apfslist[0] }
                a.append(d2.copy())
        
                # passed 
                d3 = {"value":"%s" % apfslist[1] }
                p.append(d3.copy())
                
                # failed
                d4 = {"value":"%s" % apfslist[2] }
                f.append(d4.copy())
        
                d5 = {"value":"%s" %  apfslist[3] }
                s.append(d5.copy())
        
        
    jdata = """{
          "chart": {
            "caption": "Title",
            "yaxisname": "",
            "xaxisname": "Jenkins Builds",
            "subcaption": "Test Results",
            "flatscrollbars": "0",
            "scrollheight": "12",
            "numvisibleplot": "7",
            "plottooltext": "<b>$dataValue</b> $seriesName in build $label",
            "theme": "fusion"
          },
          "categories": [ ],
          "dataset": [ ]
        }"""
        
    data = json.loads(jdata)
    
    if len(squeryset) == 1:
        data['chart']['caption'] = '%s, %s' %  (squeryset[0].name, squeryset[0].version)
        prodslist=list(squeryset[0].product_stack.products.all())
        data['chart']['subcaption'] = '%s' %  prodslist
    else:
        data['chart']['caption'] = '%s, %s' %  ('name', 'version')
        data['chart']['subcaption'] = '%s' %  'Product Matrix'

    ldict = {'category': l}
    adict = {'data': a, 'seriesname': 'Attempts'}
    pdict = {'data': p, 'seriesname': 'Passed'}
    fdict = {'data': f, 'seriesname': 'Failed'}
    sdict = {'data': s, 'seriesname': 'Skipped'}

    data['categories'].append(ldict)
    data['dataset'].append(adict)
    data['dataset'].append(pdict)
    data['dataset'].append(fdict)
    data['dataset'].append(sdict)

    barstackchartObj = FusionCharts(
         'scrollstackedcolumn2d',
         'ex1',
         '1000',
         '400',
         'chart-1',
         'json',
         json.dumps(data))







    
    
    
    
    if squeryset:
        # Chart data is passed to the `dataSource` parameter, like a dictionary in the form of key-value pairs.
        dataSource = OrderedDict()
    
        # The `chartConfig` dict contains key-value pairs of data for chart attribute
        chartConfig = OrderedDict()
        chartConfig["caption"] = "Multi Product Stack"
        chartConfig["subCaption"] = "Products"
        chartConfig["numberSuffix"] = ""
        chartConfig["theme"] = "fusion"
    
        # The `chartData` dict contains key-value pairs of data
        chartData = OrderedDict()
        prodlist = squeryset[0].product_stack.products.all()
        
        for p in prodlist:
            chartData[str(p)] = 1
    
        dataSource["chart"] = chartConfig
        dataSource["data"] = []
    
        for key, value in chartData.items():
            data = {}
            data["label"] = key
            data['tooltext'] = "Products in the Test Stack"
            data["value"] = value
            dataSource["data"].append(data)
            
        doughnutproductstack3d = FusionCharts("doughnut3d", "ex2", "600", "400", "chart-2", "json", dataSource)
        return render(request, 'ui/chart1.html', {'output1': barstackchartObj.render(),'output2': doughnutproductstack3d.render(), "data": context_dict })
        
    return render(request, 'ui/chart1.html', {'output1': barstackchartObj.render(), "data": context_dict })
        




def runs_chart(request):

    # query for runs
    queryset = Run.objects.all().order_by('-id')
    interop_count = queryset.filter(definition__test_type="INTEROP").count()

    queryset = Run.objects.all().order_by('-id')
    scenario_count = queryset.filter(definition__test_type="SCENARIO").count()

    queryset = Run.objects.all().order_by('-id')
    system_count = queryset.filter(definition__test_type="SYSTEM").count()

    interop = FusionCharts(
         'angulargauge',
         'ex1',
         '300',
         '200',
         'chart-interop',
         'json',
         """{
      "chart": {
        "caption": "Total Interop Runs",
        "lowerlimit": "0",
        "upperlimit": "100",
        "showvalue": "1",
        "numbersuffix": "",
        "theme": "fusion",
        "showtooltip": "0"
      },
      "colorrange": {
        "color": [
          {
            "minvalue": "0",
            "maxvalue": "50",
            "code": "#F2726F"
          },
          {
            "minvalue": "50",
            "maxvalue": "75",
            "code": "#FFC533"
          },
          {
            "minvalue": "75",
            "maxvalue": "100",
            "code": "#62B58F"
          }
        ]
      },
      "dials": {
        "dial": [
          {
            "value": "%s"
          }
        ]
      }
    }""" % interop_count)

    css = FusionCharts(
         'angulargauge',
         'ex2',
         '300',
         '200',
         'chart-css',
         'json',
         """{
      "chart": {
        "caption": "Total CSS Runs",
        "lowerlimit": "0",
        "upperlimit": "100",
        "showvalue": "1",
        "numbersuffix": "",
        "theme": "fusion",
        "showtooltip": "0"
      },
      "colorrange": {
        "color": [
          {
            "minvalue": "0",
            "maxvalue": "50",
            "code": "#F2726F"
          },
          {
            "minvalue": "50",
            "maxvalue": "75",
            "code": "#FFC533"
          },
          {
            "minvalue": "75",
            "maxvalue": "100",
            "code": "#62B58F"
          }
        ]
      },
      "dials": {
        "dial": [
          {
            "value": "%s"
          }
        ]
      }
    }""" % scenario_count)

    sys = FusionCharts(
         'angulargauge',
         'ex3',
         '300',
         '200',
         'chart-sys',
         'json',
         """{
      "chart": {
        "caption": "Total SYS Runs",
        "lowerlimit": "0",
        "upperlimit": "100",
        "showvalue": "1",
        "numbersuffix": "",
        "theme": "fusion",
        "showtooltip": "0"
      },
      "colorrange": {
        "color": [
          {
            "minvalue": "0",
            "maxvalue": "50",
            "code": "#F2726F"
          },
          {
            "minvalue": "50",
            "maxvalue": "75",
            "code": "#FFC533"
          },
          {
            "minvalue": "75",
            "maxvalue": "100",
            "code": "#62B58F"
          }
        ]
      },
      "dials": {
        "dial": [
          {
            "value": "%s"
          }
        ]
      }
    }""" % system_count)

    return render(request, 'ui/runs.html', {'interop': interop.render(), 'css': css.render(), 'sys': sys.render()})


def recipes_chart(request):

    # query for recipes
    queryset = Definition.objects.all().order_by('-id')
    interop_count = queryset.filter(testtype="INTEROP").count()

    queryset = Definition.objects.all().order_by('-id')
    scenario_count = queryset.filter(testtype="SCENARIO").count()

    queryset = Definition.objects.all().order_by('-id')
    system_count = queryset.filter(testtype="SYSTEM").count()

    interop = FusionCharts(
         'angulargauge',
         'ex1',
         '300',
         '200',
         'chart-interop',
         'json',
         """{
      "chart": {
        "caption": "Total Interop Recipes",
        "lowerlimit": "0",
        "upperlimit": "100",
        "showvalue": "1",
        "numbersuffix": "",
        "theme": "fusion",
        "showtooltip": "0"
      },
      "colorrange": {
        "color": [
          {
            "minvalue": "0",
            "maxvalue": "50",
            "code": "#F2726F"
          },
          {
            "minvalue": "50",
            "maxvalue": "75",
            "code": "#FFC533"
          },
          {
            "minvalue": "75",
            "maxvalue": "100",
            "code": "#62B58F"
          }
        ]
      },
      "dials": {
        "dial": [
          {
            "value": "%s"
          }
        ]
      }
    }""" % interop_count)

    css = FusionCharts(
         'angulargauge',
         'ex2',
         '300',
         '200',
         'chart-css',
         'json',
         """{
      "chart": {
        "caption": "Total CSS Recipes",
        "lowerlimit": "0",
        "upperlimit": "100",
        "showvalue": "1",
        "numbersuffix": "",
        "theme": "fusion",
        "showtooltip": "0"
      },
      "colorrange": {
        "color": [
          {
            "minvalue": "0",
            "maxvalue": "50",
            "code": "#F2726F"
          },
          {
            "minvalue": "50",
            "maxvalue": "75",
            "code": "#FFC533"
          },
          {
            "minvalue": "75",
            "maxvalue": "100",
            "code": "#62B58F"
          }
        ]
      },
      "dials": {
        "dial": [
          {
            "value": "%s"
          }
        ]
      }
    }""" % scenario_count)

    sys = FusionCharts(
         'angulargauge',
         'ex3',
         '300',
         '200',
         'chart-sys',
         'json',
         """{
      "chart": {
        "caption": "Total SYS Recipes",
        "lowerlimit": "0",
        "upperlimit": "100",
        "showvalue": "1",
        "numbersuffix": "",
        "theme": "fusion",
        "showtooltip": "0"
      },
      "colorrange": {
        "color": [
          {
            "minvalue": "0",
            "maxvalue": "50",
            "code": "#F2726F"
          },
          {
            "minvalue": "50",
            "maxvalue": "75",
            "code": "#FFC533"
          },
          {
            "minvalue": "75",
            "maxvalue": "100",
            "code": "#62B58F"
          }
        ]
      },
      "dials": {
        "dial": [
          {
            "value": "%s"
          }
        ]
      }
    }""" % system_count)

    return render(request, 'ui/recipes.html', {'interop': interop.render(), 'css': css.render(), 'sys': sys.render()})


def meter_chart(request):
    chartObj1 = FusionCharts(
         'angulargauge',
         'ex1',
         '600',
         '400',
         'chart-1',
         'json',
         """{
      "chart": {
        "caption": "Total Recipies for 2018",
        "lowerlimit": "0",
        "upperlimit": "100",
        "showvalue": "1",
        "numbersuffix": "",
        "theme": "fusion",
        "showtooltip": "0"
      },
      "colorrange": {
        "color": [
          {
            "minvalue": "0",
            "maxvalue": "50",
            "code": "#F2726F"
          },
          {
            "minvalue": "50",
            "maxvalue": "75",
            "code": "#FFC533"
          },
          {
            "minvalue": "75",
            "maxvalue": "100",
            "code": "#62B58F"
          }
        ]
      },
      "dials": {
        "dial": [
          {
            "value": "81"
          }
        ]
      }
    }""")

    chartObj2 = FusionCharts(
         'angulargauge',
         'ex2',
         '600',
         '400',
         'chart-2',
         'json',
         """{
          "chart": {
            "caption": "Product BU Satisfaction Score",
            "subcaption": "2017",
            "lowerlimit": "0",
            "upperlimit": "100",
            "showvalue": "1",
            "numbersuffix": "%",
            "theme": "fusion"
          },
          "colorrange": {
            "color": [
              {
                "minvalue": "0",
                "maxvalue": "50",
                "code": "#F2726F"
              },
              {
                "minvalue": "50",
                "maxvalue": "75",
                "code": "#FFC533"
              },
              {
                "minvalue": "75",
                "maxvalue": "100",
                "code": "#62B58F"
              }
            ]
          },
          "dials": {
            "dial": [
              {
                "value": "71",
                "tooltext": "<b>9%</b> lesser that target"
              }
            ]
          },
          "trendpoints": {
            "point": [
              {
                "startvalue": "80",
                "displayvalue": "Target",
                "thickness": "2",
                "color": "#E15A26",
                "usemarker": "1",
                "markerbordercolor": "#E15A26",
                "markertooltext": "80%"
              }
            ]
          }
        }""")

    return render(request, 'ui/meter.html', {'output1': chartObj1.render(), 'output2': chartObj2.render()})


def bar_chart(request):
    # Chart data is passed to the `dataSource` parameter, like a dictionary in the form of key-value pairs.
    dataSource = OrderedDict()

    # The `chartConfig` dict contains key-value pairs of data for chart attribute
    chartConfig = OrderedDict()
    chartConfig["caption"] = "Interop Test Results [OpenShift v3.10]"
    chartConfig["subCaption"] = "MPQE"
    chartConfig["xAxisName"] = "Definitions"
    chartConfig["yAxisName"] = "Runs"
    chartConfig["numberSuffix"] = ""
    chartConfig["theme"] = "fusion"

    # The `chartData` dict contains key-value pairs of data
    chartData = OrderedDict()
    chartData["S1:OCP3.10-Interop-1"] = 25
    chartData["S2:OCP3.10-Interop-2"] = 45
    chartData["S3:OCP3.10-Interop-3"] = 55

    dataSource["chart"] = chartConfig
    dataSource["data"] = []

    # Convert the data in the `chartData`array into a format that can be consumed by FusionCharts.
    # The data for the chart should be in an array wherein each element of the array
    # is a JSON object# having the `label` and `value` as keys.

    # Iterate through the data in `chartData` and insert into the `dataSource['data']` list.
    for key, value in chartData.items():
        data = {}
        data["label"] = key
        if key.startswith('S1'):
            data['tooltext'] = "Soution:OCP3.10-Interop-1{br}Stack:ocp3.10-osp10-gluster3.4-1{br}Arch: x86-64{br}Products:openshift v3.10{br}gluster v3.4{br}openstack v10"

        if key.startswith('S2'):
            data['tooltext'] = "Soution:OCP3.10-Interop-2{br}Stack:ocp3.10-osp12-gluster3.4-1{br}Arch: x86-64{br}Products:openshift v3.10{br}gluster v3.4{br}openstack v12"

        if key.startswith('S3'):
            data['tooltext'] = "Soution:OCP3.10-Interop-3{br}Stack:ocp3.10-osp13-gluster3.4-1{br}Arch: x86-64{br}Products:openshift v3.10{br}gluster v3.4{br}openstack v13"

        data["value"] = value
        dataSource["data"].append(data)

    # Create an object for the column 2D chart using the FusionCharts class constructor
    # The chart data is passed to the `dataSource` parameter.
    column2D = FusionCharts("bar3d", "myFirstChart", "1000", "400", "chart-1", "json", dataSource)

    return render(request, 'ui/chart.html', { 'output': column2D.render() })

import re
import json

def load_dirty_json(dirty_json):
    regex_replace = [(r"([ \{,:\[])(u)?'([^']+)'", r'\1"\3"'), (r" False([, \}\]])", r' false\1'), (r" True([, \}\]])", r' true\1')]
    for r, s in regex_replace:
        dirty_json = re.sub(r, s, dirty_json)
    clean_json = json.loads(dirty_json)
    return clean_json

def bar_stack_chart(request):
    
    
    GET = False
    context_dict = {}


    # is authn
    if request.META['REQUEST_METHOD'] == 'GET':
        #rname = request.session.get('rname', '')
        #rtype = request.session.get('rtype', '')
        #rstate = request.session.get('rstate', '')
        rname = request.GET.get('rname', '')
        rtype = request.GET.get('rtype', '')
        rstate = request.GET.get('rstate', '')            
        GET = True

    if request.META['REQUEST_METHOD'] == 'POST':
        rname = request.POST.get('rname', '')
        rtype = request.POST.get('rtype', '')
        rstate = request.POST.get('rstate', '')
        request.session['rname'] = rname
        request.session['rtype'] = rtype
        request.session['rstate'] = rstate            
        GET = False
        
    # set selection for template
    context_dict['rname'] = rname
    context_dict['rtype'] = rtype
    context_dict['rstate'] = rstate        


    print('hello...', rname,rtype,rstate)


    l = []
    a = []
    p = []
    f = []
    s = []

    cnt = random.randint(2, 200 )
    for x in range(cnt, 0, -1):
        
        x +=1
        q = '"' 
        #jlink = "<a href=%shttps://pit-stg-jenkins.rhev-ci-vms.eng.rdu2.redhat.com%s>%s</a>"  % (q,q,x)
        #print (jlink) 
        #d1 = {"label": jlink }
        
        d1 = {"label": '%s'  % x }

        l.append(d1.copy())

        
        # attempts
        x1 = random.randint(40, 50)
        d2 = {"value":"%s" % x1 }
        a.append(d2.copy())

        # passed 
        x2 = random.randint(0, x1)
        d3 = {"value":"%s" % x2 }
        p.append(d3.copy())
        
        # failed
        failed = x1 - x2
        x3 = random.randint(0, failed)
        d4 = {"value":"%s" % x3 }
        f.append(d4.copy())

        skipped =  (x1 -(x2 + x3))
        d5 = {"value":"%s" %  skipped }
        s.append(d5.copy())
    
    
    jdata = """{
          "chart": {
            "caption": "CSS  - Red Hat xHyperconverged Infrastructure V1.1 (RHHI)",
            "yaxisname": "",
            "xaxisname": "Jenkins Build",
            "subcaption": "Test hello Results",
            "flatscrollbars": "0",
            "scrollheight": "12",
            "numvisibleplot": "10",
            "plottooltext": "<b>$dataValue</b> $seriesName in build $label",
            "theme": "fusion"
          },
          "categories": [ ],
          "dataset": [ ]
        }"""
        
 
    
    data = json.loads(jdata)

    ldict = {'category': l}
    adict = {'data': a, 'seriesname': 'Attempts'}
    pdict = {'data': p, 'seriesname': 'Passed'}
    fdict = {'data': f, 'seriesname': 'Failed'}
    sdict = {'data': s, 'seriesname': 'Skipped'}

    data['categories'].append(ldict)
    data['dataset'].append(adict)
    data['dataset'].append(pdict)
    data['dataset'].append(fdict)
    data['dataset'].append(sdict)

    chartObj = FusionCharts(
         'scrollstackedcolumn2d',
         'ex1',
         '600',
         '400',
         'chart-1',
         'json',
         json.dumps(data))
        
        

    return render(request, 'ui/chart1.html', { 'output': chartObj.render(), "data": context_dict })




def bar_stack_chart1(request):
    
    GET = False
    context_dict = {}
    rid=''

    if request.META['REQUEST_METHOD'] == 'GET':
        #rname = request.session.get('rname', '')
        #rtype = request.session.get('rtype', '')
        #rstate = request.session.get('rstate', '')
        
        print ('GET')
        rname = request.GET.get('rname', '')
        rtype = request.GET.get('rtype', '')
        rstate = request.GET.get('rstate', '')
        rid = request.GET.get('rid', '')
        stime = request.GET.get('stime', '')
        etime = request.GET.get('etime', '')
        GET = True

    if request.META['REQUEST_METHOD'] == 'POST':
        print ('POST')
        rname = request.POST.get('rname', '')
        rtype = request.POST.get('rtype', '')
        rstate = request.POST.get('rstate', '')
        stime = request.POST.get('stime', '')
        etime = request.POST.get('etime', '')
        GET = False
        
        
    if stime == "":
        myDate = datetime.now() + timedelta(days=-7)
        stime =  myDate.strftime("%Y-%m-%d")
        
    if etime == "":
        myDate = datetime.now()
        etime =  myDate.strftime("%Y-%m-%d")


        
    print(rname,rtype,rstate, stime, etime)

    # set session info    
    request.session['rname'] = rname
    request.session['rtype'] = rtype
    request.session['rstate'] = rstate
    request.session['stime'] = stime
    request.session['etime'] = etime
        
        
    # set selection for template
    context_dict['rname'] = rname
    context_dict['rtype'] = rtype
    context_dict['rstate'] = rstate
    context_dict['stime'] = stime
    context_dict['etime'] = etime
    
    context_dict['readystate'] = ['DEVELOPMENT','PRODUCTION']
    context_dict['readytype'] = ['INTEROP','CSS','SYSTEM']




    
    
    # query for solutions
    squeryset = []
    if rname is not '':
        squeryset = Definition.objects.all().order_by('-id')
        if rid is not '':
            squeryset = squeryset.filter(id = rid).distinct()
        squeryset = squeryset.filter(name = rname).distinct()
    print ('Definition>>>>>>>>>>>>>>>>>>>>>>>>>>',len(squeryset))        
    
    # query for runs
    rqueryset = []
    if rname is not '':
        rqueryset = Run.objects.all().order_by('-id')
        rqueryset = rqueryset.filter(run_status = 'COMPLETE').distinct()
        rqueryset = rqueryset.filter(definition__name = rname).distinct()
        
        local = pytz.timezone ("America/New_York")        
        if stime:
            stime = '%s 00:00:00' % stime
            format_str = "%Y-%m-%d %H:%M:%S"
            naive = datetime.strptime (stime, format_str)
            local_dt = local.localize(naive, is_dst=None)
            run_start_obj= local_dt.astimezone(pytz.utc)            
            rqueryset = rqueryset.filter(run_start__date__gte=run_start_obj)
                
        if etime:
            etime = '%s 23:59:59' % etime
            format_str = '%Y-%m-%d %H:%M:%S'
            naive = datetime.strptime (etime, format_str)
            local_dt = local.localize(naive, is_dst=None)
            run_end_obj= local_dt.astimezone(pytz.utc)
            rqueryset = rqueryset.filter(run_stop__date__lte=run_end_obj)
            
        print(rname,rtype,rstate)            
        print( stime, etime)
        print(str(run_start_obj), str(run_end_obj))
        
        
        if rtype is not '':
            rqueryset = rqueryset.filter(definition__test_type = rtype).distinct()
            
        if rstate is not '':
            rqueryset = rqueryset.filter(definition__ready_state = rstate).distinct()
            
    print ('Runs>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',len(rqueryset))
        
   
    
#     run_step = request.query_params.get('run_step', None)
#     if run_step is not None:
#         queryset = queryset.filter(run_step = run_step).distinct()
#     
#     
#     run_status = request.query_params.get('run_status', None)
#     if run_status is not None:
#         queryset = queryset.filter(run_status = run_status).distinct()
#     
# 
#     import datetime
#     run_start = request.query_params.get('run_start', None)
#     format_str = '%Y-%m-%d'
#     if run_start is not None:
#         print (run_start)
#         run_start_obj = datetime.datetime.strptime(run_start, format_str)
#         queryset = queryset.filter(run_start__date__gte=run_start_obj)
#         #queryset = queryset.filter(run_start__range=["2011-01-01", "2011-01-31"]).distinct()
#         
#     run_stop = request.query_params.get('run_stop', None)
#     format_str = '%Y-%m-%d'
#     if run_stop is not None:
#         print (run_stop)
#         run_stop_obj = datetime.datetime.strptime(run_stop, format_str)
#         # add 1 day because its really 0 hundred hours
#         queryset = queryset.filter(run_stop__date__lte=run_stop_obj)

    l = []
    a = []
    p = []
    f = []
    s = []

    if len(squeryset) == 1:
    
        for r in rqueryset:
            
            #print (r.id, r.test_info)
            
            # (Att: 1 , Pass: 1 , Fail: 0 , Skip: 0)
            apfs = r.test_info
            
            if apfs.startswith("(Att:"):
                apfs = apfs.replace ('(', '')
                apfs = apfs.replace (')', '')
                apfs = apfs.replace (' ', '')
                apfs = apfs.replace ('Att:', '')
                apfs = apfs.replace ('Pass:', '')
                apfs = apfs.replace ('Fail:', '')
                apfs = apfs.replace ('Skip:', '')
                apfslist =  apfs.split(',')
                
                # label
                d1 = {"label": 'j%s (%s)'  % (r.id, r.run_start)}
                l.append(d1.copy())
                
                # attempts
                d2 = {"value":"%s" % apfslist[0] }
                a.append(d2.copy())
        
                # passed 
                d3 = {"value":"%s" % apfslist[1] }
                p.append(d3.copy())
                
                # failed
                d4 = {"value":"%s" % apfslist[2] }
                f.append(d4.copy())
        
                d5 = {"value":"%s" %  apfslist[3] }
                s.append(d5.copy())
        
        
    jdata = """{
          "chart": {
            "caption": "Title",
            "yaxisname": "",
            "xaxisname": "Jenkins Builds",
            "subcaption": "Test Results",
            "flatscrollbars": "0",
            "scrollheight": "12",
            "numvisibleplot": "7",
            "plottooltext": "<b>$dataValue</b> $seriesName in build $label",
            "theme": "fusion"
          },
          "categories": [ ],
          "dataset": [ ]
        }"""
        
    data = json.loads(jdata)
    
    if len(squeryset) == 1:
        data['chart']['caption'] = '%s, %s' %  (squeryset[0].name, squeryset[0].version)
        prodslist=list(squeryset[0].product_stack.products.all())
        data['chart']['subcaption'] = '%s' %  prodslist
    else:
        data['chart']['caption'] = '%s, %s' %  ('name', 'version')
        data['chart']['subcaption'] = '%s' %  'Product Matrix'

    ldict = {'category': l}
    adict = {'data': a, 'seriesname': 'Attempts'}
    pdict = {'data': p, 'seriesname': 'Passed'}
    fdict = {'data': f, 'seriesname': 'Failed'}
    sdict = {'data': s, 'seriesname': 'Skipped'}

    data['categories'].append(ldict)
    data['dataset'].append(adict)
    data['dataset'].append(pdict)
    data['dataset'].append(fdict)
    data['dataset'].append(sdict)

    barstackchartObj = FusionCharts(
         'scrollstackedcolumn2d',
         'ex1',
         '1000',
         '400',
         'chart-1',
         'json',
         json.dumps(data))







    
    
    
    
    if squeryset:
        # Chart data is passed to the `dataSource` parameter, like a dictionary in the form of key-value pairs.
        dataSource = OrderedDict()
    
        # The `chartConfig` dict contains key-value pairs of data for chart attribute
        chartConfig = OrderedDict()
        chartConfig["caption"] = "Multi Product Stack"
        chartConfig["subCaption"] = "Products"
        chartConfig["numberSuffix"] = ""
        chartConfig["theme"] = "fusion"
    
        # The `chartData` dict contains key-value pairs of data
        chartData = OrderedDict()
        prodlist = squeryset[0].product_stack.products.all()
        
        for p in prodlist:
            chartData[str(p)] = 1
    
        dataSource["chart"] = chartConfig
        dataSource["data"] = []
    
        for key, value in chartData.items():
            data = {}
            data["label"] = key
            data['tooltext'] = "Products in the Test Stack"
            data["value"] = value
            dataSource["data"].append(data)
            
        doughnutproductstack3d = FusionCharts("doughnut3d", "ex2", "600", "400", "chart-2", "json", dataSource)
        return render(request, 'ui/chart1.html', {'output1': barstackchartObj.render(),'output2': doughnutproductstack3d.render(), "data": context_dict })
        
    return render(request, 'ui/chart1.html', {'output1': barstackchartObj.render(), "data": context_dict })
        


















def multi_line_chart(request):

    l = []
    a = []
    p = []
    f = []
    s = []

    cnt = random.randint(2, 200)
    for x in range(cnt):

        d1 = {"label":"%s" % x }
        l.append(d1.copy())

        # attempts
        x1 = random.randint(40, 50)
        d2 = {"value":"%s" % x1 }
        a.append(d2.copy())

        # passed 
        x2 = random.randint(0, x1)
        d3 = {"value":"%s" % x2 }
        p.append(d3.copy())
        
        # failed
        failed = x1 - x2
        x3 = random.randint(0, failed)
        d4 = {"value":"%s" % x3 }
        f.append(d4.copy())

        skipped =  (x1 -(x2 + x3))
        d5 = {"value":"%s" %  skipped }
        s.append(d5.copy())

    jdata = """{
          "chart": {
            "caption": "Red Hat Hyperconverged Infrastructure V1.1 (RHHI)",
            "yaxisname": "Counts",
            "xaxisname": "Test Runs",
            "subcaption": "Customer Scenario and Solutions",
            "showhovereffect": "1",
            "numbersuffix": "",
            "drawcrossline": "1",
            "plottooltext": "<b>$dataValue</b> $seriesName",
            "theme": "fusion"
          },
          "categories": [ ],
          "dataset": [ ]
        }"""

    data = json.loads(jdata)
    ldict = {'category': l}
    adict = {'data': a, 'seriesname': 'Attempts'}
    pdict = {'data': p, 'seriesname': 'Passed'}
    fdict = {'data': f, 'seriesname': 'Failed'}
    sdict = {'data': s, 'seriesname': 'Skipped'}

    data['categories'].append(ldict)
    data['dataset'].append(adict)
    data['dataset'].append(pdict)
    data['dataset'].append(fdict)
    data['dataset'].append(sdict)

    chartObj = FusionCharts(
         'msline',
         'ex1',
         '1400',
         '700',
         'chart-1',
         'json',
         json.dumps(data)
         )


    return render(request, 'ui/chart.html', {'output': chartObj.render()})


def line_chart(request):

    chartObj = FusionCharts(
         'line',
         'ex1',
         '1000',
         '400',
         'chart-1',
         'json',
         """{
  "chart": {
    "caption": "MPQE Test Runs - OpenStack v12",
    "yaxisname": "Velocity)",
    "subcaption": "[2018]",
    "numbersuffix": " runs",
    "rotatelabels": "1",
    "setadaptiveymin": "1",
    "theme": "fusion"
  },
  "data": [
    {
      "label": "Jan",
      "value": "89.45"
    },
    {
      "label": "Feb",
      "value": "89.87"
    },
    {
      "label": "Mar",
      "value": "89.64"
    },
    {
      "label": "Apl",
      "value": "90.13"
    },
    {
      "label": "May",
      "value": "90.67"
    },
    {
      "label": "June",
      "value": "90.54"
    },
    {
      "label": "July",
      "value": "90.75"
    },
    {
      "label": "Aug",
      "value": "90.8"
    },
    {
      "label": "Sept",
      "value": "91.16"
    },
    {
      "label": "Oct",
      "value": "91.37"
    },
    {
      "label": "Nov",
      "value": "91.66"
    },
    {
      "label": "Dec",
      "value": "91.8"
    }
  ]
}""")
    return render(request, 'ui/chart.html', {'output': chartObj.render()})


def pie_chart(request):
    # Chart data is passed to the `dataSource` parameter, like a dictionary in the form of key-value pairs.
    dataSource = OrderedDict()

    # The `chartConfig` dict contains key-value pairs of data for chart attribute
    chartConfig = OrderedDict()
    chartConfig["caption"] = "Interop Test Results [OpenShift v3.10]"
    chartConfig["subCaption"] = "MPQE"
    chartConfig["xAxisName"] = "Definitions"
    chartConfig["yAxisName"] = "Runs"
    chartConfig["numberSuffix"] = ""
    chartConfig["theme"] = "fusion"

    # The `chartData` dict contains key-value pairs of data
    chartData = OrderedDict()
    chartData["S1:OCP3.10-Interop-1"] = 25
    chartData["S2:OCP3.10-Interop-2"] = 45
    chartData["S3:OCP3.10-Interop-3"] = 55

    dataSource["chart"] = chartConfig
    dataSource["data"] = []

    # Convert the data in the `chartData`array into a format that can be consumed by FusionCharts.
    # The data for the chart should be in an array wherein each element of the array
    # is a JSON object# having the `label` and `value` as keys.

    # Iterate through the data in `chartData` and insert into the `dataSource['data']` list.
    for key, value in chartData.items():
        data = {}
        data["label"] = key
        if key.startswith('S1'):
            data['tooltext'] = "Soution:OCP3.10-Interop-1{br}Stack:ocp3.10-osp10-gluster3.4-1{br}Arch: x86-64{br}Products:openshift v3.10{br}gluster v3.4{br}openstack v10"

        if key.startswith('S2'):
            data['tooltext'] = "Soution:OCP3.10-Interop-2{br}Stack:ocp3.10-osp12-gluster3.4-1{br}Arch: x86-64{br}Products:openshift v3.10{br}gluster v3.4{br}openstack v12"

        if key.startswith('S3'):
            data['tooltext'] = "Soution:OCP3.10-Interop-3{br}Stack:ocp3.10-osp13-gluster3.4-1{br}Arch: x86-64{br}Products:openshift v3.10{br}gluster v3.4{br}openstack v13"

        data["value"] = value
        dataSource["data"].append(data)

    # Create an object for the column 2D chart using the FusionCharts class constructor
    # The chart data is passed to the `dataSource` parameter.
    doughnut2d = FusionCharts("doughnut2d", "ex1", "600", "400", "chart-1", "json", dataSource)
    doughnut3d = FusionCharts("doughnut3d", "ex2", "600", "400", "chart-2", "json", dataSource)

    return render(request, 'ui/chart.html', { 'output': doughnut2d.render(), 'output1': doughnut3d.render() })

